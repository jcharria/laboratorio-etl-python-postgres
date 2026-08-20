import pandas as pd

# Simulación de un reporte de ventas desordenado enviado por un cliente
datos_desordenados = {
    "CLIENTE ": ["  Juan Pérez  ", "MARIA LOPEZ", "  Carlos Gomez", None, "Ana Silva "],
    "FECHA_VENTA": ["2026-08-01", "02/08/2026", "2026-08-03", "2026-08-04", None],
    "MONTO": ["$150.00", "$ 200.50", "350", None, "$120.00"],
    "ESTADO": ["completado", "COMPLETADO", " pendiente ", "cancelado", "completado"]
}

# Crear DataFrame y exportar a Excel
df_sucio = pd.DataFrame(datos_desordenados)
df_sucio.to_excel("reporte_ventas_bruto.xlsx", index=False)

print("¡Archivo 'reporte_ventas_bruto.xlsx' creado exitosamente con datos desordenados!")