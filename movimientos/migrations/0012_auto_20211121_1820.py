# Generated by Django 2.2.2 on 2021-11-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0011_movimientocaja'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientocaja',
            name='cerrado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='movimientocaja',
            name='tipo_movimiento',
            field=models.IntegerField(choices=[(1, 'COMPRA'), (2, 'VENTA'), (3, 'APERTURA')], default=2, verbose_name='Tipo'),
        ),
    ]