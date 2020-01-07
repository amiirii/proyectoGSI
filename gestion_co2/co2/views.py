# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as do_logout, login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .graficos import *

from .models import ConsumosVehiculosForm, ConsumosEdificiosForm

# Create your views here.
def index(request):
    return render(request, 'index.html', context={
        'emisiones_vehiculos': grafico_emisiones_vehiculos(), 
        'emisiones_edificios': grafico_emisiones_edificios(), 
        'emisiones_evitadas': grafico_emisiones_evitadas(),
        'nombre_empresa': settings.NOMBRE_EMPRESA
    })

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
    return render(request, "login.html", context={
        'form': form, 
        'nxt': nxt, 
        'nombre_empresa': settings.NOMBRE_EMPRESA
    })

def logout(request):
    do_logout(request)
    return redirect('/')

def informe_mensual(request):
    graf_comparativa, total_emisiones = grafico_comparativa()
    return render(request, 'informe.html', context={
        'emisiones_vehiculos': grafico_emisiones_vehiculos(), 
        'emisiones_edificios': grafico_emisiones_edificios(), 
        'emisiones_evitadas': grafico_emisiones_evitadas(),
        'emisiones_sistemas_inteligentes': grafico_sistemas_inteligentes(),
        'grafico_comparativa': graf_comparativa,
        'total_kg_co2': total_emisiones,
        'nombre_empresa': settings.NOMBRE_EMPRESA
    })

@login_required(login_url='/login')
def add(request):
    if request.method == 'GET':
	    return render(request, 'addco2.html', context={
            'form_vehiculo': ConsumosVehiculosForm(), 
            'form_edificio': ConsumosEdificiosForm(), 
            'nombre_empresa': settings.NOMBRE_EMPRESA
        })
    else:
        if request.POST['tipo_emisiones'] == 'edificio':
            form = ConsumosEdificiosForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Los datos se han añadido correctamente')
            else:
                return HttpResponse('Ha ocurrido un error')

        else:
            form = ConsumosVehiculosForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.conductor = request.user
                instance.save()
                return HttpResponse('Los datos se han añadido correctamente')
            else:
                return HttpResponse('Ha ocurrido un error')