-- ============================================================
-- AgroMercado - Script SQL para MySQL Workbench
-- Versión: 1.0
-- Fecha: 2026-05-30
-- ============================================================
 
-- Crear y seleccionar la base de datos
CREATE DATABASE IF NOT EXISTS agro_mercado
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_spanish_ci;

USE agro_mercado;

-- ============================================================
-- TABLA: categorias
-- (se crea primero porque lotes la referencia)
-- ============================================================
CREATE TABLE IF NOT EXISTS categorias (
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT pk_categorias PRIMARY KEY (nombre)
);

-- ============================================================
-- TABLA: usuarios
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id     INT          NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    rol    VARCHAR(50)  NOT NULL,
    CONSTRAINT pk_usuarios  PRIMARY KEY (id),
    CONSTRAINT chk_usuarios_rol CHECK (rol IN ('Productor', 'Comprador', 'Administrador'))
);

-- ============================================================
-- TABLA: lotes
-- ============================================================
CREATE TABLE IF NOT EXISTS lotes (
    id        INT          NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INT          NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    CONSTRAINT pk_lotes          PRIMARY KEY (id),
    CONSTRAINT chk_lotes_cant    CHECK (cantidad > 0),
    CONSTRAINT fk_lotes_categoria
        FOREIGN KEY (categoria) REFERENCES categorias(nombre)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================================
-- TABLA: compradores
-- ============================================================
CREATE TABLE IF NOT EXISTS compradores (
    id     INT          NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    CONSTRAINT pk_compradores PRIMARY KEY (id)
);

-- ============================================================
-- TABLA: reservas
-- ============================================================
CREATE TABLE IF NOT EXISTS reservas (
    id        INT          NOT NULL,
    comprador VARCHAR(150) NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INT          NOT NULL,
    fecha     VARCHAR(20)  NOT NULL DEFAULT '09/05/2026',
    CONSTRAINT pk_reservas      PRIMARY KEY (id),
    CONSTRAINT chk_reservas_cant CHECK (cantidad > 0)
);

-- ============================================================
-- TABLA: historial_seguimiento
-- ============================================================
CREATE TABLE IF NOT EXISTS historial_seguimiento (
    id       INT          NOT NULL AUTO_INCREMENT,
    accion   VARCHAR(200) NOT NULL,
    lote     INT,
    producto VARCHAR(150) NOT NULL,
    fecha    DATE         NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT pk_historial_seguimiento PRIMARY KEY (id),
    CONSTRAINT fk_historial_lote
        FOREIGN KEY (lote) REFERENCES lotes(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- ============================================================
-- TABLA: compras
-- ============================================================
CREATE TABLE IF NOT EXISTS compras (
    id        INT          NOT NULL,
    comprador VARCHAR(150) NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INT          NOT NULL,
    fecha     DATE         NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT pk_compras      PRIMARY KEY (id),
    CONSTRAINT chk_compras_cant CHECK (cantidad > 0)
);

-- ============================================================
-- TABLA: ventas
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas (
    id        INT          NOT NULL,
    comprador VARCHAR(150) NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INT          NOT NULL,
    fecha     DATE         NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT pk_ventas      PRIMARY KEY (id),
    CONSTRAINT chk_ventas_cant CHECK (cantidad > 0)
);

-- ============================================================
-- TABLA: historial_reservas
-- ============================================================
CREATE TABLE IF NOT EXISTS historial_reservas (
    id        INT          NOT NULL AUTO_INCREMENT,
    comprador VARCHAR(150) NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INT          NOT NULL,
    fecha     VARCHAR(20)  NOT NULL DEFAULT '09/05/2026',
    CONSTRAINT pk_historial_reservas  PRIMARY KEY (id),
    CONSTRAINT chk_hist_res_cant      CHECK (cantidad > 0)
);

-- ============================================================
-- DATOS INICIALES
-- ============================================================

-- Categorias
INSERT INTO categorias (nombre) VALUES
    ('Tubérculos'),
    ('Frutas'),
    ('Verduras'),
    ('Hortalizas');

-- Usuarios
INSERT INTO usuarios (id, nombre, rol) VALUES
    (1, 'Valentina', 'Productor'),
    (2, 'Danna',     'Comprador');

-- Lotes
INSERT INTO lotes (id, producto, cantidad, categoria) VALUES
    (1, 'Papa',     500, 'Tubérculos'),
    (2, 'Tomate',   200, 'Verduras'),
    (3, 'Mango',    300, 'Frutas'),
    (4, 'Espinaca', 150, 'Hortalizas');

-- Compradores
INSERT INTO compradores (id, nombre, ciudad) VALUES
    (1, 'Jesus', 'Bogotá'),
    (2, 'Sofia',  'Medellín');

-- Reservas
INSERT INTO reservas (id, comprador, producto, cantidad, fecha) VALUES
    (1, 'Jesus', 'Papa', 10, '09/05/2026');

-- Historial seguimiento (creación de lotes)
INSERT INTO historial_seguimiento (accion, lote, producto) VALUES
    ('Creación de lote', 1, 'Papa'),
    ('Creación de lote', 2, 'Tomate'),
    ('Creación de lote', 3, 'Mango'),
    ('Creación de lote', 4, 'Espinaca');

-- ============================================================
-- VERIFICACIÓN DE DATOS
-- ============================================================
SELECT 'categorias'          AS tabla, COUNT(*) AS registros FROM categorias
UNION ALL
SELECT 'usuarios',            COUNT(*) FROM usuarios
UNION ALL
SELECT 'lotes',               COUNT(*) FROM lotes
UNION ALL
SELECT 'compradores',         COUNT(*) FROM compradores
UNION ALL
SELECT 'reservas',            COUNT(*) FROM reservas
UNION ALL
SELECT 'historial_seguimiento', COUNT(*) FROM historial_seguimiento
UNION ALL
SELECT 'compras',             COUNT(*) FROM compras
UNION ALL
SELECT 'ventas',              COUNT(*) FROM ventas
UNION ALL
SELECT 'historial_reservas',  COUNT(*) FROM historial_reservas;
