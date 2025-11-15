from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.core.db import get_conn
from app.models.productos import PaginaProductos, Producto
import mysql.connector
import asyncio

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/buscar", response_model=dict)
async def buscar_productos(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    limite: int = Query(20, ge=1, le=100)
):
    """
    Busca productos por nombre, descripción, categoría o subcategoría
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
            SELECT 
                p.id,
                p.nombre,
                p.descripcion,
                p.precio,
                p.precio_anterior,
                p.stock,
                p.rating,
                p.reviews,
                p.destacado,
                s.nombre as subcategoria,
                c.nombre as categoria,
                (SELECT ruta FROM imagenes WHERE producto_id = p.id LIMIT 1) as imagen
            FROM productos p
            LEFT JOIN subcategorias s ON p.subcategoria_id = s.id
            LEFT JOIN categorias c ON s.categoria_id = c.id
            WHERE p.activo = 1 
            AND (
                p.nombre LIKE %s 
                OR p.descripcion LIKE %s
                OR s.nombre LIKE %s
                OR c.nombre LIKE %s
            )
            ORDER BY 
                CASE 
                    WHEN p.nombre LIKE %s THEN 1
                    WHEN p.descripcion LIKE %s THEN 2
                    ELSE 3
                END,
                p.nombre
            LIMIT %s
        """
        
        search_term = f"%{q}%"
        search_start = f"{q}%"
        
        cursor.execute(sql, (
            search_term, search_term, search_term, search_term,
            search_start, search_start,
            limite
        ))
        
        productos = cursor.fetchall()
        
        
        for producto in productos:
            if producto.get('imagen'):
                ruta_limpia = producto['imagen'].replace("media/", "")
                producto['imagen'] = f"http://192.168.18.19:8001/media/{ruta_limpia}"
            else:
                producto['imagen'] = None
        
        return {
            "success": True,
            "total": len(productos),
            "query": q,
            "productos": productos
        }
        
    except mysql.connector.Error as e:
        return {
            "success": False,
            "error": str(e),
            "productos": []
        }
    
    finally:
        cursor.close()
        conn.close()

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
            imagen_url = None
            if r["imagen"]:
                ruta_limpia = r["imagen"].replace("media/", "")
                imagen_url = f"http://192.168.18.19:8001/media/{ruta_limpia}"
            
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
                imagen=imagen_url
            )
            productos.append(producto)

        return PaginaProductos(total=total, items=productos)
    
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/destacados/lista", response_model=dict)
async def obtener_productos_destacados(
    limite: int = Query(6, ge=1, le=20)
):
    """
    Obtiene los productos destacados con todas sus imágenes
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        # Obtener productos destacados
        sql_productos = """
            SELECT 
                p.id,
                p.nombre,
                p.descripcion,
                s.nombre as subcategoria,
                c.nombre as categoria
            FROM productos p
            LEFT JOIN subcategorias s ON p.subcategoria_id = s.id
            LEFT JOIN categorias c ON s.categoria_id = c.id
            WHERE p.destacado = 1 AND p.activo = 1
            ORDER BY p.fecha_creacion DESC
            LIMIT %s
        """
        
        cursor.execute(sql_productos, (limite,))
        productos = cursor.fetchall()
        
        # Para cada producto, obtener sus imágenes
        for producto in productos:
            sql_imagenes = """
                SELECT id, ruta, tipo, ancho, alto
                FROM imagenes
                WHERE producto_id = %s
                ORDER BY fecha_carga ASC
            """
            cursor.execute(sql_imagenes, (producto['id'],))
            imagenes = cursor.fetchall()
            
            
            imagenes_procesadas = []
            for img in imagenes:
                ruta_limpia = img['ruta'].replace("media/", "")
                img_url = f"http://192.168.18.19:8001/media/{ruta_limpia}"
                imagenes_procesadas.append({
                    'id': img['id'],
                    'ruta': img_url,
                    'tipo': img['tipo'],
                    'ancho': img['ancho'],
                    'alto': img['alto']
                })
            
            producto['imagenes'] = imagenes_procesadas
        
        return {
            "success": True,
            "total": len(productos),
            "productos": productos
        }
        
    except mysql.connector.Error as e:
        return {
            "success": False,
            "error": str(e),
            "productos": []
        }
    
    finally:
        cursor.close()
        conn.close()


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
            imagen_url = None
            if r["imagen"]:
                ruta_limpia = r["imagen"].replace("media/", "")
                imagen_url = f"http://192.168.18.19:8001/media/{ruta_limpia}"
            
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
                imagen=imagen_url
            )
            productos.append(producto)

        return PaginaProductos(total=total, items=productos)
    
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    finally:
        cursor.close()
        conn.close()


@router.get("/{producto_id}", response_model=Producto)
async def obtener_producto(producto_id: int):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
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

        imagen_url = None
        if row["imagen"]:
            ruta_limpia = row["imagen"].replace("media/", "")
            imagen_url = f"http://192.168.18.19:8001/media/{ruta_limpia}"

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
            imagen=imagen_url
        )

        return producto
    
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    finally:
        cursor.close()
        conn.close()


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

@router.delete("/{producto_id}", response_model=dict)
async def eliminar_producto(producto_id: int):
    print(f"🔍 DELETE - Recibiendo petición para eliminar producto ID: {producto_id}")
    
    conn = get_conn()
    cursor = conn.cursor()

    try:
        # Verificar si el producto existe
        print(f" Verificando si existe producto ID: {producto_id}")
        cursor.execute("SELECT id, nombre, activo FROM productos WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        
        if not producto:
            print(f" Producto ID {producto_id} NO encontrado")
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        print(f" Producto encontrado: ID={producto[0]}, Nombre={producto[1]}, Activo={producto[2]}")

        # Verificar si hay dependencias
        cursor.execute("SELECT COUNT(*) FROM carrito WHERE producto_id = %s", (producto_id,))
        carrito_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM detalle_pedido WHERE producto_id = %s", (producto_id,))
        pedidos_count = cursor.fetchone()[0]
        
        print(f" Dependencias: {carrito_count} en carrito, {pedidos_count} en pedidos")

        # Si hay productos en el carrito, eliminarlos primero
        if carrito_count > 0:
            print(f"🗑 Eliminando {carrito_count} items del carrito...")
            cursor.execute("DELETE FROM carrito WHERE producto_id = %s", (producto_id,))
            print(f" Items eliminados del carrito")

        # Ahora hacer el soft delete del producto
        sql = "UPDATE productos SET activo = 0 WHERE id = %s"
        print(f"Ejecutando SQL: {sql} con ID={producto_id}")
        
        cursor.execute(sql, (producto_id,))
        rows_affected = cursor.rowcount
        print(f" Filas afectadas: {rows_affected}")
        
        conn.commit()
        print(f" COMMIT exitoso - Producto ID {producto_id} marcado como inactivo")
        
        # Verificar que se actualizó
        cursor.execute("SELECT activo FROM productos WHERE id = %s", (producto_id,))
        nuevo_estado = cursor.fetchone()
        print(f" Verificación post-update: activo = {nuevo_estado[0]}")
        
        return {
            "mensaje": "Producto eliminado exitosamente",
            "producto_id": producto_id,
            "rows_affected": rows_affected,
            "items_carrito_eliminados": carrito_count
        }
    
    except mysql.connector.Error as e:
        print(f" Error de MySQL: {str(e)}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")
    except Exception as e:
        print(f" Error general: {str(e)}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    finally:
        cursor.close()
        conn.close()
        print(f" Conexión cerrada para producto ID: {producto_id}")