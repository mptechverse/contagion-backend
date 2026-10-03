from django.db import migrations, models
from django.db.models import Q


def keep_latest_active_event(apps, schema_editor):
    Evento = apps.get_model('inscricoes', 'Evento')
    active_ids = list(
        Evento.objects.filter(ativo=True)
        .order_by('-id')
        .values_list('id', flat=True)
    )
    if len(active_ids) > 1:
        Evento.objects.filter(
            id__in=active_ids[1:]
        ).update(ativo=False)


class Migration(migrations.Migration):

    dependencies = [
        ('inscricoes', '0008_evento_data_fim'),
    ]

    operations = [
        migrations.RunPython(
            keep_latest_active_event,
            migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name='evento',
            constraint=models.UniqueConstraint(
                condition=Q(ativo=True),
                fields=('ativo',),
                name='unico_evento_ativo',
            ),
        ),
    ]