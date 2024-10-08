# Generated by Django 4.1 on 2024-04-09 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0015_remove_transportadora_cpfcnpj'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataEntrada', models.DateField()),
                ('dataSaida', models.DateField()),
                ('codigoPedido', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loja.pedido')),
            ],
        ),
    ]
