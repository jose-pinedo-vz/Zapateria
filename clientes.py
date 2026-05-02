import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox

# from Controlador.clientes import mostrarUser
from Controlador import clientes
from FuncionesEspeciales import F_claves
from FuncionesEspeciales import F_whatsapp


# xhost +local:

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

        lb_busqueda1 = ctk.CTkLabel(self.frame_busqueda, text="BUSCAR CLAVE", text_color="#1A1A1A")
        lb_busqueda1.grid(row=0, column=0, padx=10, pady=10)

        self.ent_buscar_calve = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Ej: P001", width=250)
        self.ent_buscar_calve.grid(row=0, column=1, padx=5, pady=5)

        # def buscar_clave():
        #     calve = self.ent_buscar_calve.get().strip()
        #     clientes.buscar_clave()



        self.btn_buscar_clave = ctk.CTkButton(self.frame_busqueda, text="Buscar", width=100, fg_color="#3E3E3E",
                                             command=lambda: self.buscar_clave())
        self.btn_buscar_clave.grid(row=0, column=2, padx=5, pady=5)

        lb_busqueda2 = ctk.CTkLabel(self.frame_busqueda, text="BUSCAR NOMBRE", text_color="#1A1A1A")
        lb_busqueda2.grid(row=0, column=3, padx=10, pady=10)

        self.ent_buscar_nombre = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Ej: Juan", width=250)
        self.ent_buscar_nombre.grid(row=0, column=4, padx=5, pady=5)

        self.btn_buscar_nombre = ctk.CTkButton(self.frame_busqueda, text="Buscar", width=100, fg_color="#3E3E3E",
                                              command=lambda: self.BuscarPorNombre())
        self.btn_buscar_nombre.grid(row=0, column=5, padx=5, pady=5)

        self.btn_buscar_nombre = ctk.CTkButton(self.frame_busqueda, text="Todos", width=100, fg_color="#3E3E3E",
                                              command=lambda: self.mostrarTalbe())
        self.btn_buscar_nombre.grid(row=0, column=6, padx=5, pady=5)

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

        self.clientes.bind("<<TreeviewSelect>>", self.eliminar)

        self.frame_acciones = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_acciones.pack(pady=20, fill="x", padx=20)

        self.btnEditar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="EDITAR", width=150,
            command=lambda: self.edita())
        self.btnEditar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_eliminar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="ELIMINAR", width=150,
            command=lambda: self.eliminar_UI())
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


    def BuscarPorNombre(self):
        nombre = self.ent_buscar_nombre.get().strip()
        for item in self.clientes.get_children():
            self.clientes.delete(item)

        clientes.buscar_por_nombre(nombre)
        for item in self.clientes.get_children():
                self.clientes.delete(item)
        datos = clientes.buscar_por_nombre(nombre)
        if datos:
            for fila in datos:
                self.clientes.insert("", "end", values=tuple(str(item).strip() for item in fila))
        else:
            print("No hay datos para mostrar en la interfaz.")

    def buscar_clave(self):
        clave = self.ent_buscar_calve.get().strip()
        for item in self.clientes.get_children():
            self.clientes.delete(item)

        clientes.buscar_clave(clave)
        for item in self.clientes.get_children():
                self.clientes.delete(item)
        datos = clientes.buscar_clave(clave)
        if datos:
            for fila in datos:
                self.clientes.insert("", "end", values=tuple(str(item).strip() for item in fila))
        else:
            print("No hay datos para mostrar en la interfaz.")



    def mostrarTalbe(self):
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

        colupnas = ("NOMBRE", "CORREO", "NUMERO")
        self.user_tabla = ttk.Treeview(ventana_correo, columns=colupnas, show="headings")

        self.user_tabla.heading("NOMBRE", text="NOMBRE")
        self.user_tabla.heading("CORREO", text="CORREO")
        self.user_tabla.heading("NUMERO", text="NUMERO")

        self.user_tabla.column("NOMBRE", width=100)
        self.user_tabla.column("CORREO", width=80, anchor="center")
        self.user_tabla.column("NUMERO",  width=80, anchor="center")

        self.user_tabla.pack(pady=20, padx=20, fill="both", expand=True)

        self.user_tabla.bind("<<TreeviewSelect>>", self.Mostrar_correos)

        self.mostrarTablaCorreos()

        self.correo_destino = ctk.CTkEntry(ventana_correo, placeholder_text="CORREO", text_color="#FFFFFF", width=600, height=70, font=("Arial", 15))
        self.correo_destino.pack(padx=10, pady=5)

        self.telefono_destino = ctk.CTkEntry(ventana_correo, placeholder_text="TELEFONO", text_color="#FFFFFF", width=600, height=70, font=("Arial", 15))
        self.telefono_destino.pack(padx=10, pady=5)

        mensaje = ctk.CTkTextbox(ventana_correo, text_color="#FFFFFF", width=600, height=200, font=("Arial", 15),
            )
        mensaje.pack(padx=10, pady=5)

        def enviar():
            from FuncionesEspeciales import F_embiarCorreo
            correo = self.correo_destino.get()
            contenido = mensaje.get("0.0", "end")
            azunto = "Trata de algun tema"
            F_embiarCorreo.embiarCorreo(correo, contenido, azunto)
            messagebox.showinfo("Envio", "se embio el correo")

        emviar = ctk.CTkButton(ventana_correo, text="EMVIAR CORREO", fg_color="#3E3E3E",
                width=200, height=70, font=("Arial", 15), command=lambda: enviar())
        emviar.pack(padx=10, pady=5)

        def enviar_texto():
            telefono = self.telefono_destino.get()
            contenido = mensaje.get("0.0", "end")

            quey = F_whatsapp.enviar_whatsapp(telefono, contenido)
            if quey:
                messagebox.showinfo("Envio", "se embio el correro")
            else:
                messagebox.showinfo("Envio", "Ubo un error")



        emviar = ctk.CTkButton(ventana_correo, text="EMVIAR MENSAJE", fg_color="#3E3E3E",
                width=200, height=70, font=("Arial", 15), command=lambda: enviar_texto())
        emviar.pack(padx=10, pady=5)

    def Mostrar_correos(self, event):
        seleccion = self.user_tabla.selection()
        if seleccion:
            item = self.user_tabla.item(seleccion)
            valores = item['values']

            self.correlo_electronico = valores[1]
            self.whatsap = valores[2]

            self.correo_destino.delete(0, "end")
            self.telefono_destino.delete(0, "end")

            self.correo_destino.insert(0, str(valores[1]).strip())
            self.telefono_destino.insert(0, str(valores[2]).strip())


    def mostrarTablaCorreos(self):
        for item in self.user_tabla.get_children():
            self.user_tabla.delete(item)
        datos = clientes.mostrarTablaCorreo()
        if datos:
            for fila in datos:
                 self.user_tabla.insert("", "end", values=tuple(str(item).strip() for item in fila))

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

    def eliminar_UI(self):
        COLOR_ROSA = "#F8C8DC"
        COLOR_NEGRO = "#1A1A1A"
        COLOR_FONDO = "#F2F2F2"
        COLOR_BLANCO = "#FFFFFF"

        try:
            calve_a_eliminar = self.clave_cliente_a_eliminar
            nombre_eliminar = self.nombre_a_eliminar

            ventana_mini = ctk.CTkToplevel()
            ventana_mini.title("Confirmar Eliminación")

            ventana_mini.geometry("600x400")
            ventana_mini.resizable(False, False)
            ventana_mini.configure(fg_color=COLOR_FONDO)
        except:
            from tkinter import messagebox
            messagebox.showinfo("ERORR", "SELECCIONE UN CLIENTE")
            return

        # ventana_mini.grab_set()

        frame = ctk.CTkFrame(ventana_mini, fg_color=COLOR_ROSA, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        texto = f"¿Quieres eliminar al usuario:\n{nombre_eliminar}?"
        label = ctk.CTkLabel(frame, text=texto, text_color=COLOR_NEGRO,
                                 font=("Arial", 14, "bold"), wraplength=300)
        label.pack(pady=(30, 20))

        def eliminar_cliente():
            print(f"se eliminara: {calve_a_eliminar}")
            clientes.delate(calve_a_eliminar)
            self.mostrarTalbe()

        btn_aceptar = ctk.CTkButton(frame, text="ACEPTAR",
                                        fg_color=COLOR_NEGRO,
                                        text_color=COLOR_BLANCO,
                                        hover_color="#333333",
                                        command=lambda: [eliminar_cliente(), ventana_mini.destroy()])
        btn_aceptar.pack(pady=10)

        btn_aceptar = ctk.CTkButton(frame, text="CANSELAR",
                                        fg_color=COLOR_NEGRO,
                                        text_color=COLOR_BLANCO,
                                        hover_color="#333333",
                                        command=lambda: [ventana_mini.destroy()])
        btn_aceptar.pack(pady=10)



    def eliminar(self, event):
        seleccion = self.clientes.selection()
        if seleccion:
            item = self.clientes.item(seleccion)
            valores = item['values']
            self.clave_cliente_a_eliminar = valores[0]
            self.nombre_a_eliminar = valores[1]
            print(self.clave_cliente_a_eliminar)



if __name__ == "__main__":
    obj = cliente()
