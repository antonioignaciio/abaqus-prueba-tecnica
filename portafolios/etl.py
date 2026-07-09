import pandas as pd
from decimal import Decimal
from portafolios.models import Activo, Portafolio, Precio, Weight
from django.db import transaction


def leer_excel(ruta_archivo):
    weights_df = pd.read_excel(ruta_archivo, sheet_name='weights')
    precios_df = pd.read_excel(ruta_archivo, sheet_name='Precios')
    return weights_df, precios_df


def crear_activos(weights_df):
    activos = {}
    for nombre in weights_df['activos']:
        activo = Activo.objects.create(nombre=nombre)
        activos[nombre] = activo
    return activos


def crear_portafolios():
    p1 = Portafolio.objects.create(nombre='Portafolio 1', valor_inicial=Decimal('1000000000'))
    p2 = Portafolio.objects.create(nombre='Portafolio 2', valor_inicial=Decimal('1000000000'))
    return p1, p2


def crear_weights(weights_df, activos, p1, p2):
    weights = []
    for _, fila in weights_df.iterrows():
        nombre_activo = fila['activos']
        weights.append(Weight(
            portafolio=p1,
            activo=activos[nombre_activo],
            valor=Decimal(str(fila['portafolio 1'])),
        ))
        weights.append(Weight(
            portafolio=p2,
            activo=activos[nombre_activo],
            valor=Decimal(str(fila['portafolio 2'])),
        ))
    Weight.objects.bulk_create(weights)


def transformar_precios_a_largo(precios_df):
    return precios_df.melt(id_vars=['Dates'], var_name='activo', value_name='valor')


def crear_precios(precios_largo, activos):
    precios = []
    for _, fila in precios_largo.iterrows():
        precios.append(Precio(
            activo=activos[fila['activo']],
            fecha=fila['Dates'],
            precio=Decimal(str(fila['valor'])),
        ))
    Precio.objects.bulk_create(precios)

@transaction.atomic
def cargar_datos(ruta_archivo):
    weights_df, precios_df = leer_excel(ruta_archivo)

    activos = crear_activos(weights_df)
    p1, p2 = crear_portafolios()
    crear_weights(weights_df, activos, p1, p2)

    precios_largo = transformar_precios_a_largo(precios_df)
    crear_precios(precios_largo, activos)