# Generated by Django 4.1 on 2024-12-09 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0008_alter_pedido_desconto'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='status_oramento',
            field=models.CharField(choices=[('1', 'Orçado'), ('2', 'Faturado')], default='1', max_length=2),
        ),
    ]
