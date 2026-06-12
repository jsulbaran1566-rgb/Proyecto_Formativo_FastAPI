-- ============================================================
-- AgroMercado - Script SQL para PostgreSQL con Relaciones Añadidas
-- ============================================================

CREATE TABLE IF NOT EXISTS categorias (
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT pk_categorias PRIMARY KEY (nombre)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id     INTEGER      NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    rol    VARCHAR(50)  NOT NULL,
    CONSTRAINT pk_usuarios  PRIMARY KEY (id),
    CONSTRAINT chk_usuarios_rol CHECK (rol IN ('Productor', 'Comprador', 'Administrador'))
);

CREATE TABLE IF NOT EXISTS compradores (
    id     INTEGER      NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    CONSTRAINT pk_compradores PRIMARY KEY (id),
    -- Relación opcional: Vincula al comprador con su cuenta de usuario del sistema si aplica
    CONSTRAINT fk_compradores_usuario FOREIGN KEY (id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lotes (
    id        INTEGER      NOT NULL,
    producto  VARCHAR(150) NOT NULL,
    cantidad  INTEGER      NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    productor_id INTEGER   NOT NULL, -- RELACIÓN AÑADIDA: Quién sembró el lote
    CONSTRAINT pk_lotes            PRIMARY KEY (id),
    CONSTRAINT chk_lotes_cant      CHECK (cantidad > 0),
    CONSTRAINT fk_lotes_categoria  FOREIGN KEY (categoria) REFERENCES categorias(nombre) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_lotes_productor  FOREIGN KEY (productor_id) REFERENCES usuarios(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS reservas (
    id           INTEGER      NOT NULL,
    comprador_id INTEGER      NOT NULL, -- RELACIÓN AÑADIDA: ID del comprador real
    lote_id      INTEGER      NOT NULL, -- RELACIÓN AÑADIDA: ID del lote exacto reservado
    cantidad     INTEGER      NOT NULL,
    fecha        VARCHAR(20)  NOT NULL DEFAULT '09/05/2026',
    CONSTRAINT pk_reservas       PRIMARY KEY (id),
    CONSTRAINT chk_reservas_cant CHECK (cantidad > 0),
    CONSTRAINT fk_reservas_comprador FOREIGN KEY (comprador_id) REFERENCES compradores(id) ON DELETE RESTRICT,
    CONSTRAINT fk_reservas_lote      FOREIGN KEY (lote_id) REFERENCES lotes(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS historial_seguimiento (
    id       SERIAL       NOT NULL,
    accion   VARCHAR(200) NOT NULL,
    lote     INTEGER,
    producto VARCHAR(150) NOT NULL,
    fecha    DATE         NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_historial_seguimiento PRIMARY KEY (id),
    CONSTRAINT fk_historial_lote FOREIGN KEY (lote) REFERENCES lotes(id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS compras (
    id           INTEGER      NOT NULL,
    comprador_id INTEGER      NOT NULL, -- RELACIÓN AÑADIDA: Quién compra
    lote_id      INTEGER      NOT NULL, -- RELACIÓN AÑADIDA: Qué lote compra
    cantidad     INTEGER      NOT NULL,
    fecha        DATE         NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_compras      PRIMARY KEY (id),
    CONSTRAINT chk_compras_cant CHECK (cantidad > 0),
    CONSTRAINT fk_compras_comprador FOREIGN KEY (comprador_id) REFERENCES compradores(id),
    CONSTRAINT fk_compras_lote      FOREIGN KEY (lote_id) REFERENCES lotes(id)
);

CREATE TABLE IF NOT EXISTS ventas (
    id           INTEGER      NOT NULL,
    vendedor_id  INTEGER      NOT NULL, -- RELACIÓN AÑADIDA: Productor que vende (Usuario)
    lote_id      INTEGER      NOT NULL, -- RELACIÓN AÑADIDA: Lote vendido
    cantidad     INTEGER      NOT NULL,
    fecha        DATE         NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_ventas      PRIMARY KEY (id),
    CONSTRAINT chk_ventas_cant CHECK (cantidad > 0),
    CONSTRAINT fk_ventas_vendedor  FOREIGN KEY (vendedor_id) REFERENCES usuarios(id),
    CONSTRAINT fk_ventas_lote      FOREIGN KEY (lote_id) REFERENCES lotes(id)
);

CREATE TABLE IF NOT EXISTS historial_reservas (
    id         SERIAL       NOT NULL,
    reserva_id INTEGER      NOT NULL, -- RELACIÓN AÑADIDA: Apunta a la reserva para auditar cambios de estado
    estado     VARCHAR(50)  NOT NULL, 
    fecha      VARCHAR(20)  NOT NULL DEFAULT '09/05/2026',
    CONSTRAINT pk_historial_reservas PRIMARY KEY (id),
    CONSTRAINT fk_historial_reserva_id FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE
);
