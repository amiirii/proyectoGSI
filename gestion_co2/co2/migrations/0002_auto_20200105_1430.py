# Generated by Django 2.2.7 on 2020-01-05 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('co2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumosvehiculos',
            name='fecha',
            field=models.DateField(),
        ),
    ]
