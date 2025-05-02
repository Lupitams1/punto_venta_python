from pydantic import BaseModel
from typing import List
from typing import List, Optional

class LibroEntrada(BaseModel):
    titulo: str
    autor: str
    categoria: str
    precio: float
    stock: int
    stock_min: int
    stock_max: int

class Libro(LibroEntrada):
    id: int
class ItemVenta(BaseModel):
    id_libro: int
    cantidad: int

class VentaEntrada(BaseModel):
    items: List[ItemVenta]

class Remision(BaseModel):
    fecha: str
    items: List[str]
    subtotal: float
    iva: float
    total: float
   

class VentaEntrada(BaseModel):
    items: List[ItemVenta]
    email: Optional[str] = None
    telefono: Optional[str] = None

class MermaEntrada(BaseModel):
    id_libro: int
    cantidad: int
    motivo: Optional[str] = "Sin especificar"

