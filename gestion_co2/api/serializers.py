from rest_framework import serializers
from co2.models import *

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

class EdificioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificio
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class ConsumosVehiculosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumosVehiculos
        fields = '__all__'

class ConsumosEdificiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumosEdificios
        fields = '__all__'

class SistemasInteligentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaInteligente
        fields = '__all__'