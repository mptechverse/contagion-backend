from rest_framework import serializers
from .models import Inscricao


class InscricaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inscricao
        fields = '__all__'
        read_only_fields = [
            'usuario',
            'evento',
            'idade',
            'criado_em'
        ]