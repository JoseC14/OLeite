
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name='login'),
    path('logout', views.logout, name='logout'),
    path('home/',views.home,name='home'),
    path('cadastrarusuario/',views.criar_usuario, name='cad_usuario'),
    path('inseriremail/',views.inserir_email, name='inserir_email'), 
    path('inserircodigo/',views.enviar_codigo, name='env_codigo'),
    path('recuperarconta/',views.recuperar_conta,name='rec_conta'),
    path('redefiirsenha/', views.redefinir_senha,name='redefinir_senha'),
    path('leite/', include('leite.urls')),
    path('chuva/',include('chuva.urls')),
    path('despesa/',include('despesa.urls')), 
    path('relatorios/',include('relatorios.urls')),
    path('registros/',views.dados_soma, name="dados_soma"),
    path('leites/', views.dados_registro, name='ver_reg'),
    path('chuvas/',views.dados_chuva, name='dados_chuva'),
    path('gados/',include('gado.urls')) 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
