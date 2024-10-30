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
from django.urls import path, re_path
from combate_aedes import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    re_path(r'^favicon\.ico$', views.favicon),
    path('registrar_cep', views.registrar_cep, name='registrar_cep'),
    path('registrar_numero', views.registrar_numero, name='registrar_numero'),
    path('registrar_localizacao', views.registrar_localizacao, name='registrar_localizacao'),
    path('registrar_telefone', views.registrar_telefone, name='registrar_telefone'),
    path('registrar_descricao', views.registrar_descricao, name='registrar_descricao'),
    path('registrar_foto', views.registrar_foto, name='registrar_foto'),
    path('registrar_politica', views.registrar_politica, name='registrar_politica'),
    path('registros', views.registros, name='registros'),
    path('registros_telefone', views.registros_telefone, name='registros_telefone'),
    path('registros_visualizar/<int:ident>', views.registros_visualizar, name='registros_visualizar'),
    path('registros_apagar/<int:ident>', views.registros_apagar, name='registros_apagar'),
    path('analise_estado', views.analise_estado, name='analise_estado'),
    path('analise_cidade', views.analise_cidade, name='analise_cidade'),
    path('analise_mapa', views.analise_mapa, name='analise_mapa'),
    path('analise_relatorio', views.analise_relatorio, name='analise_relatorio'),
    path('mais_mosquito', views.mais_mosquito, name='mais_mosquito'),
    path('mais_criadouros', views.mais_criadouros, name='mais_criadouros'),
]
