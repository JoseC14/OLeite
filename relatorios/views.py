from os import path
from django.http import HttpResponse
from django.shortcuts import render
from app.settings import BASE_DIR
from leite import utils
from leite.models import Leite
from chuva.models import Chuva
from gado.models import Gado
from despesa.models import Despesa
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Avg


@login_required
def rel_leite(request):
    if request.method == 'GET':
        return render(request,'relleite.html')
    elif request.method == 'POST':
        quant_de = request.POST.get('quant_de')
        quant_ate = request.POST.get('quant_ate')
        data_de = request.POST.get('data_de')
        data_ate = request.POST.get('data_ate')
        preco_de = request.POST.get('preco_de')
        preco_ate = request.POST.get('preco_ate')
        
        if utils.checa_data_de_ate(data_de,data_ate):
            return render(request,'relleite.html',{'msg_erro':'Data de inicio não pode ser maior que data de fim!'})
        query = Q(data__range=(data_de, data_ate)) & Q(usuario=request.user.id)

        if quant_de and quant_ate:
           query &= Q(quantidade__range=(quant_de, quant_ate))

        if preco_de and preco_ate:
            query &= Q(preco__range=(preco_de, preco_ate))

        
        leites = Leite.objects.filter(query)
        media = leites.aggregate(Avg("quantidade"))
        return render(request,'relleite.html',{'leites':leites,
                                               'media':media,
                                               'data_de':data_de,
                                               'data_ate':data_ate})

@login_required
def gerar_relatorio_leite(request):
    caminho = path.join(BASE_DIR, "relatorios/templates/relatorio.html")
    tabela = request.POST.get('tabela')
    template_w = open(caminho, "w")       
    
    template_w.write(tabela)
    template_w.close()

    pdf = utils.gerar_relatorio(caminho)
    
    return HttpResponse(pdf,content_type="application/pdf")

@login_required
def rel_chuvas(request):
    if request.method == 'GET':
        return render(request,'relchuva.html')
    elif request.method == 'POST':
        quant_de = request.POST.get('quant_de')
        quant_ate = request.POST.get('quant_ate')
        data_de = request.POST.get('data_de')
        data_ate = request.POST.get('data_ate')

        if utils.checa_data_de_ate(data_de,data_ate):
            return render(request,'relchuva.html',{'msg_erro':'Data de inicio não pode ser maior que data de fim!'})
        query = Q(data__range=(data_de, data_ate)) & Q(usuario=request.user.id)

        if quant_de and quant_ate:
           query &= Q(quantidade__range=(quant_de,quant_ate))

        chuvas = Chuva.objects.filter(query)
        media = chuvas.aggregate(Avg("milimetros"))
        return render(request,'relchuva.html',{'chuvas':chuvas,
                                               'media':media,
                                               'data_de':data_de,
                                               'data_ate':data_ate})
    
@login_required
def rel_gado(request):
    if request.method == 'GET':
        return render(request,'relgado.html')
    elif request.method == 'POST':
       nome = request.POST.get('nome') 
       tipo = request.POST.get('tipo_gado')
       leitera = request.POST.get('leitera')
       
       query = Q(usuario=request.user)
       if tipo != 'tudo':
           query &= Q(tipo=tipo)         

       if nome:
           query &= Q(nome__icontains=nome)
        
       if leitera:
           query &= Q(leitera=True)

       gado = Gado.objects.filter(query)
       return render(request,'relgado.html',{'gado':gado})

@login_required
def rel_despesa(request):
    if request.method == 'GET':
        return render(request,'reldespesa.html')
    elif request.method == 'POST':
        motivo = request.POST.get('motivo')
        gasto_de = request.POST.get('gasto_de')
        gasto_ate = request.POST.get('gasto_ate')

        query = Q(usuario=request.user)

        if motivo:
            query &= Q(tipo__icontains=motivo)
        
        if gasto_de and gasto_ate:
            query &= Q(gasto__range=(gasto_de,gasto_ate))

        despesas = Despesa.objects.filter(query)

        return render(request,'reldespesa.html',{'despesas':despesas})
       
