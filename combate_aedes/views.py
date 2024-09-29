from django.shortcuts import render
from .models import Registro
from .forms import ValidarCep, ValidarNumero, ValidarTelefone, ValidarDescricao, ValidarPolitica

# Crie suas visualizações aqui.

# Exibe página princibal do sistema
def home(request):
    return render(request, 'home.html')

# Verifica estado do form
def estado_form(request):
    if 'form' in request.session:
        if request.session.get('form', 'validado'):
            request.session['form'] = 'inicial'
    else:
        request.session.clear()
        request.session['form'] = 'inicial'
    if request.method == "POST" and request.session.get('form', 'validar'):
        return True
    else:
        return False

# Valida o CEP
def validar_cep(request):
    if estado_form(request):
        form = ValidarCep(request.POST)
        if form.is_valid():
            request.session['form'] = 'validado'
            request.session['cep'] = form.cleaned_data['cep']
            request.path = "validar_numero"
            return validar_numero(request)
    else:
        form = ValidarCep()
        if 'cep' in request.session:
            form.initial.setdefault('cep', request.session['cep'])
        request.session['form'] = 'validar'
    return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o CEP:', 'icone': 'house-fill' })

# Valida o Número
def validar_numero(request):
    if estado_form(request):
        form = ValidarNumero(request.POST)
        if form.is_valid():
            request.session['form'] = 'validado'
            request.session['numero'] = form.cleaned_data['numero']
            request.path = "validar_telefone"
            return validar_telefone(request)
    else:
        form = ValidarNumero()
        if 'numero' in request.session:
            form.initial.setdefault('numero', request.session['numero'])
        request.session['form'] = 'validar'
    return render(request, 'modal.html', {'form': form, 'titulo': 'Informe o número:', 'voltar': 'validar_cep', 'icone': 'signpost-fill' })

# Valida o Telefone
def validar_telefone(request):
    if estado_form(request):
        form = ValidarTelefone(request.POST)
        if form.is_valid():
            request.session['form'] = 'validado'
            request.session['telefone'] = form.cleaned_data['telefone']
            request.path = "validar_descricao"
            return validar_descricao(request)
    else:
        form = ValidarTelefone()
        if 'telefone' in request.session:
            form.initial.setdefault('telefone', request.session['telefone'])
        request.session['form'] = 'validar'
    return render(request, 'modal.html', {'form': form, 'titulo': 'Informe seu telefone:', 'voltar': 'validar_numero', 'icone': 'telephone-fill' })

# Valida a Descrição
def validar_descricao(request):
    if estado_form(request):
        form = ValidarDescricao(request.POST)
        if form.is_valid():
            request.session['form'] = 'validado'
            request.session['descricao'] = form.cleaned_data['descricao']
            request.path = "aceitar_politica"
            return aceitar_politica(request)
    else:
        form = ValidarDescricao()
        if 'descricao' in request.session:
            form.initial.setdefault('descricao', request.session['descricao'])
        request.session['form'] = 'validar'
    return render(request, 'modal.html', {'form': form, 'titulo': 'Descreva o local:', 'voltar': 'validar_telefone', 'icone': 'clipboard-plus-fill' })

# Adicionar foto
def adicionar_foto(request):
    if request.method == "POST":
        request.path = "aceitar_politica"
        return aceitar_politica(request)
    return render(request, 'foto.html', {'titulo': 'Adicionar uma foto:', 'voltar': 'validar_descricao', 'icone': 'camera-fill' })

# Aceitar os termos e salva o registro no banco de dados.
def aceitar_politica(request):
    if estado_form(request):
        form = ValidarPolitica(request.POST)
        if form.is_valid():
            try:
                request.session['form'] = 'validado'
                request.session['termos'] = form.cleaned_data['termos']
                registro = Registro()
                registro.cep = request.session['cep']
                registro.numero = request.session['numero']
                registro.telefone = request.session['telefone']
                registro.descricao = request.session['descricao']
                registro.termos = form.cleaned_data['termos']
                registro.save()
                request.session.clear()
                mensagem = "Registro salvo com sucesso!"
            except:
                mensagem = "Erro ao salvar o registro"
            return render(request, 'registrar.html', {"mensagem": mensagem})
    else:
        form = ValidarPolitica()
        if 'termos' in request.session:
            form.initial.setdefault('termos', request.session['termos'])
        request.session['form'] = 'validar'
    return render(request, 'politica.html', {'form': form, 'titulo': 'Privacidade:', 'voltar': 'validar_descricao', 'icone': 'shield-fill-check' })
