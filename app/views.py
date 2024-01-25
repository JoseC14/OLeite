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


@login_required
def home(request):
    if request.method == 'GET':

        total_leite = Leite.objects.aggregate(soma=Sum('quantidade'))['soma']
        total_chuvas = Chuva.objects.all().count()
        leite_entregue = Leite.objects.all().count()
        ganho = Soma.objects.aggregate(soma=Sum('total'))['soma']
        media = Leite.objects.aggregate(media=Avg('quantidade'))['media']
        total_milimetros = Chuva.objects.aggregate(soma=Sum('milimetros'))['soma']
    
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
    data = list(Chuva.objects.values())
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
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = User.objects.create_user(usuario,email,senha)
        user.save()
        return redirect('login')