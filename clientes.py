import customtkinter as ctk
from tkinter import ttk
# from Controlador.clientes import mostrarUser
from Controlador import clientes
from FuncionesEspeciales import F_claves

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

        self.clientes.column("CLAVE", width=120, stretch=True)
        self.clientes.column("NOMBRE", width=120, stretch=True)
        self.clientes.column("APELLIDO", width=120, stretch=True)
        self.clientes.column("DIRECCION", width=120, stretch=True)
        self.clientes.column("GMAIL", width=120, stretch=True)
        self.clientes.column("TELEFONO", width=120, stretch=True)


        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#F2F2F2",
                        foreground="black",
                        rowheight=35,
                        fieldbackground="#F2F2F2")
        style.map("Treeview", background=[('selected', '#3E3E3E')])

        self.clientes.configure(height=15)
        self.clientes.pack(fill="x", padx=20, pady=20)

        self.frame_acciones = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_acciones.pack(pady=20, fill="x", padx=20)

        self.btnEditar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="EDITAR", width=150,
            command=lambda: self.edita())
        self.btnEditar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_eliminar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="ELIMINAR", width=150)
        self.btn_eliminar.grid(row=1, column=0, padx=10, pady=10)

        self.btn_Agregar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="INSERTAR", width=150,
            command=lambda: self.insertar())
        self.btn_Agregar.grid(row=2, column=0, padx=10, pady=10)

        self.btn_surtir = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="ENVIAR CORREO", width=150,
            command=lambda: self.EnbiarCorreo())
        self.btn_surtir.grid(row=0, column=1, padx=10, pady=10)

        self.btn_oferta = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="MENSAJE AL GRUPO DE TELEGRAM", width=150,
            command=lambda: self.embiarTelegram())
        self.btn_oferta.grid(row=1, column=1, padx=10, pady=10)

        self.mostrarTalbe()
        self.ventana.mainloop()



    def mostrarTalbe(self):
        # print("el error no esta aqui ya que si llega ")
        for item in self.clientes.get_children():
            self.clientes.delete(item)

        clientes.mostrarUser()
        for item in self.clientes.get_children():
                self.clientes.delete(item)
        datos = clientes.mostrarUser()
        if datos:
            for fila in datos:
                self.clientes.insert("", "end", values=tuple(str(item).strip() for item in fila))
        else:
            print("No hay datos para mostrar en la interfaz.")


    def EnbiarCorreo(self):
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

    def edita(self):
        COLOR_PRIMARIO = "#F8C8DC"
        COLOR_SECUNDARIO = "#1A1A1A"
        COLOR_TERCIARIO = "#FFB0CC"
        COLOR_COMPLEMENTARIO = "#8DCCE3"
        COLOR_FONDO_BLANCO = "#F2F2F2"
        COLOR_TEXTO_NEGRO = "#1A1A1A"

        ventana_correo = ctk.CTkToplevel()
        ventana_correo.geometry("1800x1200")
        ventana_correo.title("APARTADO DE CLIENTES")
        ventana_correo.configure(fg_color=COLOR_FONDO_BLANCO)

        ventana_correo.grid_columnconfigure(0, weight=1)
        ventana_correo.grid_columnconfigure(1, weight=2)
        ventana_correo.grid_rowconfigure(0, weight=1)


        frame_izquierdo = ctk.CTkFrame(ventana_correo, fg_color=COLOR_PRIMARIO, corner_radius=15)
        frame_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(frame_izquierdo, text="DATOS DEL CLIENTE", text_color=COLOR_TEXTO_NEGRO, font=("Arial", 16, "bold")).pack(pady=20)

        self.nombre_entry = ctk.CTkEntry(frame_izquierdo, placeholder_text="NOMBRE", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        self.nombre_entry.pack(pady=10, padx=20)

        self.apellido_entry = ctk.CTkEntry(frame_izquierdo, placeholder_text="APELLIDO", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        self.apellido_entry.pack(pady=10, padx=20)

        self.ent_telefono = ctk.CTkEntry(frame_izquierdo, placeholder_text="TELEFONO", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        self.ent_telefono.pack(pady=10, padx=20)

        self.ent_email = ctk.CTkEntry(frame_izquierdo, placeholder_text="Email", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        self.ent_email.pack(pady=10, padx=20)

        self.ent_direccion = ctk.CTkEntry(frame_izquierdo, placeholder_text="DIRECCION", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        self.ent_direccion.pack(pady=10, padx=20)


        def editar():
            try:
                nombre = self.nombre_entry.get()
                apellido = self.apellido_entry.get()
                telefono = int(self.ent_telefono.get())
                email = self.ent_email.get()
                direccion = self.ent_direccion.get()
                print("Se va")
                clientes.update(self.clave_cliente, direccion, email, telefono, nombre, apellido)

                self.mostrarTalbe()

                ventana_correo.destroy()
            except:
                from tkinter import messagebox
                messagebox.showinfo("Fallo", "No se puede actualizar")

        self.btn_accion = ctk.CTkButton(frame_izquierdo, text="ACTUALIZAR", fg_color=COLOR_SECUNDARIO, hover_color=COLOR_TERCIARIO,
            command=lambda: editar())
        self.btn_accion.pack(pady=30)



        frame_derecho = ctk.CTkFrame(ventana_correo, fg_color=COLOR_FONDO_BLANCO)
        frame_derecho.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                            background=COLOR_FONDO_BLANCO,
                            foreground=COLOR_TEXTO_NEGRO,
                            rowheight=35, # Para que no se vea cortado
                            fieldbackground=COLOR_FONDO_BLANCO,
                            borderwidth=0)

        style.map("Treeview", background=[('selected', COLOR_TERCIARIO)])

        style.configure("Treeview.Heading",
                            background=COLOR_SECUNDARIO,
                            foreground="#FFFFFF",
                            font=("Arial", 10, "bold"))

        colupnas = ("CLAVE", "NOMBRE", "APELLIDOS", "TELEFONO", "EMAIL", "DIRECCION")
        self.editar_talbla = ttk.Treeview(frame_derecho, columns=colupnas, show="headings")

        self.editar_talbla.heading("CLAVE", text="CLAVE")
        self.editar_talbla.heading("NOMBRE", text="NOMBRE")
        self.editar_talbla.heading("APELLIDOS", text="APELLIDOS")
        self.editar_talbla.heading("TELEFONO", text="TELEFONO")
        self.editar_talbla.heading("EMAIL", text="EMAL")
        self.editar_talbla.heading("DIRECCION", text="DIRECCIOPM")
        self.editar_talbla.column("CLAVE", width=100, anchor="center")
        self.editar_talbla.column("NOMBRE", width=150, anchor="w")
        self.editar_talbla.column("APELLIDOS", width=150, anchor="w")
        self.editar_talbla.column("TELEFONO", width=150, anchor="w")
        self.editar_talbla.column("EMAIL", width=150, anchor="w")
        self.editar_talbla.column("DIRECCION", width=150, anchor="w")

        self.editar_talbla.pack(fill="both", expand=True)

        self.mostrarTablaEditar()

        self.editar_talbla.bind("<<TreeviewSelect>>", self.obtener_datos_seleccionados_de_editar)

    def obtener_datos_seleccionados_de_editar(self, event):
        seleccion = self.editar_talbla.selection()
        if seleccion:
            item = self.editar_talbla.item(seleccion)
            valores = item['values']
            self.clave_cliente = valores[0]
            nombre = valores[1]
            apellido = valores[2]
            telefono = valores[3]
            email = valores[4]
            direccion = valores[5]
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, nombre)
            self.apellido_entry.delete(0, "end")
            self.apellido_entry.insert(0, apellido)
            self.ent_telefono.delete(0, "end")
            self.ent_telefono.insert(0, telefono)
            self.ent_email.delete(0, "end")
            self.ent_email.insert(0, email)
            self.ent_direccion.delete(0, "end")
            self.ent_direccion.insert(0, direccion)

    def mostrarTablaEditar(self):
        for item in self.editar_talbla.get_children():
                self.editar_talbla.delete(item)
        datos = clientes.mostrarTablaEditar()
        if datos:
            for fila in datos:
                self.editar_talbla.insert("", "end", values=tuple(str(item).strip() for item in fila))


    def insertar(self):
        COLOR_PRIMARIO = "#F8C8DC"
        COLOR_SECUNDARIO = "#1A1A1A"
        COLOR_TERCIARIO = "#FFB0CC"
        COLOR_COMPLEMENTARIO = "#8DCCE3"
        COLOR_FONDO_BLANCO = "#F2F2F2"
        COLOR_TEXTO_NEGRO = "#1A1A1A"

        ventana_correo = ctk.CTkToplevel()
        ventana_correo.geometry("800x600")
        ventana_correo.title("AGREGAR CLIENTES")
        ventana_correo.configure(fg_color=COLOR_FONDO_BLANCO)

        ventana_correo.grid_columnconfigure(0, weight=1)
        # ventana_correo.grid_columnconfigure(1, weight=1)
        ventana_correo.grid_rowconfigure(0, weight=1)


        frame_izquierdo = ctk.CTkFrame(ventana_correo, fg_color=COLOR_PRIMARIO, corner_radius=15)
        frame_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(frame_izquierdo, text="DATOS DEL CLIENTE", text_color=COLOR_TEXTO_NEGRO, font=("Arial", 16, "bold")).pack(pady=20)

        nombre_entry = ctk.CTkEntry(frame_izquierdo, placeholder_text="NOMBRE", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        nombre_entry.pack(pady=10, padx=20)

        apellido_entry = ctk.CTkEntry(frame_izquierdo, placeholder_text="APELLIDO", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        apellido_entry.pack(pady=10, padx=20)

        ent_telefono = ctk.CTkEntry(frame_izquierdo, placeholder_text="TELEFONO", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        ent_telefono.pack(pady=10, padx=20)

        ent_email = ctk.CTkEntry(frame_izquierdo, placeholder_text="Email", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        ent_email.pack(pady=10, padx=20)

        ent_direccion = ctk.CTkEntry(frame_izquierdo, placeholder_text="DIRECCION", width=250, height=45, fg_color="#FFFFFF", text_color=COLOR_TEXTO_NEGRO)
        ent_direccion.pack(pady=10, padx=20)

        def agregar_valores_a_insertar():
            try:
                import random
                nombre = nombre_entry.get()
                apellido = apellido_entry.get()
                telefono = int(ent_telefono.get())
                email = ent_email.get()
                direccion = ent_direccion.get()
                print("Se va")
                clave_cliente = F_claves.Generar_clave_cliente()
                try:
                    clientes.insert(clave_cliente, direccion, email, telefono, nombre, apellido)
                except Exception as e:
                    print(clave_cliente)
                    print("error de calve ", e)

                self.mostrarTalbe()

                ventana_correo.destroy()
            except:
                from tkinter import messagebox
                messagebox.showinfo("Fallo", "Error en los datos")

        self.btn_accion = ctk.CTkButton(frame_izquierdo, text="INSERTAR", fg_color=COLOR_SECUNDARIO, hover_color=COLOR_TERCIARIO,
            command=lambda: agregar_valores_a_insertar())
        self.btn_accion.pack(pady=30)









if __name__ == "__main__":
    obj = cliente()
