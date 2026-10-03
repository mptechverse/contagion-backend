from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscricoes', '0007_remove_evento_data_fim_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='data_fim_evento',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]