from django.test import TestCase
from django.urls import reverse
from combate_aedes.views import *

# Crie seus testes aqui.
class ViewsTestCase(TestCase):
    
    def setUp(self):
        Registro.objects.create(
            cep="12220000",
            endereco="Avenida Presidente Juscelino Kubitschek",
            numero="1600",
            bairro="Vila Industrial",
            cidade="São José dos Campos",
            estado="SP",
            telefone="12987654321",
            descricao="abc 123",
            latitude=-23.1813537,
            longitude=-45.8681826,
            termos=True
        )

    def test_view_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_obtem_endereco_valido_1(self):
        endereco = (True, 'Avenida Presidente Juscelino Kubitschek', 'Vila Industrial', 'São José dos Campos', 'SP')
        results = obtem_endereco('12220000')
        self.assertEqual(results, endereco)

    def test_obtem_endereco_valido_2(self):
        endereco = (True, 'Avenida Brigadeiro Faria Lima, 2170', 'Putim', 'São José dos Campos', 'SP')
        results = obtem_endereco('12227901')
        self.assertEqual(results, endereco)

    def test_obtem_endereco_invalido(self):
        endereco = (False, '', '', '', '')
        results = obtem_endereco('12345678')
        print(results)
        self.assertEqual(results, endereco)

    def test_obtem_coordenadas_valido(self):
        coordenadas = (True, -23.1813537, -45.8681826)
        results = obtem_coordenadas('Avenida Presidente Juscelino Kubitschek', '1600', 'Vila Industrial', 'São José dos Campos', 'SP')
        self.assertEqual(results, coordenadas)

    def test_obtem_coordenadas_invalido(self):
        coordenadas = (False, '', '')
        results = obtem_coordenadas('', '', '', '', '', '')
        self.assertEqual(results, coordenadas)

    def test_registrar_cep(self):
        response = self.client.get('/registrar_cep')
        self.assertEqual(response.status_code, 200)

    def test_registrar_cep_valido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_cep'), {'cep': '12220000'})
        self.assertContains(response, 'Informe o número:')

    def test_registrar_cep_invalido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_cep'), {'cep': '123'})
        self.assertContains(response, 'CEP inválido, use somente números.')

    def test_registrar_cep_nao_encontrado(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_cep'), {'cep': '12345678'})
        self.assertContains(response, 'CEP não encontrado.')

    def test_registrar_numero(self):
        response = self.client.get('/registrar_numero')
        self.assertEqual(response.status_code, 200)

    def test_registrar_numero_valido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_numero'), {'numero': '1600'})
        self.assertEqual(response.status_code, 200)

    def test_registrar_numero_invalido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_numero'), {'numero': 'abc'})
        self.assertContains(response, 'Número inválido, use somente números.')

    def test_registrar_telefone(self):
        response = self.client.get('/registrar_telefone')
        self.assertEqual(response.status_code, 200)

    def test_registrar_telefone_valido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_telefone'), {'telefone': '12987654321'})
        self.assertContains(response, 'Descreva o local:')

    def test_registrar_telefone_invalido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_telefone'), {'telefone': '1298765'})
        self.assertContains(response, 'Telefone inválido, use somente números.')

    def test_registrar_descricao(self):
        response = self.client.get('/registrar_descricao')
        self.assertEqual(response.status_code, 200)

    def test_registrar_descricao_valido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_descricao'), {'descricao': 'abc 123'})
        self.assertContains(response, 'Privacidade:')

    def test_registrar_descricao_vazia_valido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_descricao'), {'descricao': ''})
        self.assertContains(response, 'Privacidade:')

    def test_registrar_descricao_invalido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_descricao'), {'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi sagittis arcu turpis, non tincidunt odio suscipit eu class aptent taciti.'})
        self.assertContains(response, 'Comprimento máximo permitido de 128 caracteres.')

    def test_registrar_politica(self):
        response = self.client.get('/registrar_politica')
        self.assertEqual(response.status_code, 200)

    def test_registrar_politica_valido(self):
        self.client.cookies['form'] = 'validar'
        self.client.cookies['cep'] = '12220000'
        self.client.cookies['logradouro'] = 'Avenida Presidente Juscelino Kubitschek'
        self.client.cookies['numero'] = '1600'
        self.client.cookies['bairro'] = 'Vila Industrial'
        self.client.cookies['cidade'] = 'São José dos Campos'
        self.client.cookies['estado'] = 'SP'
        self.client.cookies['telefone'] = '12987654321'
        self.client.cookies['descricao'] = 'abc 123'
        self.client.cookies['latitude'] = '-23.1813537'
        self.client.cookies['longitude'] = '-45.8681826'
        response = self.client.post(reverse('registrar_politica'), {'termos': True})
        self.assertContains(response, 'Registro salvo com sucesso!')

    def test_registrar_politica_invalido_1(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_politica'), {'termos': True})
        self.assertContains(response, 'Erro ao salvar o registro.')

    def test_registrar_politica_invalido_2(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_politica'), {'termos': False})
        self.assertContains(response, 'Este campo é obrigatório.')

    def test_registrar_foto(self):
        response = self.client.get('/registrar_foto')
        self.assertEqual(response.status_code, 200)

    def test_registrar_foto_valido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_foto'))
        self.assertContains(response, 'Privacidade:')

    def test_registrar_localizacao(self):
        response = self.client.get('/registrar_localizacao')
        self.assertEqual(response.status_code, 200)

    def test_registrar_localizacao_valido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registrar_localizacao'))
        print(response.context)
        self.assertContains(response, 'Informe seu telefone:')

    def test_registros_telefone(self):
        response = self.client.get('/registros_telefone')
        self.assertEqual(response.status_code, 200)

    def test_registros_telefone_valido_1(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registros_telefone'), {'telefone': '12987654320'})
        self.assertContains(response, 'Nenhum registro encontrado.')

    def test_registros_telefone_valido_2(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registros_telefone'), {'telefone': '12987654321'})
        print(response.context)
        self.assertContains(response, 'Avenida Presidente Juscelino Kubitschek')

    def test_registros_telefone_invalido(self):
        self.client.cookies['form'] = 'validar'
        response = self.client.post(reverse('registros_telefone'), {'telefone': '1298765'})
        self.assertContains(response, 'Telefone inválido, use somente números.')

    def test_registros(self):
        response = self.client.get('/registros')
        self.assertEqual(response.status_code, 200)

    def test_registros_visualizar(self):
        response = self.client.get('/registros_visualizar/1')
        self.assertEqual(response.status_code, 200)

    def test_registros_apagar(self):
        response = self.client.get('/registros_apagar/1')
        self.assertEqual(response.status_code, 200)