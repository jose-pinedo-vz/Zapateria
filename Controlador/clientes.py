import pyodbc

def coneccion():
    try:
        DB_CONFIG = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=zapateria;"
            "UID=sa;"
            "PWD=JitlerSQL2026!;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(DB_CONFIG)
        return conn
    except:
        print("Ubo un error")
        return None

def insert(clave, Direccion, Email, telefono, Nombre, ApellidoP) -> None:
    conn = coneccion()
    if conn == None:
        return 0
    try:
        cursor = conn.cursor()
        query = """
                INSERT INTO Clientes(clave, Direccion, Email, telefono, Nombre, ApellidoP)
                VALUES (?, ?, ?, ?, ?, ?)
            """
        valores = (clave, Direccion, Email, telefono, Nombre, ApellidoP)
        cursor.execute(query, valores)
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()


def mostrarUser():
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT clave, Nombre, ApellidoP, Direccion, Email, telefono FROM Clientes")
        usuarios = cursor.fetchall()
        if not usuarios:
            print("sin usars")
        else:
            return usuarios
    except Exception as e:
        print("error al mostrar user ", e)
    finally:
        conn.close()


def update(clave, Direccion, Email, telefono, Nombre, ApellidoP) -> None:
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        query = """
            UPDATE Clientes
            SET Direccion = ?, Email = ?, telefono = ?, Nombre = ?, ApellidoP = ?
            WHERE clave = ?
        """
        valores = (Direccion, Email, telefono, Nombre, ApellidoP, clave)
        cursor.execute(query, valores)
        conn.commit()
        if cursor.rowcount > 0:
            print(f"cliete acutalizado.")
        else:
            print("nadie con esa calve")
    except Exception as e:
        conn.rollback()
        print("Hubo un error en la actualización:", e)
    finally:
        conn.close()



def delate(clave) -> None:
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        query = """
            DELeTE FROM Clientes WHERE clave = ?
        """
        cursor.execute(query, (clave,))
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


def mostrarTablaEditar():
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT clave, Nombre, ApellidoP, telefono, Email, Direccion FROM Clientes")
        usuarios = cursor.fetchall()
        if not usuarios:
            print("sin usars")
        else:
            return usuarios
    except Exception as e:
        print("error al mostrar user ", e)
    finally:
        conn.close()

# insert("z-242", 7, "jose190", 123456789, "Jose", "Pinedo")
# mostrarUser()
# delate("z-242")
# mostrarUser()
