from fastapi import APIRouter, Query
from servidor.db_mysql import get_connection
import tkinter as tk
from tkinter import ttk, messagebox
import requests

ventana = tk.Tk()
ventana.title("Reportes del Punto de Venta")
ventana.geometry("800x600")

notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand=True)


router = APIRouter()

@router.get("/reportes/ventas")
def reporte_ventas(fecha_inicio: str = Query(...), fecha_fin: str = Query(...)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT v.fecha, v.subtotal, v.iva, v.total, GROUP_CONCAT(d.titulo SEPARATOR ', ') AS libros
        FROM ventas v
        JOIN detalles_venta d ON v.id = d.venta_id
        WHERE v.fecha BETWEEN %s AND %s
        GROUP BY v.id
    """, (fecha_inicio, fecha_fin))

    ventas = cursor.fetchall()

    cursor.execute("""
        SELECT 
            SUM(subtotal) AS total_subtotal,
            SUM(iva) AS total_iva,
            SUM(total) AS total_general
        FROM ventas
        WHERE fecha BETWEEN %s AND %s
    """, (fecha_inicio, fecha_fin))

    resumen = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "ventas": ventas,
        "resumen": resumen

    }
@router.get("/reportes/libros_mas_vendidos")
def libros_mas_vendidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT titulo, SUM(cantidad) AS total_vendidos
        FROM detalles_venta
        GROUP BY titulo
        ORDER BY total_vendidos DESC
        LIMIT 10
    """)

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    return resultado

    
@router.get("/reportes/mermas")
def reporte_mermas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.fecha, l.titulo, m.cantidad, m.motivo
        FROM mermas m
        JOIN libros l ON m.libro_id = l.id
        ORDER BY m.fecha DESC
    """)

    mermas = cursor.fetchall()

    cursor.close()
    conn.close()

    return mermas
