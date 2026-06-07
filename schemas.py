from pydantic import BaseModel
from typing import Optional


# ================= USUARIOS =================

class UsuarioBase(BaseModel):
    id: int
    nombre: str
    rol: str  # "Productor" | "Comprador" | "Administrador"

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    class Config:
        from_attributes = True


# ================= CATEGORIAS =================

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    class Config:
        from_attributes = True


# ================= LOTES =================

class LoteBase(BaseModel):
    id: int
    producto: str
    cantidad: int
    categoria: str

class LoteCreate(LoteBase):
    pass

class LoteOut(LoteBase):
    class Config:
        from_attributes = True


# ================= COMPRADORES =================

class CompradorBase(BaseModel):
    id: int
    nombre: str
    ciudad: str

class CompradorCreate(CompradorBase):
    pass

class CompradorOut(CompradorBase):
    class Config:
        from_attributes = True


# ================= RESERVAS =================

class ReservaBase(BaseModel):
    id: int
    comprador: str
    producto: str
    cantidad: int
    fecha: Optional[str] = "09/05/2026"

class ReservaCreate(ReservaBase):
    pass

class ReservaOut(ReservaBase):
    class Config:
        from_attributes = True


# ================= HISTORIAL SEGUIMIENTO =================

class HistorialSeguimientoBase(BaseModel):
    accion: str
    lote: Optional[int] = None
    producto: str
    fecha: Optional[str] = None

class HistorialSeguimientoOut(HistorialSeguimientoBase):
    id: int
    class Config:
        from_attributes = True


# ================= COMPRAS =================

class CompraBase(BaseModel):
    id: int
    comprador: str
    producto: str
    cantidad: int
    fecha: Optional[str] = None

class CompraOut(CompraBase):
    class Config:
        from_attributes = True


# ================= VENTAS =================

class VentaBase(BaseModel):
    id: int
    comprador: str
    producto: str
    cantidad: int
    fecha: Optional[str] = None

class VentaOut(VentaBase):
    class Config:
        from_attributes = True


# ================= HISTORIAL RESERVAS =================

class HistorialReservaBase(BaseModel):
    comprador: str
    producto: str
    cantidad: int
    fecha: Optional[str] = "09/05/2026"

class HistorialReservaOut(HistorialReservaBase):
    id: int
    class Config:
        from_attributes = True
