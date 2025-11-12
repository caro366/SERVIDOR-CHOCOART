from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.core.db import get_conn
from app.models.productos import PaginaProductos, Producto
import mysql.connector
import asyncio

router = APIRouter(prefix="/productos", tags=["Productos"])

# Listar todos los productos con paginación
@router.get("", response_model=PaginaProductos)
async def listar_productos(
    filtro: str = "",
    pagina: int = 1,
    cantidad: int = 20
):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        # Consulta CORREGIDA: imagen_ruta → imagen
        sql_items = """
            SELECT p.id, p.nombre, p.precio, p.descripcion, p.rating, 
                   p.reviews, p.stock, p.destacado, p.subcategoria_id,
                   s.nombre as subcategoria_nombre,
                   (SELECT ruta FROM imagenes WHERE producto_id = p.id LIMIT 1) as imagen
            FROM productos p
            LEFT JOIN subcategorias s ON p.subcategoria_id = s.id
            WHERE p.nombre LIKE %s AND p.activo = 1
            ORDER BY p.id DESC
            LIMIT %s OFFSET %s
        """
        
        inicio = (pagina - 1) * cantidad
        patron = f"%{filtro}%"
        cursor.execute(sql_items, (patron, cantidad, inicio))
        rows = cursor.fetchall()

        # Consulta para el total
        sql_total = """
            SELECT COUNT(*) AS total 
            FROM productos p 
            WHERE p.nombre LIKE %s AND p.activo = 1
        """
        cursor.execute(sql_total, (patron,))
        resultado = cursor.fetchone()
        total = resultado["total"]

        productos = []
        for r in rows:
            # ✅ Construir URL completa de la imagen - CORREGIDO
            imagen_url = None
            if r["imagen"]:  # ← CAMBIADO: era r["imagen_ruta"]
                # Remover "media/" si ya está en la ruta
                ruta_limpia = r["imagen"].replace("media/", "")  # ← CAMBIADO
                imagen_url = f"http://192.168.18.19:8001/media/{ruta_limpia}"  # ← TU IP AQUÍ
            
            producto = Producto(
                id=r["id"],
                nombre=r["nombre"],
                precio=float(r["precio"]),
                descripcion=r["descripcion"],
                rating=float(r["rating"]) if r["rating"] else 0.0,
                reviews=r["reviews"] or 0,
                stock=r["stock"] or 0,
                destacado=bool(r["destacado"]),
                subcategoria_id=r["subcategoria_id"],
                imagen=imagen_url  # ✅ URL completa
            )
            productos.append(producto)

        return PaginaProductos(total=total, items=productos)
    
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Listar productos por subcategoría
@router.get("/subcategoria/{subcategoria_id}", response_model=PaginaProductos)
async def listar_productos_por_subcategoria(
    subcategoria_id: int,
    filtro: str = "",
    pagina: int = 1,
    cantidad: int = 20
):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        # Consulta CORREGIDA: imagen_ruta → imagen
        sql_items = """
            SELECT p.id, p.nombre, p.precio, p.descripcion, p.rating, 
                   p.reviews, p.stock, p.destacado, s.nombre as subcategoria_nombre,
                   (SELECT ruta FROM imagenes WHERE producto_id = p.id LIMIT 1) as imagen
            FROM productos p
            LEFT JOIN subcategorias s ON p.subcategoria_id = s.id
            WHERE p.subcategoria_id = %s AND p.nombre LIKE %s AND p.activo = 1
            ORDER BY p.nombre 
            LIMIT %s OFFSET %s
        """
        
        inicio = (pagina - 1) * cantidad
        patron = f"%{filtro}%"
        cursor.execute(sql_items, (subcategoria_id, patron, cantidad, inicio))
        rows = cursor.fetchall()

        sql_total = """
            SELECT COUNT(*) AS total 
            FROM productos p 
            WHERE p.subcategoria_id = %s AND p.nombre LIKE %s AND p.activo = 1
        """
        cursor.execute(sql_total, (subcategoria_id, patron))
        resultado = cursor.fetchone()
        total = resultado["total"]

        productos = []
        for r in rows:
            # ✅ Construir URL completa de la imagen - CORREGIDO
            imagen_url = None
            if r["imagen"]:  # ← CAMBIADO: era r["imagen_ruta"]
                # Remover "media/" si ya está en la ruta
                ruta_limpia = r["imagen"].replace("media/", "")  # ← CAMBIADO
                imagen_url = f"http://192.168.18.19:8001/media/{ruta_limpia}"  # ← TU IP AQUÍ
            
            producto = Producto(
                id=r["id"],
                nombre=r["nombre"],
                precio=float(r["precio"]),
                descripcion=r["descripcion"],
                rating=float(r["rating"]) if r["rating"] else 0.0,
                reviews=r["reviews"] or 0,
                stock=r["stock"] or 0,
                destacado=bool(r["destacado"]),
                subcategoria_id=subcategoria_id,
                imagen=imagen_url  # ✅ URL completa
            )
            productos.append(producto)

        return PaginaProductos(total=total, items=productos)
    
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Obtener un producto por ID
@router.get("/{producto_id}", response_model=Producto)
async def obtener_producto(producto_id: int):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        # Consulta CORREGIDA: imagen_ruta → imagen
        sql = """
            SELECT p.id, p.nombre, p.precio, p.descripcion, p.rating, 
                   p.reviews, p.stock, p.destacado, p.subcategoria_id,
                   p.artesano_id, p.activo,
                   (SELECT ruta FROM imagenes WHERE producto_id = p.id LIMIT 1) as imagen
            FROM productos p
            WHERE p.id = %s
        """
        cursor.execute(sql, (producto_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # ✅ Construir URL completa de la imagen - CORREGIDO
        imagen_url = None
        if row["imagen"]:  # ← CAMBIADO: era row["imagen_ruta"]
            ruta_limpia = row["imagen"].replace("media/", "")  # ← CAMBIADO
            imagen_url = f"http://192.168.18.19:8001/media/{ruta_limpia}"  # ← TU IP AQUÍ

        producto = Producto(
            id=row["id"],
            nombre=row["nombre"],
            precio=float(row["precio"]),
            descripcion=row["descripcion"],
            rating=float(row["rating"]) if row["rating"] else 0.0,
            reviews=row["reviews"] or 0,
            stock=row["stock"] or 0,
            destacado=bool(row["destacado"]),
            subcategoria_id=row["subcategoria_id"],
            artesano_id=row["artesano_id"],
            activo=bool(row["activo"]),
            imagen=imagen_url  # ✅ URL completa
        )

        return producto
    
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo producto (mantener igual)
@router.post("", response_model=dict)
async def crear_producto(producto: Producto):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        sql = """
            INSERT INTO productos 
            (nombre, descripcion, precio, stock, subcategoria_id, artesano_id, destacado, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        valores = (
            producto.nombre,
            producto.descripcion or "",
            producto.precio,
            producto.stock or 0,
            producto.subcategoria_id,
            producto.artesano_id or 2,
            producto.destacado,
            producto.activo
        )
        
        cursor.execute(sql, valores)
        conn.commit()
        
        return {
            "mensaje": "Producto creado exitosamente",
            "id": cursor.lastrowid
        }
    
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Actualizar un producto (mantener igual)
@router.put("/{producto_id}", response_model=dict)
async def modificar_producto(producto_id: int, producto: Producto):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        campos = []
        valores = []

        if producto.nombre:
            campos.append("nombre = %s")
            valores.append(producto.nombre)
        
        if producto.descripcion is not None:
            campos.append("descripcion = %s")
            valores.append(producto.descripcion)
        
        if producto.precio is not None:
            campos.append("precio = %s")
            valores.append(producto.precio)
        
        if producto.stock is not None:
            campos.append("stock = %s")
            valores.append(producto.stock)
        
        if producto.subcategoria_id is not None:
            campos.append("subcategoria_id = %s")
            valores.append(producto.subcategoria_id)
        
        campos.append("destacado = %s")
        valores.append(producto.destacado)
        
        campos.append("activo = %s")
        valores.append(producto.activo)

        if not campos:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        valores.append(producto_id)
        sql = f"UPDATE productos SET {', '.join(campos)} WHERE id = %s"
        
        cursor.execute(sql, valores)
        conn.commit()
        
        return {"mensaje": "Producto actualizado exitosamente"}
    
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Eliminar un producto (mantener igual)
@router.delete("/{producto_id}", response_model=dict)
async def eliminar_producto(producto_id: int):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        sql = "UPDATE productos SET activo = 0 WHERE id = %s"
        cursor.execute(sql, (producto_id,))
        conn.commit()
        
        return {"mensaje": "Producto eliminado exitosamente"}
    
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")
    finally:
        cursor.close()
        conn.close()