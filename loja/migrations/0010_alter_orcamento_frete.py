# Generated by Django 4.1 on 2024-03-20 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0009_pedido_datacriacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='frete',
            field=models.DecimalField(decimal_places=3, max_digits=15),
        ),
    ]