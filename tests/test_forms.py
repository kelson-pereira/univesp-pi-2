from django.test import TestCase
from combate_aedes.forms import *

# Crie seus testes aqui.
class FromsTestCase(TestCase):

    def test_cep_valido(self):
        form_data = {'cep': '12345678'}
        form = ValidarCep(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cep_muito_curto(self):
        form_data = {'cep': '123'}
        form = ValidarCep(data=form_data)
        self.assertFalse(form.is_valid())

    def test_cep_muito_longo(self):
        form_data = {'cep': '123456789'}
        form = ValidarCep(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_cep_com_letra(self):
        form_data = {'cep': 'abc'}
        form = ValidarCep(data=form_data)
        self.assertFalse(form.is_valid())

    def test_cep_vazio(self):
        form_data = {'cep': ''}
        form = ValidarCep(data=form_data)
        self.assertFalse(form.is_valid())

    def test_numero_valido_1(self):
        form_data = {'numero': '1'}
        form = ValidarNumero(data=form_data)
        self.assertTrue(form.is_valid())

    def test_numero_valido_2(self):
        form_data = {'numero': '123'}
        form = ValidarNumero(data=form_data)
        self.assertTrue(form.is_valid())

    def test_numero_valido_3(self):
        form_data = {'numero': '123456'}
        form = ValidarNumero(data=form_data)
        self.assertTrue(form.is_valid())

    def test_numero_com_letra(self):
        form_data = {'numero': 'abc'}
        form = ValidarNumero(data=form_data)
        self.assertFalse(form.is_valid())

    def test_numero_muito_longo(self):
        form_data = {'numero': '1234567'}
        form = ValidarNumero(data=form_data)
        self.assertFalse(form.is_valid())

    def test_numero_vazio(self):
        form_data = {'numero': ''}
        form = ValidarNumero(data=form_data)
        self.assertFalse(form.is_valid())

    def test_telefone_valido(self):
        form_data = {'telefone': '12987654321'}
        form = ValidarTelefone(data=form_data)
        self.assertTrue(form.is_valid())

    def test_telefone_muito_curto(self):
        form_data = {'telefone': '1298765'}
        form = ValidarTelefone(data=form_data)
        self.assertFalse(form.is_valid())

    def test_telefone_muito_longo(self):
        form_data = {'telefone': '129876543210'}
        form = ValidarTelefone(data=form_data)
        self.assertFalse(form.is_valid())

    def test_telefone_com_letra(self):
        form_data = {'telefone': 'abc'}
        form = ValidarTelefone(data=form_data)
        self.assertFalse(form.is_valid())

    def test_telefone_vazio(self):
        form_data = {'telefone': ''}
        form = ValidarTelefone(data=form_data)
        self.assertFalse(form.is_valid())

    def test_descricao_vazia(self):
        form_data = {'descricao': ''}
        form = ValidarDescricao(data=form_data)
        self.assertTrue(form.is_valid())

    def test_descricao_com_texto(self):
        form_data = {'descricao': 'abc 123'}
        form = ValidarDescricao(data=form_data)
        self.assertTrue(form.is_valid())

    def test_descricao_com_texto_muito_longo(self):
        form_data = {'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi sagittis arcu turpis, non tincidunt odio suscipit eu class aptent taciti.'}
        form = ValidarDescricao(data=form_data)
        self.assertFalse(form.is_valid())

    def test_politica_valido(self):
        form_data = {'termos': True}
        form = ValidarPolitica(data=form_data)
        self.assertTrue(form.is_valid())

    def test_politica_invalido(self):
        form_data = {'termos': False}
        form = ValidarPolitica(data=form_data)
        self.assertFalse(form.is_valid())