# Proyecto 3: Pipeline de Automatización y Auditoría M365 / Google Workspace

Este módulo automatiza la ingesta y análisis de logs de administración de usuarios y licencias de tenants cloud (Microsoft 365 / Google Workspace) para la optimización de costos en departamentos de TI.

## 🛠️ Reglas de Negocio Implementadas
* **Ingesta de Logs:** Consolidación de estados de cuenta (`accountEnabled`) y fechas de último acceso.
* **Control de Costos:** Identificación de usuarios inactivos o deshabilitados que mantienen licencias empresariales de alto valor asignadas (`SPE_E5` / `SPE_E3`).
* **Persistencia:** Carga directa a PostgreSQL para generación de tableros de control y gestión de licencias.