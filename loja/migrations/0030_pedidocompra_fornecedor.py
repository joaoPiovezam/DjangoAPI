# Generated by Django 4.1 on 2024-09-12 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0029_remove_pedidocompra_cotacao_cotacao_pedidocompra'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidocompra',
            name='fornecedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='loja.fornecedor'),
            preserve_default=False,
        ),
    ]
