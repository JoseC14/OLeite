from django.urls import path,include
from . import views

urlpatterns = [
    path('relleites/',views.rel_leite,name='rel_leite'),
    path('gerarrelatorio/', views.gerar_relatorio_leite,name='ger_rel'),
    path('relchuvas/',view=views.rel_chuvas, name='rel_chuvas'),
    path('relgado/',views.rel_gado,name='rel_gado'),
    path('reldespesa/',views.rel_despesa, name='rel_despesa')
]