# **Tutorial: Introducción a Pandas y Cálculo de MPS para Ingeniería Industrial**

## **Objetivo:**
Este tutorial te guiará a través de los fundamentos de la librería Pandas en Python, una herramienta esencial para el análisis de datos. Aprenderás a cargar, manipular, analizar y visualizar datos de ventas. Luego, aplicaremos estos conocimientos para calcular el Plan Maestro de Producción (MPS) utilizando las estrategias Nivelada, Perseguidor y Mixta, basándonos en datos históricos de ventas como pronóstico simplificado.

## **Prerrequisitos:**
* Conocimientos básicos de Python (variables, tipos de datos, bucles, condicionales).
* Tener Python instalado en tu sistema.
* Tener la librería Pandas instalada. Si no la tienes, abre tu terminal o command prompt y ejecuta: `pip install pandas matplotlib`
* Tener el archivo `mps-mrp.csv` en el mismo directorio donde ejecutarás tu script de Python o Jupyter Notebook.

---

## **Parte 1: Fundamentos de Pandas**

### **1.1 Introducción a Pandas y Configuración Inicial**

Pandas es una librería de Python que proporciona estructuras de datos de alto rendimiento y fáciles de usar, junto con herramientas de análisis de datos. Es fundamental para cualquier tarea que involucre manipulación y análisis de datos tabulares (como hojas de cálculo o tablas de bases de datos).

* **DataFrame:** La estructura de datos principal en Pandas. Imagínala como una tabla de Excel o una tabla SQL, con filas y columnas etiquetadas.
* **Serie (Series):** Cada columna en un DataFrame es una Serie. Es como un array unidimensional etiquetado.

Empecemos importando la librería. La convención es importarla con el alias `pd`. También importaremos `matplotlib` para gráficos.

```python
# Importar las librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt # Para gráficos

print("Librerías importadas correctamente.")
```

### **1.2 Cargar Datos desde un CSV**

Usaremos `pd.read_csv()` para cargar nuestros datos de ventas en un DataFrame.

```python
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
```

* **Explicación:**
    * `pd.read_csv()` lee el archivo y lo convierte en un DataFrame.
    * `.head()` y `.tail()` nos dan un vistazo rápido de los datos.
    * `.info()` es crucial para ver los tipos de datos de cada columna (Dtype) y si hay valores faltantes (non-null count). Veremos que 'Fecha' es un `object` (texto), ¡necesitaremos convertirla!
    * `.describe()` calcula estadísticas básicas (conteo, media, desviación estándar, mínimo, cuartiles, máximo) para columnas numéricas.
    * `.shape` nos da el tamaño exacto.

**1.3 Selección de Columnas y Filas**

Seleccionar partes específicas de los datos es una tarea común.

```python
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
```

#### * **Explicación:**
    * Usamos corchetes `[]` para seleccionar columnas. Un solo nombre devuelve una `Serie`, una lista de nombres `[['col1', 'col2']]` devuelve un `DataFrame`.
    * `.loc` selecciona por la *etiqueta* de la fila (el índice, que por defecto son números, pero podrían ser fechas u otros identificadores) y nombres de columna.
    * `.iloc` selecciona por la *posición* numérica de la fila y columna (empezando en 0).
    * La **indexación booleana** es muy poderosa: creas una condición (`df['col'] > valor`) que devuelve una Serie de True/False, y al pasarla al DataFrame entre corchetes, se seleccionan solo las filas donde la condición es True.

### **1.4 Cálculos a Nivel de Filas y Columnas**

Podemos crear nuevas columnas basadas en cálculos de otras.

```python
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
```

#### * **Explicación:**
    * Crear una nueva columna es tan simple como asignar el resultado de una operación a `df['Nueva_Columna']`. Pandas realiza la operación fila por fila automáticamente (vectorización).
    * Para cálculos condicionales por fila, `.loc` junto con una condición booleana es muy eficiente para actualizar valores en filas específicas.

### **1.5 Procesamiento de Fechas y Agrupación**

Las fechas son cruciales. Necesitamos convertirlas al tipo de dato correcto y luego podremos agrupar por diferentes períodos.

```python
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
```

#### * **Explicación:**
    * `pd.to_datetime()` convierte texto a objetos de fecha/hora de Pandas.
    * El accesor `.dt` permite extraer componentes como año, mes, semana, día de la semana, etc., de una columna datetime.
    * `.groupby(['col1', 'col2'])` agrupa las filas que tienen los mismos valores en las columnas especificadas.
    * Después de `.groupby()`, especificamos la columna a agregar (`['Cantidad_Vendida']`) y la función de agregación (`.sum()`, `.mean()`, `.count()`, etc.).
    * `resample()` es específico para series temporales. Requiere un índice de fecha/hora (`set_index('Fecha')`). Permite agrupar por frecuencias estándar ('D'ía, 'W'eek, 'M'onth, 'Q'uarter, 'Y'ear) o personalizadas ('2W' = 2 semanas).

### **1.6 Gráficos Básicos**

Pandas se integra con Matplotlib para crear gráficos rápidamente.

```python
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
```

#### * **Explicación:**
    * El método `.plot()` se puede llamar directamente sobre una Serie o DataFrame de Pandas.
    * El argumento `kind=` especifica el tipo de gráfico ('line', 'bar', 'hist', 'box', 'scatter', etc.).
    * Usamos `matplotlib.pyplot` (alias `plt`) para personalizar el gráfico (títulos, etiquetas, tamaño, rejilla) y para mostrarlo (`plt.show()`).

---

## **Parte 2: Cálculo del Plan Maestro de Producción (MPS)**

Ahora aplicaremos lo aprendido para calcular el MPS.

### **2.1 Preparación de Datos para MPS**

Necesitamos una serie temporal de la demanda para un producto específico. Usaremos las ventas semanales agregadas como nuestro pronóstico de demanda.

```python
# --- Parámetros Configurables para MPS ---
PRODUCTO_A_PLANIFICAR = 'Tornillo Acero' # Puedes cambiar esto a 'Válvula Bronce' o 'Junta Silicona'
INVENTARIO_INICIAL = 150 # Unidades iniciales del producto
STOCK_SEGURIDAD = 50   # Unidades mínimas a mantener en inventario
CAPACIDAD_PRODUCCION_SEMANAL = 250 # Máximo a producir por semana

# --- Preparar la Demanda Semanal ---

# Filtrar ventas del producto seleccionado
df_producto = df_ventas[df_ventas['Nombre_Producto'] == PRODUCTO_A_PLANIFICAR].copy()

# Asegurarse que 'Fecha' sea el índice
df_producto = df_producto.set_index('Fecha')

# Agregar ventas por semana (iniciando Lunes)
# Usamos 'W-MON' para definir semanas de Lunes a Domingo
# fill_value=0 asegura que las semanas sin ventas tengan demanda 0
demanda_semanal = df_producto['Cantidad_Vendida'].resample('W-MON').sum().fillna(0).astype(int)

# Convertir el índice (que es el fin de la semana) a período semanal (e.g., número de semana)
# Opcional: podemos trabajar directamente con el índice de fecha
demanda_semanal = demanda_semanal.reset_index()
demanda_semanal.rename(columns={'Fecha': 'Inicio_Semana', 'Cantidad_Vendida': 'Demanda'}, inplace=True)

# Calcular el número de período (semana) para claridad
demanda_semanal['Periodo'] = range(1, len(demanda_semanal) + 1)
demanda_semanal = demanda_semanal[['Periodo', 'Inicio_Semana', 'Demanda']] # Reordenar

print(f"\nDemanda semanal preparada para el producto: {PRODUCTO_A_PLANIFICAR}")
print(demanda_semanal.head())
```

### **2.2 Ejercicio 1: Calcular MPS Perseguidor (Chase)**

#### * **Objetivo:** Producir lo necesario para cumplir la demanda de cada semana, terminando con el stock de seguridad, sin exceder la capacidad.

```python
print("\n--- Calculando MPS Perseguidor (Chase) ---")

# Crear DataFrame para el MPS
mps_chase = demanda_semanal.copy()
mps_chase['Inventario_Inicial'] = 0.0
mps_chase['Plan_Produccion'] = 0.0
mps_chase['Disponible'] = 0.0
mps_chase['Inventario_Final'] = 0.0

# Inicializar el inventario para el primer período
inv_anterior = INVENTARIO_INICIAL

# Iterar fila por fila (período por período) para calcular el MPS
# Esta es la forma más didáctica para entender la dependencia entre períodos
for index, row in mps_chase.iterrows():
    periodo = row['Periodo']
    demanda_periodo = row['Demanda']

    # 1. Inventario Inicial del período actual
    inv_inicial_periodo = inv_anterior
    mps_chase.loc[index, 'Inventario_Inicial'] = inv_inicial_periodo

    # 2. Calcular producción necesaria para alcanzar el stock de seguridad
    # Necesitamos producir lo suficiente para cubrir demanda Y terminar con Stock Seguridad,
    # considerando lo que ya tenemos.
    produccion_necesaria = max(0, demanda_periodo + STOCK_SEGURIDAD - inv_inicial_periodo)

    # 3. Aplicar Restricción de Capacidad
    plan_produccion_periodo = min(CAPACIDAD_PRODUCCION_SEMANAL, produccion_necesaria)
    mps_chase.loc[index, 'Plan_Produccion'] = plan_produccion_periodo

    # 4. Calcular Disponible
    disponible_periodo = inv_inicial_periodo + plan_produccion_periodo
    mps_chase.loc[index, 'Disponible'] = disponible_periodo

    # 5. Calcular Inventario Final
    inv_final_periodo = disponible_periodo - demanda_periodo
    # Asegurarnos que no sea negativo (aunque la lógica anterior debería prevenirlo
    # si la capacidad es suficiente)
    inv_final_periodo = max(0, inv_final_periodo)
    mps_chase.loc[index, 'Inventario_Final'] = inv_final_periodo

    # 6. Verificar si se cubrió la demanda + SS (si no, es por capacidad)
    if inv_final_periodo < STOCK_SEGURIDAD and produccion_necesaria > plan_produccion_periodo:
         print(f"  *Alerta Periodo {periodo}: Capacidad insuficiente. "
               f"Se necesitaban {produccion_necesaria:.0f}, se produjeron {plan_produccion_periodo:.0f}. "
               f"Inv Final: {inv_final_periodo:.0f}")
    elif inv_final_periodo < 0: # Doble chequeo por si acaso
         print(f"  *ERROR Periodo {periodo}: Inventario Final Negativo ({inv_final_periodo:.0f}) - Revisar lógica.")


    # 7. Preparar para el siguiente período
    inv_anterior = inv_final_periodo

# Mostrar resultados
print("\nResultados MPS Perseguidor:")
print(mps_chase[['Periodo', 'Inventario_Inicial', 'Demanda', 'Plan_Produccion', 'Inventario_Final']].round(0).head(15)) # Mostrar primeras 15 semanas

# Graficar resultados MPS Chase
plt.figure(figsize=(14, 7))
plt.plot(mps_chase['Periodo'], mps_chase['Demanda'], label='Demanda', color='blue', marker='o', linestyle='--')
plt.plot(mps_chase['Periodo'], mps_chase['Plan_Produccion'], label='Plan Producción Chase', color='red', marker='x')
plt.plot(mps_chase['Periodo'], mps_chase['Inventario_Final'], label='Inventario Final', color='green', marker='s')
plt.axhline(STOCK_SEGURIDAD, color='gray', linestyle=':', label=f'Stock Seguridad ({STOCK_SEGURIDAD})')
plt.axhline(CAPACIDAD_PRODUCCION_SEMANAL, color='orange', linestyle=':', label=f'Capacidad ({CAPACIDAD_PRODUCCION_SEMANAL})')
plt.title(f'MPS Perseguidor - {PRODUCTO_A_PLANIFICAR}')
plt.xlabel('Período (Semana)')
plt.ylabel('Unidades')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
```

### **2.3 Ejercicio 2: Calcular MPS Nivelado (Level)**

#### * **Objetivo:** Producir una cantidad constante cada semana, usando el inventario para absorber variaciones de demanda.

```python
print("\n--- Calculando MPS Nivelado (Level) ---")

# 1. Calcular la producción nivelada semanal necesaria
total_demanda = demanda_semanal['Demanda'].sum()
num_periodos = len(demanda_semanal)
# Objetivo: terminar con el stock de seguridad al final del horizonte
produccion_nivelada_requerida = (total_demanda + STOCK_SEGURIDAD - INVENTARIO_INICIAL) / num_periodos

# Asegurarse que la producción no sea negativa
produccion_nivelada_requerida = max(0, produccion_nivelada_requerida)

# 2. Aplicar restricción de capacidad
plan_produccion_nivelado = min(CAPACIDAD_PRODUCCION_SEMANAL, produccion_nivelada_requerida)

print(f"Demanda Total: {total_demanda}, Períodos: {num_periodos}")
print(f"Producción Nivelada Requerida (teórica): {produccion_nivelada_requerida:.2f} unidades/semana")
if plan_produccion_nivelado < produccion_nivelada_requerida:
    print(f"*Alerta: La capacidad ({CAPACIDAD_PRODUCCION_SEMANAL}) es menor a la producción nivelada requerida.")
    print(f"  Se usará el plan nivelado limitado por capacidad: {plan_produccion_nivelado:.0f} unidades/semana")
else:
    print(f"Plan de Producción Nivelado: {plan_produccion_nivelado:.0f} unidades/semana (Redondeado o exacto)")
    # Podríamos redondear hacia arriba si preferimos, pero mantengámoslo simple
    plan_produccion_nivelado = round(plan_produccion_nivelado) # Redondear al entero más cercano

# Crear DataFrame para el MPS Nivelado
mps_level = demanda_semanal.copy()
mps_level['Inventario_Inicial'] = 0.0
mps_level['Plan_Produccion'] = plan_produccion_nivelado # Es constante
mps_level['Disponible'] = 0.0
mps_level['Inventario_Final'] = 0.0

# Inicializar inventario
inv_anterior = INVENTARIO_INICIAL

# Calcular iterativamente
for index, row in mps_level.iterrows():
    periodo = row['Periodo']
    demanda_periodo = row['Demanda']

    inv_inicial_periodo = inv_anterior
    mps_level.loc[index, 'Inventario_Inicial'] = inv_inicial_periodo

    # El plan de producción es constante
    plan_prod = mps_level.loc[index, 'Plan_Produccion']

    disponible_periodo = inv_inicial_periodo + plan_prod
    mps_level.loc[index, 'Disponible'] = disponible_periodo

    inv_final_periodo = disponible_periodo - demanda_periodo

    # ¡CRÍTICO! Verificar stockouts o inventario negativo
    if inv_final_periodo < 0:
        print(f"  *ERROR Periodo {periodo}: ¡Inventario Final Negativo! ({inv_final_periodo:.0f}). "
              f"El plan nivelado no es suficiente.")
        # En un caso real, aquí se detendría o ajustaría. Para el ejemplo, lo dejamos negativo.
        # Opcionalmente, podríamos forzarlo a 0 y registrar la demanda insatisfecha.
        # inv_final_periodo = 0 # Forzar a cero si no se permiten negativos
    elif inv_final_periodo < STOCK_SEGURIDAD:
         print(f"  *Alerta Periodo {periodo}: Inventario Final ({inv_final_periodo:.0f}) "
               f"por debajo del Stock de Seguridad ({STOCK_SEGURIDAD}).")


    mps_level.loc[index, 'Inventario_Final'] = inv_final_periodo
    inv_anterior = inv_final_periodo

# Mostrar resultados
print("\nResultados MPS Nivelado:")
print(mps_level[['Periodo', 'Inventario_Inicial', 'Demanda', 'Plan_Produccion', 'Inventario_Final']].round(0).head(15))

# Graficar resultados MPS Level
plt.figure(figsize=(14, 7))
plt.plot(mps_level['Periodo'], mps_level['Demanda'], label='Demanda', color='blue', marker='o', linestyle='--')
plt.plot(mps_level['Periodo'], mps_level['Plan_Produccion'], label='Plan Producción Nivelado', color='purple', marker='^')
plt.plot(mps_level['Periodo'], mps_level['Inventario_Final'], label='Inventario Final', color='green', marker='s')
plt.axhline(STOCK_SEGURIDAD, color='gray', linestyle=':', label=f'Stock Seguridad ({STOCK_SEGURIDAD})')
plt.axhline(0, color='black', linestyle='-', linewidth=0.5) # Línea cero para ver negativos
#plt.axhline(CAPACIDAD_PRODUCCION_SEMANAL, color='orange', linestyle=':', label=f'Capacidad ({CAPACIDAD_PRODUCCION_SEMANAL})') # Ya aplicado
plt.title(f'MPS Nivelado - {PRODUCTO_A_PLANIFICAR}')
plt.xlabel('Período (Semana)')
plt.ylabel('Unidades')
plt.ylim(bottom=min(0, mps_level['Inventario_Final'].min() - 50)) # Ajustar eje Y si hay negativos
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
```

### **2.4 Ejercicio 3: Calcular MPS Mixto (Mixed)**

* **Objetivo:** Combinar estrategias. Por ejemplo, usar Nivelado cuando la demanda se acerca a la capacidad y Perseguidor el resto del tiempo.
* **Definición de la Estrategia Mixta:** Para este ejemplo, definiremos una regla simple: si la producción *requerida* por la estrategia Perseguidor (antes de aplicar capacidad) supera un umbral (ej. 80% de la capacidad), usaremos una producción Nivelada (limitada por capacidad); de lo contrario, usaremos Perseguidor.

```python
print("\n--- Calculando MPS Mixto ---")

# Umbral para decidir cuándo nivelar (ej. 80% de la capacidad)
UMBRAL_CAPACIDAD_NIVELAR = CAPACIDAD_PRODUCCION_SEMANAL * 0.80
# Producción a usar cuando se decide nivelar (podría ser la capacidad máxima)
PRODUCCION_CUANDO_NIVELADO = CAPACIDAD_PRODUCCION_SEMANAL

print(f"Estrategia Mixta: Usar Nivelado ({PRODUCCION_CUANDO_NIVELADO} unidades) si Chase requiere > {UMBRAL_CAPACIDAD_NIVELAR}, sino usar Chase.")

# Crear DataFrame para el MPS Mixto
mps_mixed = demanda_semanal.copy()
mps_mixed['Inventario_Inicial'] = 0.0
mps_mixed['Plan_Produccion'] = 0.0
mps_mixed['Disponible'] = 0.0
mps_mixed['Inventario_Final'] = 0.0
mps_mixed['Estrategia_Usada'] = '' # Para ver qué se decidió

# Inicializar inventario
inv_anterior = INVENTARIO_INICIAL

# Calcular iterativamente
for index, row in mps_mixed.iterrows():
    periodo = row['Periodo']
    demanda_periodo = row['Demanda']

    inv_inicial_periodo = inv_anterior
    mps_mixed.loc[index, 'Inventario_Inicial'] = inv_inicial_periodo

    # Calcular requerimiento según Chase (antes de capacidad)
    produccion_necesaria_chase = max(0, demanda_periodo + STOCK_SEGURIDAD - inv_inicial_periodo)

    # Decidir la estrategia
    if produccion_necesaria_chase > UMBRAL_CAPACIDAD_NIVELAR:
        # Usar estrategia Nivelada (limitada por capacidad)
        plan_produccion_periodo = min(CAPACIDAD_PRODUCCION_SEMANAL, PRODUCCION_CUANDO_NIVELADO)
        estrategia = 'Nivelado'
    else:
        # Usar estrategia Chase (limitada por capacidad)
        plan_produccion_periodo = min(CAPACIDAD_PRODUCCION_SEMANAL, produccion_necesaria_chase)
        estrategia = 'Perseguidor'

    mps_mixed.loc[index, 'Plan_Produccion'] = plan_produccion_periodo
    mps_mixed.loc[index, 'Estrategia_Usada'] = estrategia

    disponible_periodo = inv_inicial_periodo + plan_produccion_periodo
    mps_mixed.loc[index, 'Disponible'] = disponible_periodo

    inv_final_periodo = disponible_periodo - demanda_periodo
    inv_final_periodo = max(0, inv_final_periodo) # Asegurar no negativos

    mps_mixed.loc[index, 'Inventario_Final'] = inv_final_periodo

     # Chequeos opcionales de alertas
    if inv_final_periodo < STOCK_SEGURIDAD:
         # Verificar si fue por capacidad insuficiente en modo Chase
         fue_por_capacidad_chase = (estrategia == 'Perseguidor' and produccion_necesaria_chase > plan_produccion_periodo)
         # Verificar si fue porque el modo Nivelado no fue suficiente
         fue_por_nivelado_insuficiente = (estrategia == 'Nivelado' and inv_final_periodo < STOCK_SEGURIDAD)

         if fue_por_capacidad_chase:
             print(f"  *Alerta Mixta {periodo}: Capacidad ({CAPACIDAD_PRODUCCION_SEMANAL}) insuficiente en modo Chase. "
                   f"Inv Final: {inv_final_periodo:.0f}")
         elif fue_por_nivelado_insuficiente:
              print(f"  *Alerta Mixta {periodo}: Inv Final ({inv_final_periodo:.0f}) bajo SS en modo Nivelado.")
         # Podría haber otros casos donde simplemente la demanda fue alta inesperadamente

    inv_anterior = inv_final_periodo

# Mostrar resultados
print("\nResultados MPS Mixto:")
print(mps_mixed[['Periodo', 'Inventario_Inicial', 'Demanda', 'Plan_Produccion', 'Estrategia_Usada', 'Inventario_Final']].round(0).head(15))

# Graficar resultados MPS Mixed
plt.figure(figsize=(14, 7))
plt.plot(mps_mixed['Periodo'], mps_mixed['Demanda'], label='Demanda', color='blue', marker='o', linestyle='--')
# Colorear Plan Producción según estrategia usada
for idx, row in mps_mixed.iterrows():
    color = 'magenta' if row['Estrategia_Usada'] == 'Nivelado' else 'cyan'
    plt.bar(row['Periodo'], row['Plan_Produccion'], color=color, alpha=0.7, label=f"{row['Estrategia_Usada']}" if idx == 0 or mps_mixed.loc[idx-1, 'Estrategia_Usada'] != row['Estrategia_Usada'] else "") # Evitar labels repetidos

plt.plot(mps_mixed['Periodo'], mps_mixed['Inventario_Final'], label='Inventario Final', color='green', marker='s')
plt.axhline(STOCK_SEGURIDAD, color='gray', linestyle=':', label=f'Stock Seguridad ({STOCK_SEGURIDAD})')
plt.axhline(CAPACIDAD_PRODUCCION_SEMANAL, color='orange', linestyle=':', label=f'Capacidad ({CAPACIDAD_PRODUCCION_SEMANAL})')
plt.title(f'MPS Mixto - {PRODUCTO_A_PLANIFICAR}')
plt.xlabel('Período (Semana)')
plt.ylabel('Unidades')
# Crear handles para leyenda de barras manualmente
import matplotlib.patches as mpatches
handles, labels = plt.gca().get_legend_handles_labels()
patch_nivelado = mpatches.Patch(color='magenta', alpha=0.7, label='Plan Prod (Nivelado)')
patch_chase = mpatches.Patch(color='cyan', alpha=0.7, label='Plan Prod (Perseguidor)')
# Evitar duplicados y añadir parches
unique_labels = {}
new_handles = []
for h, l in zip(handles, labels):
    if l not in unique_labels and 'Nivelado' not in l and 'Perseguidor' not in l:
        unique_labels[l] = h
        new_handles.append(h)
new_handles.extend([patch_nivelado, patch_chase])

plt.legend(handles=new_handles)
plt.grid(True)
plt.tight_layout()
plt.show()
```

---

## **Parte 3: Conclusión y Próximos Pasos**

¡Felicidades! Has completado este tutorial introductorio a Pandas y su aplicación en el cálculo del MPS.

#### **Hemos cubierto:**

* Carga y exploración de datos con Pandas.
* Selección y manipulación de filas y columnas.
* Cálculos básicos y creación de nuevas columnas.
* Manejo de fechas y agrupación temporal (incluyendo `resample`).
* Creación de gráficos básicos para visualización.
* Implementación paso a paso de las estrategias MPS: Perseguidor, Nivelado y Mixta, considerando inventario inicial, stock de seguridad y capacidad.

#### **Próximos Pasos:**

* **Experimenta:** Cambia los parámetros (`INVENTARIO_INICIAL`, `STOCK_SEGURIDAD`, `CAPACIDAD_PRODUCCION_SEMANAL`), elige otro producto (`PRODUCTO_A_PLANIFICAR`) y observa cómo cambian los resultados del MPS.
* **Mejora el Pronóstico:** Investiga métodos de pronóstico más avanzados que usar simplemente las ventas históricas (medias móviles, suavización exponencial, ARIMA - aunque esto requiere más conocimiento estadístico y librerías como `statsmodels`).
* **MRP:** El siguiente paso lógico es tomar la columna `Plan_Produccion` del MPS como entrada para calcular los requerimientos de materiales (MRP), usando una lista de materiales (BOM).
* **Optimización:** Explora cómo podrías usar Python para encontrar el *mejor* plan de producción considerando costos (costo de inventario, costo de producción, costo de faltantes, costo de cambiar nivel de producción).
* **Profundiza en Pandas:** Hay mucho más que aprender: manejo de datos faltantes (`.fillna()`, `.dropna()`), unión de DataFrames (`pd.merge`, `pd.concat`), funciones más avanzadas (`.apply()`, `.pivot_table()`).

Esperamos que este tutorial te haya proporcionado una base sólida para usar Python y Pandas en tus futuros análisis y proyectos de Ingeniería Industrial.
