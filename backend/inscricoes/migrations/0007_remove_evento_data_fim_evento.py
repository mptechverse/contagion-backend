from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inscricoes', '0006_evento_limites_e_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='data_fim_evento',
        ),
    ]