import pandas as pd
import os
from sqlalchemy import create_engine

# 1. Configuración de parámetros de conexión a PostgreSQL
DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASS", "TU_CONTRASEÑA_AQUI")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"

# 2. Crear el motor de conexión mediante SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# 3. Datos de prueba (Simulación de un extracto de archivo Excel/CSV)
datos_clientes = {
    "cliente_id": [101, 102, 103, 104],
    "nombre": ["Carlos Gómez", "Ana Martínez", "Luis Rodríguez", "Diana López"],
    "servicio": ["Microsoft 365", "Google Workspace", "Soporte N2", "Pipeline ETL"],
    "monto_usd": [150.0, 200.0, 350.0, 500.0],
}

# Cargar los datos en un DataFrame de Pandas
df = pd.DataFrame(datos_clientes)

print("--- DATOS A INSERTAR EN POSTGRESQL ---")
print(df)

try:
    # 4. Inserción automática de la tabla en PostgreSQL
    df.to_sql("clientes_freelance", engine, if_exists="replace", index=False)
    print("\n¡ÉXITO! La tabla 'clientes_freelance' ha sido creada e insertada en PostgreSQL.")

    # 5. Consulta de verificación ejecutada directamente desde Python
    df_resultado = pd.read_sql("SELECT * FROM clientes_freelance WHERE monto_usd > 200", engine)
    print("\n--- CONSULTA FILTRADA DESDE LA BASE DE DATOS (Monto > $200 USD) ---")
    print(df_resultado)

except Exception as e:
    print(f"\nERROR al conectar o ejecutar la consulta: {e}")
    