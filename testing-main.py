from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db, engine, Base
import models


# Crea todas las tablas al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgroMercado API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


# ================================================================
# EXCEPCIONES PERSONALIZADAS
# ================================================================

class ErrorUsuarioNoExiste(Exception):
    def __init__(self, id):
        self.mensaje = f"No existe un usuario con el id {id}"

class ErrorStockInsuficiente(Exception):
    def __init__(self, producto, pedido, disponible):
        self.mensaje = f"No hay suficiente stock de '{producto}'. Pedido: {pedido}, Disponible: {disponible}"

@app.exception_handler(ErrorUsuarioNoExiste)
async def manejar_usuario_no_existe(request, error):
    return JSONResponse(status_code=404, content={"error": error.mensaje})

@app.exception_handler(ErrorStockInsuficiente)
async def manejar_stock_insuficiente(request, error):
    return JSONResponse(status_code=400, content={"error": error.mensaje})


# ================================================================
# USUARIOS
# ================================================================

@app.get("/usuarios")
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


@app.get("/usuarios/{id}/rol/{rol}")
def obtener_usuario_por_id_y_rol(
    id: int,
    rol: str,
    activo: bool = Query(default=True, description="Filtrar usuarios activos o inactivos"),
    db: Session = Depends(get_db),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    roles_validos = ["Productor", "Comprador", "Administrador"]
    if rol not in roles_validos:
        raise HTTPException(status_code=400, detail=f"Rol inválido. Roles permitidos: {roles_validos}")

    resultado = db.query(models.Usuario).filter(
        models.Usuario.id == id,
        models.Usuario.rol == rol
    ).all()

    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado con esos criterios")

    return {"activo": activo, "usuarios": resultado}


@app.post("/usuarios")
def agregar_usuario(
    id: int,
    nombre: str,
    rol: str,
    db: Session = Depends(get_db),
):
    roles_validos = ["Productor", "Comprador", "Administrador"]
    if rol not in roles_validos:
        raise HTTPException(status_code=400, detail=f"Rol inválido. Permitidos: {roles_validos}")

    if db.query(models.Usuario).filter(models.Usuario.id == id).first():
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese id")

    nuevo = models.Usuario(id=id, nombre=nombre, rol=rol)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Usuario agregado", "usuario": nuevo}


@app.put("/usuarios/{id}/rol/{nuevo_rol}")
def editar_usuario(
    id: int,
    nuevo_rol: str,
    nombre: str  = Query(default=None, description="Nuevo nombre del usuario"),
    activo: bool = Query(default=True,  description="Estado activo del usuario"),
    db: Session = Depends(get_db),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    roles_validos = ["Productor", "Comprador", "Administrador"]
    if nuevo_rol not in roles_validos:
        raise HTTPException(status_code=400, detail=f"Rol inválido. Permitidos: {roles_validos}")

    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise ErrorUsuarioNoExiste(id)

    usuario.rol = nuevo_rol
    if nombre:
        usuario.nombre = nombre

    db.commit()
    db.refresh(usuario)
    return {"mensaje": "Usuario actualizado", "activo": activo, "usuario": usuario}


# ================================================================
# LOTES
# ================================================================

@app.get("/lotes")
def obtener_lotes(db: Session = Depends(get_db)):
    return db.query(models.Lote).all()


@app.get("/lotes/{id}/categoria/{categoria}")
def obtener_lote_por_id_y_categoria(
    id: int,
    categoria: str,
    cantidad_min: int = Query(default=0,          description="Cantidad mínima disponible"),
    ordenar_por: str  = Query(default="producto",  description="Campo para ordenar: producto | cantidad"),
    db: Session = Depends(get_db),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")
    if cantidad_min < 0:
        raise HTTPException(status_code=400, detail="cantidad_min no puede ser negativo")

    campos_validos = ["producto", "cantidad"]
    if ordenar_por not in campos_validos:
        raise HTTPException(status_code=400, detail=f"ordenar_por debe ser uno de: {campos_validos}")

    resultado = db.query(models.Lote).filter(
        models.Lote.id == id,
        models.Lote.categoria.ilike(categoria),
        models.Lote.cantidad >= cantidad_min
    ).all()

    if not resultado:
        raise HTTPException(status_code=404, detail="Lote no encontrado con esos criterios")

    return sorted(resultado, key=lambda x: getattr(x, ordenar_por))


@app.post("/lotes")
def agregar_lote(
    id: int,
    producto: str,
    cantidad: int,
    categoria: str,
    db: Session = Depends(get_db),
):
    if db.query(models.Lote).filter(models.Lote.id == id).first():
        raise HTTPException(status_code=400, detail="Ya existe un lote con ese id")

    if not db.query(models.Categoria).filter(models.Categoria.nombre == categoria).first():
        raise HTTPException(status_code=400, detail="Categoría inválida")

    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

    nuevo = models.Lote(id=id, producto=producto, cantidad=cantidad, categoria=categoria)
    db.add(nuevo)

    historial = models.HistorialSeguimiento(accion="Creación de lote", lote=id, producto=producto)
    db.add(historial)

    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Lote agregado", "lote": nuevo}


@app.put("/lotes/{id}/producto/{nuevo_producto}")
def editar_lote(
    id: int,
    nuevo_producto: str,
    cantidad:  int = Query(default=None, description="Nueva cantidad del lote"),
    categoria: str = Query(default=None, description="Nueva categoría del lote"),
    db: Session = Depends(get_db),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    lote = db.query(models.Lote).filter(models.Lote.id == id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    lote.producto = nuevo_producto
    if cantidad is not None:
        if cantidad <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")
        lote.cantidad = cantidad
    if categoria:
        lote.categoria = categoria

    db.commit()
    db.refresh(lote)
    return {"mensaje": "Lote actualizado", "lote": lote}


# ================================================================
# COMPRADORES
# ================================================================

@app.get("/compradores")
def obtener_compradores(db: Session = Depends(get_db)):
    return db.query(models.Comprador).all()


@app.get("/compradores/{id}/ciudad/{ciudad}")
def obtener_comprador_por_id_y_ciudad(
    id: int,
    ciudad: str,
    limite: int = Query(default=10, ge=1, le=100, description="Número máximo de resultados"),
    orden:  str = Query(default="nombre",          description="Campo para ordenar: nombre | ciudad"),
    db: Session = Depends(get_db),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    campos_validos = ["nombre", "ciudad"]
    if orden not in campos_validos:
        raise HTTPException(status_code=400, detail=f"orden debe ser uno de: {campos_validos}")

    resultado = db.query(models.Comprador).filter(
        models.Comprador.id == id,
        models.Comprador.ciudad.ilike(ciudad)
    ).all()

    if not resultado:
        raise HTTPException(status_code=404, detail="Comprador no encontrado con esos criterios")

    return sorted(resultado, key=lambda x: getattr(x, orden))[:limite]


@app.post("/compradores")
def agregar_comprador(
    id: int,
    nombre: str,
    ciudad: str,
    db: Session = Depends(get_db),
):
    if db.query(models.Comprador).filter(models.Comprador.id == id).first():
        raise HTTPException(status_code=400, detail="Ya existe un comprador con ese id")

    nuevo = models.Comprador(id=id, nombre=nombre, ciudad=ciudad)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Comprador agregado", "comprador": nuevo}


@app.delete("/compradores/{id}/ciudad/{ciudad}")
def eliminar_comprador(
    id: int,
    ciudad: str,
    confirmar: bool = Query(default=False, description="Debe ser true para confirmar la eliminación"),
    notificar: bool = Query(default=False, description="Simula notificación al comprador eliminado"),
    db: Session = Depends(get_db),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")
    if not confirmar:
        raise HTTPException(status_code=400, detail="Debe confirmar la eliminación con confirmar=true")

    comprador = db.query(models.Comprador).filter(
        models.Comprador.id == id,
        models.Comprador.ciudad.ilike(ciudad)
    ).first()

    if not comprador:
        raise HTTPException(status_code=404, detail="Comprador no encontrado con esos criterios")

    nombre = comprador.nombre
    db.delete(comprador)
    db.commit()

    mensaje = "Comprador eliminado"
    if notificar:
        mensaje += f" — notificación enviada a {nombre}"
    return {"mensaje": mensaje}


# ================================================================
# RESERVAS
# ================================================================

@app.get("/reservas")
def obtener_reservas(db: Session = Depends(get_db)):
    return db.query(models.Reserva).all()


@app.get("/reservas/{id}/comprador/{comprador}")
def obtener_reserva(
    id: int,
    comprador: str,
    fecha:  str = Query(default=None, description="Filtrar por fecha (dd/mm/aaaa)"),
    estado: str = Query(default=None, description="Filtrar por estado: activa | cancelada"),
    db: Session = Depends(get_db),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    estados_validos = ["activa", "cancelada"]
    if estado and estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Permitidos: {estados_validos}")

    resultado = db.query(models.Reserva).filter(
        models.Reserva.id == id,
        models.Reserva.comprador.ilike(comprador)
    ).all()

    if fecha:
        resultado = [r for r in resultado if r.fecha == fecha]

    if not resultado:
        raise HTTPException(status_code=404, detail="Reserva no encontrada con esos criterios")

    return resultado


@app.post("/reservas/{id}/comprador/{comprador}")
def crear_reserva(
    id: int,
    comprador: str,
    producto: str = Query(...,       description="Nombre del producto a reservar"),
    cantidad: int = Query(..., ge=1, description="Cantidad a reservar (mínimo 1)"),
    db: Session = Depends(get_db),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    if db.query(models.Reserva).filter(models.Reserva.id == id).first():
        raise HTTPException(status_code=400, detail="Ya existe una reserva con ese id")

    lote = db.query(models.Lote).filter(models.Lote.producto.ilike(producto)).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Producto no encontrado en los lotes disponibles")

    if lote.cantidad < cantidad:
        raise ErrorStockInsuficiente(producto, cantidad, lote.cantidad)

    # Descontar stock
    lote.cantidad -= cantidad

    # Crear reserva
    nueva_reserva = models.Reserva(id=id, comprador=comprador, producto=producto, cantidad=cantidad)
    db.add(nueva_reserva)

    # Registrar en historial, compras, ventas e historial_reservas
    db.add(models.HistorialSeguimiento(accion="Compra realizada", lote=lote.id, producto=producto))
    db.add(models.Compra(id=id, comprador=comprador, producto=producto, cantidad=cantidad))
    db.add(models.Venta(id=id, comprador=comprador, producto=producto, cantidad=cantidad))
    db.add(models.HistorialReserva(comprador=comprador, producto=producto, cantidad=cantidad))

    db.commit()
    db.refresh(nueva_reserva)
    return {"mensaje": "Reserva creada correctamente", "reserva": nueva_reserva}


# ================================================================
# CATEGORÍAS
# ================================================================

@app.get("/categorias")
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()


@app.get("/categorias/{nombre}/lotes/{cantidad_min}")
def obtener_lotes_por_categoria(
    nombre: str,
    cantidad_min: int,
    ordenar: bool = Query(default=False, description="Ordenar por cantidad descendente"),
    limite:  int  = Query(default=10, ge=1, le=100, description="Límite de resultados (1-100)"),
    db: Session = Depends(get_db),
):
    if not db.query(models.Categoria).filter(models.Categoria.nombre == nombre).first():
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    if cantidad_min < 0:
        raise HTTPException(status_code=400, detail="cantidad_min no puede ser negativo")

    resultado = db.query(models.Lote).filter(
        models.Lote.categoria.ilike(nombre),
        models.Lote.cantidad >= cantidad_min
    ).all()

    if ordenar:
        resultado = sorted(resultado, key=lambda x: x.cantidad, reverse=True)

    return resultado[:limite]


@app.post("/categorias")
def agregar_categoria(
    nombre: str,
    db: Session = Depends(get_db),
):
    if db.query(models.Categoria).filter(models.Categoria.nombre == nombre).first():
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    nueva = models.Categoria(nombre=nombre)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"mensaje": "Categoría agregada", "categoria": nueva}


# ================================================================
# HISTORIAL Y REPORTES (solo lectura)
# ================================================================

@app.get("/historial_seguimiento")
def ver_historial_seguimiento(db: Session = Depends(get_db)):
    return db.query(models.HistorialSeguimiento).all()


@app.get("/compras")
def ver_compras(db: Session = Depends(get_db)):
    return db.query(models.Compra).all()


@app.get("/ventas")
def ver_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()


@app.get("/historial_reservas")
def ver_historial_reservas(db: Session = Depends(get_db)):
    return db.query(models.HistorialReserva).all()
