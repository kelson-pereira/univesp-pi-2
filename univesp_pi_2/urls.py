"""
Configurações de URL para projeto univesp_pi_2.

A lista `urlpatterns` roteia URLs para visualizações. Para mais informações consulte:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Exemplos:
Função views
    1. Adicione a importação:  from my_app import views
    2. Adicione a URL em urlpatterns:  path('', views.home, name='home')
Views baseada em uma classe:
    1. Adicione a importação:  from other_app.views import Home
    2. Adicione a URL em urlpatterns:  path('', Home.as_view(), name='home')
Incluindo outra configuração de URL:
    1. Importe a função include(): from django.urls import include, path
    2. 
"""
from django.contrib import admin
from django.urls import path
from combate_aedes import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]
