import altair as alt
import pandas as pd

from django.db.models import Sum
from .models import ConsumosVehiculos, ConsumosEdificios

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