from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Evento, Inscricao


class CriarInscricaoTests(TestCase):

	def setUp(self):
		self.evento = Evento.objects.create(
			nome='Acampamento de teste',
			data_evento=timezone.now() + timedelta(days=1),
			quantidade_participantes_maxima=10,
			quantidade_acampantes_maxima=1,
			quantidade_servos_maxima=1,
			ativo=True,
		)
		self.client = APIClient()
		self.payload = {
			'tipo': 'primeira_vez',
			'nome_completo': 'Pessoa de Teste',
			'data_nascimento': '2000-01-01',
			'telefone': '81999999999',
			'cidade': 'Recife',
			'estado': 'PE',
			'tamanho_camisa': 'M',
		}

	def test_recusa_inscricao_depois_do_inicio(self):
		self.evento.data_evento = timezone.now() - timedelta(minutes=1)
		self.evento.save()

		response = self.client.post(
			reverse('criar-inscricao'),
			self.payload,
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(Inscricao.objects.count(), 0)

	def test_recusa_categoria_sem_vagas(self):
		Inscricao.objects.create(
			evento=self.evento,
			tipo='primeira_vez',
			nome_completo='Acampante existente',
			data_nascimento=date(2000, 1, 1),
			telefone='81999999998',
			cidade='Recife',
			estado='PE',
			tamanho_camisa='M',
		)

		response = self.client.post(
			reverse('criar-inscricao'),
			self.payload,
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(Inscricao.objects.count(), 1)

	def test_limite_de_acampantes_nao_bloqueia_servos(self):
		Inscricao.objects.create(
			evento=self.evento,
			tipo='primeira_vez',
			nome_completo='Acampante existente',
			data_nascimento=date(2000, 1, 1),
			telefone='81999999998',
			cidade='Recife',
			estado='PE',
			tamanho_camisa='M',
		)
		payload_servo = {**self.payload, 'tipo': 'servo'}

		response = self.client.post(
			reverse('criar-inscricao'),
			payload_servo,
			format='json',
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(Inscricao.objects.filter(tipo='servo').count(), 1)

	def test_evento_atual_retorna_data_iso_do_evento(self):
		response = self.client.get(reverse('evento-atual'))

		self.assertEqual(response.status_code, 200)
		data_evento = datetime.fromisoformat(
			response.json()['data_evento'].replace('Z', '+00:00')
		)
		self.assertEqual(data_evento, self.evento.data_evento)

	def test_recusa_servo_quando_limite_de_servos_foi_atingido(self):
		Inscricao.objects.create(
			evento=self.evento,
			tipo='servo',
			nome_completo='Servo existente',
			data_nascimento=date(2000, 1, 1),
			telefone='81999999998',
			cidade='Recife',
			estado='PE',
			tamanho_camisa='M',
		)

		response = self.client.post(
			reverse('criar-inscricao'),
			{**self.payload, 'tipo': 'servo'},
			format='json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(Inscricao.objects.filter(tipo='servo').count(), 1)


class GestaoEventosTests(TestCase):

	def setUp(self):
		self.inicio = timezone.now() + timedelta(days=10)
		self.evento_ativo = Evento.objects.create(
			nome='Evento atual',
			data_evento=self.inicio,
			data_fim_evento=self.inicio + timedelta(days=2),
			quantidade_participantes_maxima=10,
			quantidade_acampantes_maxima=7,
			quantidade_servos_maxima=3,
			ativo=True,
		)
		User = get_user_model()
		self.admin = User.objects.create_user(
			username='admin',
			email='admin@example.com',
			password='senha-segura',
			nome='Admin',
			is_staff=True,
		)
		self.client.force_login(self.admin)

	def criar_inscricao(self, evento, nome):
		return Inscricao.objects.create(
			evento=evento,
			tipo='primeira_vez',
			nome_completo=nome,
			data_nascimento=date(2000, 1, 1),
			telefone='81999999999',
			cidade='Recife',
			estado='PE',
			tamanho_camisa='M',
		)

	def test_salvar_evento_ativo_desativa_o_anterior(self):
		novo_evento = Evento.objects.create(
			nome='Próximo evento',
			data_evento=self.inicio + timedelta(days=30),
			data_fim_evento=self.inicio + timedelta(days=32),
			quantidade_participantes_maxima=5,
			ativo=True,
		)

		self.evento_ativo.refresh_from_db()
		self.assertFalse(self.evento_ativo.ativo)
		self.assertTrue(novo_evento.ativo)
		self.assertEqual(Evento.objects.filter(ativo=True).count(), 1)

	def test_painel_inicial_lista_somente_inscritos_no_evento_ativo(self):
		evento_historico = Evento.objects.create(
			nome='Evento anterior',
			data_evento=self.inicio - timedelta(days=30),
			ativo=False,
			quantidade_participantes_maxima=5,
		)
		inscricao_atual = self.criar_inscricao(self.evento_ativo, 'Pessoa atual')
		self.criar_inscricao(evento_historico, 'Pessoa anterior')

		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Pessoa atual')
		self.assertNotContains(response, 'Pessoa anterior')
		self.assertEqual(list(response.context['inscricoes']), [inscricao_atual])

	def test_area_eventos_exibe_historico_e_inscritos(self):
		evento_historico = Evento.objects.create(
			nome='Evento anterior',
			data_evento=self.inicio - timedelta(days=30),
			ativo=False,
			quantidade_participantes_maxima=5,
		)
		self.criar_inscricao(evento_historico, 'Pessoa anterior')

		lista = self.client.get(reverse('listar_eventos'))
		detalhe = self.client.get(
			reverse('detalhe_evento', args=[evento_historico.id])
		)

		self.assertContains(lista, 'Evento atual')
		self.assertContains(lista, 'Evento anterior')
		self.assertContains(detalhe, 'Pessoa anterior')

	def test_criar_evento_pelo_formulario_ativa_e_calcula_limite_total(self):
		inicio = timezone.localtime(timezone.now() + timedelta(days=40))
		fim = inicio + timedelta(days=2)
		response = self.client.post(
			reverse('listar_eventos'),
			{
				'nome': 'Novo acampamento',
				'data_evento': inicio.strftime('%Y-%m-%dT%H:%M'),
				'data_fim_evento': fim.strftime('%Y-%m-%dT%H:%M'),
				'quantidade_acampantes_maxima': 20,
				'quantidade_servos_maxima': 8,
				'valor_acampante': '175.50',
				'valor_servo': '90.00',
			},
		)

		self.assertEqual(response.status_code, 302)
		novo_evento = Evento.objects.get(nome='Novo acampamento')
		self.assertTrue(novo_evento.ativo)
		self.assertEqual(novo_evento.quantidade_participantes_maxima, 28)
		self.assertEqual(novo_evento.valor_acampante, 175.50)
		self.assertEqual(novo_evento.valor_servo, 90.00)
		self.evento_ativo.refresh_from_db()
		self.assertFalse(self.evento_ativo.ativo)

	def test_formulario_recusa_fim_anterior_ao_inicio(self):
		inicio = timezone.localtime(timezone.now() + timedelta(days=40))
		response = self.client.post(
			reverse('listar_eventos'),
			{
				'nome': 'Evento inválido',
				'data_evento': inicio.strftime('%Y-%m-%dT%H:%M'),
				'data_fim_evento': (inicio - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
				'quantidade_acampantes_maxima': 20,
				'quantidade_servos_maxima': 8,
				'valor_acampante': '175.50',
				'valor_servo': '90.00',
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertFalse(Evento.objects.filter(nome='Evento inválido').exists())
