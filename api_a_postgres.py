import requests
import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine

# 1. Configuración de conexión a PostgreSQL
DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASS", "TU_CONTRASEÑA_AQUI")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("--- 1. EXTRAER: Consultando API web de divisas en tiempo real ---")
API_URL = "https://open.er-api.com/v6/latest/USD"

try:
    respuesta = requests.get(API_URL)
    datos_json = respuesta.json()

    if datos_json["result"] == "success":
        print("¡Conexión exitosa con la API!")
        
        # 2. TRANSFORMAR: Extraer monedas de interés y estructurar
        tasas = datos_json["rates"]
        monedas_interes = ["COP", "EUR", "MXN", "BRL", "GBP"]
        
        datos_filtrados = []
        fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for moneda in monedas_interes:
            if moneda in tasas:
                datos_filtrados.append({
                    "moneda_base": "USD",
                    "moneda_destino": moneda,
                    "tasa_cambio": tasas[moneda],
                    "fecha_actualizacion": fecha_consulta
                })

        # Convertir a DataFrame de Pandas
        df_divisas = pd.DataFrame(datos_filtrados)
        print("\n--- DATOS OBTENIDOS DE LA API ---")
        print(df_divisas)

        # 3. CARGAR: Guardar en la base de datos
        df_divisas.to_sql("tasas_cambio_historico", engine, if_exists="append", index=False)
        print("\n¡ÉXITO! Registros insertados en la tabla 'tasas_cambio_historico'.")

    else:
        print("Error en la respuesta de la API.")

except Exception as e:
    print(f"Error durante el proceso: {e}")