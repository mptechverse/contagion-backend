from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from .models import Inscricao, Evento
from .serializers import InscricaoSerializer

from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.db import transaction
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.db.models import Count

from .forms import EventoForm


@api_view(['GET'])
@csrf_exempt
def home(request):

    return Response({
        "status": "Backend funcionando"
    })


@api_view(['GET'])
def evento_atual(request):
    evento = Evento.objects.filter(ativo=True).first()

    if evento is None:
        return Response(
            {'detail': 'Não há evento ativo.'},
            status=404
        )

    return Response({
        'id': evento.id,
        'nome': evento.nome,
        'data_evento': evento.data_evento,
        'data_fim_evento': evento.data_fim_evento,
    })


@method_decorator(csrf_exempt, name='dispatch')
class CriarInscricao(generics.CreateAPIView):

    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):
        with transaction.atomic():
            evento = Evento.objects.select_for_update().filter(
                ativo=True
            ).first()

            if evento is None:
                raise ValidationError({
                    'evento': 'Não há evento ativo para inscrição.'
                })

            if timezone.now() >= evento.data_evento:
                raise ValidationError({
                    'evento': 'As inscrições foram encerradas porque o evento já começou.'
                })

            tipo = serializer.validated_data['tipo']
            if tipo == 'servo':
                limite = evento.quantidade_servos_maxima
                nome_categoria = 'servos'
            else:
                limite = evento.quantidade_acampantes_maxima
                nome_categoria = 'acampantes'

            total_categoria = Inscricao.objects.filter(
                evento=evento,
                tipo=tipo
            ).count()

            if limite is not None and total_categoria >= limite:
                raise ValidationError({
                    'tipo': f'As vagas para {nome_categoria} foram preenchidas.'
                })

            serializer.save(evento=evento)


@login_required
def listar_inscricoes(request):
    evento = Evento.objects.filter(ativo=True).first()

    inscricoes = Inscricao.objects.filter(
        evento=evento
    ).order_by('-criado_em') if evento else Inscricao.objects.none()

    servos = inscricoes.filter(tipo='servo').count()
    primeira_vez = inscricoes.filter(tipo='primeira_vez').count()

    acampantes_evento = 0
    servos_evento = 0
    inscricoes_encerradas = False

    if evento:
        acampantes_evento = Inscricao.objects.filter(
            evento=evento,
            tipo='primeira_vez'
        ).count()
        servos_evento = Inscricao.objects.filter(
            evento=evento,
            tipo='servo'
        ).count()
        inscricoes_encerradas = timezone.now() >= evento.data_evento

    return render(
        request,
        'inscricoes/listar.html',
        {
            'inscricoes': inscricoes,
            'servos': servos,
            'primeira_vez': primeira_vez,
            'evento': evento,
            'acampantes_evento': acampantes_evento,
            'servos_evento': servos_evento,
            'inscricoes_encerradas': inscricoes_encerradas,
        }
    )


@staff_member_required
def listar_eventos(request):
    form = EventoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        evento = form.save()
        return redirect('detalhe_evento', evento_id=evento.id)

    eventos = Evento.objects.annotate(
        total_inscricoes=Count('inscricao')
    ).order_by('-data_evento', '-id')

    return render(
        request,
        'inscricoes/eventos.html',
        {
            'eventos': eventos,
            'form': form,
        }
    )


@staff_member_required
def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscricoes = Inscricao.objects.filter(
        evento=evento
    ).order_by('-criado_em')

    return render(
        request,
        'inscricoes/evento_detalhe.html',
        {
            'evento': evento,
            'inscricoes': inscricoes,
            'servos': inscricoes.filter(tipo='servo').count(),
            'acampantes': inscricoes.filter(tipo='primeira_vez').count(),
        }
    )


@staff_member_required
@require_POST
def ativar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    evento.ativo = True
    evento.save()
    return redirect('listar_eventos')


@login_required
def detalhe_inscricao(request, id):

    inscricao = get_object_or_404(
        Inscricao,
        id=id
    )

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