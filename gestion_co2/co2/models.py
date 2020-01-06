from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .triptocarbon import TripToCarbon

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

class TiposEdificio(models.Model):
    tipo = models.AutoField(primary_key=True)
    nombre = models.TextField(unique=True)

    def __str__(self):
        return self.nombre

class Edificio(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.TextField(unique=True)
    id_gestor = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_edificio = models.ForeignKey(TiposEdificio, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.direccion, self.tipo_edificio.nombre)

class TiposVehiculo(models.Model):
    tipo = models.AutoField(primary_key=True)
    nombre = models.TextField(unique=True)
    id_triptocarbon = models.TextField(unique=True)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    matricula = models.TextField(primary_key=True)
    modelo = models.TextField()
    marca = models.TextField()
    tipo = models.ForeignKey(TiposVehiculo, on_delete=models.CASCADE)
    consumo_km = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return '{} {} ({})'.format(self.marca, self.modelo, self.matricula)

class ConsumosVehiculos(models.Model):
    matricula = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField()
    conductor = models.ForeignKey(User, on_delete=models.CASCADE)
    emisiones_co2 = models.DecimalField(decimal_places=2, max_digits=5)

class ConsumosEdificios(models.Model):
    id_edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    mes = models.IntegerField()
    year = models.IntegerField()
    emisiones_co2 = models.DecimalField(decimal_places=2, max_digits=5)

class SistemaInteligente(models.Model):
    id_sistema = models.AutoField(primary_key=True)
    id_edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    tipo = models.TextField()
    emisiones_co2 = models.DecimalField(decimal_places=2, max_digits=5)

class ConsumosEdificiosForm(forms.ModelForm):
    consumo = forms.IntegerField(help_text=_('Consumo eléctrico del edificio durante el mes en kWh'), label=_('Consumo eléctrico (en kWh)'))
    fields = ['consumo']

    class Meta:
        model = ConsumosEdificios
        fields = ['id_edificio', 'mes', 'year']
        
        labels = {
            'id_edificio': _('ID del edificio'),
            'mes': _('Mes'),
            'year': _('Año'),
        }
        help_texts = {
            'id_edificio': _('El identificador del edificio'),
            'mes': _('Mes en el que se han realizado las emisiones'),
            'year': _('Año en el que se han realizado las emisiones'),    
        }

    def save(self, commit=True):
        # 0.265 kg de CO2 = 1kWh según la Agencia Europea de Medio Ambiente
        self.instance.emisiones_co2 = self.cleaned_data['consumo'] * 0.265
        return super(ConsumosEdificiosForm, self).save(commit=commit)

class ConsumosVehiculosForm(forms.ModelForm):
    km = forms.IntegerField(help_text=_('Distancia recorrida en kilómetros'), label=_('Distancia (km)'))
    fields= ['km']

    class Meta:
        model = ConsumosVehiculos
        fields = ['matricula', 'fecha']

        labels = {
            'matricula': _('Matrícula'),
            'fecha': _('Fecha'),
        }
        help_texts = {
            'matricula': _('Matrícula del vehículo'),
            'fecha': _('Fecha del trayecto'),
        }

    def save(self, commit=True):
        ttc = TripToCarbon()
        
        consumo_km = self.instance.matricula.consumo_km / 100
        litros_consumidos = self.cleaned_data['km'] * consumo_km
        self.instance.emisiones_co2 = ttc.huella_consumo_combustible(litros_consumidos, self.instance.matricula.tipo.id_triptocarbon)
        return super(ConsumosVehiculosForm, self).save(commit=commit)