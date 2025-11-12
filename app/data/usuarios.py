# app/repositorios/usuarios_sql.py
from typing import Optional
from app.core.db import get_conn, obtener_conexion
from app.models.usuario import UsuarioEnBD


def obtener_por_email(email: str) -> Optional[UsuarioEnBD]:
    """
    Obtiene un usuario por su email
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query = """
        SELECT id, nombre, email, clave, telefono, direccion, rol, fecha_registro, activo
        FROM usuarios
        WHERE email = %s AND activo = 1
    """
    
    cursor.execute(query, (email,))
    resultado = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    if resultado:
        return UsuarioEnBD(**resultado)
    
    return None


def crear_usuario(nombre: str, email: str, clave: str, telefono: str, direccion: str, rol: str = "cliente") -> UsuarioEnBD:
    """
    Crea un nuevo usuario en la base de datos
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query = """
        INSERT INTO usuarios (nombre, email, clave, telefono, direccion, rol, activo)
        VALUES (%s, %s, %s, %s, %s, %s, 1)
    """
    
    try:
        cursor.execute(query, (nombre, email, clave, telefono, direccion, rol))
        conexion.commit()
        
        # Obtener el ID del usuario recién creado
        usuario_id = cursor.lastrowid
        
        # Consultar el usuario completo
        cursor.execute("""
            SELECT id, nombre, email, clave, telefono, direccion, rol, fecha_registro, activo
            FROM usuarios
            WHERE id = %s
        """, (usuario_id,))
        
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if resultado:
            return UsuarioEnBD(**resultado)
        else:
            raise Exception("No se pudo recuperar el usuario creado")
            
    except Exception as e:
        conexion.rollback()
        cursor.close()
        conexion.close()
        raise e