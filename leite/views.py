from django.shortcuts import render,get_object_or_404, redirect
from django.db import IntegrityError
from .models import Leite
from django.db.models import Q
from .models import Soma
from django.db.models import Sum
from django.http import HttpResponse
from . import utils
from app.settings import BASE_DIR
from os import path
from django.core.paginator import Paginator
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import pandas as pd

#CADASTRO DE LEITES
@login_required
def cadastrar_leite(request):
    if request.method == 'GET':
        return render(request,'cadastrar_leite.html')
    elif request.method == 'POST':
        quantidade = request.POST.get('quantidade')
        data = request.POST.get('data')
        leite = Leite(quantidade=quantidade,data=data,usuario=request.user)
        if Leite.objects.filter(Q(usuario=request.user) & Q(data=data)).exists():
            return render(request,'cadastrar_leite.html',{'erro':'Data duplicada!'})
        else:
            leite.save()
            return render(request,'cadastrar_leite.html', {'msg_sucesso':'Entrega cadastrada!'})

#GERENCIAMENTO DE LEITE
@login_required
def gerenciar_leite(request):
    if request.method == 'GET':
        leites = Leite.objects.filter(usuario=request.user.id).order_by('-data')

        leite_paginator = Paginator(leites,10)
        page_num = request.GET.get('page')
        page = leite_paginator.get_page(page_num)

        return render(request,'gerenciar_leite.html',{'page': page})

#SOMAR OS LEITES
@login_required
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

        leites = Leite.objects.filter(Q(data__range=[de,ate]) & Q(usuario=request.user.id)).exclude(soma__isnull=False)  
        leite_soma = leites.aggregate(soma = Sum('quantidade'))['soma']
        total = leite_soma*float(preco)
        return render(request,'somar.html',{'leites':leites,
                                            'leite_soma':leite_soma,
                                            'total':total,
                                            'preco':preco,
                                            'de':de,
                                            'ate':ate})
    
#EXCLUSÃO DE LEITES
@login_required
def deletar_leite(request,pk_id):
    if request.method == 'GET':
        leite = get_object_or_404(Leite, id=pk_id, usuario=request.user.id)
        leite.delete()
        return redirect('ger_leite')

#ALTERAÇÃO DE LEITE
@login_required
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

#PESQUISA DE REGISTROS DE LEITES
@login_required
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
                    (Q(quantidade__icontains=pesquisa) |
                    Q(id__icontains=pesquisa) |
                    Q(data__icontains=pesquisa_data)) &
                    Q(usuario=request.user.id)
            ).order_by('-data')
        elif tipo_pesquisa == 'id':
            leites = Leite.objects.filter(
                    Q(id__icontains=pesquisa) & Q(usuario=request.user.id)
            ).order_by('-data')
        elif tipo_pesquisa == 'data':
            leites = Leite.objects.filter(
                    Q(data__icontains=pesquisa_data) & Q(usuario=request.user.id)
            ).order_by('-data')
        elif tipo_pesquisa == 'quantidade':
            leites = Leite.objects.filter(
                    Q(quantidade__icontains=pesquisa) & Q(usuario=request.user.id)
            ).order_by('-data')
        
        leite_paginator = Paginator(leites,10)
        page_num = request.GET.get('page')
        page = leite_paginator.get_page(page_num)

        return render(request,'gerenciar_leite.html',{'page': page})
    
@login_required
def importar_planilha(request):
    if request.method == 'GET':
        return render(request,'importar_planilha.html')
    elif request.method == 'POST':
        print(request.FILES)
        sheet = pd.read_csv(request.FILES.get('sheet'))
        
        for index,row in sheet.iterrows():
            
            leite = Leite(quantidade=row.quantidade,data=row.data, 
                          usuario=request.user)
            leite.save()

        return render(request,'importar_planilha.html', {'msg_sucesso':'Planilha importada!'})





#CADASTRO DE SOMAS
@login_required
def cadastrar_soma(request):
    if request.method == 'POST':
        leites = request.POST.getlist('leites[]')
        total_litros = request.POST.get('total_litro')
        total = request.POST.get('total')
        preco = request.POST.get('preco')
        de = request.POST.get('de')
        ate = request.POST.get('ate')
        soma_check = Soma.objects.filter((Q(data_inicio = de) | Q(data_fim=ate)) & Q(usuario=request.user.id))

        if soma_check.exists():
            return render(request,'somar.html',{'msg_erro':'Registro de leite já existe no banco!'})
        
        soma = Soma(quantidade=total_litros, total=total, preco_litro=preco, data_inicio=de, data_fim=ate,usuario=request.user)
        soma.save()
        for id in leites:
            leite = Leite.objects.get(id=id)
            leite.soma = soma
            leite.save() 
        
        return render(request,'somar.html',{'msg_sucesso':'Registrado!'})


#SOMAS
@login_required
def somas(request):
    if request.method == 'GET':        
        somas = Soma.objects.filter(usuario=request.user.id)
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
                                            Q(data_fim__contains=data_pesquisa) &
                                            Q(usuario=request.user.id))
            elif tipo_pesquisa == 'id':
                somas = Soma.objects.filter(Q(id__contains=pesquisa) & Q(usuario=request.user.id))
            elif tipo_pesquisa == 'quantidade':
                somas = Soma.objects.filter(Q(quantidade__contains=pesquisa) & Q(usuario=request.user.id))
            elif tipo_pesquisa == 'total':
                somas = Soma.objects.filter(Q(total__contains=pesquisa) & Q(usuario=request.user.id))
            elif tipo_pesquisa == 'preco':
                somas = Soma.objects.filter(Q(preco_litro__contains=pesquisa) & Q(usuario=request.user.id))
            elif tipo_pesquisa == 'data_inicio':
                somas = Soma.objects.filter(Q(data_inicio__contains=data_pesquisa) & Q(usuario=request.user.id))
            elif tipo_pesquisa == 'data_fim':
                somas = Soma.objects.filter(Q(data_fim__contains=data_pesquisa) & Q(usuario=request.user.id))
        
        return render(request,'somas.html',{'somas':somas})
    

#DELETAR SOMAS
@login_required
def deletar_soma(request, pk_id):
    
    leites = Leite.objects.filter(soma=pk_id)
    for leite in leites:
        leite.soma = None
        leite.save()

    soma = Soma.objects.filter(id=pk_id)
    soma.delete() 
    return redirect('somas')


#GERAÇÃO DE RELATÓRIOS
@login_required
def gerar_relatorio(request):

    if request.method == 'POST':
        
        caminho = path.join(BASE_DIR, "leite/templates/ver_registro.html")
        tabela = request.POST.get('tabela')
        template_w = open(caminho, "w")       
        
        template_w.write(tabela)
        template_w.close()

        pdf = utils.gerar_relatorio(caminho)
        
        return HttpResponse(pdf,content_type="application/pdf")