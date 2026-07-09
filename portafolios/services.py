from collections import defaultdict
from datetime import date
from decimal import Decimal
from portafolios.models import Weight, Precio, Cantidad

FECHA_INICIAL = date(2022, 2, 15)

def obtener_precio_inicial(activo):
    return Precio.objects.get(activo=activo, fecha=FECHA_INICIAL)


def calcular_cantidad_inicial(weight, precio_inicial):
    return (weight.valor * weight.portafolio.valor_inicial) / precio_inicial.precio


def construir_cantidad(weight, valor_cantidad):
    return Cantidad(
        portafolio=weight.portafolio,
        activo=weight.activo,
        valor=valor_cantidad,
    )

def calcular_cantidades_iniciales():
    cantidades = []

    for weight in Weight.objects.select_related('activo', 'portafolio'):
        precio_inicial = obtener_precio_inicial(weight.activo)
        valor_cantidad = calcular_cantidad_inicial(weight, precio_inicial)
        cantidades.append(construir_cantidad(weight, valor_cantidad))

    Cantidad.objects.bulk_create(cantidades)

##################################################################################

def obtener_cantidades_fijas_portafolio(portafolio):
    return {
        c.activo_id: c.valor
        for c in Cantidad.objects.filter(portafolio=portafolio)
    }

def obtener_precios_rango(fecha_inicio, fecha_fin):
    return Precio.objects.filter(
        fecha__gte=fecha_inicio,
        fecha__lte=fecha_fin,
    ).select_related('activo')


def agrupar_precios_por_fecha(precios):
    precios_por_fecha = defaultdict(list)
    for precio in precios:
        precios_por_fecha[precio.fecha].append(precio)
    return precios_por_fecha


def calcular_montos_del_dia(precios_del_dia, cantidades):
    montos = {}
    for precio in precios_del_dia:
        cantidad = cantidades[precio.activo_id]
        montos[precio.activo_id] = precio.precio * cantidad
    return montos


def calcular_weights_del_dia(montos, valor_total):
    return {
        activo_id: monto / valor_total
        for activo_id, monto in montos.items()
    }


def calcular_evolucion(portafolio, fecha_inicio, fecha_fin):
    cantidades = obtener_cantidades_fijas_portafolio(portafolio)
    precios = obtener_precios_rango(fecha_inicio, fecha_fin)
    precios_por_fecha = agrupar_precios_por_fecha(precios)

    resultado = []
    for fecha in sorted(precios_por_fecha.keys()):
        montos = calcular_montos_del_dia(precios_por_fecha[fecha], cantidades)
        valor_total = sum(montos.values())  # V_t
        weights = calcular_weights_del_dia(montos, valor_total)

        resultado.append({
            "fecha": fecha,
            "valor_total": valor_total,
            "weights": weights,
        })

    return resultado