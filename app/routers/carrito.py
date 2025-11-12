# app/routers/carrito.py
from fastapi import APIRouter, Depends, HTTPException, Form
from app.core.db import get_conn
from app.models.usuario import Usuario
from app.routers.autenticacion import obtener_usuario_actual


router = APIRouter(prefix="/carrito")

@router.get("")
async def obtener_carrito(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT c.id, c.producto_id, c.cantidad, c.fecha_agregado,
               p.nombre, p.precio, p.descripcion, p.stock
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
        ORDER BY c.fecha_agregado DESC
    """
    
    cursor.execute(query, (usuario_actual.id,))
    items = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {"items": items}

@router.post("/agregar")
async def agregar_al_carrito(
    producto_id: int = Form(...),
    cantidad: int = Form(1),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        # Verificar si el producto existe
        cursor.execute("SELECT stock FROM productos WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        
        if not producto:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Verificar si el producto ya está en el carrito
        cursor.execute(
            "SELECT id, cantidad FROM carrito WHERE usuario_id = %s AND producto_id = %s",
            (usuario_actual.id, producto_id)
        )
        existe = cursor.fetchone()
        
        if existe:
            # Actualizar cantidad
            nueva_cantidad = existe[1] + cantidad
            cursor.execute(
                "UPDATE carrito SET cantidad = %s WHERE id = %s",
                (nueva_cantidad, existe[0])
            )
        else:
            # Insertar nuevo item
            cursor.execute(
                "INSERT INTO carrito (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s)",
                (usuario_actual.id, producto_id, cantidad)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"mensaje": "Producto agregado al carrito", "producto_id": producto_id}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.delete("/eliminar/{producto_id}")
async def eliminar_del_carrito(
    producto_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM carrito WHERE usuario_id = %s AND producto_id = %s",
        (usuario_actual.id, producto_id)
    )
    
    conn.commit()
    eliminados = cursor.rowcount
    
    cursor.close()
    conn.close()
    
    if eliminados == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")
    
    return {"mensaje": "Producto eliminado del carrito"}

@router.put("/actualizar")
async def actualizar_cantidad(
    producto_id: int = Form(...),
    cantidad: int = Form(...),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    if cantidad < 1:
        raise HTTPException(status_code=400, detail="La cantidad debe ser al menos 1")
    
    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE carrito SET cantidad = %s WHERE usuario_id = %s AND producto_id = %s",
            (cantidad, usuario_actual.id, producto_id)
        )
        
        conn.commit()
        actualizados = cursor.rowcount
        
        cursor.close()
        conn.close()
        
        if actualizados == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")
        
        return {"mensaje": "Cantidad actualizada", "producto_id": producto_id, "nueva_cantidad": cantidad}
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.delete("/limpiar")
async def limpiar_carrito(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM carrito WHERE usuario_id = %s",
        (usuario_actual.id,)
    )
    
    conn.commit()
    eliminados = cursor.rowcount
    
    cursor.close()
    conn.close()
    
    return {"mensaje": f"Carrito limpiado, {eliminados} productos eliminados"}