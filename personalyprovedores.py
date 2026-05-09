import customtkinter as ctk

class Proveedor():
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Personal Y Proveedores")
        self.ventana.state("zoomed")
        self.ventana.resizable(False, False)
        self.ventana.configure(fg_color="#1A1A1A")

        self.proveedor_interfaz()

        self.ventana.mainloop()

    def proveedor_interfaz(self):

        self.ventanapro=ctk.CTkToplevel()
        self.ventanapro.title("Proveedores")
        self.ventanapro.configure(fg_color="#1A1A1A")
        self.ventanapro.geometry("1500x1000")

        volver = ctk.CTkButton(self.ventanapro, text="← Volver al menú principal", fg_color="#8DCCE3", hover_color="#F8C8DC", font=("Arial", 20), corner_radius=15, width=120, height=40)
        volver.place(relx=0.02, rely=0.02, anchor=ctk.NW)

        marco_principal = ctk.CTkFrame(self.ventanapro, fg_color="transparent")
        marco_principal.place(relx=0.5, rely=0.5, anchor=ctk.CENTER, relwidth=0.9, relheight=0.85)

        titulo = ctk.CTkLabel(marco_principal, text="Registro de Proveedor", font=("Arial", 24, "bold"), text_color="#8DCCE3")
        titulo.pack(pady=(10, 20))

        marco_registro = ctk.CTkFrame(marco_principal, border_width=2, border_color="#F8C8DC", corner_radius=15, fg_color="white")
        marco_registro.pack(fill="x", padx=20, pady=10)

        frame_labels = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_labels.pack(pady=(15, 5))

        ctk.CTkLabel(frame_labels, text="Nombre de la empresa:", font=("Arial", 16), text_color="#1A1A1A").grid(row=0, column=0, padx=40)
        ctk.CTkLabel(frame_labels, text="Número de teléfono:", font=("Arial", 16), text_color="#1A1A1A").grid(row=0, column=1, padx=40)
        ctk.CTkLabel(frame_labels, text="Dirección o ubicación:", font=("Arial", 16), text_color="#1A1A1A").grid(row=0, column=2, padx=40)
        ctk.CTkLabel(frame_labels, text="Persona de contacto:", font=("Arial", 16), text_color="#1A1A1A").grid(row=0, column=3, padx=40)

        frame_campos = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_campos.pack(pady=(5, 15))

        self.caempresa = ctk.CTkTextbox(frame_campos, width=150, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caempresa.grid(row=0, column=0, padx=30)

        self.catelefono = ctk.CTkTextbox(frame_campos, width=150, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.catelefono.grid(row=0, column=1, padx=30)

        self.caubicacion = ctk.CTkTextbox(frame_campos, width=150, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caubicacion.grid(row=0, column=2, padx=30)

        self.cacontacto = ctk.CTkTextbox(frame_campos, width=150, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.cacontacto.grid(row=0, column=3, padx=30)

        frame_botones = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_botones.pack(pady=(5, 20))

        boton_agregar = ctk.CTkButton(frame_botones, text="+ Agregar proveedor", fg_color="#8DCCE3", hover_color="#F8C8DC", width=180, corner_radius=10, command=self.proveedor_llenado)
        boton_agregar.grid(row=0, column=0, padx=15)

        ctk.CTkButton(frame_botones, text="- Eliminar proveedor", fg_color="#8DCCE3", hover_color="#F8C8DC", width=180, corner_radius=10).grid(row=0, column=1, padx=15)

        ctk.CTkButton(frame_botones, text="Limpiar campos", fg_color="#8DCCE3", hover_color="#F8C8DC", width=180, corner_radius=10).grid(row=0, column=2, padx=15)

        marco_tabla = ctk.CTkFrame(marco_principal, border_width=2, border_color="#F8C8DC", corner_radius=15, fg_color="white")
        marco_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        frame_encabezados = ctk.CTkFrame(marco_tabla, fg_color="#8DCCE3", corner_radius=10)
        frame_encabezados.pack(pady=(10, 5))

        ctk.CTkLabel(frame_encabezados, text="Empresa", width=150, text_color="white", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=20, pady=8)
        ctk.CTkLabel(frame_encabezados, text="Teléfono", width=150, text_color="white", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=20, pady=8)
        ctk.CTkLabel(frame_encabezados, text="Ubicación", width=150, text_color="white", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=20, pady=8)
        ctk.CTkLabel(frame_encabezados, text="Persona Contacto", width=150, text_color="white", font=("Arial", 14, "bold")).grid(row=0, column=3, padx=20, pady=8)

        self.frame_datos = ctk.CTkFrame(marco_tabla, fg_color="transparent")
        self.frame_datos.pack(pady=5)

        self.fila = 0 

        bt1 = ctk.CTkButton(self.ventana, text="Salir", fg_color="#8DCCE3", hover_color="#F8C8DC", corner_radius=20, width=120, height=40, command=self.ventana.destroy)
        bt1.place(relx=0.5, rely=0.95, anchor=ctk.CENTER)

    def personal_interfaz(self):

        ctk.CTkLabel(frame_labels, text="Clave especial:", font=("Arial", 16), text_color="#1A1A1A").grid(row=0, column=0, padx=40)
        ctk.CTkLabel(frame_labels, text="Nombre del empleado:", font=("Arial", 16), text_color="#1A1A1A").grid(row=0, column=1, padx=40)
        ctk.CTkLabel(frame_labels, text="Direccion:", font=("Arial", 16), text_color="#1A1A1A").grid(row=0, column=2, padx=40)
        ctk.CTkLabel(frame_labels, text=":", font=("Arial", 16), text_color="#1A1A1A").grid(row=0, column=3, padx=40)


        self.caja_nombre= ctk.CTkTextbox(frame_campos, width=150, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caja_nombre.grid(row=0, column=0, padx=30)

        self.caja_apellidos = ctk.CTkTextbox(frame_campos, width=150, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caja_apelllidos.grid(row=0, column=1, padx=30)

        self.caubicacion = ctk.CTkTextbox(frame_campos, width=150, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caubicacion.grid(row=0, column=2, padx=30)

        self.cacontacto = ctk.CTkTextbox(frame_campos, width=150, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.cacontacto.grid(row=0, column=3, padx=30)



    def proveedor_llenado(self):
        empresa = self.caempresa.get("1.0", "end").strip()
        telefono = self.catelefono.get("1.0", "end").strip()
        ubicacion = self.caubicacion.get("1.0", "end").strip()
        contacto = self.cacontacto.get("1.0", "end").strip()

        ctk.CTkLabel(self.frame_datos, text=empresa, width=150, text_color="#1A1A1A").grid(row=self.fila, column=0, padx=20)
        ctk.CTkLabel(self.frame_datos, text=telefono, width=150, text_color="#1A1A1A").grid(row=self.fila, column=1, padx=20)
        ctk.CTkLabel(self.frame_datos, text=ubicacion, width=150, text_color="#1A1A1A").grid(row=self.fila, column=2, padx=20)
        ctk.CTkLabel(self.frame_datos, text=contacto, width=150, text_color="#1A1A1A").grid(row=self.fila, column=3, padx=20)

        self.fila += 1

    def personal__llenado(self):
        #self.clave
        nombre=self.caja_nombre.get("1.0", "end").strip()
        apellidos=self.caja_apellidos.get("1.0", "end").strip()
        telefono=self.caja_telefono.get("1.0","end").strip()
        sexo=self.caja_sexo.get("1.0","end").strip()
        edad=self.caja_edad.get("1.0", "end").strip()




    
    def clave_personal(self):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numeros = "0123456789"
        
        self.clave = ""
        for i in range(5):
            if i < 3:
                pos = random.randint(0, 25)
                self.clave = self.clave + letras[pos]
            else:
                pos = random.randint(0, 9)
                self.clave = clave + numeros[pos]
        #condicional para que no hay dos claves iguales 




Proveedor()