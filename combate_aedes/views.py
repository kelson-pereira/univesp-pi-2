from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.utils import timezone
from django.http import FileResponse
from django.views.generic.base import RedirectView
from datetime import datetime, timedelta
from django.utils import formats
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing
from svglib.svglib import svg2rlg
from reportlab.lib.utils import ImageReader
from io import BytesIO
from .models import Registro
from .forms import *

import brazilcep
import googlemaps

google_api_key = settings.GOOGLE_API_KEY
google_map_id = settings.GOOGLE_MAP_ID

# Crie suas visualizações aqui.

favicon = RedirectView.as_view(url='/static/imagens/favicon.ico', permanent=True)

# Exibe a página principal
def home(request):
    return render(request, 'home.html', {'google_api_key': google_api_key})

# Verifica se o CEP existe
def obtem_endereco(cep):
    try:
        gmaps = googlemaps.Client(key=google_api_key, timeout=5)
        resultado = gmaps.geocode(f"{cep}, Brasil")
        componentes = resultado[0]['address_components']
        for componente in componentes:
            if 'route' in componente['types']:
                logradouro = componente['long_name']
            elif 'sublocality' in componente['types']:
                bairro = componente['long_name']
            elif 'administrative_area_level_2' in componente['types']:
                cidade = componente['long_name']
            elif 'administrative_area_level_1' in componente['types']:
                estado = componente['short_name']
        return True, logradouro, bairro, cidade, estado
    except:
        try:
            endereco = brazilcep.get_address_from_cep(cep, timeout=5)
            return True, endereco['street'], endereco['district'], endereco['city'], endereco['uf']
        except:
            return False, "", "", "", ""

# Obtém as Coordenadas Geográficas (latitude e longitude)
def obtem_coordenadas(logradouro, numero, bairro, cidade, estado, pais="Brasil"):
    gmaps = googlemaps.Client(key=google_api_key)
    try:
        geocode_result = gmaps.geocode(f"{logradouro}, {numero}, {bairro}, {cidade}, {estado}, {pais}")
        return True, geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']
    except:
        return False, "", ""


# Valida o CEP
def registrar_cep(request):
    # GET e estado inicial
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        # entrega o formulário vazio
        form = ValidarCep()
        form.initial.setdefault('cep', request.COOKIES.get('cep'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe o CEP:', 'icone': 'house-fill' })
        # define o cookie para validar
        response.set_cookie('form', 'validar')
        return response
    # POST e estado validar
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        # verifica se o valor digitado é válido
        form = ValidarCep(request.POST)
        if form.is_valid():
            # a estrutura do cep é validada
            cep = form.cleaned_data['cep']
            cep_encontrado, logradouro, bairro, cidade, estado = obtem_endereco(cep)
            endereco = f"{logradouro}, {bairro} - {cidade}/{estado}"
            if not cep_encontrado:
                return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o CEP:', 'icone': 'house-fill', 'mensagem_erro': 'CEP não encontrado.' })
            form = ValidarNumero()
            request.path = 'registrar_numero'
            form.initial.setdefault('numero', request.COOKIES.get('numero'))
            response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'registrar_cep', 'icone': 'signpost-fill', 'endereco': endereco })
            # define o cookie para o cep
            response.set_cookie('cep', cep)
            # define o cookie para o logradouro
            response.set_cookie('logradouro', logradouro)
            # define o cookie para o bairro
            response.set_cookie('bairro', bairro)
            # define o cookie para o cidade
            response.set_cookie('cidade', cidade)
            # define o cookie para o estado
            response.set_cookie('estado', estado)
            # define o cookie para inicial
            response.set_cookie('form', 'validar')
            # encaminha para o próximo form
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o CEP:', 'icone': 'house-fill' })

# Valida o Número
def registrar_numero(request):
    logradouro = request.COOKIES.get('logradouro')
    bairro = request.COOKIES.get('bairro')
    cidade = request.COOKIES.get('cidade')
    estado = request.COOKIES.get('estado')
    endereco = f"{logradouro}, {bairro} - {cidade}/{estado}"
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarNumero()
        form.initial.setdefault('numero', request.COOKIES.get('numero'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'registrar_cep', 'icone': 'signpost-fill', 'endereco': endereco })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarNumero(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero']
            coord_encontradas, latitude, longitude = obtem_coordenadas(logradouro, numero, bairro, cidade, estado)
            request.path = 'registrar_telefone'
            response = render(request, 'registrar/localizacao.html', {'voltar': 'registrar_numero', 'google_api_key': google_api_key, 'google_map_id': google_map_id, 'latitude': str(latitude), 'longitude': str(longitude)})
            response.set_cookie('numero', numero)
            response.set_cookie('latitude', latitude)
            response.set_cookie('longitude', longitude)
            response.set_cookie('form', 'inicial')
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'registrar_cep', 'icone': 'signpost-fill', 'endereco': endereco })

# Valida o Telefone
def registrar_telefone(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarTelefone()
        form.initial.setdefault('telefone', request.COOKIES.get('telefone'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'voltar': 'registrar_numero', 'icone': 'telephone-fill' })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarTelefone(request.POST)
        if form.is_valid():
            telefone = form.cleaned_data['telefone']
            form = ValidarDescricao()
            request.path = 'registrar_descricao'
            form.initial.setdefault('descricao', request.COOKIES.get('descricao'))
            response = render(request, 'modal.html', {'form': form, 'titulo': 'Descreva o local:', 'voltar': 'registrar_telefone', 'icone': 'clipboard-plus-fill' })
            response.set_cookie('telefone', telefone)
            response.set_cookie('form', 'validar')
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'voltar': 'registrar_numero', 'icone': 'telephone-fill' })

# Valida a Descrição NOVA
def registrar_descricao(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarDescricao()
        form.initial.setdefault('descricao', request.COOKIES.get('descricao'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Descreva o local:', 'voltar': 'registrar_telefone', 'icone': 'clipboard-plus-fill' })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarDescricao(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data['descricao']
            form = ValidarPolitica()
            request.path = 'registrar_politica'
            response = render(request, 'registrar/politica.html', {'form': form, 'titulo': 'Privacidade:', 'voltar': 'registrar_descricao', 'icone': 'shield-fill-check' })
            response.set_cookie('descricao', descricao)
            response.set_cookie('form', 'validar')
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Descreva o local:', 'voltar': 'registrar_telefone', 'icone': 'clipboard-plus-fill' })

# Valida a Política e cria o registro no banco de dados
def registrar_politica(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarPolitica()
        form.initial.setdefault('termos', request.COOKIES.get('termos'))
        response = render(request, 'registrar/politica.html', {'form': form, 'titulo': 'Privacidade:', 'voltar': 'registrar_descricao', 'icone': 'shield-fill-check' })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarPolitica(request.POST)
        if form.is_valid():
            try:
                # cria o registro no banco de dados
                registro = Registro()
                registro.cep = request.COOKIES.get('cep')
                registro.endereco = request.COOKIES.get('logradouro')
                registro.numero = request.COOKIES.get('numero')
                registro.bairro = request.COOKIES.get('bairro')
                registro.cidade = request.COOKIES.get('cidade')
                registro.estado = request.COOKIES.get('estado')
                registro.telefone = request.COOKIES.get('telefone')
                registro.descricao = request.COOKIES.get('descricao')
                registro.latitude = request.COOKIES.get('latitude')
                registro.longitude = request.COOKIES.get('longitude')
                registro.termos = form.cleaned_data['termos']
                registro.save()
                # retorna para a tela registrar e limpa os cookies
                response = render(request, 'registrar/registro.html', {"mensagem": "Registro salvo com sucesso!"})
                response.delete_cookie('cep')
                response.delete_cookie('logradouro')
                response.delete_cookie('numero')
                response.delete_cookie('bairro')
                response.delete_cookie('cidade')
                response.delete_cookie('estado')
                #response.delete_cookie('telefone')
                response.delete_cookie('descricao')
                response.delete_cookie('endereco')
                response.delete_cookie('latitude')
                response.delete_cookie('longitude')
                response.delete_cookie('form')
                return response
            except:
                return render(request, 'registrar/registro.html', {"mensagem": "Erro ao salvar o registro."})
        else:
            return render(request, 'registrar/politica.html', {'form': form, 'titulo': 'Privacidade:', 'voltar': 'registrar_descricao', 'icone': 'shield-fill-check' })

# Adiciona uma foto
def registrar_foto(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        response = render(request, 'registrar/foto.html', {'titulo': 'Adicionar uma foto:', 'voltar': 'registrar_foto', 'icone': 'camera-fill' })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        return render(request, 'registrar/foto.html', {'titulo': 'Privacidade:', 'voltar': 'registrar_foto', 'icone': 'camera-fill' })

# Valida a localização
def registrar_localizacao(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        latitude = request.COOKIES.get('latitude')
        longitude = request.COOKIES.get('longitude')
        return render(request, 'registrar/localizacao.html', {'voltar': 'registrar_numero', 'google_map_id': google_map_id, 'latitude': latitude, 'longitude': longitude })
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        request.path = 'registrar_telefone'
        form = ValidarTelefone()
        form.initial.setdefault('telefone', request.COOKIES.get('telefone'))
        return render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'voltar': 'registrar_numero', 'icone': 'telephone-fill' })

# Obtem o Telefone
def registros_telefone(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarTelefone()
        form.initial.setdefault('telefone', request.COOKIES.get('telefone'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'icone': 'telephone-fill', 'header': 'Meus registros' })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarTelefone(request.POST)
        if form.is_valid():
            telefone = form.cleaned_data['telefone']
            forty_days = timezone.now() - timedelta(days = 40)
            registros = Registro.objects.filter(datahora__gte=forty_days, telefone=telefone).values('ident', 'datahora', 'endereco', 'numero', 'descricao')
            response = render(request, 'registros/registros.html', {"registros": registros, 'voltar': 'registros_telefone' })
            response.set_cookie('telefone', telefone)
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'icone': 'telephone-fill', 'header': 'Meus registros' })

def registros(request):
    forty_days = timezone.now() - timedelta(days = 40)
    telefone = request.COOKIES.get('telefone')
    registros = Registro.objects.filter(datahora__gte=forty_days, telefone=telefone).values('ident', 'datahora', 'endereco', 'numero', 'descricao')
    return render(request, 'registros/registros.html', {"registros": registros, 'voltar': 'registros_telefone',})

def registros_visualizar(request, ident):
    registro = Registro.objects.get(ident=ident)
    latitude = str(registro.latitude)
    longitude = str(registro.longitude)
    return render(request, 'registros/visualizar.html', {"registro": registro, 'voltar': 'registros', 'google_map_id': google_map_id, 'latitude': latitude, 'longitude': longitude })

def registros_apagar(request, ident):
    registro = Registro.objects.get(ident=ident)
    registro.delete()
    return registros(request)

def analise_mapa(request):
    forty_days = timezone.now() - timedelta(days = 40)
    registros = serializers.serialize("json", Registro.objects.filter(datahora__gte=forty_days), fields=["latitude", "longitude"])
    return render(request, 'analise/mapa.html', {"registros": registros, 'google_map_id': google_map_id})

def cabecalho_rodape(canvas, doc):
    canvas.saveState()
    logo = Image('static/imagens/favicon.png', 1.3*cm, 1.3*cm)
    titulo_s = ParagraphStyle(name='titulo', alignment=TA_LEFT, fontSize=16, leading=18)
    titulo = Paragraph('<b>Combate ao mosquito</b><br/><i>Aedes aegypti</i>', titulo_s)
    data_f = formats.date_format(datetime.now(), "DATETIME_FORMAT")
    data_s = ParagraphStyle(name='data', alignment=TA_RIGHT, fontSize=12, leading=16)
    data = Paragraph(f"Relatório gerado em:<br/>{data_f}", data_s)
    cabecalho = Table([(logo, titulo, data)], colWidths=[1.5*cm, 8*cm, 9.5*cm], rowHeights=[1.5*cm])
    cabecalho.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('BOX', (0,0), (-1,-1), 0.1, colors.white)
    ]))
    cabecalho.wrapOn(canvas, A4[0], 1.5*cm)
    cabecalho.drawOn(canvas, 1*cm, A4[1]-2.5*cm)
    rodape = Table([('UNIVESP', 'Projeto Integrador em Computação II', "Página %d" % doc.page)], colWidths=[6*cm, 7*cm, 6*cm], rowHeights=[1*cm])
    rodape.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('BOX', (0,0), (-1,-1), 0.1, colors.white)
    ]))
    rodape.wrapOn(canvas, A4[0], 1*cm)
    rodape.drawOn(canvas, 1 *cm, 1*cm)
    canvas.restoreState()

def analise_relatorio(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1*cm,
                            leftMargin=1*cm, topMargin=3*cm, bottomMargin=2*cm)
    forty_days = timezone.now() - timedelta(days = 40)
    registros = Registro.objects.filter(datahora__gte=forty_days)
    corpo = []
    dados = []
    for registro in registros:
        dados.append([Paragraph(f"{registro.cidade}, {registro.estado}"), Paragraph(registro.bairro), Paragraph(f"{registro.endereco}, {registro.numero}")])
    tabela = Table(dados, colWidths=[6*cm, 5*cm, 8*cm])
    tabela.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.grey),
        ('BOX',(0,0),(-1,-1),0.25,colors.grey),
    ]))
    corpo.append(tabela)
    doc.build(corpo, onFirstPage=cabecalho_rodape, onLaterPages=cabecalho_rodape)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="combate-aedes.pdf")