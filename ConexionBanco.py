import pyodbc
def conectar_db():
        conexion=(
        "Driver={SQL Server};"
        "Server=.;"  # El punto representa el servidor local
        "Database=BancoGuachinango;"
        "Trusted_Connection=yes;")
        try:
            conexion = pyodbc.connect(conexion)
            print("Conexión exitosa")
            return conexion
        except Exception as e:
            print(f"Error al conectar: {e}")
            return None
        
concet=conectar_db()
        
    