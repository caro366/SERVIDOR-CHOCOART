from fastapi import APIRouter, HTTPException
from app.core.db import get_conn
from datetime import datetime

router = APIRouter()

@router.post("/pedidos/crear")
async def crear_pedido(pedido_data: dict):
    try:
        usuario_id = pedido_data["usuario_id"]
        direccion_envio = pedido_data.get("direccion_envio")
        telefono_contacto = pedido_data.get("telefono_contacto")
        items = pedido_data["items"]
        
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        conn.start_transaction()
        
        cursor.execute(
            """INSERT INTO pedidos (usuario_id, total, estado, direccion_envio, telefono_contacto, fecha_pedido) 
            VALUES (%s, 0, 'pendiente', %s, %s, %s)""",
            (usuario_id, direccion_envio, telefono_contacto, datetime.now())
        )
        pedido_id = cursor.lastrowid

        for item in items:
            cursor.execute(
                "SELECT precio, stock FROM productos WHERE id = %s",
                (item["producto_id"],)
            )
            producto = cursor.fetchone()

            if producto["stock"] < item["cantidad"]:
                raise HTTPException(status_code=400, detail="Stock insuficiente")

            subtotal = producto["precio"] * item["cantidad"]

            cursor.execute(
                """INSERT INTO detalle_pedido 
                (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)""",
                (pedido_id, item["producto_id"], item["cantidad"], producto["precio"], subtotal)
            )

            cursor.execute(
                "UPDATE productos SET stock = stock - %s WHERE id = %s",
                (item["cantidad"], item["producto_id"])
            )

        cursor.execute(
            """UPDATE pedidos SET total =
            (SELECT SUM(subtotal) FROM detalle_pedido WHERE pedido_id = %s)
            WHERE id = %s""",
            (pedido_id, pedido_id)
        )

        cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", (usuario_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Pedido creado exitosamente", "pedido_id": pedido_id}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {str(e)}")


@router.get("/pedidos/usuario/{usuario_id}")
async def obtener_pedidos_usuario(usuario_id: int):
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        # Obtener pedidos del usuario con total_items
        cursor.execute("""
            SELECT 
                p.id,
                p.total,
                p.estado,
                p.direccion_envio,
                p.telefono_contacto,
                p.fecha_pedido,
                COUNT(dp.id) AS total_items
            FROM pedidos p
            LEFT JOIN detalle_pedido dp ON p.id = dp.pedido_id
            WHERE p.usuario_id = %s
            GROUP BY p.id
            ORDER BY p.fecha_pedido DESC
        """, (usuario_id,))
        pedidos = cursor.fetchall()

        # Obtener detalles por cada pedido (productos incluidos) y asegurar alias producto_nombre
        for pedido in pedidos:
            cursor.execute("""
                SELECT 
                    dp.producto_id,
                    pr.nombre AS producto_nombre,
                    dp.cantidad,
                    dp.precio_unitario,
                    dp.subtotal
                FROM detalle_pedido dp
                INNER JOIN productos pr ON dp.producto_id = pr.id
                WHERE dp.pedido_id = %s
            """, (pedido["id"],))
            pedido["detalles"] = cursor.fetchall()

        cursor.close()
        conn.close()

        return pedidos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo pedidos: {str(e)}")
