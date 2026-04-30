import customtkinter as ctk
from tkinter import ttk

class cliente:
    def __init__(self):
        self.ventana = ctk.CTkToplevel()
        self.ventana.title('CONTROL DE CLIENTES - ZAPATERIA')
        self.ventana.configure(fg_color="#1A1A1A")

        try: self.ventana.state('zoomed')
        except: self.ventana.attributes('-zoomed', True)

        self.ventana.grid_columnconfigure(0, weight=0) # Menú (no se estira)
        self.ventana.grid_columnconfigure(1, weight=1) # Contenido (sí se estira)
        self.ventana.grid_rowconfigure(0, weight=1)    # Que ocupe todo el alto

        self.frame_contenido = ctk.CTkFrame(self.ventana, fg_color="#D1D1D1", corner_radius=0)
        self.frame_contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


        # frame del centro
        self.fm_mostrar = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.fm_mostrar.pack(pady=20, fill="x", padx=20)

        apartado_inventario = ctk.CTkLabel(self.fm_mostrar, text="CLIENTES", text_color="#1A1A1A", font=("ARIAL", 40))
        apartado_inventario.grid(row=0, column=0, padx=10, pady=10)

        self.frame_busqueda = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_busqueda.pack(pady=20, fill="x", padx=20)

        self.lb_busqueda = ctk.CTkLabel(self.frame_busqueda, text="BUSCAR CLAVE", text_color="#1A1A1A")
        self.lb_busqueda.grid(row=0, column=0, padx=10, pady=10)

        self.ent_buscar = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Ej: P001", width=150)
        self.ent_buscar.grid(row=0, column=1, padx=5, pady=5)

        self.btn_buscar = ctk.CTkButton(self.frame_busqueda, text="Buscar", width=100, fg_color="#3E3E3E")
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=5)

        colupnas = ("CLAVE", "NOMBRE", "APELLIDO", "DIRECCION", "GMAIL", "TELEFONO")

        self.clientes = ttk.Treeview(self.frame_contenido, columns=colupnas, show="headings")

        self.clientes.heading("CLAVE", text="CLAVE")
        self.clientes.heading("NOMBRE", text="NOMBRE")
        self.clientes.heading("APELLIDO", text="APELLIDO")
        self.clientes.heading("DIRECCION", text="DIRECCION")
        self.clientes.heading("GMAIL", text="GMAIL")
        self.clientes.heading("TELEFONO", text="TELEFONO")

        self.clientes.column("CLAVE", width=100)
        self.clientes.column("NOMBRE", width=80, anchor="center")
        self.clientes.column("APELLIDO", width=120, anchor="center")
        self.clientes.column("DIRECCION", width=60, anchor="center")
        self.clientes.column("GMAIL", width=150, anchor="center")
        self.clientes.column("TELEFONO", width=80, anchor="center")


        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#F2F2F2",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#F2F2F2")
        style.map("Treeview", background=[('selected', '#3E3E3E')])

        self.clientes.configure(height=15)
        self.clientes.pack(fill="x", padx=20, pady=20)

        self.frame_acciones = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_acciones.pack(pady=20, fill="x", padx=20)

        self.btnEditar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="EDITAR", width=150)
        self.btnEditar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_eliminar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="ELIMINAR", width=150)
        self.btn_eliminar.grid(row=1, column=0, padx=10, pady=10)

        self.btn_surtir = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="ENVIAR CORREO", width=150,
            command=lambda: self.EnbiarCorreo())
        self.btn_surtir.grid(row=0, column=1, padx=10, pady=10)

        self.btn_oferta = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="MENSAJE AL GRUPO DE TELEGRAM", width=150,
            command=lambda: self.embiarTelegram())
        self.btn_oferta.grid(row=1, column=1, padx=10, pady=10)

        self.ventana.mainloop()


    def EnbiarCorreo(self):
        print("se envio correo")
        ventana_correo = ctk.CTkToplevel()
        ventana_correo.geometry("1200x1000")
        ventana_correo.title("APARTADO DE CLIENTES")
        ventana_correo.configure(fg_color="#E5E5E5")

        colupnas = ("NOMBRE", "CORREO")
        user_tabla = ttk.Treeview(ventana_correo, columns=colupnas, show="headings")

        user_tabla.heading("NOMBRE", text="NOMBRE")
        user_tabla.heading("CORREO", text="CORREO")
        user_tabla.column("NOMBRE", width=100)
        user_tabla.column("CORREO", width=80, anchor="center")
        user_tabla.pack(pady=20, padx=20, fill="both", expand=True)

        correo_destino = ctk.CTkEntry(ventana_correo, placeholder_text="CORREO", text_color="#FFFFFF", width=600, height=70, font=("Arial", 15))
        correo_destino.pack(padx=10, pady=5)

        mensaje = ctk.CTkTextbox(ventana_correo, text_color="#FFFFFF", width=600, height=200, font=("Arial", 15),
            )
        mensaje.pack(padx=10, pady=5)

        def enviar():
            from FuncionesEspeciales import F_embiarCorreo

            correo = correo_destino.get()
            contenido = mensaje.get("0.0", "end")
            azunto = "Trata de algun tema"
            F_embiarCorreo.embiarCorreo(correo, contenido, azunto)

        emviar = ctk.CTkButton(ventana_correo, text="EMVIAR", fg_color="#3E3E3E",
                width=200, height=70, font=("Arial", 15), command=lambda: enviar())
        emviar.pack(padx=10, pady=5)

    def embiarTelegram(self):
        ventana_telegram = ctk.CTkToplevel()
        ventana_telegram.geometry("1200x1000")
        ventana_telegram.title("APARTADO DEL CLIENTE")
        ventana_telegram.configure(fg_color="#E5E5E5")

        mensaje = ctk.CTkTextbox(ventana_telegram, text_color="#FFFFFF", width=600, height=200, font=("Arial", 15),
            )
        mensaje.pack(padx=10, pady=5)

        def enviar():
            from FuncionesEspeciales import F_enbiarTelegram
            contenido = mensaje.get("0.0", "end")
            F_enbiarTelegram.Telegram_mensaje(contenido)

        emviar = ctk.CTkButton(ventana_telegram, text="EMVIAR", fg_color="#3E3E3E",
                width=200, height=70, font=("Arial", 15), command=lambda: enviar())
        emviar.pack(padx=10, pady=5)







if __name__ == "__main__":
    obj = cliente()
