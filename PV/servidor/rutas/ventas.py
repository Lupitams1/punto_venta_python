from fastapi import APIRouter, HTTPException
from servidor.modelos import VentaEntrada, Remision
from servidor.database import db
from servidor.correo import enviar_remision_por_correo
from datetime import datetime
from servidor.database import ventas_realizadas

router = APIRouter()


@router.post("/ventas")
def procesar_venta(venta: VentaEntrada):
    # Registrar la venta general
    conn = get_connection()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO ventas (fecha, subtotal, iva, total, email, telefono) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (fecha, venta.subtotal, venta.iva, venta.total, venta.email, venta.telefono))
    conn.commit()
    venta_id = cursor.lastrowid  # Obtener el ID de la venta recién insertada

    # Registrar los detalles de los libros vendidos
    for item in venta.items:
        cursor.execute("""
           INSERT INTO detalles_venta (venta_id, titulo, cantidad) 
           VALUES (%s, %s, %s)
          """, (venta_id, item.titulo, item.cantidad))
        conn.commit()

    # Actualizar stock después de registrar la venta
    cursor.execute("SELECT id FROM libros WHERE titulo = %s", (item.titulo,))
    libro_id = cursor.fetchone()[0]
    actualizar_stock(libro_id, item.cantidad)

    return {"mensaje": "Venta registrada exitosamente"}
@router.get("/ventas/historial")
def obtener_historial():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.id, v.fecha, v.subtotal, v.iva, v.total, v.email, v.telefono, 
               GROUP_CONCAT(d.titulo) as libros
        FROM ventas v
        JOIN detalles_venta d ON v.id = d.venta_id
        GROUP BY v.id
    """)
    ventas = cursor.fetchall()
    cursor.close()
    conn.close()
    return ventas
def registrar_venta(cliente_id, productos):
    total_sin_iva = sum([p['precio'] * p['cantidad'] for p in productos])
    descuento_iva = total_sin_iva * 0.16
    total = total_sin_iva + descuento_iva

    # Guardar la venta en la base de datos
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ventas (cliente_id, total, descuento_iva) VALUES (%s, %s, %s)",
                   (cliente_id, total, descuento_iva))
    venta_id = cursor.lastrowid
    conn.commit()

    # Generar la nota de remisión
    archivo_nota = generar_nota_remision(venta_id, productos, descuento_iva, total)
    
    return archivo_nota
