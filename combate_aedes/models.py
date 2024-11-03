from django.db import models
from django.core.validators import MinLengthValidator

# Crie seus modelos aqui.

# Modelo de dados do registro
class Registro(models.Model):
    ident = models.AutoField(primary_key=True)
    datahora = models.DateTimeField(auto_now_add=True, editable=False)
    cep = models.TextField(max_length=8, validators=[MinLengthValidator(8)])
    endereco = models.TextField(max_length=128, blank=True, null=True)
    numero = models.TextField(max_length=6)
    bairro = models.TextField(max_length=128, blank=True, null=True)
    cidade = models.TextField(max_length=128, blank=True, null=True)
    estado = models.TextField(max_length=2, blank=True, null=True)
    telefone = models.TextField(max_length=11)
    descricao = models.TextField(max_length=128, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    termos = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='imagens/', blank=True, null=True)