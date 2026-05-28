from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Inscricao, Evento
from .serializers import InscricaoSerializer

from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime

from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@api_view(['GET'])
@csrf_exempt
def home(request):

    return Response({
        "status": "Backend funcionando"
    })


@method_decorator(csrf_exempt, name='dispatch')
class CriarInscricao(generics.CreateAPIView):

    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):

        evento = Evento.objects.filter(
            ativo=True
        ).first()

        serializer.save(evento=evento)


@login_required
def listar_inscricoes(request):

    inscricoes = Inscricao.objects.all().order_by(
        '-criado_em'
    )

    pagos = inscricoes.filter(
        status_pagamento='pago'
    ).count()

    pendentes = inscricoes.filter(
        status_pagamento='pendente'
    ).count()

    servos = inscricoes.filter(
        tipo='servo'
    ).count()

    primeira_vez = inscricoes.filter(
        tipo='primeira_vez'
    ).count()

    return render(
        request,
        'inscricoes/listar.html',
        {
            'inscricoes': inscricoes,
            'pagos': pagos,
            'pendentes': pendentes,
            'servos': servos,
            'primeira_vez': primeira_vez,
        }
    )


@login_required
def detalhe_inscricao(request, id):

    inscricao = get_object_or_404(
        Inscricao,
        id=id
    )

    if request.method == 'POST':

        inscricao.status_pagamento = request.POST.get(
            'status_pagamento'
        )

        inscricao.save()

        return redirect('listar_inscricoes')

    return render(
        request,
        'inscricoes/detalhe_inscricao.html',
        {
            'inscricao': inscricao
        }
    )


@login_required
def remover_inscricao(request, id):

    inscricao = get_object_or_404(
        Inscricao,
        id=id
    )

    if request.method == 'POST':

        inscricao.delete()

        return redirect(
            'listar_inscricoes'
        )

    return render(
        request,
        'inscricoes/remover_inscricao.html',
        {
            'inscricao': inscricao
        }
    )


@login_required
def editar_inscricao(request, id):

    inscricao = get_object_or_404(
        Inscricao,
        id=id
    )

    eventos = Evento.objects.all()

    if request.method == 'POST':

        inscricao.nome_completo = request.POST.get(
            'nome_completo'
        )

        inscricao.telefone = request.POST.get(
            'telefone'
        )

        inscricao.cidade = request.POST.get(
            'cidade'
        )

        inscricao.estado = request.POST.get(
            'estado'
        )

        inscricao.igreja = request.POST.get(
            'igreja'
        )

        data_nascimento = request.POST.get(
            'data_nascimento'
        )

        if data_nascimento:

            inscricao.data_nascimento = datetime.strptime(
                data_nascimento,
                '%Y-%m-%d'
            ).date()

        inscricao.tipo = request.POST.get(
            'tipo'
        )

        inscricao.tamanho_camisa = request.POST.get(
            'tamanho_camisa'
        )

        inscricao.status_pagamento = request.POST.get(
            'status_pagamento'
        )

        inscricao.quer_servir = (
            request.POST.get('quer_servir') == 'True'
        )

        inscricao.responsavel_nome = request.POST.get(
            'responsavel_nome'
        )

        inscricao.telefone_responsavel = request.POST.get(
            'telefone_responsavel'
        )

        inscricao.participa_igreja = (
            request.POST.get('participa_igreja') == 'on'
        )

        inscricao.pastor_lider = request.POST.get(
            'pastor_lider'
        )

        inscricao.telefone_lider = request.POST.get(
            'telefone_lider'
        )

        inscricao.tempo_igreja = request.POST.get(
            'tempo_igreja'
        )

        inscricao.parentesco = request.POST.get(
            'parentesco'
        )

        inscricao.alergias = request.POST.get(
            'alergias'
        )

        inscricao.doencas_pre_existentes = request.POST.get(
            'doencas_pre_existentes'
        )

        inscricao.medicamentos_continuos = request.POST.get(
            'medicamentos_continuos'
        )

        inscricao.restricoes_alimentares = request.POST.get(
            'restricoes_alimentares'
        )

        inscricao.observacoes_medicas = request.POST.get(
            'observacoes_medicas'
        )

        inscricao.como_conheceu = request.POST.get(
            'como_conheceu'
        )

        evento_id = request.POST.get(
            'evento'
        )

        if evento_id:

            inscricao.evento = Evento.objects.get(
                id=evento_id
            )

        inscricao.save()

        return redirect(
            'detalhe_inscricao',
            id=id
        )

    return render(
        request,
        'inscricoes/editar_inscricao.html',
        {
            'inscricao': inscricao,
            'eventos': eventos
        }
    )