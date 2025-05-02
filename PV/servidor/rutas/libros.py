from fastapi import APIRouter, HTTPException
from servidor.modelos import Libro, LibroEntrada
from servidor.database import db, crear_tabla
from servidor.db_mysql import get_connection

router = APIRouter()

@router.get("/libros")
def obtener_libros():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    cursor.close()
    conn.close()
    return libros

def actualizar_stock(id_libro: int, cantidad: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE libros SET stock = stock - %s WHERE id = %s", (cantidad, id_libro))
    conn.commit()
    cursor.close()
    conn.close()


def agregar_libro(titulo, categoria, precio, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO libros (titulo, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
                   (titulo, categoria, precio, stock))
    conn.commit()
    cursor.close()
    conn.close()

def agregar_libro(titulo, categoria, precio, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO libros (titulo, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
                   (titulo, categoria, precio, stock))
    conn.commit()
    cursor.close()
    conn.close()

def exportar_top_pdf(archivo_salida="libros_mas_vendidos.pdf"):
    resp = requests.get("http://localhost:8000/reportes/libros_mas_vendidos")
    if resp.status_code != 200:
        raise Exception("Error al consultar libros más vendidos")

    datos = resp.json()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "LIBROS MÁS VENDIDOS", ln=True, align='C')
    pdf.ln(10)

    for libro in datos:
        pdf.cell(0, 10, f"{libro['titulo']} - Vendidos: {libro['total_vendidos']}", ln=True)

    pdf.output(archivo_salida)
    return archivo_salida


router = APIRouter()
crear_tabla()

@router.get("/libros")
def obtener_libros():
    return db

@router.post("/libros")
def agregar_libro(libro: LibroEntrada):
    nuevo = Libro(**libro.dict(), id=len(db) + 1)
    db.append(nuevo)
    return nuevo
