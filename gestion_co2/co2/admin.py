# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Empleado)
admin.site.register(Edificio)
admin.site.register(Vehiculo)
admin.site.register(ConsumosEdificios)
admin.site.register(ConsumosVehiculos)
admin.site.register(SistemaInteligente)