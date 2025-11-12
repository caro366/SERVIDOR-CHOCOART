# main.py
 
# INSTALACIÓN DE DEPENDENCIAS:
#   1. Instalar Python 3.9+ y MySQL.
#   2. Instalar librerías necesarias:
#        pip install fastapi uvicorn mysql-connector-python
#
 
# ---------------------------------------------------------------
# EJECUCIÓN DEL SERVIDOR:
#   Iniciar el servidor con:
#        uvicorn main:app --reload --port 8001
#        uvicorn main:app --reload --host 0.0.0.0 --port 8001
#
#   Documentación automática disponible en:
#        http://127.0.0.1:8001/docs   (Swagger UI)
#        http://127.0.0.1:8001/redoc  (ReDoc)
#
 

from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware  
from app.routers import productos, categoria, autenticacion, perfil, dashboard, carrito, pedidos,imagenes
from pathlib import Path
from fastapi.staticfiles import StaticFiles

class CORSStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

app = FastAPI(title="Gestión de productos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En entorno de desarrollo se acepta cualquier origen; en producción se recomienda restringir
    allow_credentials=True, # Habilita el uso de cookies o autenticación
    allow_methods=["*"],    # Métodos HTTP permitidos
    allow_headers=["*"],    # Encabezados permitidos
)

# Carpeta donde se guardarán las imágenes
MEDIA_DIR = Path("media")
MEDIA_DIR.mkdir(exist_ok=True)

# Servir las imágenes subidas
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

app.include_router(categoria.router)      # Rutas de categorías y subcategorías
app.include_router(productos.router)      # Rutas de productos
app.include_router(autenticacion.router)  # Autenticación
app.include_router(perfil.router)         # Perfil de usuario
app.include_router(dashboard.router)   
app.include_router(carrito.router)
app.include_router(pedidos.router)
app.include_router(imagenes.router)
