from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_despesa/', views.cad_despesa, name='cad_despesa'),
    path('gerenciar_despesa/',views.ger_despesa, name='ger_despesas'),
    path('alterardespesa/<int:pk_id>/',views.upd_despesa,name='upd_despesa'),
    path('deletardespesa/<int:pk_id>/',views.del_despesa,name='del_despesa'),
    path('pesquisardespesa/',views.pes_despesa,name='pes_despesas')
]