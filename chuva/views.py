from django.shortcuts import render, get_object_or_404, redirect
from .models import Chuva
from django.db import IntegrityError
from django.core.paginator import Paginator 
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def cadastrar_chuva(request):
    if request.method == 'GET':
        return render(request,'cadastrar_chuva.html')
    elif request.method == 'POST':
        quantidade = request.POST.get('quantidade')
        data = request.POST.get('data')
        chuva = Chuva(milimetros=quantidade,data=data,usuario=request.user)
        try:
            chuva.save()
            return render(request,'cadastrar_chuva.html',{'msg_sucesso':'Chuva cadastrada!'})
        except IntegrityError:
            return render(request,'cadastrar_chuva.html',{'msg_erro':'Erro! Data duplicada'})


@login_required
def gerenciar_chuvas(request):
    if request.method == 'GET':
        chuvas = Chuva.objects.filter(usuario=request.user.id).order_by('-data')
        chuva_paginator = Paginator(chuvas,10)
        page_num = request.GET.get('page')
        page = chuva_paginator.get_page(page_num)
        return render(request,'gerenciar_chuvas.html',{'page': page})
    

@login_required
def alterar_chuvas(request, pk_id):
    chuva = get_object_or_404(Chuva, id=pk_id)
    if request.method == 'GET':       
        return render(request,'alterar_chuvas.html',{'chuva':chuva})
    elif request.method == 'POST':
        chuva.milimetros = request.POST.get('milimetros')
        chuva.data = request.POST.get('data')
        chuva.save()
        return redirect('ger_chuvas')
    

@login_required
def deletar_chuva(request, pk_id):
    if request.method == 'GET':
        chuva = get_object_or_404(Chuva, id=pk_id)
        chuva.delete()
        return redirect('ger_chuvas')        
    

