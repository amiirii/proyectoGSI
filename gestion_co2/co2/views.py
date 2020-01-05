# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import altair as alt
import pandas as pd

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as do_logout, login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import ConsumosVehiculosForm, ConsumosEdificiosForm, ConsumosVehiculos, ConsumosEdificios

# Create your views here.
def index(request):
    consumos_edificios = ConsumosEdificios.objects.values('id_edificio').annotate(dcount=Sum('consumo'))
    consumos_vehiculos = ConsumosVehiculos.objects.values('matricula').annotate(dcount=Sum('km'))

    ids_edificios = [e['id_edificio'] for e in consumos_edificios]
    ids_vehiculos = [e['matricula'] for e in consumos_vehiculos]

    emisiones_edificios = [float(e['dcount']) for e in consumos_edificios]
    emisiones_vehiculos = [float(e['dcount']) for e in consumos_vehiculos]
    

    datos = pd.DataFrame({
        'vehiculo': ids_vehiculos,
        'km': emisiones_vehiculos
    })

    chart = alt.Chart(datos).mark_bar().encode(
        x='vehiculo',
        y='km'
    ).interactive()

    datos2 = pd.DataFrame({
        'edificio': ids_edificios,
        'consumo': emisiones_edificios
    })

    chart1 = alt.Chart(datos2).mark_bar().encode(
        x='edificio',
        y='consumo',
    ).interactive()

    return render(request, 'index.html', context={'chart': chart, 'chart1': chart1, 'nombre_empresa': settings.NOMBRE_EMPRESA})

def login(request):

    # Obtenemos la página a la que se redirigirá al usuario una vez haya iniciado sesión
    if request.method == "GET" and 'next' in request.GET:
        nxt = request.GET['next']
    else:
        nxt = '/'

    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            nxt = request.POST.get('next')

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                if user.is_superuser:
                    return redirect('/admin')
                else:
                    return redirect(nxt)


    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", context={'form': form, 'nxt': nxt, 'nombre_empresa': settings.NOMBRE_EMPRESA})

def logout(request):
    do_logout(request)
    return redirect('/')

def informe_mensual(request):
    return render(request, 'informe.html', context={'nombre_empresa': settings.NOMBRE_EMPRESA})

@login_required(login_url='/login')
def add(request):
    if request.method == 'GET':
	    return render(request, 'addco2.html', context={'form_vehiculo': ConsumosVehiculosForm(), 'form_edificio': ConsumosEdificiosForm(), 'nombre_empresa': settings.NOMBRE_EMPRESA})
    else:
        if request.POST['tipo_emisiones'] == 'edificio':
            form = ConsumosEdificiosForm(request.POST)
            if form.is_valid:
                form.save()
                return HttpResponse('Los datos se han añadido correctamente')
            else:
                return HttpResponse('Ha ocurrido un error')

        else:
            form = ConsumosVehiculosForm(request.POST)
            if form.is_valid:
                # TODO establecer que el conductor es el usuario que envía el formulario
                form.save()
                return HttpResponse('Los datos se han añadido correctamente')
            else:
                return HttpResponse('Ha ocurrido un error')