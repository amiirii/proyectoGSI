from django.db import models

# Create your models here.
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=10)
    apellido = models.TextField(max_length=20)
    email = models.TextField(max_length=100)
    password = models.TextField(max_length=32)
    rol = models.IntegerField()

class Edificio(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.TextField(unique=True)
    id_gestor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Vehiculo(models.Model):
    matricula = models.TextField(primary_key=True)
    modelo = models.TextField()
    marca = models.TextField()
    consumo_km = models.DecimalField(decimal_places=2, max_digits=5)

class ConsumosVehiculos(models.Model):
    matricula = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    km = models.DecimalField(decimal_places=2, max_digits=5)
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

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