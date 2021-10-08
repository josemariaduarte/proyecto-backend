# Generated by Django 2.2.2 on 2021-10-08 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_producto_porcentaje_ganancia'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransaccionProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[('COMPRA', 1), ('VENTA', 2)], default=1, verbose_name='Tipo')),
                ('cantidad', models.FloatField(verbose_name='Cantidad')),
                ('cantidad_anterior', models.FloatField(verbose_name='Cantidad Anterior en Stock')),
                ('cantidad_actual', models.FloatField(verbose_name='Cantidad Actual en Stock')),
                ('precio_compra', models.FloatField(verbose_name='Precio Compra')),
                ('precio_compra_anterior', models.FloatField(verbose_name='Precio Compra Anterior')),
                ('precio_venta', models.FloatField(verbose_name='Precio Venta Anterior')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='productos.Producto')),
            ],
            options={
                'verbose_name': 'Transacción Producto',
                'verbose_name_plural': 'Transacciones de Producto',
                'ordering': ['-pk'],
            },
        ),
    ]
