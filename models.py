from pydantic import BaseModel, Field
from typing import List

# ================= USUARIOS =================

class Usuario(BaseModel):
    id: int = Field(gt=0)
    nombre: str = Field(min_length=3)
    rol: str = Field(min_length=3)

# ================= LOTES =================
  
class Lote(BaseModel):
    id: int = Field(gt=0)
    producto: str = Field(min_length=2)
    cantidad: int = Field(gt=0)
    categoria: str = Field(min_length=3)

# ================= COMPRADORES =================

class Comprador(BaseModel):
    id: int = Field(gt=0)
    nombre: str = Field(min_length=3)
    ciudad: str = Field(min_length=3)

# ================= RESERVAS =================

class Reserva(BaseModel):
    id: int = Field(gt=0)
    comprador: str = Field(min_length=3)
    producto: str = Field(min_length=2)
    cantidad: int = Field(gt=0)

# ================= CATEGORIAS =================

class Categoria(BaseModel):
    nombre: str = Field(min_length=3)

# ================= HISTORIAL =================

class HistorialSeguimiento(BaseModel):
    accion: str = Field(min_length=3)
    lote: int
    producto: str = Field(min_length=2)

# ================= COMPRAS Y VENTAS =================

class Compra(BaseModel):
    id: int = Field(gt=0)
    comprador: str = Field(min_length=3)
    producto: str = Field(min_length=2)
    cantidad: int = Field(gt=0)

class Venta(BaseModel):
    id: int = Field(gt=0)
    comprador: str = Field(min_length=3)
    producto: str = Field(min_length=2)
    cantidad: int = Field(gt=0)
