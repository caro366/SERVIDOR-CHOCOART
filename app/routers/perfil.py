# app/rutas/perfil.py
from fastapi import APIRouter, Depends
from app.models.usuario import Usuario
from .autenticacion import obtener_usuario_actual

router = APIRouter(tags=["Perfil"])

@router.get("/mi-perfil", response_model=Usuario)
def obtener_perfil(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return usuario_actual

@router.get("/zona-protegida")
def zona_protegida(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return {"mensaje": f"Bienvenido {usuario_actual.identificacion}, tienes acceso autorizado."}
