# Generated by Django 4.1 on 2024-07-30 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0021_remove_usuario_senha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='site',
        ),
    ]
