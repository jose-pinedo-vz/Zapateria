import pywhatkit as kit
import time

def enviar_whatsapp(numero, mensaje):
    print("mensajito")
    num_str = str(numero)
    try:
        num_str = f"+52{num_str}"
        kit.sendwhatmsg_instantly(num_str, mensaje, wait_time=15, tab_close=True)
        print("Exito")
        return True
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        return False
