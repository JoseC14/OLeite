from django.shortcuts import render,get_object_or_404, redirect
from django.db import IntegrityError
from .models import Leite
from datetime import datetime
from django.db.models import Q
from .models import Soma
from django.db.models import Sum

def home(request):
    if request.method == 'GET':
        return render(request,'home.html')


def cadastrar_leite(request):
    if request.method == 'GET':
        return render(request,'cadastrar_leite.html')
    elif request.method == 'POST':
        quantidade = request.POST.get('quantidade')
        data = request.POST.get('data')
        leite = Leite(quantidade=quantidade,data=data)
        try:
            leite.save()
            return render(request,'cadastrar_leite.html', {'msg_sucesso':'Entrega cadastrada!'})
        except IntegrityError:
            return render(request,'cadastrar_leite.html',{'erro':'Data duplicada!'})


def gerenciar_leite(request):
    if request.method == 'GET':
        leites = Leite.objects.all()
        return render(request,'gerenciar_leite.html',{'leites': leites})


def somar_leite(request):
    if request.method == 'GET':
        return render(request,'somar.html')
    elif request.method == 'POST':
        de = request.POST.get('de')
        ate = request.POST.get('ate')
        preco = request.POST.get('preco')
        leites = Leite.objects.filter(data__range=[de,ate])  
        leite_soma = leites.aggregate(soma = Sum('quantidade'))['soma']
        total = leite_soma*int(preco) 
        return render(request,'somar.html',{'leites':leites,
                                            'leite_soma':leite_soma,
                                            'total':total,
                                            'preco':preco,
                                            'de':de,
                                            'ate':ate})
    

def deletar_leite(request,pk_id):
    if request.method == 'GET':
        leite = get_object_or_404(Leite, pk=pk_id)
        leite.delete()
        return redirect('ger_leite')
    

def alterar_leite(request,pk_id):
    
    if request.method == 'GET':
        leite = get_object_or_404(Leite, pk=pk_id)   
        
        return render(request,'alterar_leite.html',{'leite':leite})
    elif request.method == 'POST':
        leite = get_object_or_404(Leite, pk=pk_id)
        leite.quantidade = request.POST.get('quantidade')
        leite.data = request.POST.get('data')
        
        leite.save()    
        return redirect('ger_leite')


def pesquisar_leite(request):
    if request.method == 'POST':
        pesquisa = request.POST.get('pesquisa')
        tipo_pesquisa = request.POST.get('tipo_pesquisa')

        if tipo_pesquisa == 'all':
            leites = Leite.objects.filter(
                    Q(quantidade__icontains=pesquisa) |
                    Q(id__icontains=pesquisa) |
                    Q(data__icontains=pesquisa)
            )
        elif tipo_pesquisa == 'id':
            leites = Leite.objects.filter(
                    id__icontains=pesquisa
            )
        elif tipo_pesquisa == 'data':
            leites = Leite.objects.filter(
                    data__icontains=pesquisa
            )
        elif tipo_pesquisa == 'quantidade':
            leites = Leite.objects.filter(
                    quantidade__icontains=pesquisa
            )

        
        
        return render(request,'gerenciar_leite.html',{'leites':leites})
    

def cadastrar_soma(request):
    if request.method == 'POST':
        leites = request.POST.getlist('leites[]')
        total_litros = request.POST.get('total_litro')
        total = request.POST.get('total')
        preco = request.POST.get('preco')
        de = request.POST.get('de')
        ate = request.POST.get('ate')


        soma = Soma(quantidade=total_litros, total=total, preco_litro=preco, data_inicio=de, data_fim=ate)
        soma.save()

        for id in leites:
            leite = Leite.objects.filter(id=id)
            leite.id_soma = soma.id
            leite.update() 
        
        return redirect('sum_leite')


