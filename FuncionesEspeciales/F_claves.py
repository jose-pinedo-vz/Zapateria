import os
def Generar_clave_cliente() -> str:
    ruta = "FuncionesEspeciales/archivosDeTexto/clave_actual_poducto.txt"
    try:
        with open(ruta, "r") as archivo:
            clave = archivo.read().strip()
            if not clave:
                print("vacio")
                with open(ruta, "w") as archivo:
                    archivo.write("1")
                return "C1"

            clave = int(clave) + 1

            with open(ruta, "w") as archivo:
                archivo.write(f"{clave}")
            return f"C{clave}"
    except:
        with open(ruta, "w") as archivo:
            archivo.write("1")
        return "C1"


def Generar_clave_producto() -> str:
    base_path = os.path.dirname(os.path.abspath(__file__))


    ruta = os.path.join(base_path, "archivosDeTexto", "alamacen_de_claves_producto.text")
    print(ruta)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    try:
        if os.path.exists(ruta):
            with open(ruta, "r") as archivo:
                contenido = archivo.read().strip()
                if contenido:
                    nueva_clave = int(contenido) + 1
                else:
                    nueva_clave = 1
        else:
            nueva_clave = 1


        with open(ruta, "w") as archivo:
            archivo.write(str(nueva_clave))

        return f"C{nueva_clave}"

    except Exception as e:
        print(f"Error al generar clave: {e}")

        with open(ruta, "w") as archivo:
            archivo.write("1")
        return "C1"
