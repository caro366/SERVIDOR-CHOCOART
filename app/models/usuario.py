from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Usuario(BaseModel):
    id: Optional[int] = None
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    rol: Optional[str] = "cliente"
    fecha_registro: Optional[datetime] = None
    activo: Optional[bool] = True

class UsuarioEnBD(Usuario):
    clave: Optional[str] = None  
