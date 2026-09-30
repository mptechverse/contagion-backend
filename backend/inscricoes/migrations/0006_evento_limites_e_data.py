from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscricoes', '0005_remove_pagamento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='data_inicio',
            new_name='data_evento',
        ),
        migrations.RenameField(
            model_name='evento',
            old_name='data_fim',
            new_name='data_fim_evento',
        ),
        migrations.AddField(
            model_name='evento',
            name='quantidade_participantes_maxima',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evento',
            name='quantidade_acampantes_maxima',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='quantidade_servos_maxima',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]