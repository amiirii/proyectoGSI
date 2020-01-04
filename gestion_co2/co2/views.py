# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'index.html', context={'nombre_empresa': 'Empresa'})

    else:
        if (request.user.empleado.rol == 2):
            return render(request, 'indexGestor.html', context={'nombre_empresa': 'Empresa'})

        else:
            return render(request, 'index.html', context={'nombre_empresa': 'Empresa'})


def login(request):
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

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", context={'form': form, 'nombre_empresa': 'Empresa'})

@login_required(login_url='/login')
def add(request):
	return render(request, 'addco2.html', context={'nombre_empresa': 'Empresa'})
