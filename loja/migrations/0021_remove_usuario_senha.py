# Generated by Django 4.1 on 2024-07-30 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0020_usuario_senha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='senha',
        ),
    ]
