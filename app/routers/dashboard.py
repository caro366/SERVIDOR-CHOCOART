from fastapi import APIRouter, Depends
from app.models.usuario import Usuario
from .autenticacion import obtener_usuario_actual
from ..models.dashboard import RespuestaDashboard, NombreValor
from app.core.db import get_conn



router = APIRouter()


@router.get("/dashboard", response_model=RespuestaDashboard)
def obtener_valores(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    conn = None
    cursor = None

    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        
        #  1. Ventas del mes
       
        sql_ventas_mes = """
            SELECT 
                DAY(fecha_pedido) AS dia, 
                SUM(total) AS total
            FROM pedidos
            WHERE
                MONTH(fecha_pedido) = MONTH(CURDATE())
                AND YEAR(fecha_pedido) = YEAR(CURDATE())
                AND estado NOT IN ('cancelado')
            GROUP BY dia
            ORDER BY dia
        """

        cursor.execute(sql_ventas_mes)
        datos_ventas_mes = cursor.fetchall()

        ventas_mes = [
            NombreValor(
                nombre=str(row["dia"]),
                valor=float(row["total"]) if row["total"] else 0.0
            )
            for row in datos_ventas_mes
        ]

       
        #  2. Ventas por artesanos
        
        sql_ventas_artesanos = """
            SELECT 
                u.nombre AS artesano, 
                SUM(dp.subtotal) AS total
            FROM pedidos ped
            JOIN detalle_pedido dp ON ped.id = dp.pedido_id
            JOIN productos p ON dp.producto_id = p.id
            JOIN usuarios u ON p.artesano_id = u.id
            WHERE ped.estado NOT IN ('cancelado')
            GROUP BY u.id, u.nombre
        """

        cursor.execute(sql_ventas_artesanos)
        datos_ventas_artesanos = cursor.fetchall()

        ventas_artesanos = [
            NombreValor(
                nombre=row["artesano"],
                valor=float(row["total"]) if row["total"] else 0.0
            )
            for row in datos_ventas_artesanos
        ]

       
        # 3. Ventas por categorías
        
        sql_ventas_categorias = """
            SELECT 
                c.nombre AS categoria,
                ROUND(SUM(dp.subtotal), 2) AS total
            FROM pedidos p
            JOIN detalle_pedido dp ON p.id = dp.pedido_id
            JOIN productos pr ON dp.producto_id = pr.id
            JOIN subcategorias sc ON pr.subcategoria_id = sc.id
            JOIN categorias c ON sc.categoria_id = c.id
            WHERE p.estado NOT IN ('cancelado')
            GROUP BY c.id, c.nombre
            ORDER BY total DESC
            LIMIT 5
        """

        cursor.execute(sql_ventas_categorias)
        datos_ventas_categorias = cursor.fetchall()

        ventas_categorias = [
            NombreValor(
                nombre=row["categoria"],
                valor=float(row["total"]) if row["total"] else 0.0
            )
            for row in datos_ventas_categorias
        ]

       
        #  4. Tarjetas del dashboard
        
        tarjetas = []

        # Usuarios
        cursor.execute("SELECT COUNT(*) AS cantidad FROM usuarios WHERE activo = 1")
        usuarios = cursor.fetchone()
        tarjetas.append(NombreValor(nombre="Usuarios", valor=usuarios["cantidad"] if usuarios else 0))

        # Categorías
        cursor.execute("SELECT COUNT(*) AS cantidad FROM categorias WHERE activa = 1")
        categorias = cursor.fetchone()
        tarjetas.append(NombreValor(nombre="Categorías", valor=categorias["cantidad"] if categorias else 0))

        # Pedidos del mes
        sql_cantidad_pedidos = """
            SELECT COUNT(*) cantidad
            FROM pedidos
            WHERE
                MONTH(fecha_pedido) = MONTH(CURDATE())
                AND YEAR(fecha_pedido) = YEAR(CURDATE())
                AND estado NOT IN ('cancelado')
        """
        cursor.execute(sql_cantidad_pedidos)
        pedidos = cursor.fetchone()
        tarjetas.append(NombreValor(nombre="Pedidos mes", valor=pedidos["cantidad"] if pedidos else 0))

        # Ventas totales del mes
        sql_ventas_totales = """
            SELECT COALESCE(SUM(total), 0) AS total
            FROM pedidos
            WHERE
                MONTH(fecha_pedido) = MONTH(CURDATE())
                AND YEAR(fecha_pedido) = YEAR(CURDATE())
                AND estado NOT IN ('cancelado')
        """
        cursor.execute(sql_ventas_totales)
        ventas_totales = cursor.fetchone()
        tarjetas.append(
            NombreValor(
                nombre="Ventas mes",
                valor=float(ventas_totales["total"]) if ventas_totales else 0.0
            )
        )

       
        #  RETORNO FINAL DEL DASHBOARD
        
        return RespuestaDashboard(
            ventas_mes=ventas_mes,
            ventas_tiendas=ventas_artesanos,
            ventas_categorias=ventas_categorias,
            tarjetas=tarjetas
        )

    except Exception as e:
        logger.error(f"Error en dashboard: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
