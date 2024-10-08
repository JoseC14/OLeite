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
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import PassRecovery
from django.shortcuts import get_object_or_404
import random
#VIEW DA HOME
@login_required
def home(request):
    if request.method == 'GET':

        total_leite = Leite.objects.filter(usuario=request.user.id).aggregate(soma=Sum('quantidade'))['soma']
        total_chuvas = Chuva.objects.filter(usuario=request.user).count()
        leite_entregue = Leite.objects.filter(usuario=request.user.id).count()
        ganho = Soma.objects.filter(usuario=request.user.id).aggregate(soma=Sum('total'))['soma']
        media = Leite.objects.filter(usuario=request.user.id).aggregate(media=Avg('quantidade'))['media']
        total_milimetros = Chuva.objects.filter(usuario=request.user.id).aggregate(soma=Sum('milimetros'))['soma']
        ultima_chuva = Chuva.objects.filter(usuario=request.user).last()
        return render(request,'home.html',
                      {'total_leite':total_leite,
                       'leite_entregue':leite_entregue,
                       'ganho':ganho,
                       'media':media,
                       'total_chuvas':total_chuvas,
                       'total_milimetros':total_milimetros,
                       'ultima_chuva':ultima_chuva})

#RETORNO DE REGISTROS DE LEITE
@login_required  
def dados_registro(request):
    data = list(Leite.objects.filter(usuario=request.user.id).values())
    return JsonResponse(data,safe=False)

#RETORNO DE REGISTRO DE SOMAS
@login_required
def dados_soma(request):
    data = list(Soma.objects.filter(usuario=request.user.id).values())
    return JsonResponse(data,safe=False)

#RETORNO DE REGISTRO DE CHUVAS
@login_required
def dados_chuva(request):
    data = list(Chuva.objects.filter(usuario=request.user.id).values())
    return JsonResponse(data,safe=False)


#LOGIN
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

#LOGOUT
@login_required
def logout(request):
    if request.method == 'GET':
        auth_logout(request)
        return redirect('login') 
    
#FUNÇÃO DE CIRAR USUARIO
def criar_usuario(request):
    if request.method == 'GET':
        return render(request,'cadastrar_usuario.html')
    elif request.method == 'POST':
        primeiro_nome = request.POST.get('primeiro_nome')
        segundo_nome = request.POST.get('sobrenome')
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        has_user = User.objects.filter(username=usuario)
        has_email = User.objects.filter(email=email)

        if has_user.exists():
            return render(request,'cadastrar_usuario.html',{'msg_erro':'Nome de usuário já cadastrado!'})
        if has_email.exists():
            return render(request,'cadastrar_usuario.html',{'msg_erro':'Email já cadastrado!'})

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
            return render(request,'cadastrar_usuario.html',{'msg_erro':'Erro'})

def inserir_email(request):
    if request.method == 'GET':
        return render(request,'inseriremail.html')
    
def enviar_codigo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        recovery_code = ""
        for x in range(0,6):
            recovery_code += str(random.randint(0,9))

        pass_recovery = PassRecovery(code=recovery_code,email=email)
        pass_recovery.save()

        send_mail(
            "Recuperação de Senha",
            f"Seu código de recuperação:{recovery_code}",
            "josecarlosv8474@gmail.com",
            [email]
        )

        return render(request,'recuperarsenha.html',{'codigo':recovery_code,'email':email})

def recuperar_conta(request):
    if request.method == 'POST':
        codigo_user = request.POST.get('codigo_user')
        email = request.POST.get('email')
        pass_recovery = PassRecovery.objects.filter(code=codigo_user,email=email)
        if pass_recovery.exists():
            return render(request,'redefinirsenha.html',{'email':email})

def redefinir_senha(request):
    if request.method == 'POST':
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        try:
            senha_usuario = User.objects.get(email=email)   
            senha_usuario.set_password(senha)
            senha_usuario.save()
            codigo = PassRecovery.objets.get(email=email)
            codigo.delete()
        except Exception as e:
            print(e)
        return render(request,'login.html',{'msg_sucesso':'Senha alterada com sucesso!'})
    
