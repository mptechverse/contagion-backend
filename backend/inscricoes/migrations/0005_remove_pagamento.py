from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inscricoes', '0004_inscricao_alergias_inscricao_autoriza_imagem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='valor_primeira_vez',
        ),
        migrations.RemoveField(
            model_name='evento',
            name='valor_servo',
        ),
        migrations.RemoveField(
            model_name='inscricao',
            name='valor',
        ),
        migrations.RemoveField(
            model_name='inscricao',
            name='status_pagamento',
        ),
        migrations.RemoveField(
            model_name='inscricao',
            name='payment_id',
        ),
    ]
