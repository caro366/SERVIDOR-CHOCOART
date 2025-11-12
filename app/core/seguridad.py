from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

from app.core.configuracion import CLAVE_SECRETA, ALGORITMO, MINUTOS_EXPIRACION_TOKEN

contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encriptar_contrasena(clave: str) -> str:
    return contexto.hash(clave)

def verificar_contrasena(clave: str, hash_guardado: str) -> bool:
    return contexto.verify(clave, hash_guardado)

def crear_token_acceso(nombre_usuario: str, id_usuario: int, minutos: Optional[int] = None) -> str:
    ahora = datetime.now(UTC)
    expira = ahora + timedelta(minutes=minutos or MINUTOS_EXPIRACION_TOKEN)
    carga = {"sub": nombre_usuario, "uid": id_usuario, "exp": expira, "iat": ahora}
    return jwt.encode(carga, CLAVE_SECRETA, algorithm=ALGORITMO)
