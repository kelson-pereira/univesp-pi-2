from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Registro
from .forms import *
import brazilcep
import googlemaps

google_api_key = settings.GOOGLE_API_KEY
google_map_id = settings.GOOGLE_MAP_ID

# Crie suas visualizações aqui.

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
def obtem_coordenadas(logradouro, numero, cidade, estado):
    gmaps = googlemaps.Client(key=google_api_key)
    try:
        geocode_result = gmaps.geocode(f"{logradouro}, {numero}, {cidade}, {estado}, Brasil")
        return True, geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']
    except:
        return False, "", ""


# Valida o CEP
def validar_cep(request):
    # GET e estado inicial
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        # entregar o formulário vazio
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
            # validado
            cep = form.cleaned_data['cep']
            cep_encontrado, logradouro, bairro, cidade, estado = obtem_endereco(cep)
            endereco = f"{logradouro}, {bairro} - {cidade}/{estado}"
            if not cep_encontrado:
                return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o CEP:', 'icone': 'house-fill', 'mensagem_erro': 'CEP não encontrado.' })
            form = ValidarNumero()
            request.path = 'validar_numero'
            form.initial.setdefault('numero', request.COOKIES.get('numero'))
            response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'validar_cep', 'icone': 'signpost-fill', 'endereco': endereco })
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
def validar_numero(request):
    logradouro = request.COOKIES.get('logradouro')
    bairro = request.COOKIES.get('bairro')
    cidade = request.COOKIES.get('cidade')
    estado = request.COOKIES.get('estado')
    endereco = f"{logradouro}, {bairro} - {cidade}/{estado}"
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarNumero()
        form.initial.setdefault('numero', request.COOKIES.get('numero'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'validar_cep', 'icone': 'signpost-fill', 'endereco': endereco })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarNumero(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero']
            coord_encontradas, latitude, longitude = obtem_coordenadas(logradouro, numero, cidade, estado)
            if not coord_encontradas:
                return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o numero:', 'voltar': 'validar_cep', 'icone': 'signpost-fill', 'mensagem_erro': 'Coordenadas não encontradas.' })
            request.path = 'validar_telefone'
            response = render(request, 'localizacao.html', {'voltar': 'validar_numero', 'google_api_key': google_api_key, 'google_map_id': google_map_id, 'latitude': str(latitude), 'longitude': str(longitude)})
            response.set_cookie('numero', numero)
            response.set_cookie('latitude', latitude)
            response.set_cookie('longitude', longitude)
            response.set_cookie('form', 'inicial')
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'validar_cep', 'icone': 'signpost-fill', 'endereco': endereco })

# Valida o Telefone NOVA
def validar_telefone(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarTelefone()
        form.initial.setdefault('telefone', request.COOKIES.get('telefone'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'voltar': 'validar_numero', 'icone': 'telephone-fill' })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarTelefone(request.POST)
        if form.is_valid():
            telefone = form.cleaned_data['telefone']
            form = ValidarDescricao()
            request.path = 'validar_descricao'
            form.initial.setdefault('descricao', request.COOKIES.get('descricao'))
            response = render(request, 'modal.html', {'form': form, 'titulo': 'Descreva o local:', 'voltar': 'validar_telefone', 'icone': 'clipboard-plus-fill' })
            response.set_cookie('telefone', telefone)
            response.set_cookie('form', 'validar')
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'voltar': 'validar_numero', 'icone': 'telephone-fill' })

# Valida a Descrição NOVA
def validar_descricao(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarDescricao()
        form.initial.setdefault('descricao', request.COOKIES.get('descricao'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Descreva o local:', 'voltar': 'validar_telefone', 'icone': 'clipboard-plus-fill' })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarDescricao(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data['descricao']
            form = ValidarPolitica()
            request.path = 'validar_politica'
            response = render(request, 'politica.html', {'form': form, 'titulo': 'Privacidade:', 'voltar': 'validar_descricao', 'icone': 'shield-fill-check' })
            response.set_cookie('descricao', descricao)
            response.set_cookie('form', 'validar')
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Descreva o local:', 'voltar': 'validar_telefone', 'icone': 'clipboard-plus-fill' })

# Valida a Política e cria o registro no banco de dados
def validar_politica(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarPolitica()
        form.initial.setdefault('termos', request.COOKIES.get('termos'))
        response = render(request, 'politica.html', {'form': form, 'titulo': 'Privacidade:', 'voltar': 'validar_descricao', 'icone': 'shield-fill-check' })
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
                response = render(request, 'registro.html', {"mensagem": "Registro salvo com sucesso!"})
                response.delete_cookie('cep')
                response.delete_cookie('logradouro')
                response.delete_cookie('numero')
                response.delete_cookie('bairro')
                response.delete_cookie('cidade')
                response.delete_cookie('estado')
                response.delete_cookie('telefone')
                response.delete_cookie('descricao')
                response.delete_cookie('endereco')
                response.delete_cookie('latitude')
                response.delete_cookie('longitude')
                response.delete_cookie('form')
                return response
            except:
                return render(request, 'registro.html', {"mensagem": "Erro ao salvar o registro"})
        else:
            return render(request, 'politica.html', {'form': form, 'titulo': 'Privacidade:', 'voltar': 'validar_descricao', 'icone': 'shield-fill-check' })

# Adiciona uma foto
def adicionar_foto(request):
    if request.method == "POST":
        request.path = "aceitar_politica"
        return validar_politica(request)
    return render(request, 'foto.html', {'titulo': 'Adicionar uma foto:', 'voltar': 'validar_descricao', 'icone': 'camera-fill' })

# Valida a localização
def validar_localizacao(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        latitude = request.COOKIES.get('latitude')
        longitude = request.COOKIES.get('longitude')
        return render(request, 'localizacao.html', {'voltar': 'validar_numero', 'google_api_key': google_api_key, 'google_map_id': google_map_id, 'latitude': latitude, 'longitude': longitude})
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        request.path = 'validar_telefone'
        form = ValidarTelefone()
        form.initial.setdefault('telefone', request.COOKIES.get('telefone'))
        return render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'voltar': 'validar_numero', 'icone': 'telephone-fill' })

def meus_registros(request):
    forty_days = timezone.now() - timedelta(days = 40)
    registros = {'registros': Registro.objects.filter(datahora__gte=forty_days).values('ident', 'datahora', 'endereco', 'numero', 'descricao')}
    return render(request, 'meus_registros.html', registros)
