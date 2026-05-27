from rest_framework import serializers
from .models import Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'nome',
            'email',
            'password',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
        }

        def create(self, validated_data):
            user = Usuario.objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                password=validated_data['password'],
                nome=validated_data['nome']
            )
            return user