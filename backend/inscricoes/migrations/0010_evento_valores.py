from decimal import Decimal

from django.db import migrations, models
import django.core.validators
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ('inscricoes', '0009_unico_evento_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='valor_acampante',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0.00'),
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal('0.00'))],
            ),
        ),
        migrations.AddField(
            model_name='evento',
            name='valor_servo',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0.00'),
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal('0.00'))],
            ),
        ),
        migrations.AddConstraint(
            model_name='evento',
            constraint=models.CheckConstraint(
                condition=Q(valor_acampante__gte=0),
                name='valor_acampante_nao_negativo',
            ),
        ),
        migrations.AddConstraint(
            model_name='evento',
            constraint=models.CheckConstraint(
                condition=Q(valor_servo__gte=0),
                name='valor_servo_nao_negativo',
            ),
        ),
    ]