from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404,redirect
from .models import Gado
from django.core.paginator import Paginator
from django.db.models import Q

def cadastrar_gado(request):
    if request.method == 'GET':
        return render(request,'cadastrar_gado.html')
    elif request.method == 'POST':
        if request.POST.get('leitera') == 'on':
            leitera = True
        else:
            leitera = False
        gado = Gado(nome=request.POST.get('nome'),
                    leitera=leitera,
                    tipo=request.POST.get('tipo_gado'),
                    usuario=request.user)
        try:
            gado.save()
            return render(request,'cadastrar_gado.html',{'msg_sucesso':'Gado cadastrado'})
        except IntegrityError:
            return render(request,'cadastrar_gado.html',{'msg_erro':'Gado já existe!'})


def gerenciar_gado(request):
    if request.method == 'GET':
        gados = Gado.objects.filter(usuario=request.user.id).order_by('-nome')

        gado_paginator = Paginator(gados,10)
        page_num = request.GET.get('page')
        page = gado_paginator.get_page(page_num)

        return render(request,'gerenciar_gado.html',{'page': page})


def alterar_gado(request, pk_id):
    gado = get_object_or_404(Gado,id=pk_id)
    if request.method == 'GET':
        return render(request,'alterar_gado.html',{'gado':gado})
    elif request.method == 'POST':
        if request.POST.get('leitera') == 'on':
            leitera = True
        else:
            leitera = False
        gado.nome = request.POST.get('nome')
        gado.tipo = request.POST.get('tipo_gado')
        gado.leitera = leitera
        gado.save()
        return redirect('ger_gado')



def deletar_gado(request, pk_id):
    if request.method == 'GET':
        gado = get_object_or_404(Gado,id=pk_id)
        gado.delete()
        return redirect('ger_gado')


def pesquisar_gado(request):
    if request.method == 'POST':
        pesquisa = request.POST.get('pesquisa')
        tipo_pesquisa = request.POST.get('tipo_pesquisa')

        print(pesquisa)
        print(tipo_pesquisa)
        if tipo_pesquisa == 'tudo':
            gado = Gado.objects.filter(
                    ((Q(nome__icontains=pesquisa) |
                    Q(id__icontains=pesquisa) |
                    Q(tipo__icontains=pesquisa)) &
                    Q(usuario=request.user.id))
            ).order_by('-nome')
        elif tipo_pesquisa == 'id':
            gado = Gado.objects.filter(
                    Q(id__icontains=pesquisa) & Q(usuario=request.user.id)
            ).order_by('-nome')
        elif tipo_pesquisa == 'tipo':
            gado = Gado.objects.filter(
                    Q(tipo__icontains=pesquisa) & Q(usuario=request.user.id)
            ).order_by('-nome')
        elif tipo_pesquisa == 'nome':
            gado = Gado.objects.filter(
                Q(nome__icontains=pesquisa) & Q(usuario=request.user.id)
            ).order_by('-nome')
        
        gado_paginator = Paginator(gado,10)
        page_num = request.GET.get('page') 
        page = gado_paginator.get_page(page_num)

        return render(request,'gerenciar_gado.html',{'page': page})
    