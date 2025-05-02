from fastapi import FastAPI
from servidor.rutas import libros
from fastapi.middleware.cors import CORSMiddleware
from servidor.rutas import mermas
import bcrypt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import can
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app.include_router(mermas.router)


app = FastAPI()
app.include_router(libros.router)

# CORS para permitir conexiones desde el cliente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API de Libros activa"}

@app.post("/login")
def login_usuario(datos: dict):
    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (usuario,))
    resultado = cursor.fetchone()
    cursor.close()

    if resultado and bcrypt.checkpw(contrasena.encode(), resultado["contrasena"].encode()):
        return {"login": True, "rol": resultado["rol"]}
    else:
        return {"login": False}
# Obtener todos los usuarios
@app.get("/usuarios")
def obtener_usuarios():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre_usuario, rol FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return {"usuarios": usuarios}

# Crear usuario
@app.post("/usuarios")
def crear_usuario(datos: dict):
    nombre = datos["nombre_usuario"]
    contrasena = datos["contrasena"]
    rol = datos["rol"]
    hash_pw = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (%s, %s, %s)", (nombre, hash_pw, rol))
    conn.commit()
    cursor.close()
    return {"mensaje": "Usuario creado"}

# Eliminar usuario
@app.delete("/usuarios/{id_usuario}")
def eliminar_usuario(id_usuario: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
    conn.commit()
    cursor.close()
    return {"mensaje": "Usuario eliminado"}

# Actualizar rol
@app.put("/usuarios/{id_usuario}")
def actualizar_rol(id_usuario: int, datos: dict):
    nuevo_rol = datos["rol"]
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET rol = %s WHERE id = %s", (nuevo_rol, id_usuario))
    conn.commit()
    cursor.close()
    return {"mensaje": "Rol actualizado"}

def generar_nota_remision(venta_id, productos, descuento_iva, total):
    filename = f"nota_remision_{venta_id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, f"Nota de Remisión - Venta #{venta_id}")
    c.drawString(100, 735, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 715, "Productos:")

    y_position = 700
    for producto in productos:
        c.drawString(100, y_position, f"{producto['nombre']} - {producto['cantidad']} x {producto['precio']} = {producto['total']}")
        y_position -= 15

    c.drawString(100, y_position, f"Descuento IVA (16%): {descuento_iva}")
    y_position -= 15
    c.drawString(100, y_position, f"Total a Pagar: {total}")

    c.save()

    return filename

def enviar_correo(destinatario, archivo_pdf):
    remitente = "tu_correo@gmail.com"
    password = "tu_contraseña"

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = "Nota de Remisión - Punto de Venta"

    cuerpo = "Adjunto te envío la nota de remisión con el detalle de tu compra."

    msg.attach(MIMEText(cuerpo, 'plain'))

    adjunto = MIMEBase('application', 'octet-stream')
    with open(archivo_pdf, 'rb') as archivo:
        adjunto.set_payload(archivo.read())
    encoders.encode_base64(adjunto)
    adjunto.add_header('Content-Disposition', f"attachment; filename={archivo_pdf}")
    msg.attach(adjunto)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
def validar_stock(productos):
    for producto in productos:
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM inventario WHERE producto_id = %s", (producto['producto_id'],))
        stock_disponible = cursor.fetchone()['cantidad_disponible']
        if stock_disponible < producto['cantidad']:
            return False, producto['nombre']
    return True, ""

def validar_stock(productos):
    for producto in productos:
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM inventario WHERE producto_id = %s", (producto['producto_id'],))
        stock_disponible = cursor.fetchone()['cantidad_disponible']
        if stock_disponible < producto['cantidad']:
            return False, producto['nombre']
    return True, ""

    import time

def verificar_stock_minimo():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.producto_id, p.nombre, i.cantidad_disponible, i.cantidad_minima
        FROM productos p
        JOIN inventario i ON p.producto_id = i.producto_id
        WHERE i.cantidad_disponible <= i.cantidad_minima
    """)
    productos_bajos = cursor.fetchall()

    for producto in productos_bajos:
        # Realizar la compra automáticamente (esto es un ejemplo, se debe integrar con un proveedor real)
        cantidad_a_comprar = producto['cantidad_minima'] * 2  # Comprar el doble del mínimo para evitar faltantes
        registrar_compra(proveedor_id=1, producto_id=producto['producto_id'], cantidad=cantidad_a_comprar, precio_unitario=150.0)

    # Esperar 24 horas antes de verificar nuevamente
    time.sleep(86400)

# Iniciar la verificación periódica
verificar_stock_minimo()





