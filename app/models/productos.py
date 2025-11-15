from pydantic import BaseModel, field_validator
from typing import Optional, List

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    precio_anterior: Optional[float] = None
    subcategoria_id: Optional[int] = None
    rating: Optional[float] = 0.0
    reviews: Optional[int] = 0
    stock: Optional[int] = 0
    artesano_id: Optional[int] = None
    destacado: bool = False
    activo: bool = True
    fecha_creacion: Optional[str] = None  
    imagen: Optional[str] = None  

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        if not valor or len(valor.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        if len(valor.strip()) > 100:
            raise ValueError("El nombre no puede superar los 100 caracteres.")
        return valor.strip()

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor is None:
            raise ValueError("El precio es obligatorio.")
        if valor < 100:
            raise ValueError("El precio no puede ser menor de 100.")
        return valor

    @field_validator("subcategoria_id")
    @classmethod
    def validar_subcategoria(cls, valor):
        if valor is not None and (valor < 1 or valor > 8):
            raise ValueError("La subcategoría debe estar entre 1 y 8.")
        return valor

    @field_validator("stock")
    @classmethod
    def validar_stock(cls, valor):
        if valor is not None and valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        return valor

class PaginaProductos(BaseModel):
    total: int
    items: List[Producto]