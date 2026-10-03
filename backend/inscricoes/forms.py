from django import forms

from .models import Evento


class EventoForm(forms.ModelForm):

    class Meta:
        model = Evento
        fields = (
            'nome',
            'data_evento',
            'data_fim_evento',
            'quantidade_acampantes_maxima',
            'quantidade_servos_maxima',
            'valor_acampante',
            'valor_servo',
        )
        labels = {
            'nome': 'Nome do evento',
            'data_evento': 'Data e hora de início',
            'data_fim_evento': 'Data e hora de término',
            'quantidade_acampantes_maxima': 'Vagas para acampantes',
            'quantidade_servos_maxima': 'Vagas para servos',
            'valor_acampante': 'Valor para acampante (R$)',
            'valor_servo': 'Valor para servo (R$)',
        }
        widgets = {
            'data_evento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_fim_evento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'quantidade_acampantes_maxima': forms.NumberInput(attrs={'min': 0}),
            'quantidade_servos_maxima': forms.NumberInput(attrs={'min': 0}),
            'valor_acampante': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'valor_servo': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_fim_evento'].required = True
        self.fields['quantidade_acampantes_maxima'].required = True
        self.fields['quantidade_servos_maxima'].required = True

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('data_evento')
        fim = cleaned_data.get('data_fim_evento')

        if inicio and fim and fim <= inicio:
            self.add_error(
                'data_fim_evento',
                'O término deve ser depois do início do evento.'
            )

        return cleaned_data

    def save(self, commit=True):
        evento = super().save(commit=False)
        evento.quantidade_participantes_maxima = (
            self.cleaned_data['quantidade_acampantes_maxima']
            + self.cleaned_data['quantidade_servos_maxima']
        )
        evento.ativo = True

        if commit:
            evento.save()

        return evento