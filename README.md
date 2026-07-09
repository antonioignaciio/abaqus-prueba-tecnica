# Abaqus — Prueba Técnica Python/Django

Proyecto que modela un portafolio de inversión compuesto por 17 activos, distribuidos en 2 portafolios, y expone su evolución en el tiempo (valor total y weights por activo) a través de una API REST y una vista con gráficos.

## Stack

- Python 3.11
- Django + Django REST Framework
- pandas + openpyxl (ETL)
- SQLite (desarrollo)
- Chart.js (gráficos, vía CDN)

## Instalación

```bash
# 1. Clonar el repo y entrar a la carpeta
cd abaqus

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate
```

## Carga de datos

El proyecto incluye dos management commands para poblar la base de datos a partir de `datos.xlsx`:

```bash
# 1. Carga activos, portafolios, weights (t=0) y precios históricos
python manage.py cargar_datos datos.xlsx

# 2. Calcula las cantidades iniciales (C_i0) a partir de los weights y precios de t=0
python manage.py calcular_cantidades
```

El ETL es idempotente: correr `cargar_datos` varias veces sobre una base ya poblada no genera duplicados (activos y portafolios se buscan por nombre antes de crearse, y weights/precios usan restricciones de unicidad en la base de datos).

Si necesitas recargar los datos desde cero de todas formas:

```bash
rm db.sqlite3
python manage.py migrate
python manage.py cargar_datos datos.xlsx
python manage.py calcular_cantidades
```

## Levantar el servidor

```bash
python manage.py runserver
```

## Endpoints

### API REST

```
GET /api/portafolios/<id>/evolucion/?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD
```

Devuelve, para cada fecha del rango, el valor total del portafolio ($V_t$) y el weight de cada activo ($w_{i,t}$).

Ejemplo:
```
GET /api/portafolios/1/evolucion/?fecha_inicio=2022-02-15&fecha_fin=2022-03-15
```

### Vista con gráficos

```
GET /portafolios/<id>/
```

Página HTML que consume la API anterior y muestra:
- Un gráfico de línea para $V_t$ (valor total del portafolio)
- Un gráfico de área apilada ("stacked area") para $w_{i,t}$ (weight por activo)

Ejemplo: `http://127.0.0.1:8000/portafolios/1/`

## Modelo de datos

- **Activo**: cada uno de los 17 instrumentos invertibles.
- **Portafolio**: portafolio 1 y portafolio 2, cada uno con su valor inicial ($V_0$).
- **Precio**: precio histórico de cada activo por fecha (367 fechas × 17 activos). Único por `(activo, fecha)`.
- **Weight**: peso inicial ($w_{i,0}$) de cada activo en cada portafolio, a la fecha 15/02/2022. Único por `(portafolio, activo)`.
- **Cantidad**: cantidad fija de unidades ($C_{i,0}$) de cada activo en cada portafolio, calculada a partir de los weights y precios iniciales, y que permanece invariante en el tiempo. Única por `(portafolio, activo)`.

## Notas y pendientes

- El proyecto cumple los 5 puntos solicitados en el enunciado (modelado, ETL, cálculo de cantidades iniciales, API REST con ORM, y vista con gráficos).
- No se alcanzó a completar la reestructuración según la guía de estilos de [HackSoft](https://github.com/HackSoftware/Django-Styleguide) (bonus), aunque se identificaron los cambios puntuales necesarios (separación de `services.py`/`selectors.py`, serializers de entrada/salida, adelgazamiento de views).
- Pendiente conocido: tests automatizados.
-Se usó IA para mejorar el diseño de evolucion.html