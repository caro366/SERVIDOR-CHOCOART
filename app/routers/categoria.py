from fastapi import APIRouter
from typing import List
from app.core.db import get_conn

router = APIRouter(prefix="/categorias")

from pydantic import BaseModel

class Categoria(BaseModel):
    id: int
    nombre: str
    descripcion: str = None
    activa: bool = True

class Subcategoria(BaseModel):
    id: int
    categoria_id: int
    nombre: str
    descripcion: str = None
    activa: bool = True

@router.get("", response_model=List[Categoria])
async def listar_categorias():
    """
    Obtiene todas las categorías activas
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, nombre, descripcion, activa FROM categorias WHERE activa = 1")
        categorias = cursor.fetchall()
        return categorias
    finally:
        cursor.close()
        conn.close()

@router.get("/{categoria_id}/subcategorias", response_model=List[Subcategoria])
async def listar_subcategorias(categoria_id: int):
    """
    Obtiene las subcategorías de una categoría específica
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT id, categoria_id, nombre, descripcion, activa 
            FROM subcategorias 
            WHERE categoria_id = %s AND activa = 1
        """, (categoria_id,))
        subcategorias = cursor.fetchall()
        return subcategorias
    finally:
        cursor.close()
        conn.close()

@router.get("/subcategorias/todas", response_model=List[Subcategoria])
async def listar_todas_subcategorias():
    """
    Obtiene todas las subcategorías activas
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, categoria_id, nombre, descripcion, activa FROM subcategorias WHERE activa = 1")
        subcategorias = cursor.fetchall()
        return subcategorias
    finally:
        cursor.close()
        conn.close()