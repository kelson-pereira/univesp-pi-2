from django.test import TestCase
from ..models import Registro

# Crie seus testes aqui.
class RegistroTestCase(TestCase):
    
    def setUp(self):
        Registro.objects.create(
            cep="12345678",
            numero=123,
            telefone="12987654321",
            termos=True
        )

    def test_registro_cep(self):
        registro = Registro.objects.get(ident=1)
        self.assertEqual(registro.cep, "12345678")

    def test_registro_numero(self):
        registro = Registro.objects.get(ident=1)
        self.assertEqual(registro.numero, 123)

    def test_registro_telefone(self):
        registro = Registro.objects.get(ident=1)
        self.assertEqual(registro.telefone, "12987654321")

    def test_registro_termos(self):
        registro = Registro.objects.get(ident=1)
        self.assertEqual(registro.termos, True)