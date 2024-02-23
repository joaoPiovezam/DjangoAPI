# Generated by Django 4.1 on 2024-02-21 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostico', '0005_pergunta_node'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='resultadoPai',
            field=models.IntegerField(choices=[(0, 'Não'), (1, 'Sim'), (2, 'Nulo')], default=2, verbose_name='Resultado do nó Pai'),
        ),
        migrations.AlterField(
            model_name='node',
            name='resultado',
            field=models.IntegerField(choices=[(0, 'Não'), (1, 'Sim')], default=0, verbose_name='Resultado'),
        ),
    ]