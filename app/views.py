from django.shortcuts import render
from leite.models import Leite
from leite.models import Soma
from django.db.models import Sum
from django.db.models import Avg
from django.http import JsonResponse


def home(request):
    if request.method == 'GET':

        total_leite = Leite.objects.aggregate(soma=Sum('quantidade'))['soma']
        leite_entregue = Leite.objects.all().count()
        ganho = Soma.objects.aggregate(soma=Sum('total'))['soma']
        media = Leite.objects.aggregate(media=Avg('quantidade'))['media']

    
        return render(request,'home.html',
                      {'total_leite':total_leite,
                       'leite_entregue':leite_entregue,
                       'ganho':ganho,
                       'media':media})
    
def dados_registro(request):
    data = list(Leite.objects.values())
    return JsonResponse(data,safe=False)

def dados_soma(request):
    data = list(Soma.objects.values())
    return JsonResponse(data,safe=False)