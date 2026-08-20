import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Cargar variables de entorno (.env en la raíz del proyecto)
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Crear motor de base de datos SQLAlchemy
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 2. EXTRAER: Cargar el archivo Excel
archivo_excel = "PNRao_PNRaoChoco_Retail_Sales_Data.xlsx"
ruta_excel = os.path.join(os.path.dirname(__file__), "..", archivo_excel)

print("--- 1. EXTRAER: Cargando datos brutos de ventas retail ---")
df_raw = pd.read_excel(ruta_excel, sheet_name="Retail_Sales_Data")
print(f"Registros iniciales: {len(df_raw)}")

# 3. TRANSFORMAR: Limpieza y Normalización
print("\n--- 2. TRANSFORMAR: Aplicando reglas de limpieza ---")

# A. Eliminar filas duplicadas exactas
df_clean = df_raw.drop_duplicates().copy()

# B. Limpiar espacios en blanco en columnas de texto (String Stripping)
string_columns = df_clean.select_dtypes(include='object').columns
for col in string_columns:
    df_clean[col] = df_clean[col].astype(str).str.strip()
    df_clean[col] = df_clean[col].replace({'nan': None, 'None': None, '': None})

# C. Normalizar nombres de columnas a minúsculas
df_clean.columns = [col.lower() for col in df_clean.columns]

# D. Estandarización de Fechas (OrderDate)
df_clean['orderdate'] = pd.to_datetime(df_clean['orderdate'], errors='coerce')

# E. Manejo de Tipos Numéricos y Recálculo de Ingresos (TotalRevenue)
df_clean['unitssold'] = pd.to_numeric(df_clean['unitssold'], errors='coerce')
df_clean['priceperunit'] = pd.to_numeric(df_clean['priceperunit'], errors='coerce')

# Recalcular totalrevenue para garantizar consistencia matemática
df_clean['totalrevenue'] = df_clean['unitssold'] * df_clean['priceperunit']

# F. Filtrar registros inválidos sin llaves primarias esenciales
df_clean = df_clean.dropna(subset=['orderid', 'customerid'])

print(f"Registros limpios procesados: {len(df_clean)}")
print("\nMuestra de datos transformados:")
print(df_clean[['orderid', 'orderdate', 'customerid', 'productid', 'totalrevenue', 'region']].head())

# 4. CARGAR: Persistencia en PostgreSQL
print("\n--- 3. CARGAR: Insertando en PostgreSQL ---")
try:
    df_clean.to_sql(
        "ventas_retail_procesadas", 
        engine, 
        schema="public", 
        if_exists="replace", 
        index=False,
        method="multi"
    )
    print("¡ÉXITO! Tabla 'ventas_retail_procesadas' cargada exitosamente en PostgreSQL.")
except Exception as e:
    print(f"Error al guardar en la base de datos: {e}")