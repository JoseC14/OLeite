from django.shortcuts import get_object_or_404, redirect, render
from .models import Despesa
from django.core.paginator import Paginator
from django.db.models import Q

def cad_despesa(request):
    if request.method == 'GET':
        return render(request,'cadastrar_despesa.html')
    elif request.method == 'POST':
        despesa = Despesa(tipo=request.POST.get('tipo'),
                          gasto=request.POST.get('gasto'),
                          usuario=request.user)
        despesa.save()
        return render(request,'cadastrar_despesa.html',{'msg_sucesso':'Despesa cadastrada!'})
    
def ger_despesa(request):
    if request.method == 'GET':
        despesas = Despesa.objects.filter(usuario=request.user.id)

        despesa_paginator = Paginator(despesas,10)
        page_num = request.GET.get('page')
        page = despesa_paginator.get_page(page_num)

        return render(request,'gerenciar_despesas.html',{'page': page})

def upd_despesa(request,pk_id):
    despesa = get_object_or_404(Despesa,id=pk_id)
    if request.method == 'GET':
        return render(request,'alterar_despesa.html',{'despesa':despesa})
    elif request.method == 'POST':
        despesa.tipo = request.POST.get('razao')
        despesa.gasto = request.POST.get('gasto')
        despesa.save()
        return redirect('ger_despesas')

def del_despesa(request,pk_id):
    if request.method == 'GET':
        despesa = get_object_or_404(Despesa,id=pk_id)
        despesa.delete()
        return redirect('ger_despesas')
    
def pes_despesa(request):
    if request.method == 'POST':
        pesquisa = request.POST.get('pesquisa')
        tipo_pesquisa = request.POST.get('tipo_pesquisa')

        if tipo_pesquisa == 'tudo':
            despesas = Despesa.objects.filter(
                (Q(id__contains=pesquisa) |
                Q(tipo__icontains=pesquisa) |
                Q(gasto__icontains=pesquisa)) &
                Q(usuario=request.user.id))
        elif tipo_pesquisa == 'motivo':
            despesas = Despesa.objects.filter(
                tipo__icontains=pesquisa
            )
        elif tipo_pesquisa == 'gasto':
            despesas = Despesa.objects.filter(
                gasto__icontains=pesquisa
            )
        elif tipo_pesquisa == 'id':
            despesas = Despesa.objects.filter(
                id__contains=pesquisa
            )
        despesa_paginator = Paginator(despesas,10)
        page_num = request.GET.get('page') 
        page = despesa_paginator.get_page(page_num)

        return render(request,'gerenciar_despesas.html',{'page': page})
