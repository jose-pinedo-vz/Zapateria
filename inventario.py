import customtkinter as ctk
from tkinter import ttk

class inventario:
    def __init__(self):
        self.ventana = ctk.CTkToplevel()
        self.ventana.title('CONTROL DE INVENTARIO - ZAPATERIA')
        self.ventana.configure(fg_color="#1A1A1A")

        try: self.ventana.state('zoomed')
        except: self.ventana.attributes('-zoomed', True)

        self.ventana.grid_columnconfigure(0, weight=0) # Menú (no se estira)
        self.ventana.grid_columnconfigure(1, weight=1) # Contenido (sí se estira)
        self.ventana.grid_rowconfigure(0, weight=1)    # Que ocupe todo el alto

        # FRAME del menu o la izquierda
        self.frame_menu = ctk.CTkFrame(self.ventana, fg_color="#2B2B2B", corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="ns", padx=0, pady=0)

        self.btn_listaInventario = ctk.CTkButton(
            self.frame_menu,
            text="INVENTARIO",
            fg_color="#3E3E3E",
            text_color="#F2F2F2",
            hover_color="#505050",
            command=lambda: self.frameCentral()
        )
        self.btn_listaInventario.grid(row=0, column=0, padx=20, pady=20)

        self.btn_listaInventario = ctk.CTkButton(
            self.frame_menu,
            text="REGISTRAR PRODUCTO",
            fg_color="#3E3E3E",
            text_color="#F2F2F2",
            hover_color="#505050",
            command=lambda: self.frameProdicto()
        )
        self.btn_listaInventario.grid(row=1, column=0, padx=20, pady=20)

        self.frame_contenido = ctk.CTkFrame(self.ventana, fg_color="#D1D1D1", corner_radius=0)
        self.frame_contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.frameCentral()

        self.ventana.mainloop()

    def limpiar_frame_central(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def frameCentral(self):
        self.limpiar_frame_central()
        # frame del centro
        self.fm_mostrar = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.fm_mostrar.pack(pady=20, fill="x", padx=20)

        apartado_inventario = ctk.CTkLabel(self.fm_mostrar, text="INVENTARIO", text_color="#1A1A1A", font=("ARIAL", 40))
        apartado_inventario.grid(row=0, column=0, padx=10, pady=10)

        self.frame_busqueda = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_busqueda.pack(pady=20, fill="x", padx=20)

        self.lb_busqueda = ctk.CTkLabel(self.frame_busqueda, text="BUSCAR CLAVE", text_color="#1A1A1A")
        self.lb_busqueda.grid(row=0, column=0, padx=10, pady=10)

        self.ent_buscar = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Ej: P001", width=150)
        self.ent_buscar.grid(row=0, column=1, padx=5, pady=5)

        self.btn_buscar = ctk.CTkButton(self.frame_busqueda, text="Buscar", width=100, fg_color="#3E3E3E")
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=5)

        colupnas = ("IMAGEN", "CLAVE", "CANTIDAD DEL PRODUCTO", "TALLA", "FECHA DE INGRESO", "PRECIO", "COLOR")

        self.tablaProductos = ttk.Treeview(self.frame_contenido, columns=colupnas, show="headings")

        self.tablaProductos.heading("IMAGEN", text="IMAGEN")
        self.tablaProductos.heading("CLAVE", text="CLAVE")
        self.tablaProductos.heading("CANTIDAD DEL PRODUCTO", text="CANTIDAD DEL PRODUCTO")
        self.tablaProductos.heading("TALLA", text="TALLA")
        self.tablaProductos.heading("FECHA DE INGRESO", text="FECHA DE INGRESO")
        self.tablaProductos.heading("PRECIO", text="PRECIO")
        self.tablaProductos.heading("COLOR", text="COLOR")

        self.tablaProductos.column("IMAGEN", width=100)
        self.tablaProductos.column("CLAVE", width=80, anchor="center")
        self.tablaProductos.column("CANTIDAD DEL PRODUCTO", width=120, anchor="center")
        self.tablaProductos.column("TALLA", width=60, anchor="center")
        self.tablaProductos.column("FECHA DE INGRESO", width=150, anchor="center")
        self.tablaProductos.column("PRECIO", width=80, anchor="center")
        self.tablaProductos.column("COLOR", width=80, anchor="center")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#F2F2F2",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#F2F2F2")
        style.map("Treeview", background=[('selected', '#3E3E3E')])

        self.tablaProductos.configure(height=15)
        self.tablaProductos.pack(fill="x", padx=20, pady=20)

        self.frame_acciones = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_acciones.pack(pady=20, fill="x", padx=20)

        self.btnEditar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="EDITAR", width=150)
        self.btnEditar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_eliminar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="ELIMINAR", width=150)
        self.btn_eliminar.grid(row=1, column=0, padx=10, pady=10)

        self.btn_surtir = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="SURTIR", width=150)
        self.btn_surtir.grid(row=0, column=1, padx=10, pady=10)

        self.btn_oferta = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="MOVE A OFERTA", width=150)
        self.btn_oferta.grid(row=1, column=1, padx=10, pady=10)

        self.btn_PROVEDORES = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="CORREO A PROVEEDORES", width=150,
            command=lambda: self.EnbiarCorreo())
        self.btn_PROVEDORES.grid(row=0, column=2, padx=10, pady=10)



    def frameProdicto(self):
        self.limpiar_frame_central()

        self.fm_mostrar = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.fm_mostrar.pack(pady=20, fill="x", padx=20)

        apartado_producto = ctk.CTkLabel(self.fm_mostrar, text="REGISTRO DE PRODUCTOS", text_color="#1A1A1A", font=("ARIAL", 40))
        apartado_producto.grid(row=0, column=0, padx=10, pady=10)

        self.frame_busqueda = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_busqueda.pack(pady=20, fill="x", padx=20)

        self.lb_busqueda = ctk.CTkLabel(self.frame_busqueda, text="BUSCAR CLAVE", text_color="#1A1A1A")
        self.lb_busqueda.grid(row=0, column=0, padx=10, pady=10)

        self.ent_buscar = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Ej: P001", width=150)
        self.ent_buscar.grid(row=0, column=1, padx=5, pady=5)

        self.btn_buscar = ctk.CTkButton(self.frame_busqueda, text="Buscar", width=100, fg_color="#3E3E3E")
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=5)
        colupnas = ("CLAVE", "MODELO", "MARCA", "SECCION", "CATEGORIA")
        self.tablaProductos = ttk.Treeview(self.frame_contenido, columns=colupnas, show="headings")

        self.tablaProductos.heading("CLAVE", text="CLAVE")
        self.tablaProductos.heading("MODELO", text="MODELO")
        self.tablaProductos.heading("MARCA", text="MARCA")
        self.tablaProductos.heading("SECCION", text="SECCION")
        self.tablaProductos.heading("CATEGORIA", text="CATEGORIA")

        self.tablaProductos.column("CLAVE", width=100)
        self.tablaProductos.column("MODELO", width=80, anchor="center")
        self.tablaProductos.column("MARCA", width=120, anchor="center")
        self.tablaProductos.column("SECCION", width=60, anchor="center")
        self.tablaProductos.column("CATEGORIA", width=150, anchor="center")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#F2F2F2",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#F2F2F2")
        style.map("Treeview", background=[('selected', '#3E3E3E')])

        self.tablaProductos.configure(height=15)
        self.tablaProductos.pack(fill="x", padx=20, pady=20)

        self.frame_acciones = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_acciones.pack(pady=20, fill="x", padx=20)

        self.btnEditar = ctk.CTkButton(self.frame_acciones, fg_color="#3E3E3E", text="EDITAR", width=150)
        self.btnEditar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_eliminar = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="ELIMINAR", width=150)
        self.btn_eliminar.grid(row=1, column=0, padx=10, pady=10)

        self.btn_surtir = ctk.CTkButton(self.frame_acciones,fg_color="#3E3E3E", text="AGREGAR",
                                        width=150,
                                        command=lambda: self.AgregarProducto()
                                        )
        self.btn_surtir.grid(row=0, column=1, padx=10, pady=10)

    def AgregarProducto(self):
        self.create_producto = ctk.CTkToplevel()
        self.create_producto.geometry("300x500")
        self.create_producto.title("DAR DE ALTA UN NUEVO PRODICTO")
        self.create_producto.configure(fg_color="#E5E5E5")

        self.en_modelo = ctk.CTkEntry(self.create_producto, placeholder_text="MODELO", text_color="#1A1A1A", width=200, height=70, font=("Arial", 15))
        self.en_modelo.pack(padx=10, pady=5)

        self.en_marca = ctk.CTkEntry(self.create_producto, placeholder_text="MARCA", text_color="#1A1A1A", width=200, height=70, font=("Arial", 15))
        self.en_marca.pack(padx=10, pady=5)

        opciones_seccion = ["Caballeros", "Damas", "Niños"]

        self.lbl_seccion = ctk.CTkLabel(self.create_producto, text="Sección:", text_color="#1A1A1A", width=200, height=70, font=("Arial", 15))
        self.lbl_seccion.pack(padx=10, pady=5)

        self.combo_seccion = ctk.CTkComboBox(
            self.create_producto,
            values=opciones_seccion,
            corner_radius=0,
            fg_color="#F2F2F2",
            text_color="#1A1A1A",
            width=200, height=70,
            font=("Arial", 15)
        )
        self.combo_seccion.pack(padx=10, pady=5)

        self.btn_registrar = ctk.CTkButton(self.create_producto, text="REGISTRAR", fg_color="#3E3E3E",
                                        width=200, height=70, font=("Arial", 15),
                                        command=lambda: self.insertarDatosProducto())
        self.btn_registrar.pack(padx=10, pady=5)

    def insertarDatosProducto(self):
        modelo = self.en_modelo.get()
        marca = self.en_marca.get()
        combo_box = self.combo_seccion.get()

        print(f"modelo {modelo}, marca {marca}, seccion {combo_box}")

    def EnbiarCorreo(self):
        ventana_correo = ctk.CTkToplevel()
        ventana_correo.geometry("1200x1000")
        ventana_correo.title("PEDIR PRODUCTO")
        ventana_correo.configure(fg_color="#E5E5E5")

        colupnas = ("NOMBRE", "CORREO")
        provedores_tabla = ttk.Treeview(ventana_correo, columns=colupnas, show="headings")

        provedores_tabla.heading("NOMBRE", text="NOMBRE")
        provedores_tabla.heading("CORREO", text="CORREO")
        provedores_tabla.column("NOMBRE", width=100)
        provedores_tabla.column("CORREO", width=80, anchor="center")
        provedores_tabla.pack(pady=20, padx=20, fill="both", expand=True)

        correo_destino = ctk.CTkEntry(ventana_correo, placeholder_text="CORREO", text_color="#FFFFFF", width=600, height=70, font=("Arial", 15))
        correo_destino.pack(padx=10, pady=5)

        mensaje = ctk.CTkTextbox(ventana_correo, text_color="#FFFFFF", width=600, height=200, font=("Arial", 15),
            )
        mensaje.pack(padx=10, pady=5)

        def enviar():
            from FuncionesEspeciales import F_embiarCorreo

            correo = correo_destino.get()
            contenido = mensaje.get("0.0", "end")
            azunto = "Reabastecimineto de algun tipo de producto: "
            F_e.embiarCorreo(correo, contenido, azunto)

        emviar = ctk.CTkButton(ventana_correo, text="EMVIAR", fg_color="#3E3E3E",
                                        width=200, height=70, font=("Arial", 15),
                                        command=lambda: enviar())
        emviar.pack(padx=10, pady=5)










obj = inventario()
