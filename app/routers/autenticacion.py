# app/rutas/autenticacion.py
from fastapi import APIRouter, HTTPException, status, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from ..models.autenticacion import Token
from ..models.usuario import Usuario, UsuarioEnBD
from ..core.seguridad import verificar_contrasena, crear_token_acceso, encriptar_contrasena
from ..core.configuracion import CLAVE_SECRETA, ALGORITMO
from app.data.usuarios import obtener_por_email, crear_usuario

router = APIRouter(prefix="/autenticacion")

# Solo header Authorization: Bearer <token>
oauth2 = OAuth2PasswordBearer(tokenUrl="/autenticacion/iniciar-sesion")

@router.post("/iniciar-sesion")
async def iniciar_sesion(username: str = Form(...), password: str = Form(...)):
    # validar usuario y devolver token
    
    email = username  # en este caso usamos email como username

    usuario = obtener_por_email(email)
    # Validacion de usuario + clave (en BD esperamos hash bcrypt en columna 'clave')
    if not usuario or not usuario.clave or not verificar_contrasena(password, usuario.clave):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

    # sub = identificacion, uid = id
    access_token = crear_token_acceso(nombre_usuario=usuario.email, id_usuario=usuario.id)

    token = Token( 
        access_token = access_token,
        token_type = "bearer",
        rol = usuario.rol
    )
    

    return token


@router.post("/register")
async def registrar(
    nombre: str = Form(...),
    email: str = Form(...),
    clave: str = Form(...),
    telefono: str = Form(...),
    direccion: str = Form(...),
    rol: str = Form("cliente")
):
    """
    Registrar un nuevo usuario en el sistema
    """
    # Validar que el email no exista
    usuario_existente = obtener_por_email(email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    # Validar formato de email
    if "@" not in email or "." not in email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de correo electrónico inválido"
        )
    
    # Validar longitud de contraseña
    if len(clave) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    # Validar teléfono (10 dígitos)
    if not telefono.isdigit() or len(telefono) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El teléfono debe tener 10 dígitos"
        )
    
    # Encriptar la contraseña
    clave_encriptada = encriptar_contrasena(clave)
    
    # Crear el usuario en la base de datos
    try:
        nuevo_usuario = crear_usuario(
            nombre=nombre,
            email=email,
            clave=clave_encriptada,
            telefono=telefono,
            direccion=direccion,
            rol=rol
        )
        
        return {
            "message": "Usuario registrado exitosamente",
            "usuario": {
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email,
                "rol": nuevo_usuario.rol
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )


def obtener_usuario_actual(token: str = Depends(oauth2)) -> Usuario:
    error_credenciales = HTTPException(
        status_code=401,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        datos = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        email = datos.get("sub")  # usamos email como 'sub'
        uid = datos.get("uid")
        if not email or not uid:
            raise error_credenciales
    except JWTError:
        raise error_credenciales

    usuario_bd: Optional[UsuarioEnBD] = obtener_por_email(email)
    
    if not usuario_bd:
        raise error_credenciales

    # No exponemos 'clave' en la respuesta
    return Usuario(
        id=usuario_bd.id,
        nombre=usuario_bd.nombre,
        email=usuario_bd.email,
        telefono=usuario_bd.telefono,
        direccion=usuario_bd.direccion,
        rol=usuario_bd.rol,
        activo=usuario_bd.activo
    )