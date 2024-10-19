from django import forms
from django.core.validators import RegexValidator, MaxLengthValidator

# Crie seus formulários aqui.

class ValidarCep(forms.Form):
    cep = forms.CharField(initial='', widget=forms.TextInput(attrs={'class':'form-control fs-2 mt-3','inputmode':'numeric'}), label='Por favor, informe o CEP do local do foco suspeito no formato 12345678.', validators=[RegexValidator('^([0-9]{8})$', message='CEP inválido, use somente números.')])

class ValidarNumero(forms.Form):
    numero = forms.CharField(initial='', widget=forms.TextInput(attrs={'class':'form-control fs-2 mt-3','inputmode':'numeric'}), label='Forneça o número do endereço do local do foco suspeito.', validators=[RegexValidator('^[0-9]{0,6}$', message='Número inválido, use somente números.')])

class ValidarTelefone(forms.Form):
    telefone = forms.CharField(initial='', widget=forms.TextInput(attrs={'class':'form-control fs-2 mt-3','inputmode':'numeric'}), label='Informe seu número de telefone com DDD no formato 12987654321. Ele será solicitado se você optar por apagar esses dados.', validators=[RegexValidator('^([0-9]{11})$', message='Telefone inválido, use somente números.')])

class ValidarDescricao(forms.Form):
    descricao = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control fs-4 mt-3','rows': '3', 'maxlength': '128'}), label='(Opcional) Se possível, forneça uma descrição do local suspeito, como água parada em latas, garrafas vazias, pneus, lixo, entre outros.', validators=[MaxLengthValidator(128, message='Comprimento máximo permitido de 128 caracteres.')], required=False)

class ValidarPolitica(forms.Form):
    termos = forms.BooleanField(initial=False, label='Concordo com a política.', widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), required=True)