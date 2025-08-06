# generador_datos.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Parámetros
num_registros = 5000
productos = ['A', 'B', 'C', 'D']
regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime(2024, 12, 31)

# Función para generar una fecha aleatoria entre dos fechas
def fecha_aleatoria(inicio, fin):
    delta = fin - inicio
    return inicio + timedelta(days=random.randint(0, delta.days))

# Función para generar ventas con estacionalidad
def generar_ventas(fecha, producto, region):
    mes = fecha.month

    # Base de ventas aleatoria
    base = random.randint(100, 300)

    # Aumentos por estacionalidad
    if mes in [3, 4]:  # primavera
        base *= 1.2
    elif mes in [11, 12]:  # fin de año
        base *= 1.5
    elif mes in [6, 9]:  # ventas bajas
        base *= 0.8

    # Ajustes por producto
    if producto == 'A':
        base *= 1.1
    elif producto == 'C':
        base *= 0.95

    # Ajustes por región
    if region == 'Centro':
        base *= 1.3
    elif region == 'Sur':
        base *= 0.9

    return int(base)

# Generar registros
data = []
for _ in range(num_registros):
    fecha = fecha_aleatoria(fecha_inicio, fecha_fin)
    producto = random.choice(productos)
    region = random.choice(regiones)
    ventas = generar_ventas(fecha, producto, region)

    data.append([fecha, producto, region, ventas])

# Crear DataFrame
df = pd.DataFrame(data, columns=['Fecha', 'Producto', 'Región', 'Ventas'])

# Guardar CSV
df.to_csv('ventas.csv', index=False, encoding='utf-8')
print("Archivo 'ventas.csv' generado con estacionalidad.")