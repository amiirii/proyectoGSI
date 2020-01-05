from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        empleado = Empleado()
        empleado.user = instance

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'empleado'):
        instance.empleado.save()

# Create your models here.
class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.IntegerField(default=0)

class Edificio(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.TextField(unique=True)
    id_gestor = models.ForeignKey(User, on_delete=models.CASCADE)

class Vehiculo(models.Model):
    matricula = models.TextField(primary_key=True)
    modelo = models.TextField()
    marca = models.TextField()
    consumo_km = models.DecimalField(decimal_places=2, max_digits=5)

class ConsumosVehiculos(models.Model):
    matricula = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    km = models.DecimalField(decimal_places=2, max_digits=5)
    conductor = models.ForeignKey(User, on_delete=models.CASCADE)

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

class ConsumosEdificiosForm(ModelForm):
    class Meta:
        model = ConsumosEdificios
        fields = ['id_edificio', 'mes', 'year', 'consumo']

class ConsumosVehiculosForm(ModelForm):
    class Meta:
        model = ConsumosVehiculos
        fields = ['matricula', 'fecha', 'km', 'conductor']