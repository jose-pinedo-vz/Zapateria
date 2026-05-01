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
