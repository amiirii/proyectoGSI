from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Empleado(AbstractUser):
    rol = models.IntegerField(default=0)    # 0 = Emleado; 1 = Gestor
    REQUIRED_FIELDS = ['rol', 'email']

class Edificio(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.TextField(unique=True)
    id_gestor = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class Vehiculo(models.Model):
    matricula = models.TextField(primary_key=True)
    modelo = models.TextField()
    marca = models.TextField()
    consumo_km = models.DecimalField(decimal_places=2, max_digits=5)

class ConsumosVehiculos(models.Model):
    matricula = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    km = models.DecimalField(decimal_places=2, max_digits=5)
    conductor = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class ConsumosEdificios(models.Model):
    id_edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    mes = models.IntegerField()
    year = models.IntegerField()
    consumo = models.DecimalField(decimal_places=2, max_digits=5)

class SistemaInteligente(models.Model):
    id_sistema = models.AutoField(primary_key=True)
    id_edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    tipo = models.TextField()
    generado = models.DecimalField(decimal_places=2, max_digits=5)