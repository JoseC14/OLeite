from django.shortcuts import render,get_object_or_404, redirect
from django.db import IntegrityError
from .models import Leite
from django.db.models import Q
from .models import Soma
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from . import utils
from app.settings import BASE_DIR
from os import path
from django.core.paginator import Paginator
from django.db.models import Avg


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
        leites = Leite.objects.all().order_by('-data')

        leite_paginator = Paginator(leites,10)
        page_num = request.GET.get('page')
        page = leite_paginator.get_page(page_num)

        return render(request,'gerenciar_leite.html',{'page': page})


def somar_leite(request):
    if request.method == 'GET':
        return render(request,'somar.html')
    elif request.method == 'POST':
        de = request.POST.get('de')
        ate = request.POST.get('ate')
        preco = request.POST.get('preco')

        if de == "":
            return render(request,'somar.html',{'msg_erro':'Data de inicio não pode ser nula!'})
        if ate == "":
            return render(request,'somar.html',{'msg_erro':'Data final não pode ser nula!'}) 
        if preco == "":
            return render(request,'somar.html',{'msg_erro':'Preço não pode ser nulo!'}) 

        leites = Leite.objects.filter(Q(data__range=[de,ate])).exclude(soma__isnull=False)  
        leite_soma = leites.aggregate(soma = Sum('quantidade'))['soma']
        total = leite_soma*float(preco)
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

        try:
            pesquisa_data = utils.formataData(pesquisa)
        except:
            pesquisa_data = pesquisa
        
        if tipo_pesquisa == 'tudo':
            leites = Leite.objects.filter(
                    Q(quantidade__icontains=pesquisa) |
                    Q(id__icontains=pesquisa) |
                    Q(data__icontains=pesquisa_data)
            ).order_by('-data')
        elif tipo_pesquisa == 'id':
            leites = Leite.objects.filter(
                    id__icontains=pesquisa
            ).order_by('-data')
        elif tipo_pesquisa == 'data':
            leites = Leite.objects.filter(
                    data__icontains=pesquisa_data
            ).order_by('-data')
        elif tipo_pesquisa == 'quantidade':
            leites = Leite.objects.filter(
                    quantidade__icontains=pesquisa
            ).order_by('-data')
        
        leite_paginator = Paginator(leites,10)
        page_num = request.GET.get('page')
        page = leite_paginator.get_page(page_num)

        return render(request,'gerenciar_leite.html',{'page': page})
    

def cadastrar_soma(request):
    if request.method == 'POST':
        leites = request.POST.getlist('leites[]')
        total_litros = request.POST.get('total_litro')
        total = request.POST.get('total')
        preco = request.POST.get('preco')
        de = request.POST.get('de')
        ate = request.POST.get('ate')
        soma_check = Soma.objects.filter(Q(data_inicio = de) | Q(data_fim=ate) )

        if soma_check.exists():
            return render(request,'somar.html',{'msg_erro':'Registro de leite já existe no banco!'})
        
        soma = Soma(quantidade=total_litros, total=total, preco_litro=preco, data_inicio=de, data_fim=ate)
        soma.save()
        for id in leites:
            leite = Leite.objects.get(id=id)
            leite.soma = soma
            leite.save() 
        
        return render(request,'somar.html',{'msg_sucesso':'Registrado!'})


def somas(request):
    if request.method == 'GET':        
        somas = Soma.objects.all()
        return render(request,'somas.html',{'somas':somas})
    if request.method == 'POST':
        pesquisa = request.POST.get('pesquisa')
        tipo_pesquisa = request.POST.get('tipo_pesquisa')
        print(pesquisa)
        print(type(pesquisa))
        try:
            data_pesquisa = utils.formataData(pesquisa)
        except:
            print("Não foi possível formatar data")
            data_pesquisa = pesquisa
        finally:
            if tipo_pesquisa == 'all':
                somas = Soma.objects.filter(Q(id__contains=pesquisa) |
                                            Q(quantidade__contains=pesquisa) |
                                            Q(total__contains=data_pesquisa) |
                                            Q(preco_litro__contains=pesquisa) |
                                            Q(data_inicio__contains=data_pesquisa) |
                                            Q(data_fim__contains=data_pesquisa)) 
            elif tipo_pesquisa == 'id':
                somas = Soma.objects.filter(id__contains=pesquisa)
            elif tipo_pesquisa == 'quantidade':
                somas = Soma.objects.filter(quantidade__contains=pesquisa)
            elif tipo_pesquisa == 'total':
                somas = Soma.objects.filter(total__contains=pesquisa)
            elif tipo_pesquisa == 'preco':
                somas = Soma.objects.filter(preco_litro__contains=pesquisa)
            elif tipo_pesquisa == 'data_inicio':
                somas = Soma.objects.filter(data_inicio__contains=data_pesquisa)
            elif tipo_pesquisa == 'data_fim':
                somas = Soma.objects.filter(data_fim__contains=data_pesquisa)
        
        return render(request,'somas.html',{'somas':somas})
    



def deletar_soma(request, pk_id):
    
    leites = Leite.objects.filter(soma=pk_id)
    for leite in leites:
        leite.soma = None
        leite.save()

    soma = Soma.objects.filter(id=pk_id)
    soma.delete() 
    return redirect('somas')


def gerar_relatorio(request):

    if request.method == 'POST':
        
        caminho = path.join(BASE_DIR, "leite/templates/ver_registro.html")
        tabela = request.POST.get('tabela')
        template_w = open(caminho, "w")       
        
        template_w.write(tabela)
        template_w.close()

        pdf = utils.gerar_relatorio(caminho)
        
        return HttpResponse(pdf,content_type="application/pdf")