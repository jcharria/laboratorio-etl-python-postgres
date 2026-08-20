# Proyecto 2: Motor de Auditoría y SQL Avanzado en PostgreSQL

Este módulo implementa lógica de negocio del lado de la base de datos para rastrear cambios en la infraestructura de servidores y generar vistas analíticas.

## 🛠️ Funcionalidades Clave
* **Triggers y Procedimientos Almacenados (PL/pgSQL):** Captura automática de eventos DML (`UPDATE`) para auditar cambios de estado de equipos sin intervención de la capa de aplicación.
* **Tablas de Log:** Registro histórico de eventos con marcas de tiempo (`TIMESTAMP`) y usuario ejecutor (`CURRENT_USER`).
* **Vistas Analíticas:** Abstracción de datos agregados para consultar el estado del inventario activo optimizando el rendimiento de lectura.