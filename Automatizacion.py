import imaplib
import email
from email.header import decode_header
import pywhatkit as kit

# Función para obtener el último correo de Gmail
def get_last_email(username, password):
    # Conectar al servidor de Gmail usando IMAP
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)

    # Seleccionar el buzón de entrada
    mail.select("inbox")

    # Buscar todos los correos (de más nuevo a más viejo)
    status, messages = mail.search(None, "ALL")
    messages = messages[0].split(b' ')
    
    # Obtener el último correo
    latest_email_id = messages[-1]
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if "attachment" not in content_disposition:
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
            else:
                body = msg.get_payload(decode=True).decode()
            return f"Subject: {subject}\n\n{body}"

    mail.close()
    mail.logout()

# Función para enviar un mensaje a WhatsApp usando pywhatkit
def send_whatsapp_message(phone_number, message):
    # Enviar el mensaje instantáneamente
    kit.sendwhatmsg_instantly(phone_number, message, 10, tab_close=True)

# Configuración de Gmail
username = "juandavidcano0120@gmail.com"  # Reemplaza con tu correo de Gmail
password = "ecji plus kakf lwxa"  # Reemplaza con tu contraseña de aplicación

# Configuración de WhatsApp
phone_number = "+573505154489"  # Reemplaza con el número de teléfono del contacto o grupo

if __name__ == '__main__':
    # Obtener el último correo
    last_email = get_last_email(username, password)
    if last_email:
        # Enviar el correo al contacto o grupo de WhatsApp
        send_whatsapp_message(phone_number, last_email)
    else:
        print("No se encontró ningún correo.")
