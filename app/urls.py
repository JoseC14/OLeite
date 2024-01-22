
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('leite/', include('leite.urls')),
    path('registros/',views.dados_soma, name="dados_soma"),
    path('leites/', views.dados_registro, name='ver_reg'),
]
