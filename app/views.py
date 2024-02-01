from django.shortcuts import render, redirect
from leite.models import Leite
from chuva.models import Chuva
from leite.models import Soma
from django.db.models import Sum
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    if request.method == 'GET':

        total_leite = Leite.objects.filter(usuario=request.user.id).aggregate(soma=Sum('quantidade'))['soma']
        total_chuvas = Chuva.objects.filter(usuario=request.user).count()
        leite_entregue = Leite.objects.filter(usuario=request.user.id).count()
        ganho = Soma.objects.filter(usuario=request.user.id).aggregate(soma=Sum('total'))['soma']
        media = Leite.objects.filter(usuario=request.user.id).aggregate(media=Avg('quantidade'))['media']
        total_milimetros = Chuva.objects.filter(usuario=request.user.id).aggregate(soma=Sum('milimetros'))['soma']
    
        return render(request,'home.html',
                      {'total_leite':total_leite,
                       'leite_entregue':leite_entregue,
                       'ganho':ganho,
                       'media':media,
                       'total_chuvas':total_chuvas,
                       'total_milimetros':total_milimetros})

@login_required  
def dados_registro(request):
    data = list(Leite.objects.filter(usuario=request.user.id).values())
    return JsonResponse(data,safe=False)

@login_required
def dados_soma(request):
    data = list(Soma.objects.filter(usuario=request.user.id).values())
    return JsonResponse(data,safe=False)

@login_required
def dados_chuva(request):
    data = list(Chuva.objects.filter(usuario=request.user.id).values())
    return JsonResponse(data,safe=False)


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')      
        else:
            return render(request,'login.html')
    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(request,username=usuario,password=senha)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'msg_erro':'Login ou senha inválidos'})


@login_required
def logout(request):
    if request.method == 'GET':
        auth_logout(request)
        return redirect('login') 
    

def criar_usuario(request):
    if request.method == 'GET':
        return render(request,'cadastrar_usuario.html')
    elif request.method == 'POST':
        primeiro_nome = request.POST.get('primeiro_nome')
        segundo_nome = request.POST.get('sobrenome')
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if primeiro_nome or segundo_nome is None:
           return render(request,'cadastrar_usuario.html',{'msg_erro':'Erro! Campos não preenchidos'})
        try:
            user = User.objects.create_user(
                username=usuario,
                email=email,
                password=senha,
            )
            user.first_name = primeiro_nome
            user.last_name = segundo_nome
            user.save()
            return render(request,'login.html',{'msg_sucesso':'Você se cadastrou com sucesso! Use seu usuário e senha para continuar'})
        except ValueError:
            return render(request,'cadastrar_usuario.html',{'msg_erro':'Erro! Campos não preenchidos'})
        