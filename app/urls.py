
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name='login'),
    path('logout', views.logout, name='logout'),
    path('home/',views.home,name='home'),
    path('cadastrarusuario/',views.criar_usuario, name='cad_usuario'),
    path('leite/', include('leite.urls')),
    path('chuva/',include('chuva.urls')),
    path('registros/',views.dados_soma, name="dados_soma"),
    path('leites/', views.dados_registro, name='ver_reg'),
    path('chuvas/',views.dados_chuva, name='dados_chuva')
]
