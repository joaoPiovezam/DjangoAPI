# Generated by Django 4.1 on 2024-04-05 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0012_notificar_usuario_orcamento_cidadeentrega_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificar',
            name='orcamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='loja.orcamento'),
            preserve_default=False,
        ),
    ]
