# Generated by Django 4.1 on 2024-11-14 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0004_alter_pedidocompra_data_emissao'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='desconto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='descricao',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]