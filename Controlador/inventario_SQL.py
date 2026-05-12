import pyodbc

def coneccion():
    try:
        DB_CONFIG = (
            "DRIVER={SQL Server};"
            "SERVER=.;"
            "DATABASE=Zapateria;"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(DB_CONFIG)
        # print("Conexión exitosa")
        return conn
    except:
        # print("Ubo un error")
        # return None
        try:
            DB_CONFIG = (
                "DRIVER={ODBC Driver 18 for SQL Server};"
                "SERVER=localhost;"
                "DATABASE=Zapateria2;"
                "UID=sa;"
                "PWD=JitlerSQL2026!;"
                "Encrypt=yes;"
                "TrustServerCertificate=yes;"
            )
            conn = pyodbc.connect(DB_CONFIG)
            print("Funciono")
            return conn
        except:
            print("Ubo un error2")
            return None


def insert(Clave, CantidadPorducto, Talla, Precio, color, RuraImagen) -> None:
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        query = """
                INSERT INTO Inventario (Clave, CantidadProducto, Talla, FechaIngreso, Precio, Color, RutaImagen)
                VALUES (?, ?, ?, GETDATE(), ?, ?, ?)"""
        valores = (Clave, CantidadPorducto, Talla, Precio, color, RuraImagen)
        cursor.execute(query, valores)
        conn.commit()
        print("extio")
    except Exception as e:
        print("Error en la insercion {e}")
    finally:
        conn.close()

def consultar() -> list:
    conn = coneccion()
    if conn == None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT RutaImagen, Clave, CantidadProducto, Talla, FechaIngreso, Precio, Color FROM dbo.Inventario")
        inventario = cursor.fetchall()
        if not inventario:
            print("sin productos")
            return []
        else:
            return inventario
    except Exception as e:
        print(f"Error en la extraccion {e}")
    finally:
        conn.close()

def update(Clave, CantidadPorducto, Talla, Precio, color, RuraImagen) -> None:
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        query = """
            UPDATE Inventario
            SET calve = ?, CantidadPorducto = ?, talla = ?, Precio = ?, color = ?, RutaImagen = ?"""
        valores = (Clave, CantidadPorducto, Talla, Precio, color, RuraImagen)
        cursor.execute(query, valores)
        conn.commit()
        if cursor.rowcout > 0:
            print(f"Inventario acutalizado")
        else:
            print("Ubo un problema")
    except Exception as e:
        print(f"Ubo un error a la hora de actualizar {e}")
    finally:
        conn.close()

def delate(clave, talla, color) -> None:
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        clave_formateada = str(clave).strip()
        query = """
            DELeTE FROM Inventario WHERE clave = ? AND Talla = ? AND Color = ?
        """

        cursor.execute(query, (clave, talla, color))
        conn.commit()
        filas = cursor.rowcount
        if filas > 0:
            print("prosedimiento correcto")
        else:
            print("posible problema")
    except Exception as e:
        print("error al eliminar ", e)
    finally:
        conn.close()


def actualizar(Clave, CantidadProducto, Talla, Precio, color, clave_anterior, talla_anterior, color_anterior):
    conn = coneccion()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        query = """
            UPDATE Inventario
            SET clave = ?, CantidadProducto = ?, talla = ?, Precio = ?, color = ?
            WHERE clave = ? AND talla = ? AND color = ?
        """

        valores = (
            Clave, CantidadProducto, Talla, Precio, color,
            clave_anterior, talla_anterior, color_anterior
        )

        cursor.execute(query, valores)
        conn.commit()

        if cursor.rowcount > 0:
            print("Inventario actualizado con éxito.")
        else:
            print("No se encontró el registro original o los datos son idénticos.")

    except Exception as e:
        print(f"Hubo un error a la hora de actualizar: {e}")
    finally:
        conn.close()


def buscarPorColor(color):
    c = coneccion()
    if c == None:
        return []

    try:
        cursor = c.cursor()
        query = ("""
            SELECT RutaImagen, Clave, CantidadProducto, Talla, FechaIngreso, Precio, Color
            FROM dbo.Inventario
            WHERE Color LIKE ?
            """)
        valor_busqueda = f"%{color}%"

        cursor.execute(query, (valor_busqueda,))

        inventario = cursor.fetchall()
        return inventario if inventario else []

    except Exception as e:
        print("Error de consulta ", e)
        return []
    finally:
        c.close()


def buscarPorClave(clave):
    c = coneccion()
    if c == None:
        return []
    try:
        cursor = c.cursor()
        query = ("""
            SELECT RutaImagen, Clave, CantidadProducto, Talla, FechaIngreso, Precio, Color FROM dbo.Inventario
            WHERE Clave = ?
            """)

        cursor.execute(query, clave)
        inventario = cursor.fetchall()
        if not inventario:
            print("Ubo un error")
        else:
            return inventario

    except Exception as e:
        print("Error de consulta ", e)
    finally:
        c.close()


def buscarPorTalla(talla):
    c = coneccion()
    if c == None:
        return []

    try:
        cursor = c.cursor()
        query = ("""
            SELECT RutaImagen, Clave, CantidadProducto, Talla, FechaIngreso, Precio, Color
            FROM dbo.Inventario
            WHERE Talla = ?
            """)
        talla = int(talla)
        cursor.execute(query, talla)

        inventario = cursor.fetchall()
        return inventario if inventario else []

    except Exception as e:
        print("Error de consulta ", e)
        return []
    finally:
        c.close()
