from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
class ErrorUsuarioNoExiste(Exception):
    def __init__(self, id):
        self.mensaje = f"No existe un usuario con el id {id}"

class ErrorStockInsuficiente(Exception):
    def __init__(self, producto, pedido, disponible):
        self.mensaje = f"No hay suficiente stock de '{producto}'. Pedido: {pedido}, Disponible: {disponible}"

@app.exception_handler(ErrorUsuarioNoExiste)
async def manejar_usuario_no_existe(request, error):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=404, content={"error": error.mensaje})
    
@app.exception_handler(ErrorStockInsuficiente)
async def manejar_stock_insuficiente(request, error):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=400, content={"error": error.mensaje})


# ============================================================
# DATOS INICIALES
# ============================================================
usuarios = [
    {"id": 1, "nombre": "Valentina", "rol": "Productor"},
    {"id": 2, "nombre": "Danna",     "rol": "Comprador"},
]

lotes = [
    {"id": 1, "producto": "Papa",   "cantidad": 500, "categoria": "Tubérculos"},
    {"id": 2, "producto": "Tomate", "cantidad": 200, "categoria": "Verduras"},
]

compradores = [
    {"id": 1, "nombre": "Jesus", "ciudad": "Bogotá"},
    {"id": 2, "nombre": "Sofia",  "ciudad": "Medellín"},
]

reservas           = [{"id": 1, "comprador": "Jesus", "producto": "Papa"}]
categorias         = ["Tubérculos", "Frutas", "Verduras", "Hortalizas"]
historial_seguimiento = []
compras            = []
ventas             = []
historial_reservas = []


# ============================================================
# USUARIOS
# ============================================================

# --- GET /usuarios/{id}/rol/{rol} ---
# Parámetros dinámicos : id, rol
# Query params         : activo (bool), ciudad (str)
@app.get("/usuarios/{id}/rol/{rol}")
def obtener_usuario_por_id_y_rol(
    id: int,
    rol: str,
    activo: bool = Query(default=True,  description="Filtrar usuarios activos o inactivos"),
    ciudad: str  = Query(default=None,  description="Filtrar por ciudad del usuario"),
):
    # Validación: id debe ser positivo
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    # Validación: rol permitido
    roles_validos = ["Productor", "Comprador", "Administrador"]
    if rol not in roles_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Rol inválido. Roles permitidos: {roles_validos}"
        )

    resultado = [u for u in usuarios if u["id"] == id and u["rol"] == rol]

    # Query param: ciudad (ejemplo de uso si el usuario tuviese campo ciudad)
    if ciudad:
        resultado = [u for u in resultado if u.get("ciudad", "").lower() == ciudad.lower()]

    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado con esos criterios")

    return {"activo": activo, "usuarios": resultado}


# --- POST /usuarios ---
@app.post("/usuarios")
def agregar_usuario(id: int, nombre: str, rol: str):
    # Validación: id no duplicado
    if any(u["id"] == id for u in usuarios):
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese id")

    # Validación: nombre no vacío
    if not nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    roles_validos = ["Productor", "Comprador", "Administrador"]
    if rol not in roles_validos:
        raise HTTPException(status_code=400, detail=f"Rol inválido. Permitidos: {roles_validos}")

    usuarios.append({"id": id, "nombre": nombre, "rol": rol})
    return {"mensaje": "Usuario agregado", "usuario": {"id": id, "nombre": nombre, "rol": rol}}


# --- PUT /usuarios/{id}/rol/{rol} ---
# Parámetros dinámicos : id, rol (nuevo rol)
# Query params         : nombre (nuevo nombre), activo (bool)
@app.put("/usuarios/{id}/rol/{nuevo_rol}")
def editar_usuario(
    id: int,
    nuevo_rol: str,
    nombre:  str  = Query(default=None, description="Nuevo nombre del usuario"),
    activo:  bool = Query(default=True, description="Estado activo del usuario"),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    roles_validos = ["Productor", "Comprador", "Administrador"]
    if nuevo_rol not in roles_validos:
        raise HTTPException(status_code=400, detail=f"Rol inválido. Permitidos: {roles_validos}")

    for u in usuarios:
        if u["id"] == id:
            u["rol"] = nuevo_rol
            if nombre:
                if not nombre.strip():
                    raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")
                u["nombre"] = nombre
            return {"mensaje": "Usuario actualizado", "activo": activo, "usuario": u}

    raise ErrorUsuarioNoExiste(id)


# ============================================================
# LOTES
# ============================================================

# --- GET /lotes/{id}/categoria/{categoria} ---
# Parámetros dinámicos : id, categoria
# Query params         : cantidad_min (int), ordenar_por (str)
@app.get("/lotes/{id}/categoria/{categoria}")
def obtener_lote_por_id_y_categoria(
    id: int,
    categoria: str,
    cantidad_min: int = Query(default=0,        description="Cantidad mínima disponible"),
    ordenar_por: str  = Query(default="producto", description="Campo para ordenar: producto | cantidad"),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    if cantidad_min < 0:
        raise HTTPException(status_code=400, detail="cantidad_min no puede ser negativo")

    campos_validos = ["producto", "cantidad"]
    if ordenar_por not in campos_validos:
        raise HTTPException(status_code=400, detail=f"ordenar_por debe ser uno de: {campos_validos}")

    resultado = [
        l for l in lotes
        if l["id"] == id
        and l["categoria"].lower() == categoria.lower()
        and l["cantidad"] >= cantidad_min
    ]

    if not resultado:
        raise HTTPException(status_code=404, detail="Lote no encontrado con esos criterios")

    resultado_ordenado = sorted(resultado, key=lambda x: x[ordenar_por])
    return resultado_ordenado


# --- POST /lotes ---
@app.post("/lotes")
def agregar_lote(id: int, producto: str, cantidad: int, categoria: str):
    if any(l["id"] == id for l in lotes):
        raise HTTPException(status_code=400, detail="Ya existe un lote con ese id")

    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

    if categoria not in categorias:
        raise HTTPException(status_code=400, detail=f"Categoría inválida. Categorías: {categorias}")

    nuevo_lote = {"id": id, "producto": producto, "cantidad": cantidad, "categoria": categoria}
    lotes.append(nuevo_lote)
    historial_seguimiento.append({"accion": "Creación de lote", "lote": id, "producto": producto})
    return {"mensaje": "Lote agregado", "lote": nuevo_lote}


# --- PUT /lotes/{id}/producto/{producto} ---
# Parámetros dinámicos : id, producto (nuevo nombre)
# Query params         : cantidad (int), categoria (str)
@app.put("/lotes/{id}/producto/{nuevo_producto}")
def editar_lote(
    id: int,
    nuevo_producto: str,
    cantidad:  int = Query(default=None, description="Nueva cantidad del lote"),
    categoria: str = Query(default=None, description="Nueva categoría del lote"),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    if cantidad is not None and cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

    if categoria and categoria not in categorias:
        raise HTTPException(status_code=400, detail=f"Categoría inválida. Categorías: {categorias}")

    for l in lotes:
        if l["id"] == id:
            l["producto"] = nuevo_producto
            if cantidad is not None:
                l["cantidad"] = cantidad
            if categoria:
                l["categoria"] = categoria
            historial_seguimiento.append({"accion": "Actualización de lote", "lote": id, "producto": nuevo_producto})
            return {"mensaje": "Lote actualizado", "lote": l}

    raise HTTPException(status_code=404, detail="Lote no encontrado")


# --- DELETE /lotes/{id}/categoria/{categoria} ---
# Parámetros dinámicos : id, categoria (confirmación de categoría antes de eliminar)
# Query params         : confirmar (bool), registrar (bool)
@app.delete("/lotes/{id}/categoria/{categoria}")
def eliminar_lote(
    id: int,
    categoria: str,
    confirmar: bool = Query(default=False, description="Debe ser true para confirmar la eliminación"),
    registrar: bool = Query(default=True,  description="Registrar la eliminación en el historial"),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    if not confirmar:
        raise HTTPException(status_code=400, detail="Debe confirmar la eliminación con confirmar=true")

    for i, l in enumerate(lotes):
        if l["id"] == id and l["categoria"].lower() == categoria.lower():
            lotes.pop(i)
            if registrar:
                historial_seguimiento.append({"accion": "Eliminación de lote", "lote": id})
            return {"mensaje": "Lote eliminado"}

    raise HTTPException(status_code=404, detail="Lote no encontrado con esos criterios")


# ============================================================
# COMPRADORES
# ============================================================

# --- GET /compradores/{id}/ciudad/{ciudad} ---
# Parámetros dinámicos : id, ciudad
# Query params         : limite (int), orden (str)
@app.get("/compradores/{id}/ciudad/{ciudad}")
def obtener_comprador_por_id_y_ciudad(
    id: int,
    ciudad: str,
    limite: int = Query(default=10, ge=1, le=100, description="Número máximo de resultados (1-100)"),
    orden:  str = Query(default="nombre",          description="Campo para ordenar: nombre | ciudad"),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    campos_validos = ["nombre", "ciudad"]
    if orden not in campos_validos:
        raise HTTPException(status_code=400, detail=f"orden debe ser uno de: {campos_validos}")

    resultado = [
        c for c in compradores
        if c["id"] == id and c["ciudad"].lower() == ciudad.lower()
    ]

    if not resultado:
        raise HTTPException(status_code=404, detail="Comprador no encontrado con esos criterios")

    resultado_ordenado = sorted(resultado, key=lambda x: x[orden])[:limite]
    return resultado_ordenado


# --- POST /compradores ---
@app.post("/compradores")
def agregar_comprador(id: int, nombre: str, ciudad: str):
    if any(c["id"] == id for c in compradores):
        raise HTTPException(status_code=400, detail="Ya existe un comprador con ese id")

    if not nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    if not ciudad.strip():
        raise HTTPException(status_code=400, detail="La ciudad no puede estar vacía")

    compradores.append({"id": id, "nombre": nombre, "ciudad": ciudad})
    return {"mensaje": "Comprador agregado", "comprador": {"id": id, "nombre": nombre, "ciudad": ciudad}}


# --- DELETE /compradores/{id}/ciudad/{ciudad} ---
# Parámetros dinámicos : id, ciudad (confirmación antes de eliminar)
# Query params         : confirmar (bool), notificar (bool)
@app.delete("/compradores/{id}/ciudad/{ciudad}")
def eliminar_comprador(
    id: int,
    ciudad: str,
    confirmar: bool = Query(default=False, description="Debe ser true para confirmar la eliminación"),
    notificar: bool = Query(default=False, description="Simula notificación al comprador eliminado"),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    if not confirmar:
        raise HTTPException(status_code=400, detail="Debe confirmar la eliminación con confirmar=true")

    for i, c in enumerate(compradores):
        if c["id"] == id and c["ciudad"].lower() == ciudad.lower():
            eliminado = compradores.pop(i)
            mensaje = "Comprador eliminado"
            if notificar:
                mensaje += f" — notificación enviada a {eliminado['nombre']}"
            return {"mensaje": mensaje}

    raise HTTPException(status_code=404, detail="Comprador no encontrado con esos criterios")


# ============================================================
# RESERVAS
# ============================================================

# --- GET /reservas/{id}/comprador/{comprador} ---
# Parámetros dinámicos : id, comprador
# Query params         : fecha (str), estado (str)
@app.get("/reservas/{id}/comprador/{comprador}")
def obtener_reserva(
    id: int,
    comprador: str,
    fecha:  str = Query(default=None, description="Filtrar por fecha de reserva (dd/mm/aaaa)"),
    estado: str = Query(default=None, description="Filtrar por estado: activa | cancelada"),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    estados_validos = ["activa", "cancelada"]
    if estado and estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Permitidos: {estados_validos}")

    resultado = [
        r for r in reservas
        if r["id"] == id and r["comprador"].lower() == comprador.lower()
    ]

    if fecha:
        resultado = [r for r in resultado if r.get("mensaje") == fecha]

    if not resultado:
        raise HTTPException(status_code=404, detail="Reserva no encontrada con esos criterios")

    return resultado


# --- POST /reservas/{id}/comprador/{comprador} ---
# Parámetros dinámicos : id, comprador
# Query params         : producto (str), cantidad (int)
@app.post("/reservas/{id}/comprador/{comprador}")
def crear_reserva(
    id: int,
    comprador: str,
    producto: str = Query(...,        description="Nombre del producto a reservar"),
    cantidad: int = Query(..., ge=1,  description="Cantidad a reservar (mínimo 1)"),
):
    if id <= 0:
        raise HTTPException(status_code=400, detail="El id debe ser un número positivo")

    if not comprador.strip():
        raise HTTPException(status_code=400, detail="El nombre del comprador no puede estar vacío")

    if any(r["id"] == id for r in reservas):
        raise HTTPException(status_code=400, detail="Ya existe una reserva con ese id")

    for l in lotes:
        if l["producto"].lower() == producto.lower():
            if l["cantidad"] < cantidad:
                raise HTTPException(status_code=400, detail="No hay suficiente cantidad disponible")

            l["cantidad"] -= cantidad
            nueva_reserva = {
                "id": id,
                "comprador": comprador,
                "producto": producto,
                "cantidad": cantidad,
                "mensaje": "09/05/2026",
            }
            reservas.append(nueva_reserva)
            historial_reservas.append(nueva_reserva)
            compras.append(nueva_reserva)
            ventas.append(nueva_reserva)
            historial_seguimiento.append({
                "accion": "Compra realizada",
                "producto": producto,
                "cantidad": cantidad,
                "mensaje": "09/05/2026",
            })
            return {"mensaje": "Reserva creada correctamente", "reserva": nueva_reserva}

    raise HTTPException(status_code=404, detail="Producto no encontrado en los lotes disponibles")


# ============================================================
# CATEGORÍAS
# ============================================================

# --- GET /categorias/{nombre}/lotes/{cantidad_min} ---
# Parámetros dinámicos : nombre (categoría), cantidad_min
# Query params         : ordenar (bool), limite (int)
@app.get("/categorias/{nombre}/lotes/{cantidad_min}")
def obtener_lotes_por_categoria(
    nombre:      str,
    cantidad_min: int,
    ordenar: bool = Query(default=False, description="Ordenar resultados por cantidad"),
    limite:  int  = Query(default=10, ge=1, le=100, description="Límite de resultados (1-100)"),
):
    if nombre not in categorias:
        raise HTTPException(status_code=404, detail=f"Categoría no encontrada. Categorías: {categorias}")

    if cantidad_min < 0:
        raise HTTPException(status_code=400, detail="cantidad_min no puede ser negativo")

    resultado = [
        l for l in lotes
        if l["categoria"].lower() == nombre.lower() and l["cantidad"] >= cantidad_min
    ]

    if ordenar:
        resultado = sorted(resultado, key=lambda x: x["cantidad"], reverse=True)

    return resultado[:limite]


# --- POST /categorias ---
@app.post("/categorias")
def agregar_categoria(nombre: str):
    if not nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre de la categoría no puede estar vacío")

    if nombre in categorias:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    categorias.append(nombre)
    return {"mensaje": "Categoría agregada", "categoria": nombre}


# ============================================================
# HISTORIAL (solo lectura)
# ============================================================

@app.get("/historial_seguimiento")
def ver_historial_seguimiento():
    return historial_seguimiento

@app.get("/compras")
def ver_compras():
    return compras

@app.get("/ventas")
def ver_ventas():
    return ventas

@app.get("/historial_reservas")
def ver_historial_reservas():
    return historial_reservas
