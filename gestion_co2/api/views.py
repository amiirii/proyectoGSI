from rest_framework import viewsets
from co2.models import *
from .serializers import *

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class EdificioViewSet(viewsets.ModelViewSet):
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class ConsumosVehiculosViewSet(viewsets.ModelViewSet):
    queryset = ConsumosVehiculos.objects.all()
    serializer_class = ConsumosVehiculosSerializer

class ConsumosEdificiosViewSet(viewsets.ModelViewSet):
    queryset = ConsumosEdificios.objects.all()
    serializer_class = ConsumosEdificiosSerializer

class SistemasInteligentesViewSet(viewsets.ModelViewSet):
    queryset = SistemaInteligente.objects.all()
    serializer_class = SistemasInteligentesSerializer