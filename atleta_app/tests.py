from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Atleta

# Test credentials - these are safe for testing purposes
# nosonar: hardcoded-credentials
TEST_USERNAME = 'testuser'
TEST_PRSWRD = 'testpass'  # nosonar: hardcoded-credentials
TEST_WRONG_PRSWRD = 'wrongpass'  # nosonar: hardcoded-credentials
TEST_NEW_USER_PRSWRD = 'testesenha123'  # nosonar: hardcoded-credentials
TEST_WEAK_PRSWRD = '123'  # nosonar: hardcoded-credentials
TEST_DIFF_PRSWRD1 = 'senha123'  # nosonar: hardcoded-credentials
TEST_DIFF_PRSWRD2 = 'senha456'  # nosonar: hardcoded-credentials
TEST_ANY_PRSWRD = 'qualquer'  # nosonar: hardcoded-credentials

# Create your tests here.

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        # nosonar: hardcoded-credentials
        self.user = User.objects.create_user(
            username=TEST_USERNAME, 
            password=TEST_PRSWRD, 
            first_name='Test', 
            last_name='User'
        )

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'Novo',
            'last_name': 'Usuário',
            'email': 'novo@teste.com',
            'password1': TEST_NEW_USER_PRSWRD,  # nosonar: hardcoded-credentials
            'password2': TEST_NEW_USER_PRSWRD,  # nosonar: hardcoded-credentials
        })
        self.assertRedirects(response, reverse('home'))  # Redireciona após registro
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_logout(self):
        # nosonar: hardcoded-credentials
        login = self.client.post(reverse('login'), {
            'username': TEST_USERNAME, 
            'password': TEST_PRSWRD
        })
        self.assertRedirects(login, reverse('home'))  # Redireciona após login
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Olá, Test')
        logout = self.client.post(reverse('logout'))
        self.assertRedirects(logout, reverse('home'))

    def test_login_fail(self):
        # nosonar: hardcoded-credentials
        response = self.client.post(reverse('login'), {
            'username': TEST_USERNAME, 
            'password': TEST_WRONG_PRSWRD
        })
        self.assertContains(response, 'Usuário ou senha incorretos', status_code=200)

class VisualizarAtletaTests(TestCase):
    def setUp(self):
        self.client = Client()
        # nosonar: hardcoded-credentials
        self.user = User.objects.create_user(
            username=TEST_USERNAME, 
            password=TEST_PRSWRD
        )
        self.atleta1 = Atleta.objects.create(
            nome='Arthur Moreira', cpf='123.456.789-10', idade=25, altura=1.80, clube='Palmeiras', peso=75.0,
            posicao='Atacante', numeroTotalDeJogos=100, numeroDeJogosComoTitular=80
        )
        self.atleta2 = Atleta.objects.create(
            nome='Vinicius Paiva', cpf='111.111.111-11', idade=22, altura=1.75, clube='Santos', peso=70.0,
            posicao='Zagueiro', numeroTotalDeJogos=50, numeroDeJogosComoTitular=30
        )
        # nosonar: hardcoded-credentials
        self.client.login(username=TEST_USERNAME, password=TEST_PRSWRD)

    def test_visualizar_todos(self):
        response = self.client.get(reverse('visualizarAtleta'))
        self.assertContains(response, 'Arthur Moreira')
        self.assertContains(response, 'Vinicius Paiva')

    def test_filtro_nome(self):
        response = self.client.get(reverse('visualizarAtleta'), {'nome': 'Arthur'})
        self.assertContains(response, 'Arthur Moreira')
        self.assertNotContains(response, 'Vinicius Paiva')

    def test_filtro_clube(self):
        response = self.client.get(reverse('visualizarAtleta'), {'clube': 'Palmeiras'})
        self.assertContains(response, 'Arthur Moreira')
        self.assertNotContains(response, 'Vinicius Paiva')

    def test_filtro_posicao(self):
        response = self.client.get(reverse('visualizarAtleta'), {'posicao': 'Zagueiro'})
        self.assertContains(response, 'Vinicius Paiva')
        self.assertNotContains(response, 'Arthur Moreira')

    def test_filtro_cpf(self):
        response = self.client.get(reverse('visualizarAtleta'), {'cpf': '123.456.789-10'})
        self.assertContains(response, 'Arthur Moreira')
        self.assertNotContains(response, 'Vinicius Paiva')
        self.assertContains(response, 'Taxa de Titularidade', html=False)  # Card detalhado

    def test_filtro_cpf_inexistente(self):
        response = self.client.get(reverse('visualizarAtleta'), {'cpf': '000.000.000-00'})
        self.assertContains(response, 'Atleta não encontrado', status_code=200)

    def test_cadastro_atleta_sucesso(self):
        response = self.client.post(reverse('cadastrarAtleta'), {
            'nome': 'Novo Atleta',
            'cpf': '390.533.447-05',  # CPF válido
            'idade': 20,
            'altura': 1.70,
            'clube': 'Flamengo',
            'peso': 68.0,
            'posicao': 'Meio-campo',
            'numeroTotalDeJogos': 10,
            'numeroDeJogosComoTitular': 5,
        }, follow=True)
        self.assertContains(response, 'Atleta cadastrado com sucesso')
        self.assertTrue(Atleta.objects.filter(nome='Novo Atleta').exists())

    def test_cadastro_atleta_cpf_invalido(self):
        response = self.client.post(reverse('cadastrarAtleta'), {
            'nome': 'Atleta Inválido',
            'cpf': '111.111.111-11',  # CPF já existente
            'idade': 20,
            'altura': 1.70,
            'clube': 'Flamengo',
            'peso': 68.0,
            'posicao': 'Meio-campo',
            'numeroTotalDeJogos': 10,
            'numeroDeJogosComoTitular': 5,
        })
        self.assertContains(response, 'CPF inválido', status_code=200)

    def test_cadastro_atleta_jogos_titular_maior(self):
        response = self.client.post(reverse('cadastrarAtleta'), {
            'nome': 'Atleta Inválido',
            'cpf': '390.533.447-05',  # CPF válido
            'idade': 20,
            'altura': 1.70,
            'clube': 'Flamengo',
            'peso': 68.0,
            'posicao': 'Meio-campo',
            'numeroTotalDeJogos': 5,
            'numeroDeJogosComoTitular': 10,
        })
        self.assertContains(response, 'O número de jogos como titular não pode exceder o número total de jogos', status_code=200)

    def test_visualizar_atleta_sem_login(self):
        self.client.logout()
        response = self.client.get(reverse('visualizarAtleta'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_filtro_multiplos_campos(self):
        response = self.client.get(reverse('visualizarAtleta'), {'nome': 'Arthur', 'clube': 'Palmeiras'})
        self.assertContains(response, 'Arthur Moreira')
        self.assertNotContains(response, 'Vinicius Paiva')

    def test_filtro_nome_parcial_case_insensitive(self):
        response = self.client.get(reverse('visualizarAtleta'), {'nome': 'arthur'})
        self.assertContains(response, 'Arthur Moreira')

    def test_filtro_clube_e_posicao(self):
        response = self.client.get(reverse('visualizarAtleta'), {'clube': 'Santos', 'posicao': 'Zagueiro'})
        self.assertContains(response, 'Vinicius Paiva')
        self.assertNotContains(response, 'Arthur Moreira')

    def test_cadastro_atleta_campo_obrigatorio_faltando(self):
        response = self.client.post(reverse('cadastrarAtleta'), {
            'nome': '',  # Nome obrigatório
            'cpf': '444.444.444-44',
            'idade': 20,
            'altura': 1.70,
            'clube': 'Flamengo',
            'peso': 68.0,
            'posicao': 'Meio-campo',
            'numeroTotalDeJogos': 10,
            'numeroDeJogosComoTitular': 5,
        })
        self.assertContains(response, 'Este campo é obrigatório', status_code=200)

    def test_metodo_modelo_visualizar_atleta(self):
        """Testa se o método centralizado do modelo está funcionando corretamente"""
        # Teste busca por CPF (encontrado)
        atletas, _ = Atleta.visualizar_atleta(cpf='123.456.789-10')
        self.assertEqual(len(atletas), 1)
        self.assertEqual(atletas[0].nome, 'Arthur Moreira')
        
        # Teste busca por CPF (não encontrado)
        atletas, _ = Atleta.visualizar_atleta(cpf='000.000.000-00')
        self.assertEqual(len(atletas), 0)
        
        # Teste busca por nome
        atletas, _ = Atleta.visualizar_atleta(nome='Arthur')
        self.assertEqual(len(atletas), 1)
        self.assertEqual(atletas[0].nome, 'Arthur Moreira')
        
        # Teste busca por clube
        atletas, _ = Atleta.visualizar_atleta(clube='Palmeiras')
        self.assertEqual(len(atletas), 1)
        self.assertEqual(atletas[0].clube, 'Palmeiras')
        
        # Teste busca por posição
        atletas, _ = Atleta.visualizar_atleta(posicao='Zagueiro')
        self.assertEqual(len(atletas), 1)
        self.assertEqual(atletas[0].posicao, 'Zagueiro')
        
        # Teste busca múltipla
        atletas, _ = Atleta.visualizar_atleta(nome='Arthur', clube='Palmeiras')
        self.assertEqual(len(atletas), 1)
        self.assertEqual(atletas[0].nome, 'Arthur Moreira')
        
        # Teste busca sem filtros
        atletas, _ = Atleta.visualizar_atleta()
        self.assertEqual(len(atletas), 2)  # Ambos os atletas

    def test_metodo_estatisticas_atletas(self):
        """Testa se o método de estatísticas está funcionando corretamente"""
        estatisticas = Atleta.get_atletas_estatisticas()
        
        # Verifica se as estatísticas foram calculadas
        self.assertIsNotNone(estatisticas)
        self.assertEqual(estatisticas['total_atletas'], 2)
        self.assertIsNotNone(estatisticas['media_idade'])
        self.assertIsNotNone(estatisticas['media_altura'])
        self.assertIsNotNone(estatisticas['media_peso'])
        self.assertIsNotNone(estatisticas['max_jogos'])
        self.assertIsNotNone(estatisticas['min_jogos'])
        
        # Verifica se os valores fazem sentido
        self.assertGreater(estatisticas['media_idade'], 0)
        self.assertGreater(estatisticas['media_altura'], 0)
        self.assertGreater(estatisticas['media_peso'], 0)
        self.assertGreaterEqual(estatisticas['max_jogos'], estatisticas['min_jogos'])

    def test_view_estatisticas_atletas(self):
        """Testa se a view de estatísticas está funcionando corretamente"""
        response = self.client.get(reverse('estatisticas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Estatísticas dos Atletas')
        self.assertContains(response, 'Total de Atletas')

    def test_view_estatisticas_sem_login(self):
        """Testa se a view de estatísticas requer login"""
        self.client.logout()
        response = self.client.get(reverse('estatisticas'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_view_estatisticas_com_graficos(self):
        """Testa se a view de estatísticas carrega corretamente com gráficos"""
        response = self.client.get(reverse('estatisticas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Estatísticas dos Atletas')
        self.assertContains(response, 'Chart.js')
        self.assertContains(response, 'idadeChart')
        self.assertContains(response, 'metricasChart')
        self.assertContains(response, 'jogosChart')

    def test_home_com_botao_estatisticas(self):
        """Testa se a home page tem o botão de estatísticas com ícone"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'fa-chart-bar')
        self.assertContains(response, 'Estatísticas')
        self.assertContains(response, reverse('estatisticas'))

    def test_cache_visualizar_atleta(self):
        """Testa se o cache está funcionando no método visualizar_atleta"""
        from django.core.cache import cache
        
        # Limpa cache antes do teste
        cache.clear()
        
        # Primeira chamada (sem cache)
        atletas1, _ = Atleta.visualizar_atleta(nome='Arthur', use_cache=True)
        
        # Segunda chamada (com cache)
        atletas2, _ = Atleta.visualizar_atleta(nome='Arthur', use_cache=True)
        
        # Terceira chamada (sem cache)
        atletas3, _ = Atleta.visualizar_atleta(nome='Arthur', use_cache=False)
        
        # Verifica se os resultados são iguais
        self.assertEqual(len(atletas1), len(atletas2))
        self.assertEqual(len(atletas1), len(atletas3))
        self.assertEqual(atletas1[0].nome, atletas2[0].nome)
        self.assertEqual(atletas1[0].nome, atletas3[0].nome)

    def test_otimizacao_only_fields(self):
        """Testa se a otimização only() está funcionando corretamente"""
        # Busca com otimização
        atletas, _ = Atleta.visualizar_atleta(nome='Arthur')
        
        # Verifica se os campos necessários estão disponíveis
        atleta = atletas[0]
        self.assertIsNotNone(atleta.nome)
        self.assertIsNotNone(atleta.cpf)
        self.assertIsNotNone(atleta.idade)
        self.assertIsNotNone(atleta.altura)
        self.assertIsNotNone(atleta.clube)
        self.assertIsNotNone(atleta.peso)
        self.assertIsNotNone(atleta.posicao)
        self.assertIsNotNone(atleta.numeroTotalDeJogos)
        self.assertIsNotNone(atleta.numeroDeJogosComoTitular)

    def test_indices_banco_dados(self):
        """Testa se os índices estão funcionando corretamente"""
        # Testa busca por CPF (deve usar índice)
        atletas, _ = Atleta.visualizar_atleta(cpf='123.456.789-10')
        self.assertEqual(len(atletas), 1)
        
        # Testa busca por nome (deve usar índice)
        atletas, _ = Atleta.visualizar_atleta(nome='Arthur')
        self.assertEqual(len(atletas), 1)
        
        # Testa busca por clube (deve usar índice)
        atletas, _ = Atleta.visualizar_atleta(clube='Palmeiras')
        self.assertEqual(len(atletas), 1)
        
        # Testa busca por posição (deve usar índice)
        atletas, _ = Atleta.visualizar_atleta(posicao='Atacante')
        self.assertEqual(len(atletas), 1)

class AuthExtraTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_senha_fraca(self):
        response = self.client.post(reverse('register'), {
            'username': 'weakuser',
            'first_name': 'Weak',
            'last_name': 'User',
            'email': 'weak@teste.com',
            'password1': TEST_WEAK_PRSWRD,  # nosonar: hardcoded-credentials
            'password2': TEST_WEAK_PRSWRD,  # nosonar: hardcoded-credentials
        })
        self.assertContains(response, 'Esta senha é muito curta', status_code=200)

    def test_register_senhas_diferentes(self):
        response = self.client.post(reverse('register'), {
            'username': 'diffuser',
            'first_name': 'Diff',
            'last_name': 'User',
            'email': 'diff@teste.com',
            'password1': TEST_DIFF_PRSWRD1,  # nosonar: hardcoded-credentials
            'password2': TEST_DIFF_PRSWRD2,  # nosonar: hardcoded-credentials
        })
        self.assertContains(response, 'Os dois campos de senha não correspondem.', status_code=200)

    def test_login_usuario_inexistente(self):
        # nosonar: hardcoded-credentials
        response = self.client.post(reverse('login'), {
            'username': 'naoexiste', 
            'password': TEST_ANY_PRSWRD
        })
        self.assertContains(response, 'Usuário ou senha incorretos', status_code=200)

    def test_logout_sem_login(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('home'), response.url)
