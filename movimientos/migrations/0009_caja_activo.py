# Generated by Django 2.2.2 on 2021-11-20 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0008_caja'),
    ]

    operations = [
        migrations.AddField(
            model_name='caja',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]