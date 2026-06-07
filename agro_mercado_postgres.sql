-- ============================================================
-- AgroMercado - Script SQL para PostgreSQL / pgAdmin
-- Versión: 2.0  (migrado desde MySQL)
-- ============================================================

-- Crear base de datos (ejecutar conectado a postgres o cualquier otra BD)
-- CREATE DATABASE agro_mercado
--     ENCODING 'UTF8'
--     LC_COLLATE 'es_CO.UTF-8'
--     LC_CTYPE   'es_CO.UTF-8'
--     TEMPLATE template0;

-- Conectarse a agro_mercado antes de correr el resto:
-- \c agro_mercado

-- ============================================================
-- TABLA: categorias  (sin AUTO_INCREMENT; PK es el nombre)
-- ============================================================
CREATE TABLE IF NOT EXISTS categorias (
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT pk_categorias PRIMARY KEY (nombre)
);

-- ============================================================
-- TABLA: usuarios
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id     INTEGER      NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    rol    VARCHAR(50)  NOT NULL,
    CONSTRAINT pk_usuarios  PRIMARY KEY (id),
    CONSTRAINT chk_usuarios_rol CHECK (rol IN ('Productor', 'Comprador', 'Administrador'))
);

-- ============================================================
-- TABLA: lotes
-- ============================================================
CREATE TABLE IF NOT EXISTS lotes (
    id        INTEGER      NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INTEGER      NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    CONSTRAINT pk_lotes            PRIMARY KEY (id),
    CONSTRAINT chk_lotes_cant      CHECK (cantidad > 0),
    CONSTRAINT fk_lotes_categoria  FOREIGN KEY (categoria)
        REFERENCES categorias(nombre)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================================
-- TABLA: compradores
-- ============================================================
CREATE TABLE IF NOT EXISTS compradores (
    id     INTEGER      NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    CONSTRAINT pk_compradores PRIMARY KEY (id)
);

-- ============================================================
-- TABLA: reservas
-- ============================================================
CREATE TABLE IF NOT EXISTS reservas (
    id        INTEGER      NOT NULL,
    comprador VARCHAR(150) NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INTEGER      NOT NULL,
    fecha     VARCHAR(20)  NOT NULL DEFAULT '09/05/2026',
    CONSTRAINT pk_reservas       PRIMARY KEY (id),
    CONSTRAINT chk_reservas_cant CHECK (cantidad > 0)
);

-- ============================================================
-- TABLA: historial_seguimiento  (SERIAL en vez de AUTO_INCREMENT)
-- ============================================================
CREATE TABLE IF NOT EXISTS historial_seguimiento (
    id       SERIAL       NOT NULL,
    accion   VARCHAR(200) NOT NULL,
    lote     INTEGER,
    producto VARCHAR(150) NOT NULL,
    fecha    DATE         NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_historial_seguimiento PRIMARY KEY (id),
    CONSTRAINT fk_historial_lote FOREIGN KEY (lote)
        REFERENCES lotes(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- ============================================================
-- TABLA: compras
-- ============================================================
CREATE TABLE IF NOT EXISTS compras (
    id        INTEGER      NOT NULL,
    comprador VARCHAR(150) NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INTEGER      NOT NULL,
    fecha     DATE         NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_compras      PRIMARY KEY (id),
    CONSTRAINT chk_compras_cant CHECK (cantidad > 0)
);

-- ============================================================
-- TABLA: ventas
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas (
    id        INTEGER      NOT NULL,
    comprador VARCHAR(150) NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INTEGER      NOT NULL,
    fecha     DATE         NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_ventas      PRIMARY KEY (id),
    CONSTRAINT chk_ventas_cant CHECK (cantidad > 0)
);

-- ============================================================
-- TABLA: historial_reservas  (SERIAL en vez de AUTO_INCREMENT)
-- ============================================================
CREATE TABLE IF NOT EXISTS historial_reservas (
    id        SERIAL       NOT NULL,
    comprador VARCHAR(150) NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INTEGER      NOT NULL,
    fecha     VARCHAR(20)  NOT NULL DEFAULT '09/05/2026',
    CONSTRAINT pk_historial_reservas PRIMARY KEY (id),
    CONSTRAINT chk_hist_res_cant     CHECK (cantidad > 0)
);

-- ============================================================
-- DATOS INICIALES
-- ============================================================

INSERT INTO categorias (nombre) VALUES
    ('Tubérculos'),
    ('Frutas'),
    ('Verduras'),
    ('Hortalizas');

INSERT INTO usuarios (id, nombre, rol) VALUES
    (1, 'Valentina', 'Productor'),
    (2, 'Danna',     'Comprador');

INSERT INTO lotes (id, producto, cantidad, categoria) VALUES
    (1, 'Papa',     500, 'Tubérculos'),
    (2, 'Tomate',   200, 'Verduras'),
    (3, 'Mango',    300, 'Frutas'),
    (4, 'Espinaca', 150, 'Hortalizas');

INSERT INTO compradores (id, nombre, ciudad) VALUES
    (1, 'Jesus', 'Bogotá'),
    (2, 'Sofia', 'Medellín');

INSERT INTO reservas (id, comprador, producto, cantidad, fecha) VALUES
    (1, 'Jesus', 'Papa', 10, '09/05/2026');

INSERT INTO historial_seguimiento (accion, lote, producto) VALUES
    ('Creación de lote', 1, 'Papa'),
    ('Creación de lote', 2, 'Tomate'),
    ('Creación de lote', 3, 'Mango'),
    ('Creación de lote', 4, 'Espinaca');

-- ============================================================
-- VERIFICACIÓN
-- ============================================================
SELECT 'categorias'             AS tabla, COUNT(*) AS registros FROM categorias
UNION ALL
SELECT 'usuarios',               COUNT(*) FROM usuarios
UNION ALL
SELECT 'lotes',                  COUNT(*) FROM lotes
UNION ALL
SELECT 'compradores',            COUNT(*) FROM compradores
UNION ALL
SELECT 'reservas',               COUNT(*) FROM reservas
UNION ALL
SELECT 'historial_seguimiento',  COUNT(*) FROM historial_seguimiento
UNION ALL
SELECT 'compras',                COUNT(*) FROM compras
UNION ALL
SELECT 'ventas',                 COUNT(*) FROM ventas
UNION ALL
SELECT 'historial_reservas',     COUNT(*) FROM historial_reservas;
