import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configura tu cuenta de envío aquí
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "tucuenta@gmail.com"
PASSWORD = "tu_contraseña_o_app_password"

def enviar_remision_por_correo(destinatario: str, remision):
    asunto = "Nota de Remisión - Librería"
    mensaje = f"Fecha: {remision['fecha']}\n\n"
    for item in remision["items"]:
        mensaje += f"{item}\n"
    mensaje += f"\nSubtotal: ${remision['subtotal']:.2f}"
    mensaje += f"\nIVA (16%): ${remision['iva']:.2f}"
    mensaje += f"\nTotal: ${remision['total']:.2f}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Correo enviado correctamente.")
        return True
    except Exception as e:
        print("Error al enviar el correo:", e)
        return False
