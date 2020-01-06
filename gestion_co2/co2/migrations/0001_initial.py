# Generated by Django 3.0.2 on 2020-01-06 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Edificio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('direccion', models.TextField(unique=True)),
                ('id_gestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TiposEdificio',
            fields=[
                ('tipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TiposVehiculo',
            fields=[
                ('tipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(unique=True)),
                ('id_triptocarbon', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('matricula', models.TextField(primary_key=True, serialize=False)),
                ('modelo', models.TextField()),
                ('marca', models.TextField()),
                ('consumo_km', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='co2.TiposVehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='SistemaInteligente',
            fields=[
                ('id_sistema', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.TextField()),
                ('emisiones_co2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('id_edificio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='co2.Edificio')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.IntegerField(default=0)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='edificio',
            name='tipo_edificio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='co2.TiposEdificio'),
        ),
        migrations.CreateModel(
            name='ConsumosVehiculos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('emisiones_co2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('conductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='co2.Vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='ConsumosEdificios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.IntegerField()),
                ('year', models.IntegerField()),
                ('emisiones_co2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('id_edificio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='co2.Edificio')),
            ],
        ),
    ]
