import json
import time
import random
import requests
from requests.auth import HTTPBasicAuth

vehiculos = {
    'Ford': ['Fiesta', 'Transit', 'Transit Connect'],
    'Renault': ['Master'],
    'Toyota': ['Corolla'],
    'Volkswagen': ['Tiguan', 'Atlas']
    }

combustibles = [0, 1]

def generar_fecha(inicio, fin):
    frmt = '%Y-%m-%d'
    i = time.mktime(time.strptime(inicio, frmt))
    f = time.mktime(time.strptime(fin, frmt))
    t = random.uniform(i, f)
    return time.strftime(frmt, time.localtime(t))

def generar_matricula():
    letras = list('abcdefghijklmnopqrstuvwxyz')
    random.shuffle(letras)
    num = str(random.randint(0, 9999)).zfill(4)

    return num + ''.join(letras[0:3]).upper()

def generar_vehiculo():
    marca, modelos = random.choice(list(vehiculos.items()))
    modelo = random.choice(modelos)

    return {
        'matricula': generar_matricula(),
        'modelo': modelo,
        'marca': marca,
        'tipo': random.randint(1, 2),
        'consumo_km': round(random.uniform(4, 7), 2)
    }

def generar_trayecto(vehiculo, conductor, fecha_inicio='2018-01-01', fecha_fin='2019-12-31'):
    return {
        'matricula': vehiculo['matricula'],
        'fecha': generar_fecha(fecha_inicio, fecha_fin),
        'conductor': conductor['id'],
        'emisiones_co2': round(random.uniform(50, 200), 2)
    }

def generar_consumo(edificio, m, y):
    return {
        'id_edificio': edificio['id'],
        'mes': m,
        'year': y,
        'emisiones_co2': round(random.uniform(500, 999), 2)
    }

def generar_co2_compensado(sistema, m, y):
    return {
        'id_sistema': sistema['id_sistema'],
        'mes': m,
        'year': y,
        'emisiones_co2': round(random.uniform(500, 999), 2)
    }

# Generar la flota de vehiculos
# for i in range(0, 12):
#     print('Generando vehículo {}...'.format(i))
#     response = requests.post('http://localhost:8000/api/vehiculos/', auth=HTTPBasicAuth('admin', 'admin'), data=generar_vehiculo())
#     print('Respuesta: {} ({})'.format(response.text, response.status_code))

# Obtener los vehiculos en la base de datos
response = requests.get('http://localhost:8000/api/vehiculos/', auth=HTTPBasicAuth('admin', 'admin'))
flota = json.loads(response.text)

# Obtener los empleados de la base de datos
response = requests.get('http://localhost:8000/api/empleados/', auth=HTTPBasicAuth('admin', 'admin'))
empleados = json.loads(response.text)

# Obtener los edificios de la base de datos
response = requests.get('http://localhost:8000/api/edificios/', auth=HTTPBasicAuth('admin', 'admin'))
edificios = json.loads(response.text)

# Obtener los sistemas inteligentes de la base de datos
response = requests.get('http://localhost:8000/api/sistemas_inteligentes/', auth=HTTPBasicAuth('admin', 'admin'))
sistemas = json.loads(response.text)

# Insertar el co2 compensado
for sistema in sistemas:
    print('Generando el CO2 compensado para {}...'.format(sistema['id_sistema']))
    for y in [2018, 2019]:
        for m in range(1, 13):
            response = requests.post('http://localhost:8000/api/co2_compensado/', auth=HTTPBasicAuth('admin', 'admin'), data=generar_co2_compensado(sistema, m, y))
            print('Respuesta: {} ({})'.format(response.text, response.status_code))

# Insertar las emisiones
for i in range(0, 2200):
    # Seleccionar aleatoriamente un vehiculo de todos los disponibles
    v = random.choice(flota)
    # Seleccionar aleatoriamente un empleado de todos los disponibles
    e = random.choice(empleados)

    print('Generando emisiones para {}...'.format(v['matricula']))
    response = requests.post('http://localhost:8000/api/consumos_vehiculos/', auth=HTTPBasicAuth('admin', 'admin'), data=generar_trayecto(v, e))
    print('Respuesta: {} ({})'.format(response.text, response.status_code))

# Insertar los consumos
for edificio in edificios:
    print('Generando los consumos para el edificio {} ({})...'.format(edificio['direccion'], edificio['tipo_edificio']))
    for y in [2018, 2019]:
        for m in range(1, 13):
            response = requests.post('http://localhost:8000/api/consumos_edificios/', auth=HTTPBasicAuth('admin', 'admin'), data=generar_consumo(edificio, m, y))
            print('Respuesta: {} ({})'.format(response.text, response.status_code))