from django.urls import path
from .views import (
    CriarInscricao,
    listar_inscricoes,
    detalhe_inscricao,
    editar_inscricao,
    remover_inscricao
)

urlpatterns = [

    path(
        '',
        CriarInscricao.as_view(),
        name='criar-inscricao'
    ),

    path(
        'lista/',
        listar_inscricoes,
        name='listar_inscricoes'
    ),

    path(
        'inscricao/<int:id>/',
        detalhe_inscricao,
        name='detalhe_inscricao'
    ),

    path(
        'inscricao/<int:id>/editar/',
        editar_inscricao,
        name='editar_inscricao'
    ),

    path(
        'inscricao/<int:id>/remover/',
        remover_inscricao,
        name='remover_inscricao'
    ),
]