import shutil
import os
from datetime import datetime

# CopiasSeguridad
def HoraparaNOmbre() -> str:
    hora = datetime.now()
    nombre = hora.strftime("%Y-%m-%d_%H-%M")
    return nombre

def CrearCopia() -> None:
    origin = "Zapateria_forma_normal.sql"
    nombre = HoraparaNOmbre()
    destino = os.path.join("CopiasSeguridad", f"{nombre}.sql")

    if not os.path.exists("CopiasSeguridad"):
        os.makedirs("CopiasSeguridad")

    shutil.copy2(origin, destino)

# CrearCopia()

def remplazarcopia(archivo_nombre):
    nombre = "Zapateria_forma_normal.sql"
    if os.path.exists(nombre):
        os.remove(nombre)

    # traer nuevo archivo
    rutaCarpeta = os.path.join(os.getcwd(), "CopiasSeguridad")
    rutaOrigenCopia = os.path.join(rutaCarpeta, archivo_nombre)
    ruta_destino = os.path.join(os.getcwd(), archivo_nombre)

    if os.path.exists(rutaOrigenCopia):
        shutil.copy2(rutaOrigenCopia, ruta_destino)
        print(f"Exito")
    else:
        print(f"Algo salio mal")

    os.rename(archivo_nombre, "Zapateria_forma_normal2.sql")

remplazarcopia("2026-05-12_12-23.sql")
