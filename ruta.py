import os
base_path = os.path.dirname(os.path.abspath(__file__))
print(base_path)
ruta_absoluta = os.path.join(base_path, "PDF")
print(f"Buscando en: {ruta_absoluta}")