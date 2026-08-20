import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Cargar variables de entorno
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Crear motor de base de datos
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 2. Extracción de datos
logs_tenant_brutos = {
    "user_principal_name": ["j.perez@empresa.com ", "m.lopez@empresa.com", "c.gomez@empresa.com", "a.silva@empresa.com "],
    "displayName": ["Juan Perez", "Maria Lopez", "Carlos Gomez", "Ana Silva"],
    "assignedLicenses": ["SPE_E5", "SPE_E3", "SPE_E5", "SPE_E3"],
    "accountEnabled": [True, True, False, False],
    "lastSignInDateTime": ["2026-08-10", "2026-08-18", "2025-12-01", "2025-11-15"]
}

df_logs = pd.DataFrame(logs_tenant_brutos)

# 3. Transformación
df_logs["user_principal_name"] = df_logs["user_principal_name"].str.strip().str.lower()
df_logs["lastSignInDateTime"] = pd.to_datetime(df_logs["lastSignInDateTime"])

# Regla de negocio
df_logs["alerta_licencia_inactiva"] = (~df_logs["accountEnabled"]) & (df_logs["assignedLicenses"].notna())

# Convertir tipos complejos a tipos SQL estándar para evitar fallos de encoding en el driver
df_logs["accountEnabled"] = df_logs["accountEnabled"].astype(bool)
df_logs["alerta_licencia_inactiva"] = df_logs["alerta_licencia_inactiva"].astype(bool)

print("--- DATOS LISTOS PARA CARGAR ---")
print(df_logs)

# 4. Carga usando método executemany (evita errores de codificación en lotes)
try:
    df_logs.to_sql(
        "audit_licencias_m365", 
        engine, 
        schema="public", 
        if_exists="replace", 
        index=False,
        method="multi"
    )
    print("\n¡ÉXITO! Log de auditoría M365/Workspace cargado en 'public.audit_licencias_m365'.")
except Exception as e:
    print(f"\nError al guardar en base de datos: {e}")