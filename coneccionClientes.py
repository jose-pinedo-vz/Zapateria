import pyodbc

DB_CONFIG = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=zapateria;"
    "UID=sa;"
    "PWD=JitlerSQL2026!;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

def obtener_conexion():
    return pyodbc.connect(DB_CONFIG)

def mostrar():
    try:
        comexion = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT NumeroDeCuenta, nombreDeEmpresa, ubicacioin FROM dbo.Provedor")
        
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID: {fila[0].strip()} | Empresa: {fila[1].strip()} | Origen: {fila[2].strip()}")
            
        cursor.close()
        comexion.close()
    except Exception:
        print(f"error en mostar")

mostrar()