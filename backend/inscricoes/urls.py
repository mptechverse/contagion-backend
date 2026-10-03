from django.urls import path
from .views import (
    CriarInscricao,
    evento_atual,
    listar_eventos,
    detalhe_evento,
    ativar_evento,
    listar_inscricoes,
    detalhe_inscricao,
    editar_inscricao,
    remover_inscricao
)

urlpatterns = [

    path(
        'painel/eventos/',
        listar_eventos,
        name='listar_eventos'
    ),

    path(
        'painel/eventos/<int:evento_id>/',
        detalhe_evento,
        name='detalhe_evento'
    ),

    path(
        'painel/eventos/<int:evento_id>/ativar/',
        ativar_evento,
        name='ativar_evento'
    ),

    path(
        'evento/',
        evento_atual,
        name='evento-atual'
    ),

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