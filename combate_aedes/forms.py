from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator, MaxLengthValidator, FileExtensionValidator
from .models import Registro
from datetime import timedelta

# Crie seus formulários aqui.

class ValidarCep(forms.Form):
    cep = forms.CharField(initial='', widget=forms.TextInput(attrs={'class':'form-control fs-2 mt-3','inputmode':'numeric'}), label='Por favor, informe o CEP do local do foco suspeito no formato 12345678.', validators=[RegexValidator('^([0-9]{8})$', message='CEP inválido, use somente números.')])

class ValidarNumero(forms.Form):
    numero = forms.CharField(initial='', widget=forms.TextInput(attrs={'class':'form-control fs-2 mt-3','inputmode':'numeric'}), label='Forneça o número do endereço do local do foco suspeito.', validators=[RegexValidator('^[0-9]{0,6}$', message='Número inválido, use somente números.')])

class ValidarTelefone(forms.Form):
    telefone = forms.CharField(initial='', widget=forms.TextInput(attrs={'class':'form-control fs-2 mt-3','inputmode':'numeric'}), label='Informe seu número de telefone com DDD no formato 12987654321. Ele será solicitado se você optar por visualizar ou apagar esses dados.', validators=[RegexValidator('^([0-9]{11})$', message='Telefone inválido, use somente números.')])

class ValidarFoto(forms.Form):
    imagem = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control mt-3','id':'file-input','data-btnText':'Select'}), label='(Opcional) Se possível, adicione uma foto do local suspeito. Isso pode auxiliar significativamente nas ações de combate ao mosquito.', validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','heic'], message='Formato inválido, use .jpg, .jpeg, .png ou .heic')], required=False)

class ValidarDescricao(forms.Form):
    descricao = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control fs-4 mt-3','rows': '3', 'maxlength': '128'}), label='(Opcional) Se possível, forneça uma descrição do local suspeito, como água parada em latas, garrafas vazias, pneus, lixo, entre outros.', validators=[MaxLengthValidator(128, message='Comprimento máximo permitido de 128 caracteres.')], required=False)

class ValidarPolitica(forms.Form):
    termos = forms.BooleanField(initial=False, label='Concordo com a política.', widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), required=True)

class SelecionarEstado(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SelecionarEstado, self).__init__(*args, **kwargs)

        estados = []
        forty_days = timezone.now() - timedelta(days = 40)
        registros = Registro.objects.filter(datahora__gte=forty_days).values('estado').distinct().order_by('estado')
        for registro in registros:
            estados.append((registro['estado'], registro['estado']))
        self.fields['estado'].choices = estados
        
    estado = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-select fs-4 mt-3'}), label='Selecione o estado desejado para obter a análise de dados.')

class SelecionarCidade(forms.Form):
    def __init__(self, *args, **kwargs):
        estado = kwargs.pop('estado')
        super(SelecionarCidade, self).__init__(*args, **kwargs)

        cidades = []
        forty_days = timezone.now() - timedelta(days = 40)
        registros = Registro.objects.filter(datahora__gte=forty_days, estado=estado).values('cidade').distinct().order_by('cidade')
        for registro in registros:
            cidades.append((registro['cidade'], registro['cidade']))
        self.fields['cidade'].choices = cidades

    cidade = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-select fs-4 mt-3'}), label = 'Selecione a cidade desejada para obter a análise de dados.')