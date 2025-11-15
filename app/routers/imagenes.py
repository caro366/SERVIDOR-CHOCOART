from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from uuid import uuid4
from PIL import Image
import io
import mysql.connector
from app.core.db import get_conn 
from app.models.usuario import Usuario
from .autenticacion import obtener_usuario_actual

router = APIRouter()

MAX_SIZE_BYTES = 5 * 1024 * 1024  
MEDIA_DIR = Path("media")

# Crear carpeta "media" si no existe
MEDIA_DIR.mkdir(exist_ok=True)


#  Endpoint para subir imagen
@router.post("/imagenes")
async def guardar(
    producto_id: int = Form(...),
    archivo: UploadFile = File(...),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    tipo = ""
    ancho = 0
    alto = 0
    formato = ""

    # 1️ Validar que sea imagen
    tipo_contenido = archivo.content_type or ""
    if not tipo_contenido.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida (MIME).")

    # 2️ Leer bytes
    data = await archivo.read()
    if len(data) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="Imagen demasiado grande (>5MB).")

    # 3️ Obtener dimensiones y formato
    img = Image.open(io.BytesIO(data))
    formato = (img.format or "PNG").lower()
    ancho, alto = img.size

    # 4️ Generar nombre único y guardar
    nombre = f"{uuid4().hex}.{formato}"
    ruta_completa = MEDIA_DIR / nombre

    with open(ruta_completa, "wb") as f:
        f.write(data)

    # 5️ Guardar en base de datos
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        INSERT INTO imagenes (producto_id, tipo, ancho, alto, ruta, fecha_carga)
        VALUES (%s, %s, %s, %s, %s, CURDATE())
    """
    cur.execute(sql, (producto_id, tipo_contenido, ancho, alto, str(ruta_completa)))
    conn.commit()
    cur.close()
    conn.close()

    return {
        "mensaje": "Imagen subida correctamente",
        "producto_id": producto_id,
        "nombre_archivo": nombre,
        "url": str(ruta_completa)
    }


#  Listar todas las imágenes
@router.get("/imagenes/listar")
def listar_imagenes():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM imagenes;")
        imagenes = cursor.fetchall()
        cursor.close()
        conn.close()

        if not imagenes:
            raise HTTPException(status_code=404, detail="No hay imágenes registradas.")

        return imagenes

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener imágenes: {e}")


#  Listar imágenes por producto
@router.get("/imagenes/producto/{producto_id}")
def listar_imagenes_por_producto(producto_id: int):
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM imagenes WHERE producto_id = %s;", (producto_id,))
        imagenes = cursor.fetchall()
        cursor.close()
        conn.close()

        if not imagenes:
            raise HTTPException(status_code=404, detail="No hay imágenes para este producto.")

        return imagenes

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener imágenes: {e}")
