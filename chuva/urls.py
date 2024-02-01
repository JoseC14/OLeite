from django.urls import path
from . import views

urlpatterns=[
    path('cadastrarchuva/',view=views.cadastrar_chuva,name='cad_chuva'),
    path('gerenciarchuvas/',view=views.gerenciar_chuvas, name='ger_chuvas'),
    path('alterarchuvas/<int:pk_id>', view=views.alterar_chuvas, name='upd_chuva'),
    path('deletarchuva/<int:pk_id>', view=views.deletar_chuva, name='del_chuva'),
    path('pesquisarchuvas/',view=views.pesquisar_chuvas,name='pes_chuvas')
]