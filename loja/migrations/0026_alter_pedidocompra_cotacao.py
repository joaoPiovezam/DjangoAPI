# Generated by Django 4.1 on 2024-09-09 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0025_estoque_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidocompra',
            name='cotacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.cotacao'),
        ),
    ]