from django.urls import path
from . import views


urlpatterns = [
    path('',views.home),
    path('cadastrarleite/', views.cadastrar_leite, name='cad_leite'),
    path('gerenciarleite/' ,views.gerenciar_leite, name='ger_leite'),
    path('somarleite/', views.somar_leite,name='sum_leite'),
    path('deletarleite/<int:pk_id>', views.deletar_leite, name='del_leite'),
    path('alterarleite/<int:pk_id>', views.alterar_leite, name='upd_leite'),
    path('pesquisaleite/',views.pesquisar_leite,name='pes_leite')
]