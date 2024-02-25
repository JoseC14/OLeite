from django.urls import path
from . import views


urlpatterns = [
    path('cadastrargado',view=views.cadastrar_gado,name='cad_gado'),
    path('gerenciargado',view=views.gerenciar_gado,name='ger_gado'),
    path('alterargado/<int:pk_id>',view=views.alterar_gado,name='upd_gado'),
    path('deletargado/<int:pk_id>',view=views.deletar_gado,name='del_gado'),
    path('pesquisargado',view=views.pesquisar_gado,name='pes_gado')
]