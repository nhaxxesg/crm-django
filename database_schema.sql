-- ============================================
-- Script SQL para crear la base de datos CRM
-- Basado en el diagrama ER (er-diagram.puml)
-- MySQL 8.0+
-- ============================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS crm_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE crm_db;

-- ============================================
-- TABLA: authentication_user (Usuario)
-- ============================================
-- Hereda campos de AbstractUser de Django
-- Campos adicionales: nombre_completo, tipo, activo, fecha_creacion
CREATE TABLE IF NOT EXISTS authentication_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL COMMENT 'Contraseña hasheada (PBKDF2)',
    last_login DATETIME(6) NULL,
    is_superuser TINYINT(1) NOT NULL DEFAULT 0,
    username VARCHAR(150) NOT NULL UNIQUE COMMENT 'Nombre de usuario único',
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT 'Email único',
    is_staff TINYINT(1) NOT NULL DEFAULT 0,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    date_joined DATETIME(6) NOT NULL,
    -- Campos personalizados
    nombre_completo VARCHAR(150) NOT NULL COMMENT 'Nombre completo del usuario',
    tipo ENUM('admin', 'regular') NOT NULL DEFAULT 'regular' COMMENT 'Tipo de usuario',
    activo TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Estado activo/inactivo',
    fecha_creacion DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'Fecha de creación del registro',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_tipo (tipo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tabla de usuarios del sistema con autenticación';

-- ============================================
-- TABLA: empresas_empresa
-- ============================================
CREATE TABLE IF NOT EXISTS empresas_empresa (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL UNIQUE COMMENT 'Nombre de la empresa (único)',
    industria ENUM('tecnologia', 'servicios', 'manufactura', 'comercio', 'salud', 'educacion', 'otros') NULL COMMENT 'Sector industrial',
    num_empleados INT UNSIGNED NULL COMMENT 'Número de empleados',
    sitio_web VARCHAR(200) NULL COMMENT 'URL del sitio web',
    telefono VARCHAR(20) NULL COMMENT 'Teléfono de contacto',
    direccion VARCHAR(300) NULL COMMENT 'Dirección física',
    notas TEXT NULL COMMENT 'Notas adicionales sobre la empresa',
    fecha_creacion DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'Fecha de creación del registro',
    INDEX idx_nombre (nombre),
    INDEX idx_industria (industria),
    INDEX idx_fecha_creacion (fecha_creacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tabla central de organizaciones/empresas cliente';

-- ============================================
-- TABLA: clientes_cliente
-- ============================================
CREATE TABLE IF NOT EXISTS clientes_cliente (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL COMMENT 'Nombre completo del contacto',
    empresa_id BIGINT NOT NULL COMMENT 'FK a empresas_empresa (PROTECT)',
    cargo VARCHAR(100) NULL COMMENT 'Cargo o posición en la empresa',
    telefono VARCHAR(20) NOT NULL COMMENT 'Teléfono de contacto',
    email VARCHAR(255) NOT NULL COMMENT 'Email de contacto',
    direccion VARCHAR(300) NULL COMMENT 'Dirección física',
    notas TEXT NULL COMMENT 'Notas adicionales sobre el cliente',
    fecha_creacion DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'Fecha de creación del registro',
    FOREIGN KEY (empresa_id) REFERENCES empresas_empresa(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_empresa_id (empresa_id),
    INDEX idx_nombre_completo (nombre_completo),
    INDEX idx_email (email),
    INDEX idx_fecha_creacion (fecha_creacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Contactos individuales asociados a empresas';

-- ============================================
-- TABLA: oportunidades_oportunidad
-- ============================================
CREATE TABLE IF NOT EXISTS oportunidades_oportunidad (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL COMMENT 'Nombre de la oportunidad',
    cliente_id BIGINT NOT NULL COMMENT 'FK a clientes_cliente (PROTECT)',
    empresa_id BIGINT NOT NULL COMMENT 'FK a empresas_empresa (PROTECT)',
    valor DECIMAL(12, 2) NOT NULL COMMENT 'Valor monetario de la oportunidad',
    moneda CHAR(3) NOT NULL DEFAULT 'PEN' COMMENT 'Código de moneda (PEN, USD, EUR)',
    probabilidad INT NOT NULL COMMENT 'Probabilidad de cierre (0-100)',
    fecha_cierre_estimada DATE NOT NULL COMMENT 'Fecha estimada de cierre',
    etapa ENUM('prospeccion', 'calificacion', 'propuesta', 'negociacion', 'cerrado_ganado', 'cerrado_perdido') NOT NULL COMMENT 'Etapa del pipeline',
    estado ENUM('abierta', 'cerrada') NOT NULL DEFAULT 'abierta' COMMENT 'Estado de la oportunidad',
    resultado ENUM('ganada', 'perdida') NULL COMMENT 'Resultado si está cerrada',
    notas TEXT NULL COMMENT 'Notas adicionales',
    fecha_creacion DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'Fecha de creación del registro',
    fecha_cierre_real DATETIME(6) NULL COMMENT 'Fecha real de cierre',
    FOREIGN KEY (cliente_id) REFERENCES clientes_cliente(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (empresa_id) REFERENCES empresas_empresa(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_cliente_id (cliente_id),
    INDEX idx_empresa_id (empresa_id),
    INDEX idx_etapa (etapa),
    INDEX idx_estado (estado),
    INDEX idx_fecha_cierre_estimada (fecha_cierre_estimada),
    INDEX idx_fecha_creacion (fecha_creacion),
    CHECK (probabilidad >= 0 AND probabilidad <= 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Oportunidades comerciales y pipeline de ventas';

-- ============================================
-- TABLA: actividades_actividad
-- ============================================
CREATE TABLE IF NOT EXISTS actividades_actividad (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('llamada', 'reunion', 'email', 'tarea') NOT NULL COMMENT 'Tipo de actividad',
    asunto VARCHAR(200) NOT NULL COMMENT 'Asunto o título de la actividad',
    descripcion TEXT NULL COMMENT 'Descripción detallada',
    fecha_hora DATETIME(6) NOT NULL COMMENT 'Fecha y hora programada',
    estado ENUM('pendiente', 'completada', 'cancelada') NOT NULL DEFAULT 'pendiente' COMMENT 'Estado de la actividad',
    cliente_id BIGINT NULL COMMENT 'FK a clientes_cliente (CASCADE, opcional)',
    oportunidad_id BIGINT NULL COMMENT 'FK a oportunidades_oportunidad (CASCADE, opcional)',
    usuario_id BIGINT NOT NULL COMMENT 'FK a authentication_user (CASCADE)',
    resultado TEXT NULL COMMENT 'Resultado o notas de la actividad',
    fecha_creacion DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'Fecha de creación del registro',
    FOREIGN KEY (cliente_id) REFERENCES clientes_cliente(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (oportunidad_id) REFERENCES oportunidades_oportunidad(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES authentication_user(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_cliente_id (cliente_id),
    INDEX idx_oportunidad_id (oportunidad_id),
    INDEX idx_usuario_id (usuario_id),
    INDEX idx_tipo (tipo),
    INDEX idx_estado (estado),
    INDEX idx_fecha_hora (fecha_hora),
    INDEX idx_fecha_creacion (fecha_creacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Registro de actividades, interacciones y tareas';

-- ============================================
-- TABLA: django_migrations (Django)
-- ============================================
-- Esta tabla es creada automáticamente por Django
-- Se incluye aquí solo como referencia
CREATE TABLE IF NOT EXISTS django_migrations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME(6) NOT NULL,
    UNIQUE KEY django_migrations_app_name (app, name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ============================================

-- Índice compuesto para búsquedas frecuentes en clientes
CREATE INDEX idx_cliente_empresa_nombre ON clientes_cliente(empresa_id, nombre_completo);

-- Índice compuesto para filtros comunes en oportunidades
CREATE INDEX idx_oportunidad_estado_etapa ON oportunidades_oportunidad(estado, etapa);

-- Índice compuesto para reportes de actividades
CREATE INDEX idx_actividad_usuario_fecha ON actividades_actividad(usuario_id, fecha_hora);

-- ============================================
-- COMENTARIOS FINALES
-- ============================================
-- 
-- RELACIONES:
-- - Empresa -> Cliente (1:N, PROTECT): No se puede eliminar empresa si tiene clientes
-- - Empresa -> Oportunidad (1:N, PROTECT): No se puede eliminar empresa si tiene oportunidades
-- - Cliente -> Oportunidad (1:N, PROTECT): No se puede eliminar cliente si tiene oportunidades
-- - Cliente -> Actividad (1:N, CASCADE, opcional): Se eliminan actividades al eliminar cliente
-- - Oportunidad -> Actividad (1:N, CASCADE, opcional): Se eliminan actividades al eliminar oportunidad
-- - Usuario -> Actividad (1:N, CASCADE): Se eliminan actividades al eliminar usuario
--
-- NOTAS:
-- - Todos los campos de fecha usan DATETIME(6) para microsegundos
-- - Se usa utf8mb4 para soporte completo de Unicode (emojis, etc.)
-- - Los ENUMs coinciden exactamente con las opciones del diagrama ER
-- - Las claves foráneas tienen índices automáticos para mejor rendimiento
-- - El campo valor_ponderado se calcula en la aplicación (no se almacena)
--
-- ============================================

