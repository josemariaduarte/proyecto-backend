# Generated by Django 2.2.2 on 2021-10-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_auto_20211008_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='cantidad',
            field=models.FloatField(default=0, verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_compra',
            field=models.FloatField(default=0, verbose_name='Precio Compra'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_venta',
            field=models.FloatField(default=0, verbose_name='Precio Venta'),
        ),
    ]