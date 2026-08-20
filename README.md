# Pipeline de Integración de Datos, Automatización ETL y Consumo de APIs

Este repositorio contiene un laboratorio de **Ingeniería de Datos y ETL** diseñado para demostrar procesos automatizados de Extracción, Transformación y Carga (ETL), procesamiento de datos no estructurados/desordenados y persistencia en bases de datos relacionales.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.13
* **Procesamiento de Datos:** Pandas, Openpyxl[cite: 2]
* **Base de Datos:** PostgreSQL 16[cite: 2]
* **ORM & Controladores:** SQLAlchemy, Psycopg2[cite: 2]
* **Consumo Web:** Requests (APIs REST)
* **Gestión & Entorno:** VS Code, Git, DBeaver[cite: 2]

---

## 🚀 Arquitectura y Módulos del Proyecto

El proyecto se divide en tres flujos de trabajo principales:

1. **Prueba de Conexión y Carga Base (`prueba_etl.py`):**
   * Creación de estructuras de datos en memoria (DataFrames)[cite: 2].
   * Conexión automatizada mediante SQLAlchemy e inserción directa en PostgreSQL[cite: 2].

2. **Pipeline de Limpieza y Estandarización (`pipeline_limpieza_etl.py`):**
   * **Extracción:** Lectura de reportes en Excel con inconsistencias de formato[cite: 2].
   * **Transformación:** Normalización de texto (Title Case/Upper), eliminación de espacios en blanco, limpieza de caracteres especiales en montos numéricos, manejo de valores nulos y estandarización de fechas[cite: 2].
   * **Carga:** Persistencia en la tabla `ventas_procesadas` de PostgreSQL[cite: 2].

3. **Consumo de APIs REST en Tiempo Real (`api_a_postgres.py`):**
   * Extracción de datos en vivo desde API financiera pública.
   * Filtrado y estructuración de divisas de interés.
   * Carga incremental con registro de timestamp en la base de datos[cite: 2].

---

## 📂 Estructura del Repositorio

```text
laboratorio-etl-python-postgres/
├── .gitignore                   # Exclusión de credenciales y datos temporales
├── README.md                    # Documentación del proyecto
├── api_a_postgres.py            # Extracción desde API Web e inserción
├── generar_excel_desordenado.py # Generador de datos de prueba inestructurados
├── pipeline_limpieza_etl.py     # Pipeline ETL de limpieza y transformación
└── prueba_etl.py               # Script base de integración