# Generated by Django 4.1 on 2024-07-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0019_pack'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='senha',
            field=models.CharField(default=123, max_length=250),
            preserve_default=False,
        ),
    ]
