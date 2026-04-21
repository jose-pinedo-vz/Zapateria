import tkinter as tk
import os
from pathlib import Path
from tkinter import filedialog
import shutil
import tkinter as tk
from PIL import Image, ImageTk




class RegistroProductos():
    def __init__(self, root):
        self.root = root
        self.root.title("registro de productos")
        self.root.geometry("600x400")

        self.etiqueta = tk.Label(self.root, text=("bienvenido al camino de la maestria"))
        self.etiqueta.pack(pady=20)

        self.boton = tk.Button(self.root, text=("seleccionar archivo"),
                               command=lambda: self.ExtraerImagen()
                               )
        self.boton.pack(pady=10)

        self.boton2 = tk.Button(self.root, text="ir a ver imagenes", 
                                command=lambda: self.mostrarImagen())
        self.boton2.pack(pady=20)

    def ExtraerImagen(self):
        """
        Funcion con la capasidad de habir una ventana usando tkinter.
        de esta forma se seleccionara una imagen con las nominaciones correspondieste
        y hacer si despeus ago que las pueda meter en una carpeta adicional
        
        :param self: solo resive la ventana 
        no retorna nada
        """

        app.crearCarpetas()

        formatos = [
            ("Archivos de imagen", "*.jpg *.jpeg *.png *.webp"),
            ("Todos los archivos", "*.*")
        ]

        ruta_imagen = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=formatos
        )


        if ruta_imagen:
            print(f"Ruta completa: {ruta_imagen}")
            self.insertarImagen(ruta_imagen)
        else:
            print("El usuario canceló la selección.")


    def insertarImagen(self, ruta_imagen):
        """
        insercion de la imagen dentro de la carpeta seleccionada
        
        :param ruta_imagen: se recibe como parametro la ruta de la imagen en el formato 
            correcto
        """

        carpeta_destino = "imagenes_productos" # donde terminara la carpeta

        nombre_archivo = os.path.basename(ruta_imagen) # se extrae el nombre del archivo

        ruta_final = os.path.join(carpeta_destino, nombre_archivo) # creacion de la tura dinal

        try:
            shutil.copy2(ruta_imagen, ruta_final)
            print(f"Imagen copiada con éxito")

            print("ruta de la imagen: ", ruta_final)

            with open("Imagenes_productos.txt", "a") as r:
                r.write(f"{ruta_final}\n")


        except FileNotFoundError:
            print("Error: No se encontró la imagen de origen")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")


    def crearCarpetas(self):
        """
        creacion y confirmacion de una carpeta
        
        :param self: sin parametros ni return
        """
        ruta = Path("imagenes_productos")
        ruta.mkdir(parents=True, exist_ok=True)

    def mostrarImagen(self):
        """
        Mostrar la imagen del arhivo
        
        :param self: Description
        """
        mostrar = tk.Toplevel()


        mostrar.title("Probando imagenes")
        mostrar.geometry("800x400")

        etiqueta = tk.Label(mostrar, text="probando imagenes")
        etiqueta.pack(pady=10, padx=50)

        with open("Imagenes_productos.txt", "r") as r:
            imagenes = r.readlines()
            for i in imagenes:
                ruta_limpia = i.strip()
                print(f"Intentando abrir: '{ruta_limpia}'") # Para verificar en terminal
                
                try:
                    imagen_original = Image.open(ruta_limpia)
                    
                    imagen_res = imagen_original.resize((200, 200))
                    
                    foto = ImageTk.PhotoImage(imagen_res)

                    etiqueta_imagen = tk.Label(mostrar, image=foto)
                    etiqueta_imagen.pack(pady=20)
                    
                    etiqueta_imagen.image = foto 
                    
                except Exception as e:
                    print(f"Error al cargar {ruta_limpia}: {e}")


if __name__ == "__main__":
    print("desde python")

    root = tk.Tk()
    app = RegistroProductos(root)
    root.mainloop()
