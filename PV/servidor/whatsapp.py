from twilio.rest import Client

# Configura tus credenciales de Twilio aquí
ACCOUNT_SID = "TU_SID"
AUTH_TOKEN = "TU_TOKEN"
TWILIO_NUMBER = "whatsapp:+14155238886"  # número oficial de Twilio para pruebas

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def enviar_remision_whatsapp(telefono: str, remision):
    mensaje = f"*Nota de Remisión*\nFecha: {remision['fecha']}\n\n"
    for item in remision["items"]:
        mensaje += f"{item}\n"
    mensaje += f"\nSubtotal: ${remision['subtotal']:.2f}"
    mensaje += f"\nIVA (16%): ${remision['iva']:.2f}"
    mensaje += f"\nTotal: ${remision['total']:.2f}"
#V5LBDBMJX244D9CAQTR1PTS4
    try:
        mensaje = client.messages.create(
            from_=TWILIO_NUMBER,
            body=mensaje,
            to=f"whatsapp:{telefono}"  # ejemplo: "whatsapp:+521234567890"
        )
        print("Mensaje enviado:", mensaje.sid)
        return True
    except Exception as e:
        print("Error al enviar WhatsApp:", e)
        return False
