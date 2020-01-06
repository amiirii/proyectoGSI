from rest_framework import serializers
from co2.models import *

from co2.triptocarbon import TripToCarbon, TTCException

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
    def validate_emisiones_co2(self, value):
        v = Vehiculo.objects.get(matricula=self.initial_data['matricula'])
        ttc = TripToCarbon()
        litros_consumidos = float(value * v.consumo_km) / 100
        try:
            emisiones = ttc.huella_consumo_combustible(litros_consumidos, v.tipo.id_triptocarbon)
        except TTCException as e:
            print(e)
        return emisiones

    class Meta:
        model = ConsumosVehiculos
        fields = '__all__'

class ConsumosEdificiosSerializer(serializers.ModelSerializer):
    def validate_emisiones_co2(self, value):
        return float(value) * 0.265

    class Meta:
        model = ConsumosEdificios
        fields = '__all__'

class SistemasInteligentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaInteligente
        fields = '__all__'

class Co2CompensadoSerializer(serializers.ModelSerializer):
    def validate_emisiones_co2(self, value):
        s = SistemaInteligente.objects.get(id_sistema=self.initial_data['id_sistema'])
        return float(value * s.tipo.factor) * 0.265

    class Meta:
        model = Co2Compensado
        fields = '__all__'