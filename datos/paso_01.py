# Importar las librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt # Para gráficos
# Cargar el archivo CSV en un DataFrame de Pandas
file_path = 'datos/mps-mrp.csv' # Asegúrate que el archivo esté en la misma carpeta
try:
    df_ventas = pd.read_csv(file_path)
    print("Archivo CSV cargado exitosamente.")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta: {file_path}")
    # Detener ejecución si no se encuentra el archivo
    exit()

# --- Visualización Básica del DataFrame ---

# Mostrar las primeras 5 filas para entender la estructura
print("\nPrimeras 5 filas del DataFrame:")
print(df_ventas.head())

# Mostrar las últimas 5 filas
print("\nÚltimas 5 filas del DataFrame:")
print(df_ventas.tail())

# Obtener información general del DataFrame (tipos de datos, valores no nulos)
print("\nInformación general del DataFrame:")
df_ventas.info()

# Obtener estadísticas descriptivas para las columnas numéricas
print("\nEstadísticas descriptivas:")
print(df_ventas.describe())

# Obtener las dimensiones del DataFrame (filas, columnas)
print(f"\nDimensiones del DataFrame: {df_ventas.shape[0]} filas, {df_ventas.shape[1]} columnas")

# --- Selección de Columnas ---

# Seleccionar una sola columna (devuelve una Serie)
print("\nSelección de la columna 'Nombre_Producto':")
nombres_producto = df_ventas['Nombre_Producto']
print(nombres_producto.head())
print(f"Tipo de dato de la selección: {type(nombres_producto)}")

# Seleccionar múltiples columnas (devuelve un DataFrame)
print("\nSelección de las columnas 'Fecha', 'Nombre_Producto', 'Cantidad_Vendida':")
seleccion_multi = df_ventas[['Fecha', 'Nombre_Producto', 'Cantidad_Vendida']]
print(seleccion_multi.head())
print(f"Tipo de dato de la selección: {type(seleccion_multi)}")

# --- Selección de Filas ---

# Selección por índice de etiqueta (.loc) - Selecciona las primeras 3 filas (índices 0, 1, 2)
print("\nSelección de las primeras 3 filas usando .loc:")
print(df_ventas.loc[0:2]) # .loc incluye el final del rango

# Selección por posición entera (.iloc) - Selecciona las primeras 3 filas (posiciones 0, 1, 2)
print("\nSelección de las primeras 3 filas usando .iloc:")
print(df_ventas.iloc[0:3]) # .iloc excluye el final del rango

# Selección de filas basada en condiciones (Boolean Indexing)
# Seleccionar ventas donde la Cantidad_Vendida sea mayor a 100
print("\nSelección de ventas con Cantidad_Vendida > 100:")
ventas_grandes = df_ventas[df_ventas['Cantidad_Vendida'] > 100]
print(ventas_grandes.head())

# Combinar condiciones: Ventas de 'Tornillo Acero' con Cantidad > 80
print("\nSelección de ventas de 'Tornillo Acero' con Cantidad > 80:")
condicion1 = df_ventas['Nombre_Producto'] == 'Tornillo Acero'
condicion2 = df_ventas['Cantidad_Vendida'] > 80
ventas_tornillo_grandes = df_ventas[condicion1 & condicion2] # '&' para AND, '|' para OR
print(ventas_tornillo_grandes.head())

# Seleccionar filas y columnas específicas al mismo tiempo usando .loc
# Filas donde Cliente es 'Industrias ACME', columnas 'Fecha', 'Cliente', 'Cantidad_Vendida'
print("\nSelección de filas y columnas específicas con .loc:")
print(df_ventas.loc[df_ventas['Cliente'] == 'Industrias ACME', ['Fecha', 'Cliente', 'Cantidad_Vendida']])

# --- Cálculos entre Columnas ---

# Calcular el Ingreso Total por Venta (Cantidad * Precio Unitario)
df_ventas['Ingreso_Total'] = df_ventas['Cantidad_Vendida'] * df_ventas['Precio_Unitario']
print("\nDataFrame con la nueva columna 'Ingreso_Total':")
print(df_ventas[['Fecha', 'Nombre_Producto', 'Cantidad_Vendida', 'Precio_Unitario', 'Ingreso_Total']].head())

# --- Cálculos a Nivel de Filas (Ejemplo: aplicar un descuento condicional) ---

# Supongamos un descuento del 10% si el Ingreso_Total > 100
# Usaremos una función lambda con apply (más avanzado, pero útil)
# O un enfoque más simple con .loc para este caso:
descuento_tasa = 0.10
condicion_descuento = df_ventas['Ingreso_Total'] > 100

# Inicializar la columna Descuento en 0
df_ventas['Descuento'] = 0.0

# Aplicar descuento donde la condición es verdadera
df_ventas.loc[condicion_descuento, 'Descuento'] = df_ventas.loc[condicion_descuento, 'Ingreso_Total'] * descuento_tasa

# Calcular el Ingreso Neto
df_ventas['Ingreso_Neto'] = df_ventas['Ingreso_Total'] - df_ventas['Descuento']

print("\nDataFrame con columnas de Descuento e Ingreso Neto:")
print(df_ventas[['Ingreso_Total', 'Descuento', 'Ingreso_Neto']].head())

# Eliminar columnas que ya no necesitamos para simplificar (opcional)
# df_ventas = df_ventas.drop(columns=['Descuento', 'Ingreso_Neto'])

# --- Conversión de Fechas ---

# Convertir la columna 'Fecha' a tipo datetime
# El formato se infiere automáticamente en este caso, pero se puede especificar con 'format='
df_ventas['Fecha'] = pd.to_datetime(df_ventas['Fecha'])
print("\nInformación después de convertir 'Fecha' a datetime:")
df_ventas.info() # Ahora 'Fecha' debería ser datetime64[ns]

# --- Extracción de Componentes de Fecha ---

# Crear nuevas columnas para análisis temporal
df_ventas['Año'] = df_ventas['Fecha'].dt.year
df_ventas['Mes'] = df_ventas['Fecha'].dt.month
df_ventas['Semana_del_Año'] = df_ventas['Fecha'].dt.isocalendar().week # Semana ISO
df_ventas['Dia_Semana'] = df_ventas['Fecha'].dt.dayofweek # Lunes=0, Domingo=6

print("\nDataFrame con columnas de componentes de fecha:")
print(df_ventas[['Fecha', 'Año', 'Mes', 'Semana_del_Año', 'Dia_Semana']].head())

# --- Agrupación por Fechas y Productos ---

# Agrupar por Mes y Nombre_Producto para obtener la Cantidad Vendida total
print("\nCantidad Vendida Total por Mes y Producto:")
ventas_mes_producto = df_ventas.groupby(['Año', 'Mes', 'Nombre_Producto'])['Cantidad_Vendida'].sum()
print(ventas_mes_producto.head(10)) # Muestra las primeras 10 agrupaciones

# Agrupar por Semana del Año y Nombre_Producto
print("\nCantidad Vendida Total por Semana y Producto:")
ventas_semana_producto = df_ventas.groupby(['Año', 'Semana_del_Año', 'Nombre_Producto'])['Cantidad_Vendida'].sum()
print(ventas_semana_producto.head(10))

# --- Agrupación por Períodos Personalizados (Resampling) ---
# 'Resampling' es poderoso para agrupar por frecuencias fijas (días, semanas, meses, etc.)
# Requiere que la columna de fecha sea el índice del DataFrame.

# Establecer 'Fecha' como índice temporalmente para resampling
df_ventas_idx = df_ventas.set_index('Fecha')

# Agrupar por períodos de 2 semanas (frecuencia '2W') y sumar Cantidad_Vendida
# 'W-Mon' significa semanas que terminan en Lunes
print("\nVentas totales agrupadas por períodos de 2 semanas:")
ventas_2semanas = df_ventas_idx.resample('2W-Mon')['Cantidad_Vendida'].sum()
print(ventas_2semanas.head())

# Agrupar por producto y luego por semana
print("\nVentas semanales por producto (usando resample en un grupo):")
# Agrupamos primero por producto, luego aplicamos resample a cada grupo
ventas_semanales_prod_resample = df_ventas_idx.groupby('Nombre_Producto')['Cantidad_Vendida'].resample('W-Mon').sum()
print(ventas_semanales_prod_resample.head(10)) # Muestra ventas semanales de los primeros productos

# Volver al índice numérico por defecto si es necesario
# df_ventas = df_ventas_idx.reset_index()

# --- Gráficos Básicos ---

# Gráfico de línea de las ventas totales diarias
print("\nGenerando gráfico de ventas diarias...")
plt.figure(figsize=(12, 6)) # Tamaño de la figura
ventas_diarias_totales = df_ventas.groupby('Fecha')['Cantidad_Vendida'].sum()
ventas_diarias_totales.plot(kind='line', title='Ventas Diarias Totales')
plt.ylabel('Cantidad Vendida')
plt.xlabel('Fecha')
plt.grid(True) # Añadir rejilla
plt.tight_layout() # Ajustar diseño
plt.show() # Mostrar el gráfico
plt.savefig('ventas_diarias_totales.png') # Guardar gráfico como imagen
print("Gráfico de ventas diarias totales guardado como 'ventas_diarias_totales.png'.")

# Gráfico de barras de ventas totales por producto
print("\nGenerando gráfico de ventas totales por producto...")
plt.figure(figsize=(10, 7))
ventas_por_producto = df_ventas.groupby('Nombre_Producto')['Cantidad_Vendida'].sum().sort_values(ascending=False)
ventas_por_producto.plot(kind='bar', title='Ventas Totales por Producto')
plt.ylabel('Cantidad Total Vendida')
plt.xlabel('Producto')
plt.xticks(rotation=45, ha='right') # Rotar etiquetas del eje X
plt.tight_layout()
plt.show()
plt.savefig('ventas_totales_por_producto.png') # Guardar gráfico como imagen
print("Gráfico de ventas totales por producto guardado como 'ventas_totales_por_producto.png'.")

# Gráfico de línea comparando ventas semanales de los productos principales
print("\nGenerando gráfico de ventas semanales por producto principal...")
producto_principal = ventas_por_producto.index[0] # El más vendido
producto_secundario = ventas_por_producto.index[1]

plt.figure(figsize=(12, 6))
df_ventas_idx[df_ventas_idx['Nombre_Producto'] == producto_principal]['Cantidad_Vendida'].resample('W-Mon').sum().plot(label=producto_principal, legend=True)
df_ventas_idx[df_ventas_idx['Nombre_Producto'] == producto_secundario]['Cantidad_Vendida'].resample('W-Mon').sum().plot(label=producto_secundario, legend=True)
plt.title('Ventas Semanales Comparadas')
plt.ylabel('Cantidad Vendida Semanal')
plt.xlabel('Semana (Inicio Lunes)')
plt.grid(True)
plt.tight_layout()
plt.show()
plt.savefig('ventas_semanales_comparadas.png') # Guardar gráfico como imagen
print("Gráfico de ventas semanales comparadas guardado como 'ventas_semanales_comparadas.png'.")