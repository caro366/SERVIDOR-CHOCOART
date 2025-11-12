from pydantic import BaseModel
from typing import List

class NombreValor(BaseModel):
    nombre: str
    valor: float

class RespuestaDashboard(BaseModel):
    ventas_mes: List[NombreValor]
    ventas_tiendas: List[NombreValor]
    ventas_categorias: List[NombreValor]
    tarjetas: List[NombreValor]