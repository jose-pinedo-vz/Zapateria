import pyodbc
def conectar_db():
        conexion=(
        "Driver={SQL Server};"
        "Server=.;"
        "Database=BancoGuachinango;"
        "Trusted_Connection=yes;")
        try:
            conexion = pyodbc.connect(conexion)
            print("Conexión exitosa")
            return conexion
        except Exception as e:
            print(f"Error al conectar: {e}")
            return None
        
def Consulta(cursor):
    cursor.execute("SELECT Nombre_Sucursal,Ciudad_Sucursal FROM Sucursal")

    for fila in cursor:
        print(f"Sucursal: {fila.Nombre_Sucursal}, Ciudad: {fila.Ciudad_Sucursal}")

def Insertar(conexion,cursor):
    cursor.execute("INSERT INTO Productos (nombre, precio) VALUES (?, ?)", ('Tenis Nike', 1200))
    conexion.commit() 

def Editar(conexion,cursor):
    cursor.execute("UPDATE Productos SET precio = ? WHERE id = ?", (1500, 1))
    conexion.commit()

def Elimiar(conexion,cursor):
    cursor.execute("DELETE FROM Productos WHERE id = ?", (1,))
    conexion.commit()

def CrearClave():
    clave=""
    conexion=conectar_db()
    cursor=conexion.cursor()

    cursor.execute("SELECT Cuenta.ClaveCuenta,PIN,Cliente.NombreCliente,Saldo FROM Cuenta,Cliente WHERE Cliente.ClaveCuenta=Cuenta.ClaveCuenta")
    for fila in cursor:
        print(fila)
    


