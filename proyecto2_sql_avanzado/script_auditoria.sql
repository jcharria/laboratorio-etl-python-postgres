-- 1. Tabla principal
CREATE TABLE IF NOT EXISTS public.inventario_equipos (
    equipo_id SERIAL PRIMARY KEY,
    hostname VARCHAR(50) NOT NULL,
    ip_address VARCHAR(15) NOT NULL,
    sistema_operativo VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'ACTIVO',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Auditoría
CREATE TABLE IF NOT EXISTS public.log_auditoria_equipos (
    log_id SERIAL PRIMARY KEY,
    equipo_id INT,
    accion VARCHAR(20),
    usuario_bd VARCHAR(50) DEFAULT CURRENT_USER,
    fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT
);

-- 3. Función de Auditoría en PL/pgSQL
CREATE OR REPLACE FUNCTION public.fn_auditar_cambio_equipo()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.log_auditoria_equipos(equipo_id, accion, detalles)
    VALUES (
        NEW.equipo_id,
        TG_OP,
        CONCAT('Estado cambiado de ', OLD.estado, ' a ', NEW.estado)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 4. Trigger
DROP TRIGGER IF EXISTS trg_audita_equipo ON public.inventario_equipos;
CREATE TRIGGER trg_audita_equipo
AFTER UPDATE OF estado ON public.inventario_equipos
FOR EACH ROW
EXECUTE FUNCTION public.fn_auditar_cambio_equipo();

-- 5. Vista Analítica
CREATE OR REPLACE VIEW public.vw_resumen_equipos_activos AS
SELECT 
    sistema_operativo,
    COUNT(*) AS total_activos,
    MAX(fecha_registro) AS ultimo_registro
FROM public.inventario_equipos
WHERE estado = 'ACTIVO'
GROUP BY sistema_operativo;