import pyodbc

def coneccion():
    try:
        DB_CONFIG = (
            "DRIVER={SQL Server};"
            "SERVER=localhost;"
            "DATABASE=Zapateria;"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(DB_CONFIG)
        print("conexion exitosa")
        return conn
    except:
        print("Hubo un error")
        return None


def insert(clave, modelo, marca, seccion, categoria) -> None:
    c = coneccion()
    if c == None:
        return
    try:
        cursor = c.cursor()
        query = """
            INSERT INTO Productos(Clave, Modelo, Marca, Seccion, categoria)
            VALUES (?, ?, ?, ?, ?)"""
        valores = (clave, modelo, marca, seccion, categoria)
        cursor.execute(query, valores)
        c.commit()
    except Exception as e:
        print(f"error de insercion {e}")
        c.rollback()
    finally:
        c.close()



def mostrar() -> list:
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Clave, Modelo, Marca, Seccion, Categoria FROM Productos")
        productos = cursor.fetchall()
        if not productos:
            print("no hay noy productos")
        else:
            return productos
    except Exception as e:
        print(f"Error al mostrar {e}")
    finally:
        conn.close



def update(clave, modelo, marca, seccion, categoria) -> None:
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        query = """
            UPDATE Productos
            SET Modelo = ?, Marca = ?, Seccion = ?, categoria = ?
            WHERE Clave = ?"""
        valores = (modelo, marca, seccion, categoria, clave)
        cursor.execute(query, valores)
        conn.commit()
        if cursor.rowcount > 0:
            print("cliente actualizado")
        else:
            print("erorr")
    except Exception as e:
        print(f"error en el update {e}")
    finally:
        conn.close()

def delate(clave):
    conn = coneccion()
    if conn == None:
        return
    try:
        cursor = conn.cursor()
        calve_formateada = str(clave).strip()
        query = """
            DELETE FROM Productos WHERE Clave = ?"""
        cursor.execute(query, (calve_formateada,))
        conn.commit()
        filas = cursor.rowcount
        if filas > 0:
            print("correco")
        else:
            print("in correcto")
    except Exception as e:
        print(f"error de eliminacion {e}")
    finally:
        conn.close()
