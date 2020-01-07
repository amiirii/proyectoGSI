import datetime

import altair as alt
import pandas as pd

from django.db.models import Sum
from .models import ConsumosVehiculos, ConsumosEdificios, Co2Compensado

def grafico_emisiones_edificios():
    consumos = ConsumosEdificios.objects.values('id_edificio').annotate(s=Sum('emisiones_co2')).values('id_edificio__tipo_edificio__nombre', 's')
    ids = [str(e['id_edificio__tipo_edificio__nombre']) for e in consumos]
    emisiones = [float(e['s']) for e in consumos]

    datos = pd.DataFrame({
        'Tipo de edificio': ids,
        'CO2 emitido': emisiones
    })

    chart = alt.Chart(datos).mark_bar().encode(
        x='Tipo de edificio',
        y='CO2 emitido'
    ).interactive()

    return chart

def grafico_emisiones_vehiculos():
    consumos = ConsumosVehiculos.objects.values('matricula').annotate(s=Sum('emisiones_co2')).values('matricula__tipo__nombre', 's')
    ids = [str(e['matricula__tipo__nombre']) for e in consumos]
    emisiones = [float(e['s']) for e in consumos] 

    datos = pd.DataFrame({
        'Tipo de vehiculo': ids,
        'CO2 emitido': emisiones
    })

    chart = alt.Chart(datos).mark_bar().encode(
        x='Tipo de vehiculo',
        y='CO2 emitido'
    ).interactive()

    return chart

def grafico_emisiones_evitadas():
    consumos = Co2Compensado.objects.filter(emisiones_co2__lt=0).annotate(s=Sum('emisiones_co2')).values('id_sistema__tipo__nombre', 's')
    ids = [str(e['id_sistema__tipo__nombre']) for e in consumos]
    emisiones = [float(e['s']) for e in consumos] 

    datos = pd.DataFrame({
        'Tipo de sistema': ids,
        'CO2 emitido': emisiones
    })

    chart = alt.Chart(datos).mark_bar().encode(
        x='Tipo de sistema',
        y='CO2 emitido'
    ).interactive()

    return chart

def grafico_sistemas_inteligentes():
    consumos = Co2Compensado.objects.annotate(s=Sum('emisiones_co2')).values('id_sistema__tipo__nombre', 's')
    ids = [str(e['id_sistema__tipo__nombre']) for e in consumos]
    emisiones = [float(e['s']) for e in consumos] 

    datos = pd.DataFrame({
        'Tipo de sistema': ids,
        'CO2 emitido': emisiones
    })

    chart = alt.Chart(datos).mark_bar().encode(
        x='Tipo de sistema',
        y='CO2 emitido'
    ).interactive()

    return chart

def grafico_emisiones(y, c='red'):
    emisiones_total = dict([(i, 0) for i in range(1, 13)])
    # Vehiculos
    consumos_vehiculos = ConsumosVehiculos.objects.values('fecha__month').filter(fecha__year=y).annotate(s=Sum('emisiones_co2')).values('fecha__month', 's')
    for e in consumos_vehiculos:
        emisiones_total[e['fecha__month']] += float(e['s'])

    # Edificios
    consumos_edificios = ConsumosEdificios.objects.values('mes').filter(year=y).annotate(s=Sum('emisiones_co2')).values('mes', 's')
    for e in consumos_edificios:
        emisiones_total[e['mes']] += float(e['s'])

    # Sistemas inteligentes
    consumos_si = Co2Compensado.objects.values('mes').filter(year=y).annotate(s=Sum('emisiones_co2')).values('mes', 's')
    for e in consumos_si:
        emisiones_total[e['mes']] += float(e['s'])

    ids = list(emisiones_total.keys())
    emisiones = list(emisiones_total.values())

    datos = pd.DataFrame({
        'Meses': ids,
        'CO2 emitido': emisiones
    })

    return alt.Chart(datos).mark_line(color=c).encode(
        x='Meses',
        y='CO2 emitido'
    ).interactive(), sum(emisiones)

def grafico_comparativa():
    year = datetime.datetime.now().year - 1
    previous_year = year - 1
    chart1, emisiones1 = grafico_emisiones(year, 'red')
    chart2, emisiones2 = grafico_emisiones(previous_year, 'blue')

    return chart1 + chart2, emisiones1