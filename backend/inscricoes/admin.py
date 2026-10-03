from django.contrib import admin
from .models import Evento, Inscricao


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
	list_display = (
		'nome',
		'data_evento',
		'data_fim_evento',
		'quantidade_acampantes_maxima',
		'quantidade_servos_maxima',
		'valor_acampante',
		'valor_servo',
		'ativo',
	)
	list_filter = ('ativo',)
	search_fields = ('nome',)


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
	list_display = (
		'nome_completo',
		'evento',
		'tipo',
		'telefone',
		'criado_em',
	)
	list_filter = ('evento', 'tipo')
	search_fields = ('nome_completo', 'telefone', 'email')