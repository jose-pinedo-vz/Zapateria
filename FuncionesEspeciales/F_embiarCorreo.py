# embiar correo a un usuario
import smtplib
from email.message import EmailMessage

def embiarCorreo(destino, mensaje, azunto):
    remitente = "josepinedov.24826@gmail.com"
    password = "aplezzodhhzcwkgt"
    destinatario = destino

    cuerpo = mensaje

    msg = EmailMessage()
    msg['Subject'] = azunto
    msg['From'] = remitente
    msg['To'] = destinatario
    msg.set_content(cuerpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(msg)
            print("se e,boa")
    except Exception as e:
        print(f"Error al enviar: {e}")
