# Generated by Django 2.2.2 on 2021-11-24 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0007_auto_20211021_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='impuesto',
            field=models.IntegerField(choices=[(5, '5%'), (10, '10%')], default=10),
        ),
    ]