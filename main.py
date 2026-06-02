from fastapi import FastAPI


app = FastAPI()
  

# Listas con datos
usuarios = [
    {"id": 1, "nombre": "Valentina", "rol": "Productor"},
    {"id": 2, "nombre": "Danna", "rol": "Comprador"}
]

lotes = [
    {"id": 1, "producto": "Papa", "cantidad": 500, "categoria": "Tubérculos"},
    {"id": 2, "producto": "Tomate", "cantidad": 200, "categoria": "Verduras"}
]

compradores = [
    {"id": 1, "nombre": "Jesus", "ciudad": "Bogotá"},
    {"id": 2, "nombre": "Sofia", "ciudad": "Medellín"}
]

reservas = [
    {"id": 1, "comprador": "Jesus", "producto": "Papa"}
]

categorias = ["Tubérculos", "Frutas", "Verduras", "Hortalizas"]

# HISTORIALES Y REGISTROS
historial_seguimiento = []
compras = []
ventas = []
historial_reservas = []


# ========= GET =========
@app.get("/usuarios")
def ver_usuarios():
    return usuarios

@app.get("/lotes")
def ver_lotes():
    return lotes

@app.get("/compradores")
def ver_compradores():
    return compradores

@app.get("/categorias")
def ver_categorias():
    return categorias

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


# ========= POST =========
@app.post("/usuarios")
def agregar_usuario(id: int, nombre: str, rol: str):
    usuarios.append({"id": id, "nombre": nombre, "rol": rol})
    return "Usuario agregado"

@app.post("/lotes")
def agregar_lote(id: int, producto: str, cantidad: int, categoria: str):
    lotes.append({
        "id": id,
        "producto": producto,
        "cantidad": cantidad,
        "categoria": categoria
    })

    historial_seguimiento.append({
        "accion": "Creación de lote",
        "lote": id,
        "producto": producto
    })

    return "Lote agregado"

@app.post("/compradores")
def agregar_comprador(id: int, nombre: str, ciudad: str):
    compradores.append({"id": id, "nombre": nombre, "ciudad": ciudad})
    return "Comprador agregado"

@app.post("/categorias")
def agregar_categoria(nombre: str):
    categorias.append(nombre)
    return "Categoría agregada"


# RESERVAS
@app.post("/reservas")
def crear_reserva(id: int, comprador: str, producto: str, cantidad: int):

    for l in lotes:
        if l["producto"] == producto:

            if l["cantidad"] >= cantidad:
                l["cantidad"] -= cantidad

                nueva_reserva = {
                    "id": id,
                    "comprador": comprador,
                    "producto": producto,
                    "cantidad": cantidad,
                    "mensaje": "02/05/2026"
                }

                reservas.append(nueva_reserva)
                historial_reservas.append(nueva_reserva)

                compras.append(nueva_reserva)
                ventas.append(nueva_reserva)

                historial_seguimiento.append({
                    "accion": "Compra realizada",
                    "producto": producto,
                    "cantidad": cantidad,
                    "mensaje": "02/05/2026"
                })

                return "Compra realizada correctamente"

            else:
                return "No hay suficiente cantidad disponible"

    return "Producto no encontrado"


# ========= PUT =========
@app.put("/usuarios/{id}")
def editar_usuario(id: int, nombre: str, rol: str):
    usuarios[id] = {"id": id, "nombre": nombre, "rol": rol}
    return "Usuario actualizado"

@app.put("/lotes/{id}")
def editar_lote(id: int, producto: str, cantidad: int):
    lotes[id]["producto"] = producto
    lotes[id]["cantidad"] = cantidad

    historial_seguimiento.append({
        "accion": "Actualización de lote",
        "lote": id,
        "producto": producto
    })

    return "Lote actualizado"


# ========= DELETE =========
@app.delete("/compradores/{id}")
def eliminar_comprador(id: int):
    compradores.pop(id)
    return "Comprador eliminado"

@app.delete("/lotes/{id}")
def eliminar_lote(id: int):
    lotes.pop(id)

    historial_seguimiento.append({
        "accion": "Eliminación de lote",
        "lote": id
    })

    return "Lote eliminado"
