# olap_practica.py
import pandas as pd

# Cargar datos
df = pd.read_csv('ventas.csv', parse_dates=['Fecha'])
df['Mes'] = df['Fecha'].dt.month
df['Año'] = df['Fecha'].dt.year

# Mostrar datos base
print("=== Datos originales ===")
print(df)

# Crear cubo: Producto x Región x Mes
print("\n=== Cubo OLAP: Producto x Región x Mes ===")
cubo = pd.pivot_table(df, values='Ventas', index=['Producto'], columns=['Región', 'Mes'], aggfunc='sum', fill_value=0)
print(cubo)

# Slice: Producto A
print("\n=== Slice: Ventas del Producto A ===")
slice_A = df[df['Producto'] == 'A']
print(slice_A)

# Dice: Productos A y B en Región Centro
print("\n=== Dice: Productos A y B en Región Centro ===")
dice = df[(df['Producto'].isin(['A', 'B'])) & (df['Región'] == 'Centro')]
print(dice)

# Roll-up: Ventas por Año y Producto
print("\n=== Roll-up: Ventas por Año y Producto ===")
rollup = df.groupby(['Año', 'Producto'])['Ventas'].sum().reset_index()
print(rollup)

# Drill-down: Ventas por Año, Mes y Producto
print("\n=== Drill-down: Ventas por Año, Mes y Producto ===")
drill = df.groupby(['Año', 'Mes', 'Producto'])['Ventas'].sum().reset_index()
print(drill)

# Pivot: Región vs Producto
print("\n=== Pivot: Ventas por Región y Producto ===")
pivot = df.pivot_table(values='Ventas', index='Región', columns='Producto', aggfunc='sum', fill_value=0)
print(pivot)

# Exportar a Excel para Power BI
output_file = 'cubo_para_powerbi.xlsx'
pivot.to_excel(output_file)
print(f"\nArchivo exportado a Excel: {output_file}")
