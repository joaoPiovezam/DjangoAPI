# Generated by Django 4.1 on 2024-02-20 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostico', '0004_pergunta_escala_alter_pergunta_opcao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pergunta',
            name='node',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='diagnostico.node'),
            preserve_default=False,
        ),
    ]
