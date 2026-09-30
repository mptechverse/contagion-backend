from django.contrib import admin
from .models import Evento, Inscricao


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
	list_display = (
		'nome',
		'data_evento',
		'quantidade_acampantes_maxima',
		'quantidade_servos_maxima',
		'ativo',
	)
	list_filter = ('ativo',)
	search_fields = ('nome',)


admin.site.register(Inscricao)