from rest_framework import serializers
from co2.models import *

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado

class EdificioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificio

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo

class ConsumosVehiculosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumosVehiculos

class ConsumosEdificiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumosEdificios

class SistemasInteligentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaInteligente