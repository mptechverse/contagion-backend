from rest_framework import generics
from .models import Usuario
from .serializers import UserSerializer

class CriarUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer