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