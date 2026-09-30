from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import date, datetime, timedelta
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
