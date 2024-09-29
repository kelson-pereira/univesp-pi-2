from django.shortcuts import render
from .models import Registro
from .forms import ValidarCep, ValidarNumero, ValidarTelefone, ValidarDescricao, ValidarPolitica

# Crie suas visualizações aqui.

# Exibe a página principal
def home(request):
    return render(request, 'home.html')

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
            form = ValidarNumero()
            request.path = 'validar_numero'
            form.initial.setdefault('numero', request.COOKIES.get('numero'))
            response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'validar_cep', 'icone': 'signpost-fill' })
            # define o cookie para o cep
            response.set_cookie('cep', cep)
            # define o cookie para inicial
            response.set_cookie('form', 'validar')
            # encaminha para o próximo form
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o CEP:', 'icone': 'house-fill' })

# Valida o Número
def validar_numero(request):
    if request.method == "GET" or request.COOKIES.get('form') == 'inicial':
        form = ValidarNumero()
        form.initial.setdefault('numero', request.COOKIES.get('numero'))
        response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'validar_cep', 'icone': 'signpost-fill' })
        response.set_cookie('form', 'validar')
        return response
    elif request.method == "POST" and request.COOKIES.get('form') == 'validar':
        form = ValidarNumero(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero']
            form = ValidarTelefone()
            request.path = 'validar_telefone'
            form.initial.setdefault('telefone', request.COOKIES.get('telefone'))
            response = render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'voltar': 'validar_numero', 'icone': 'telephone-fill' })
            response.set_cookie('numero', numero)
            response.set_cookie('form', 'validar')
            return response
        else:
            return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'validar_cep', 'icone': 'signpost-fill' })

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
                registro.numero = request.COOKIES.get('numero')
                registro.telefone = request.COOKIES.get('telefone')
                registro.descricao = request.COOKIES.get('descricao')
                registro.termos = form.cleaned_data['termos']
                registro.save()
                # retorna para a tela registrar e limpa os cookies
                response = render(request, 'registrar.html', {"mensagem": "Registro salvo com sucesso!"})
                response.delete_cookie('cep')
                response.delete_cookie('numero')
                response.delete_cookie('telefone')
                response.delete_cookie('descricao')
                response.delete_cookie('form')
                return response
            except:
                return render(request, 'registrar.html', {"mensagem": "Erro ao salvar o registro"})
        else:
            return render(request, 'politica.html', {'form': form, 'titulo': 'Privacidade:', 'voltar': 'validar_descricao', 'icone': 'shield-fill-check' })

# Adiciona uma foto
def adicionar_foto(request):
    if request.method == "POST":
        request.path = "aceitar_politica"
        return validar_politica(request)
    return render(request, 'foto.html', {'titulo': 'Adicionar uma foto:', 'voltar': 'validar_descricao', 'icone': 'camera-fill' })
