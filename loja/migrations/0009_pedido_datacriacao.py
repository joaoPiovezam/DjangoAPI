# Generated by Django 4.1 on 2024-03-19 13:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0008_pecafornecedor_preco'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='dataCriacao',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
