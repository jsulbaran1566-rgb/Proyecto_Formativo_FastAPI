from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.sql import func
from database import Base


# ================= USUARIOS =================

class Usuario(Base):
    __tablename__ = "usuarios"

    id     = Column(Integer,     primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    rol    = Column(String(50),  nullable=False)
    # rol válido: "Productor" | "Comprador" | "Administrador"
    # La validación se hace en main.py con HTTPException


# ================= CATEGORIAS =================

class Categoria(Base):
    __tablename__ = "categorias"

    nombre = Column(String(100), primary_key=True, index=True)


# ================= LOTES =================

class Lote(Base):
    __tablename__ = "lotes"

    id        = Column(Integer,     primary_key=True, index=True)
    producto  = Column(String(150), nullable=False)
    cantidad  = Column(Integer,     nullable=False)
    categoria = Column(String(100), ForeignKey("categorias.nombre",
                                               onupdate="CASCADE",
                                               ondelete="RESTRICT"),
                       nullable=False)


# ================= COMPRADORES =================

class Comprador(Base):
    __tablename__ = "compradores"

    id     = Column(Integer,     primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    ciudad = Column(String(100), nullable=False)


# ================= RESERVAS =================

class Reserva(Base):
    __tablename__ = "reservas"

    id        = Column(Integer,     primary_key=True, index=True)
    comprador = Column(String(150), nullable=False)
    producto  = Column(String(150), nullable=False)
    cantidad  = Column(Integer,     nullable=False)
    fecha     = Column(String(20),  nullable=False, default="09/05/2026")


# ================= HISTORIAL SEGUIMIENTO =================

class HistorialSeguimiento(Base):
    __tablename__ = "historial_seguimiento"

    id       = Column(Integer,     primary_key=True, index=True, autoincrement=True)
    accion   = Column(String(200), nullable=False)
    lote     = Column(Integer,     ForeignKey("lotes.id",
                                              onupdate="CASCADE",
                                              ondelete="SET NULL"),
                      nullable=True)
    producto = Column(String(150), nullable=False)
    # En PostgreSQL usamos Date con server_default=func.current_date()
    fecha    = Column(Date, nullable=True, server_default=func.current_date())


# ================= COMPRAS =================

class Compra(Base):
    __tablename__ = "compras"

    id        = Column(Integer,     primary_key=True, index=True)
    comprador = Column(String(150), nullable=False)
    producto  = Column(String(150), nullable=False)
    cantidad  = Column(Integer,     nullable=False)
    fecha     = Column(Date, nullable=True, server_default=func.current_date())


# ================= VENTAS =================

class Venta(Base):
    __tablename__ = "ventas"

    id        = Column(Integer,     primary_key=True, index=True)
    comprador = Column(String(150), nullable=False)
    producto  = Column(String(150), nullable=False)
    cantidad  = Column(Integer,     nullable=False)
    fecha     = Column(Date, nullable=True, server_default=func.current_date())


# ================= HISTORIAL RESERVAS =================

class HistorialReserva(Base):
    __tablename__ = "historial_reservas"

    id        = Column(Integer,     primary_key=True, index=True, autoincrement=True)
    comprador = Column(String(150), nullable=False)
    producto  = Column(String(150), nullable=False)
    cantidad  = Column(Integer,     nullable=False)
    fecha     = Column(String(20),  nullable=False, default="09/05/2026")
