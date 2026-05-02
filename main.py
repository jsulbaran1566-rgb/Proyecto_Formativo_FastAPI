from fastapi import FastAPI

app = FastAPI()

# Listas con datos
usuarios = [
    {"id": 0, "nombre": "Juan", "rol": "Productor"},
    {"id": 1, "nombre": "Ana", "rol": "Comprador"}
]

lotes = [
    {"id": 0, "producto": "Papa", "cantidad": 500},
    {"id": 1, "producto": "Tomate", "cantidad": 200}
]

compradores = [
    {"id": 0, "nombre": "Carlos", "ciudad": "Bogotá"},
    {"id": 1, "nombre": "Maria", "ciudad": "Medellín"}
]

reservas = [
    {"id": 0, "comprador": "Carlos", "producto": "Papa"}
]

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

# ========= POST =========
@app.post("/usuarios")
def agregar_usuario(id: int, nombre: str, rol: str):
    usuarios.append({"id": id, "nombre": nombre, "rol": rol})
    return "Usuario agregado"

@app.post("/lotes")
def agregar_lote(id: int, producto: str, cantidad: int):
    lotes.append({"id": id, "producto": producto, "cantidad": cantidad})
    return "Lote agregado"

@app.post("/compradores")
def agregar_comprador(id: int, nombre: str, ciudad: str):
    compradores.append({"id": id, "nombre": nombre, "ciudad": ciudad})
    return "Comprador agregado"

# ========= PUT =========
@app.put("/usuarios/{id}")
def editar_usuario(id: int, nombre: str, rol: str):
    usuarios[id] = {"id": id, "nombre": nombre, "rol": rol}
    return "Usuario actualizado"

@app.put("/lotes/{id}")
def editar_lote(id: int, producto: str, cantidad: int):
    lotes[id] = {"id": id, "producto": producto, "cantidad": cantidad}
    return "Lote actualizado"

# ========= DELETE =========
@app.delete("/compradores/{id}")
def eliminar_comprador(id: int):
    compradores.pop(id)
    return "Comprador eliminado"

@app.delete("/lotes/{id}")
def eliminar_lote(id: int):
    lotes.pop(id)
    return "Lote eliminado"