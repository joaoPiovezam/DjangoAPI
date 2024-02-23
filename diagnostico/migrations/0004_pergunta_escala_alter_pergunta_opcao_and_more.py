# Generated by Django 4.1 on 2024-02-20 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostico', '0003_alter_questionario_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='pergunta',
            name='escala',
            field=models.IntegerField(choices=[(0, 'Nulo'), (1, 'Muito Pouco'), (2, 'Pouco'), (3, 'Razoavel'), (4, 'Ok'), (5, 'Muito')], default=0, verbose_name='Escala'),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='opcao',
            field=models.IntegerField(choices=[(0, 'Nulo'), (1, 'Sim'), (2, 'Não')], default=0, verbose_name='Opção'),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='tecnica',
            field=models.IntegerField(choices=[(0, 'Multipla Escolha'), (1, 'Dicotômica')], default=0, verbose_name='Tipo de Pergunta'),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado', models.IntegerField(choices=[(0, 'Não'), (1, 'Sim'), (2, 'Nulo')], default=2, verbose_name='Resultado do nó Pai')),
                ('codigoNode', models.IntegerField(unique=True)),
                ('noPai', models.IntegerField(null=True)),
                ('questao', models.CharField(max_length=255)),
                ('questionario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='node', to='diagnostico.questionario')),
            ],
        ),
    ]