# app/rutas/perfil.py
from fastapi import APIRouter, Depends
from app.models.usuario import Usuario
from .autenticacion import obtener_usuario_actual
from ..models.dashboard import RespuestaDashboard, NombreValor
from app.core.db import get_conn

router = APIRouter()

@router.get("/dashboard", response_model=RespuestaDashboard)
def obtener_valores(usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    conn = get_conn() 
    cursor = conn.cursor(dictionary=True)

    # Ventas del mes
    sql_ventas_mes = """SELECT 
                        DAY(fecha_pedido) AS dia, SUM(total) AS total
                    FROM
                        pedidos
                    WHERE
                        MONTH(fecha_pedido) = MONTH(CURDATE())
                            AND YEAR(fecha_pedido) = YEAR(CURDATE())
                    GROUP BY dia
                    ORDER BY dia"""
 
    cursor.execute(sql_ventas_mes)

    datos_ventas_mes = cursor.fetchall()
    ventas_mes = []

    for row in datos_ventas_mes:
        ventas_mes.append(
            NombreValor(
                nombre=str(row["dia"]),   # convierte int → str
                valor=float(row["total"]  )
            )
        )
    
    # Ventas por tiendas
    sql_ventas_tientas = """ 
                            SELECT 
                                t.nombre AS tienda, SUM(p.total) AS total
                            FROM
                                pedidos p
                                    JOIN
                                tiendas t ON p.tienda_id = t.id
                            GROUP BY t.id , t.nombre

                            """
    cursor.execute(sql_ventas_tientas)
    datos_ventas_tiendas = cursor.fetchall()

    ventas_tiendas = []
    for row in datos_ventas_tiendas:
        ventas_tiendas.append(
            NombreValor(
                nombre=row["tienda"],   
                valor=float(row["total"]  )
            )
        )

    #Ventas por categorias - CORREGIDA: usar detalle_pedido (singular)
    sql_ventas_categorias = """
            SELECT 
                c.nombre AS categoria,
                ROUND(SUM(dp.subtotal), 2) AS total
            FROM
                pedidos p
                    JOIN
                detalle_pedido dp ON dp.pedido_id = p.id
                    JOIN
                productos pr ON dp.producto_id = pr.id
                    JOIN
                categorias c ON pr.categoria_id = c.id
            GROUP BY c.id , c.nombre
            ORDER BY total DESC
            LIMIT 5
            """

    cursor.execute(sql_ventas_categorias)
    datos_ventas_categorias = cursor.fetchall()

    ventas_categorias = []
    for row in datos_ventas_categorias:
        ventas_categorias.append(
            NombreValor(
                nombre=row["categoria"],   
                valor=float(row["total"]  )
            )
        )

    #Tarjetas 

    tarjetas = []

    # Cantidad de usuarios
    sql_cantidad_usuarios = "SELECT COUNT(*) AS cantidad FROM usuarios"
    cursor.execute(sql_cantidad_usuarios)
    usuarios = cursor.fetchone()

    tarjetas.append(
        NombreValor(
            nombre="Usuarios", 
            valor=usuarios["cantidad"]
        )
    )

    # Cantidad de categorias
    sql_cantidad_categorias = "SELECT COUNT(*) AS cantidad FROM categorias"
    cursor.execute(sql_cantidad_categorias)
    categorias = cursor.fetchone()

    tarjetas.append(
        NombreValor(
            nombre="Categorías", 
            valor=categorias["cantidad"]
        )
    )

    # Cantidad de pedidos del mes
    sql_cantidad_pedidos = """
            SELECT 
                COUNT(*) cantidad
            FROM
                pedidos
            WHERE
                MONTH(fecha_pedido) = MONTH(CURDATE())
                    AND YEAR(fecha_pedido) = YEAR(CURDATE())
            """
    cursor.execute(sql_cantidad_pedidos)
    pedidos = cursor.fetchone()

    tarjetas.append(
        NombreValor(
            nombre="Pedidos mes", 
            valor=pedidos["cantidad"]
        )
    )


    return RespuestaDashboard(
        ventas_mes = ventas_mes,
        ventas_tiendas = ventas_tiendas,
        ventas_categorias = ventas_categorias,
        tarjetas = tarjetas
    )