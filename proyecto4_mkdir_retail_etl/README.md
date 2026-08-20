# Proyecto 4: Pipeline ETL de Ventas Retail (PNRao Choco Data)

Pipeline automatizado para ingesta, depuración y carga de datos de transacciones de ventas minoristas a PostgreSQL.

## 🛠️ Reglas de Transformación Aplicadas
* **Limpieza de Cadenas:** Eliminación de espacios en blanco (*whitespaces*) sobrantes e imputación de valores vacíos (`None`).
* **Integridad de Datos:** Eliminación de duplicados y descarte de registros corruptos carentes de `OrderID` o `CustomerID`.
* **Consistencia Numérica:** Normalización de fechas a tipo `TIMESTAMP` y recálculo dinámico de `TotalRevenue` (`UnitsSold` * `PricePerUnit`).
* **Persistencia:** Carga directa en lotes mediante `SQLAlchemy` a la tabla `public.ventas_retail_procesadas`.