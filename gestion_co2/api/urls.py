"""gestion_co2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework import routers
from api.views import EmpleadoViewSet, EdificioViewSet, VehiculoViewSet, ConsumosVehiculosViewSet, ConsumosEdificiosViewSet, SistemasInteligentesViewSet, Co2CompensadoViewSet

router = routers.DefaultRouter()
router.register(r'empleados', EmpleadoViewSet)
router.register(r'edificios', EdificioViewSet)
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'consumos_vehiculos', ConsumosVehiculosViewSet)
router.register(r'consumos_edificios', ConsumosEdificiosViewSet)
router.register(r'sistemas_inteligentes', SistemasInteligentesViewSet)
router.register(r'co2_compensado', Co2CompensadoViewSet)

urlpatterns = router.urls