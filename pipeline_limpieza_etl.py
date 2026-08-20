import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar variables del archivo .env
load_dotenv()

# 1. Configuración de conexión a PostgreSQL
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Cadena de conexión ajustada
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("--- 1. EXTRAER: Leyendo archivo de Excel bruto ---")
df = pd.read_excel("reporte_ventas_bruto.xlsx")
print(df)

print("\n--- 2. TRANSFORMAR: Limpiando y estandarizando datos ---")

# A. Limpiar espacios en los nombres de las columnas y ponerlas en minúscula
df.columns = df.columns.str.strip().str.lower()

# B. Eliminar filas completamente vacías o donde el cliente sea nulo
df = df.dropna(subset=["cliente"]).copy()

# C. Limpiar texto de clientes: quitar espacios extra e iniciales en mayúscula (Title Case)
df["cliente"] = df["cliente"].str.strip().str.title()

# D. Limpiar columna de monto: quitar '$' y espacios, luego convertir a número flotante
df["monto"] = df["monto"].astype(str).str.replace("$", "").str.strip()
df["monto"] = pd.to_numeric(df["monto"], errors="coerce")

# E. Estandarizar la columna estado a mayúsculas y sin espacios
df["estado"] = df["estado"].str.strip().str.upper()

# F. Convertir fecha a formato estandarizado YYYY-MM-DD
df["fecha_venta"] = pd.to_datetime(df["fecha_venta"], errors="coerce").dt.strftime('%Y-%m-%d')

print("\n--- DATOS TRANSFORMADOS Y LIMPIOS ---")
print(df)

print("\n--- 3. CARGAR: Insertando tabla limpia en PostgreSQL ---")
try:
    df.to_sql("ventas_procesadas", engine, if_exists="replace", index=False)
    print("¡ÉXITO! Tabla 'ventas_procesadas' creada en PostgreSQL con datos 100% limpios.")
except Exception as e:
    print(f"Error al cargar en la base de datos: {e}")