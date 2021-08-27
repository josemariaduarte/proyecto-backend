# Generated by Django 2.2.2 on 2021-08-27 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_doc', models.CharField(max_length=50, verbose_name='Nro. Documento')),
                ('nombres', models.CharField(max_length=150, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('telefono', models.CharField(blank=True, max_length=60, null=True, verbose_name='Numero de Telefono')),
                ('sexo', models.IntegerField(blank=True, choices=[(1, 'Masculino'), (2, 'Femenino')], default=2, null=True, verbose_name='Sexo')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dirección')),
                ('estado_civil', models.IntegerField(blank=True, choices=[(1, 'SOLTERO'), (2, 'CASADO'), (3, 'DIVORCIADO'), (4, 'VIUDO')], null=True, verbose_name='Estado Civil')),
                ('correo', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo Electronico')),
                ('activo', models.BooleanField(default=True)),
                ('comentario_desactivado', models.CharField(blank=True, max_length=200, null=True, verbose_name='Comentario')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=100, verbose_name='Nombre o Razón Social')),
                ('ruc', models.CharField(max_length=20, verbose_name='RUC')),
                ('direccion', models.CharField(max_length=100, verbose_name='Dirección')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['-pk'],
            },
        ),
    ]
