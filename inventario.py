import customtkinter as ctk
from tkinter import ttk
from tkinter import ttk, filedialog
import os
from FuncionesEspeciales import F_claves
from Controlador import productos
from tkinter import messagebox
from Controlador import inventario_SQL
from PIL import Image, ImageTk
import os
import os
import shutil

class inventario:
    def __init__(self):
        self.imagenes_renderizadas = []


        self.ventana = ctk.CTkToplevel()
        self.ventana.title('CONTROL DE INVENTARIO - ZAPATERIA')
        self.ventana.configure(fg_color="#1A1A1A")

        try: self.ventana.state('zoomed')
        except: self.ventana.attributes('-zoomed', True)

        self.ventana.grid_columnconfigure(0, weight=0)
        self.ventana.grid_columnconfigure(1, weight=1)
        self.ventana.grid_rowconfigure(0, weight=1)

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

        self.frame_contenido = ctk.CTkScrollableFrame(
                self.ventana,
                fg_color="#D1D1D1",
                corner_radius=0,
                orientation="vertical"
        )
        self.frame_contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.frameCentral()

        self.ventana.mainloop()

    def limpiar_frame_central(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def frameCentral(self):
        self.limpiar_frame_central()
        # frame del centro
        self.fm_mostrar = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5",corner_radius=15)
        self.fm_mostrar.pack(pady=20, fill="x", padx=20)

        apartado_inventario = ctk.CTkLabel(self.fm_mostrar, text="INVENTARIO", text_color="#1A1A1A", font=("ARIAL", 40))
        apartado_inventario.grid(row=0, column=0, padx=10, pady=10)

        self.frame_busqueda = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_busqueda.pack(pady=20, fill="x", padx=20)

        self.lb_busqueda = ctk.CTkLabel(self.frame_busqueda, text="BUSCAR CLAVE", text_color="#1A1A1A")
        self.lb_busqueda.grid(row=0, column=0, padx=10, pady=10)

        self.ent_buscar = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Ej: P001", width=150)
        self.ent_buscar.grid(row=0, column=1, padx=5, pady=5)

        self.btn_buscar = ctk.CTkButton(self.frame_busqueda, text="Buscar", width=100, fg_color="#FF5733")
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=5)

        self.frame_acciones = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.frame_acciones.pack(pady=20, fill="x", padx=20)

        self.btnEditar = ctk.CTkButton(self.frame_acciones,fg_color="#FF5733", text="EDITAR", width=150,
            command=lambda: self.editar_inventario())
        self.btnEditar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_eliminar = ctk.CTkButton(self.frame_acciones,fg_color="#FF5733", text="ELIMINAR", width=150,
             command=lambda: self.eliminar_inventario())
        self.btn_eliminar.grid(row=1, column=0, padx=10, pady=10)

        self.btn_surtir = ctk.CTkButton(self.frame_acciones,fg_color="#FF5733", text="SURTIR", width=150,
                                     command=lambda: self.agregarInventario())
        self.btn_surtir.grid(row=0, column=1, padx=10, pady=10)

        self.btn_oferta = ctk.CTkButton(self.frame_acciones,fg_color="#FF5733", text="MOVE A OFERTA", width=150)
        self.btn_oferta.grid(row=1, column=1, padx=10, pady=10)

        self.btn_PROVEDORES = ctk.CTkButton(self.frame_acciones,fg_color="#FF5733", text="CORREO A PROVEEDORES", width=150,
             command=lambda: self.EnbiarCorreo())
        self.btn_PROVEDORES.grid(row=0, column=2, padx=10, pady=10)

        colupnas = ("CLAVE", "CANTIDAD DEL PRODUCTO", "TALLA", "FECHA DE INGRESO", "PRECIO", "COLOR")

        # self.frame_tabla_fijo = ctk.CTkFrame(self.frame_contenido, width=800, height=450)
        # self.frame_tabla_fijo.pack_propagate(False) # ¡VITAL! Evita que el frame cambie de tamaño
        # self.frame_tabla_fijo.pack(pady=20)


        self.tablaProductos = ttk.Treeview(self.frame_contenido, columns=colupnas, show="tree headings")

        for col in colupnas:
            self.tablaProductos.heading(col, text=col)

        self.tablaProductos.column("#0", width=100, anchor="center")
        self.tablaProductos.heading("#0", text="IMAGEN")

        # La suma de estos 'width' define el ancho total de la tabla
        self.tablaProductos.column("#0", width=150, stretch=False, anchor="center")
        self.tablaProductos.column("CLAVE", width=100, stretch=True, anchor="center")
        self.tablaProductos.column("CANTIDAD DEL PRODUCTO", width=200, stretch=True, anchor="center")
        self.tablaProductos.column("TALLA", width=100, stretch=True, anchor="center")
        self.tablaProductos.column("FECHA DE INGRESO", width=200, stretch=True, anchor="center")
        self.tablaProductos.column("PRECIO", width=100, stretch=True, anchor="center")
        self.tablaProductos.column("COLOR", width=150, stretch=True, anchor="center")


        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#F2F2F2",
                        foreground="black",
                        rowheight=100,
                        fieldbackground="#F2F2F2")

        style.map("Treeview", background=[('selected', '#3E3E3E')])

        self.tablaProductos.pack(side="top", fill="both", expand=True)

        self.tablaProductos.bind("<<TreeviewSelect>>", self.eliminar_inve)
        # scrrol barr pos si algun dia se nesesita

        # self.scrollbar = ttk.Scrollbar(self.frame_tabla_fijo, orient="vertical", command=self.tablaProductos.yview)
        # self.tablaProductos.configure(yscrollcommand=self.scrollbar.set)
        # self.scrollbar.pack(side="right", fill="y")



        self.llenarTalbaProd()


    def llenarTalbaProd(self):
        self.imagenes_renderizadas.clear()

        for item in self.tablaProductos.get_children():
            self.tablaProductos.delete(item)

        datos = inventario_SQL.consultar()

        if datos:
            for fila in datos:
                ruta_img = fila[0]
                resto_datos = fila[1:]

                foto_final = self.cargar_y_redimensionar(ruta_img)
                self.imagenes_renderizadas.append(foto_final)

                self.tablaProductos.insert(
                    "",
                    "end",
                    image=foto_final,
                    values=tuple(str(item).strip() for item in resto_datos)
                )
        # print(self.imagenes_renderizadas)

    def cargar_y_redimensionar(self, ruta):
        try:
            ruta = ruta.strip()
            if ruta == "SIN IMAGEN" or not os.path.exists(ruta):
                img = Image.new('RGB', (90, 90), color=(200, 200, 200))
            else:
                img = Image.open(ruta)

            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        except Exception as e:
            print(f"ERROR CRÍTICO cargando imagen {ruta}: {e}")
            return ImageTk.PhotoImage(Image.new('RGB', (50, 50), color=(255, 0, 0)))


    def frameProdicto(self):
        self.limpiar_frame_central()

        self.fm_mostrar = ctk.CTkFrame(self.frame_contenido, fg_color="#E5E5E5")
        self.fm_mostrar.pack(pady=20, fill="x", padx=20)

        apartado_producto = ctk.CTkLabel(self.fm_mostrar, text="REGISTRO DE PRODUCTOS", text_color="#1A1A1A", font=("ARIAL", 40))
        apartado_producto.grid(row=0, column=0, padx=10, pady=10)

        self.frame_busqueda = ctk.CTkFrame(self.frame_contenido, fg_color="#FFFFFF", corner_radius=15)
        self.frame_busqueda.pack(pady=20, fill="x", padx=20)

        self.lb_busqueda = ctk.CTkLabel(self.frame_busqueda, text="BUSCAR CLAVE", text_color="#1A1A1A")
        self.lb_busqueda.grid(row=0, column=0, padx=10, pady=10)

        self.ent_buscar = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Ej: P001", width=150)
        self.ent_buscar.grid(row=0, column=1, padx=5, pady=5)

        self.btn_buscar = ctk.CTkButton(self.frame_busqueda, text="Buscar", width=100, fg_color="#FF5733")
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
                        rowheight=35,
                        fieldbackground="#F2F2F2")
        style.map("Treeview", background=[('selected', '#3E3E3E')])

        self.tablaProductos.configure(height=15)
        self.tablaProductos.pack(fill="x", padx=20, pady=20)

        self.tablaProductos.bind("<<TreeviewSelect>>", self.eliminar)

        self.frame_acciones = ctk.CTkFrame(self.frame_contenido, fg_color="#FFFFFF", corner_radius=15)
        self.frame_acciones.pack(pady=20, fill="x", padx=20)

        self.btnEditar = ctk.CTkButton(self.frame_acciones, fg_color="#FF5733", text="EDITAR", width=150,
            command=lambda: self.edita())
        self.btnEditar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_eliminar = ctk.CTkButton(self.frame_acciones,fg_color="#FF5733", text="ELIMINAR", width=150,
                                        command=lambda: self.eliminar_UI())
        self.btn_eliminar.grid(row=1, column=0, padx=10, pady=10)

        self.btn_surtir = ctk.CTkButton(self.frame_acciones,fg_color="#FF5733", text="AGREGAR",
                                        width=150,
                                        command=lambda: self.AgregarProducto()
                                        )
        self.btn_surtir.grid(row=0, column=1, padx=10, pady=10)

        self.llenarTablaProductos()

    def llenarTablaProductos(self):
        for item in self.tablaProductos.get_children():
            self.tablaProductos.delete(item)

        productos.mostrar()
        for item in self.tablaProductos.get_children():
                self.tablaProductos.delete(item)
        datos = productos.mostrar()
        if datos:
            for fila in datos:
                self.tablaProductos.insert("", "end", values=tuple(str(item).strip() for item in fila))
        else:
            print("No hay datos para mostrar en la interfaz.")

    def AgregarProducto(self):
        self.create_producto = ctk.CTkToplevel()
        self.create_producto.geometry("500x800")
        self.create_producto.title("DAR DE ALTA UN NUEVO PRODICTO")
        self.create_producto.configure(fg_color="#E5E5E5")

        self.en_modelo = ctk.CTkEntry(self.create_producto, placeholder_text="MODELO", text_color="#FFFFFF", width=200, height=70, font=("Arial", 15))
        self.en_modelo.pack(padx=10, pady=5)

        self.en_marca = ctk.CTkEntry(self.create_producto, placeholder_text="MARCA", text_color="#FFFFFF", width=200, height=70, font=("Arial", 15))
        self.en_marca.pack(padx=10, pady=5)

        opciones_seccion = ["Caballeros", "Damas", "Niños", "Niña", "Bebé", "Unisex"]

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

        categorias = ["Escolar", "Casual", "Vestir", "Bota", "Deportivo", "Urbano", "Fútbol",
            "Sandalia", "Pantufla", "Huarache", "Bota de Lluvia"]

        self.lbl_categoria = ctk.CTkLabel(self.create_producto, text="Sección:", text_color="#1A1A1A", width=200, height=70, font=("Arial", 15))
        self.lbl_categoria.pack(padx=10, pady=5)

        self.combo_categoria = ctk.CTkComboBox(
            self.create_producto,
            values=categorias,
            corner_radius=0,
            fg_color="#F2F2F2",
            text_color="#1A1A1A",
            width=200, height=70,
            font=("Arial", 15)
        )
        self.combo_categoria.pack(padx=10, pady=5)


        self.btn_registrar = ctk.CTkButton(self.create_producto, text="REGISTRAR", fg_color="#3E3E3E",
                                        width=200, height=70, font=("Arial", 15),
                                        command=lambda: self.insertarDatosProducto())
        self.btn_registrar.pack(padx=10, pady=5)

    def insertarDatosProducto(self):
        modelo = self.en_modelo.get()
        marca = self.en_marca.get()
        seccion = self.combo_seccion.get()
        categoria = self.combo_categoria.get()

        clave = F_claves.Generar_clave_producto()
        try:
            productos.insert(clave, modelo, marca, seccion, categoria)
            # messagebox.showinfo("Todo correcto", "todo salio correcto")
            self.llenarTablaProductos()
        except:
            messagebox.showinfo("Error", "Ubo un error en la insercion de datos")


    def edita(self):
            COLOR_PRIMARIO = "#FFFFFF"
            COLOR_SECUNDARIO = "#FF5733"
            COLOR_TERCIARIO = "#FFB0CC"
            COLOR_COMPLEMENTARIO = "#8DCCE3"
            COLOR_FONDO_BLANCO = "#1A1A1A"
            COLOR_TEXTO_NEGRO = "#1A1A1A"

            ventana_correo = ctk.CTkToplevel()
            ventana_correo.geometry("1800x1200")
            ventana_correo.title("APARTADO DE PRODUCTOS")
            ventana_correo.configure(fg_color=COLOR_FONDO_BLANCO)

            ventana_correo.grid_columnconfigure(0, weight=1)
            ventana_correo.grid_columnconfigure(1, weight=2)
            ventana_correo.grid_rowconfigure(0, weight=1)


            frame_izquierdo = ctk.CTkFrame(ventana_correo, fg_color=COLOR_PRIMARIO, corner_radius=15)
            frame_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

            ctk.CTkLabel(frame_izquierdo, text="DATOS DEL PRODUCTO", text_color=COLOR_TEXTO_NEGRO, font=("Arial", 16, "bold")).pack(pady=20)

            self.en_modelo = ctk.CTkEntry(frame_izquierdo, placeholder_text="MODELO", text_color="#FFFFFF", width=200, height=70, font=("Arial", 15))
            self.en_modelo.pack(padx=10, pady=5)

            self.en_marca = ctk.CTkEntry(frame_izquierdo, placeholder_text="MARCA", text_color="#FFFFFF", width=200, height=70, font=("Arial", 15))
            self.en_marca.pack(padx=10, pady=5)

            opciones_seccion = ["Caballeros", "Damas", "Niños", "Niña", "Bebé", "Unisex"]

            self.lbl_seccion = ctk.CTkLabel(frame_izquierdo, text="Sección:", text_color="#1A1A1A", width=200, height=70, font=("Arial", 15))
            self.lbl_seccion.pack(padx=10, pady=5)

            self.combo_seccion = ctk.CTkComboBox(
                frame_izquierdo,
                values=opciones_seccion,
                corner_radius=0,
                fg_color="#F2F2F2",
                text_color="#1A1A1A",
                width=200, height=70,
                font=("Arial", 15)
            )
            self.combo_seccion.pack(padx=10, pady=5)

            categorias = ["Escolar", "Casual", "Vestir", "Bota", "Deportivo", "Urbano", "Fútbol",
                "Sandalia", "Pantufla", "Huarache", "Bota de Lluvia"]

            self.lbl_categoria = ctk.CTkLabel(frame_izquierdo, text="Sección:", text_color="#1A1A1A", width=200, height=70, font=("Arial", 15))
            self.lbl_categoria.pack(padx=10, pady=5)

            self.combo_categoria = ctk.CTkComboBox(
                frame_izquierdo,
                values=categorias,
                corner_radius=0,
                fg_color="#F2F2F2",
                text_color="#1A1A1A",
                width=200, height=70,
                font=("Arial", 15)
            )
            self.combo_categoria.pack(padx=10, pady=5)


            def editar():
                try:
                    modelo = self.en_modelo.get()
                    marca = self.en_marca.get()
                    seccion = self.combo_seccion.get()
                    categoria = self.combo_categoria.get()
                    print("Se va")
                    productos.update(self.clave_productos, modelo, marca, seccion, categoria)
                    self.llenarTablaProductos()
                    ventana_correo.destroy()
                except Exception as e:
                    print(f"El erro es {e}")
                    from tkinter import messagebox
                    messagebox.showinfo("Fallo", "No se puede actualizar")

            self.btn_accion = ctk.CTkButton(frame_izquierdo, text="ACTUALIZAR", fg_color=COLOR_SECUNDARIO, hover_color=COLOR_TERCIARIO,
                command=lambda: editar())
            self.btn_accion.pack(pady=30)

            frame_derecho = ctk.CTkFrame(ventana_correo, fg_color=COLOR_FONDO_BLANCO)
            frame_derecho.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

            COLOR_FONDO_TABLA = "#FFFFFF"  # Blanco puro
            COLOR_TEXTO_TABLA = "#000000"  # Negro puro
            COLOR_CABECERA = "#1A1A1A"     # Gris muy oscuro (Negro)
            COLOR_SELECCION = "#D3D3D3"    # Gris claro para cuando seleccionas una fila

            style = ttk.Style()
            style.theme_use("clam")

            style.configure("Treeview",
                            background=COLOR_FONDO_TABLA,
                            foreground=COLOR_TEXTO_TABLA,
                            rowheight=35,
                            fieldbackground=COLOR_FONDO_TABLA,
                            borderwidth=0,
                            font=("Arial", 11))

            style.map("Treeview",
                      background=[('selected', COLOR_SELECCION)],
                      foreground=[('selected', COLOR_TEXTO_TABLA)])

            style.configure("Treeview.Heading",
                            background=COLOR_CABECERA,
                            foreground="#FFFFFF",
                            relief="flat",
                            font=("Arial", 10, "bold"))


            style.map("Treeview.Heading",
                      background=[('active', COLOR_CABECERA)])

            colupnas = ("Clave", "Modelo", "Marca", "Seccion", "categoria")
            self.editar_talbla = ttk.Treeview(frame_derecho, columns=colupnas, show="headings", style="Treeview")


            self.editar_talbla.heading("Clave", text="Clave")
            self.editar_talbla.heading("Modelo", text="Modelo")
            self.editar_talbla.heading("Marca", text="Marca")
            self.editar_talbla.heading("Seccion", text="Seccion")
            self.editar_talbla.heading("categoria", text="categoria")

            self.editar_talbla.pack(fill="both", expand=True)

            self.mostrarTablaEditar()

            self.editar_talbla.bind("<<TreeviewSelect>>", self.obtener_datos_seleccionados_de_editar)

    def obtener_datos_seleccionados_de_editar(self, event):
            seleccion = self.editar_talbla.selection()
            if seleccion:
                item = self.editar_talbla.item(seleccion)
                valores = item['values']
                self.clave_productos = valores[0]
                Modelo = valores[1]
                marca = valores[2]

                self.en_modelo.delete(0, "end")
                self.en_modelo.insert(0, Modelo)
                self.en_marca.delete(0, "end")
                self.en_marca.insert(0, marca)

    def mostrarTablaEditar(self):
        for item in self.editar_talbla.get_children():
                self.editar_talbla.delete(item)
        datos = productos.mostrar()
        if datos:
            for fila in datos:
                self.editar_talbla.insert("", "end", values=tuple(str(item).strip() for item in fila))

    def EnbiarCorreo(self):
        ventana_correo = ctk.CTkToplevel()
        ventana_correo.geometry("700x800") # Ajusté un poco el tamaño para que sea más manejable
        ventana_correo.title("GESTIÓN DE PEDIDOS A PROVEEDORES")
        ventana_correo.configure(fg_color="#E5E5E5")

        # --- TABLA DE PROVEEDORES ---
        colupnas = ("NOMBRE", "CORREO")
        provedores_tabla = ttk.Treeview(ventana_correo, columns=colupnas, show="headings")

        provedores_tabla.heading("NOMBRE", text="PROVEEDOR")
        provedores_tabla.heading("CORREO", text="CORREO ELECTRÓNICO")
        provedores_tabla.column("NOMBRE", width=200, anchor="center")
        provedores_tabla.column("CORREO", width=300, anchor="center")

        # Datos de ejemplo (puedes cambiarlos por tus proveedores reales)
        proveedores = [
            ("Nike", "josepinedovaldes@gmail.com"),
            ("Adiadas", "pedidos@gmail.mx")
        ]

        for p in proveedores:
            provedores_tabla.insert("", "end", values=p)

        provedores_tabla.pack(pady=20, padx=20, fill="x")

        # --- CAMPOS DE TEXTO ---
        label_correo = ctk.CTkLabel(ventana_correo, text="Destinatario:", text_color="#000000")
        label_correo.pack(padx=10, pady=(10, 0))

        correo_destino = ctk.CTkEntry(ventana_correo, placeholder_text="Seleccione un proveedor de la tabla...",
                                      text_color="#FFFFFF", width=500, height=40, font=("Arial", 14))
        correo_destino.pack(padx=10, pady=5)

        label_msg = ctk.CTkLabel(ventana_correo, text="Mensaje del Pedido:", text_color="#000000")
        label_msg.pack(padx=10, pady=(10, 0))

        mensaje = ctk.CTkTextbox(ventana_correo, text_color="#FFFFFF", width=500, height=250, font=("Arial", 14))
        mensaje.pack(padx=10, pady=5)

        # --- FUNCIONALIDAD ---

        def seleccionar_proveedor(event):
            """ Inserta el correo del proveedor seleccionado en el Entry """
            seleccion = provedores_tabla.selection()
            if seleccion:
                item = provedores_tabla.item(seleccion)
                email = item['values'][1] # El índice 1 es el CORREO
                correo_destino.delete(0, "end")
                correo_destino.insert(0, email)

        # Vincular el evento de clic en la tabla
        provedores_tabla.bind("<<TreeviewSelect>>", seleccionar_proveedor)

        def generar_mensaje_auto():
            """ Genera un texto predefinido """
            # Aquí puedes usar variables globales de tu stock si quieres hacerlo más dinámico
            texto_auto = "Estimado proveedor,\n\nPor medio de la presente solicito el reabastecimiento de insumos para el restaurante.\nFavor de enviar cotización de los productos faltantes según el inventario actual.\n\nQuedo a la espera de su confirmación.\nSaludos cordiales."
            mensaje.delete("1.0", "end")
            mensaje.insert("1.0", texto_auto)

        def enviar():
            from FuncionesEspeciales import F_embiarCorreo
            correo = correo_destino.get()
            contenido = mensaje.get("1.0", "end")
            azunto = "Pedido de Reabastecimiento - Zapateria 2 Hermanos"
            F_embiarCorreo.embiarCorreo(correo, contenido, azunto)

        # --- BOTONES ---
        btn_container = ctk.CTkFrame(ventana_correo, fg_color="transparent")
        btn_container.pack(pady=20)

        btn_auto = ctk.CTkButton(btn_container, text="MENSAJE AUTOMÁTICO", fg_color="#3E3E3E",
                                 width=220, height=50, font=("Arial", 13, "bold"),
                                 command=generar_mensaje_auto)
        btn_auto.grid(row=0, column=0, padx=10)

        btn_enviar = ctk.CTkButton(btn_container, text="ENVIAR CORREO", fg_color="#3E3E3E",
                                   width=220, height=50, font=("Arial", 13, "bold"),
                                   command=enviar)
        btn_enviar.grid(row=0, column=1, padx=10)

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

        frame = ctk.CTkFrame(ventana_mini, fg_color=COLOR_BLANCO, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        texto = f"¿Quieres eliminar al usuario:\n{nombre_eliminar}?"
        label = ctk.CTkLabel(frame, text=texto, text_color=COLOR_NEGRO,
                                font=("Arial", 14, "bold"), wraplength=300)
        label.pack(pady=(30, 20))

        def eliminar_cliente():
            print(f"se eliminara: {calve_a_eliminar}")
            productos.delate(calve_a_eliminar)
            self.llenarTablaProductos()

        btn_aceptar = ctk.CTkButton(frame, text="ACEPTAR",
                                        fg_color=COLOR_NEGRO,
                                        text_color=COLOR_BLANCO,
                                        hover_color="#FF5733",
                                        command=lambda: [eliminar_cliente(), ventana_mini.destroy()])
        btn_aceptar.pack(pady=10)

        btn_aceptar = ctk.CTkButton(frame, text="CANSELAR",
                                        fg_color=COLOR_NEGRO,
                                        text_color=COLOR_BLANCO,
                                        hover_color="#FF5733",
                                        command=lambda: [ventana_mini.destroy()])
        btn_aceptar.pack(pady=10)

    def eliminar(self, event):
        seleccion = self.tablaProductos.selection()
        if seleccion:
            item = self.tablaProductos.item(seleccion)
            valores = item['values']
            self.clave_cliente_a_eliminar = valores[0]
            self.nombre_a_eliminar = valores[1]
            print(self.clave_cliente_a_eliminar)


    def agregarInventario(self):
        COLOR_FONDO = "#1A1A1A"
        COLOR_ENTRADAS = "#2B2B2B"
        COLOR_BOTON = "#FF5733"

        ventana_inv = ctk.CTkToplevel()
        ventana_inv.geometry("1600x800")
        ventana_inv.title("SURTIR")
        ventana_inv.configure(fg_color=COLOR_FONDO)

        # Configuración de proporciones (1:2)
        ventana_inv.grid_columnconfigure(0, weight=1) # Panel Izquierdo (Captura)
        ventana_inv.grid_columnconfigure(1, weight=3) # Panel Derecho (Tabla)
        ventana_inv.grid_rowconfigure(0, weight=1)

        # --- LADO IZQUIERDO: FORMULARIO ---
        frame_izq = ctk.CTkFrame(ventana_inv, fg_color=COLOR_FONDO, corner_radius=0)
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(frame_izq, text="DATOS DE ENTRADA", font=("Arial", 20, "bold")).pack(pady=(0, 20))

        self.ent_clave = ctk.CTkEntry(frame_izq, placeholder_text="Clave", width=250, height=45)
        self.ent_clave.pack(pady=10)

        self.ent_clave.configure(state="disabled")


        self.ent_cantidad = ctk.CTkEntry(frame_izq, placeholder_text="Cantidad de Producto", width=250, height=45)
        self.ent_cantidad.pack(pady=10)

        self.ent_talla = ctk.CTkEntry(frame_izq, placeholder_text="Talla", width=250, height=45)
        self.ent_talla.pack(pady=10)

        self.ent_precio = ctk.CTkEntry(frame_izq, placeholder_text="Precio $", width=250, height=45)
        self.ent_precio.pack(pady=10)

        self.ent_color = ctk.CTkEntry(frame_izq, placeholder_text="Color", width=250, height=45)
        self.ent_color.pack(pady=10)

        frame_img = ctk.CTkFrame(frame_izq, fg_color="transparent")
        frame_img.pack(pady=20)

        self.ent_ruta_img = ctk.CTkEntry(frame_img, placeholder_text="Ruta de imagen...", width=160, height=40)
        self.ent_ruta_img.pack(side="left", padx=5)

        def seleccionar_archivo():
            ruta = filedialog.askopenfilename(initialdir="/", title="Imagen",
                                             filetypes=(("Archivos de imagen", "*.jpg *.png *.jpeg"), ("Todos", "*.*")))
            self.ent_ruta_img.delete(0, 'end')
            self.ent_ruta_img.insert(0, ruta)

        btn_explorar = ctk.CTkButton(frame_img, text="...", width=40, height=40, command=seleccionar_archivo)
        btn_explorar.pack(side="left")

        def recupareraDatos():

            CARPETA_DESTINO = "imagenes_productos"
            if not os.path.exists(CARPETA_DESTINO):
                os.mkedir(CARPETA_DESTINO)\

            ruta = self.ent_ruta_img.get()
            if ruta.strip() == ""  or not os.path.exists(ruta):
                ruta = "SIN IMAGEN"
            else:
                nombre_arhivo = os.path.basename(ruta)
                ruta_destino = os.path.join(CARPETA_DESTINO, nombre_arhivo)
                shutil.copy2(ruta, ruta_destino)
                ruta_final = ruta_destino

            try:
                Clave = self.ent_clave.get()
                CantidadPorducto = int(self.ent_cantidad.get())
                Talla = int(self.ent_talla.get())
                Precio = float(self.ent_precio.get())
                color = self.ent_color.get()
                ventana_inv.destroy()
            except:
                from tkinter import messagebox
                messagebox.showinfo("ERORR", "POSIBLE ERROR EN LOS DATOS")

            inventario_SQL.insert(Clave, CantidadPorducto, Talla, Precio, color, ruta_final)

        self.btn_surtir = ctk.CTkButton(frame_izq, text="SURTIR PRODUCTO", fg_color=COLOR_BOTON,
                                       height=60, font=("Arial", 16, "bold"),
                                       command=lambda: recupareraDatos())
        self.btn_surtir.pack(side="bottom", pady=20, fill="x")


        # derecha
        frame_der = ctk.CTkFrame(ventana_inv, fg_color="#FFFFFF", corner_radius=15)
        frame_der.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#000000", fieldbackground="#FFFFFF", rowheight=40)
        style.configure("Treeview.Heading", background="#1A1A1A", foreground="#FFFFFF", font=("Arial", 11, "bold"))

        columnas = ("Clave", "Modelo", "Marca", "Seccion", "Categoria")
        self.tabla_inv = ttk.Treeview(frame_der, columns=columnas, show="headings", style="Treeview")

        for col in columnas:
            self.tabla_inv.heading(col, text=col)
            self.tabla_inv.column(col, anchor="center")

        self.tabla_inv.pack(fill="both", expand=True, padx=10, pady=10)
        self.llenarTalbaInv()

        self.tabla_inv.bind("<<TreeviewSelect>>", self.OptenerClaveparaLlaveForanea)

    def llenarTalbaInv(self):
        for item in self.tabla_inv.get_children():
                self.tabla_inv.delete(item)
        datos = productos.mostrar()
        if datos:
            for fila in datos:
                self.tabla_inv.insert("", "end", values=tuple(str(item).strip() for item in fila))

    def OptenerClaveparaLlaveForanea(self, event):
            seleccion = self.tabla_inv.selection()
            if seleccion:
                item = self.tabla_inv.item(seleccion)
                valores = item['values']
                self.clave_producto = valores[0]
                self.ent_clave.configure(state="normal")
                self.ent_clave.delete(0, "end")
                self.ent_clave.insert(0, self.clave_producto)
                self.ent_clave.configure(state="disabled")




    def editar_inventario(self):
        COLOR_FONDO = "#1A1A1A"
        COLOR_ENTRADAS = "#2B2B2B"
        COLOR_BOTON = "#FF5733"

        ventana_inv = ctk.CTkToplevel()
        ventana_inv.geometry("1600x800")
        ventana_inv.title("EDITAR INVENTARIO")
        ventana_inv.configure(fg_color=COLOR_FONDO)

        # Configuración de proporciones (1:2)
        ventana_inv.grid_columnconfigure(0, weight=1) # Panel Izquierdo (Captura)
        ventana_inv.grid_columnconfigure(1, weight=3) # Panel Derecho (Tabla)
        ventana_inv.grid_rowconfigure(0, weight=1)

        # --- LADO IZQUIERDO: FORMULARIO ---
        frame_izq = ctk.CTkFrame(ventana_inv, fg_color=COLOR_FONDO, corner_radius=0)
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(frame_izq, text="DATOS DE ENTRADA", font=("Arial", 20, "bold")).pack(pady=(0, 20))

        self.ent_clave = ctk.CTkEntry(frame_izq, placeholder_text="Clave", width=250, height=45)
        self.ent_clave.pack(pady=10)

        self.ent_clave.configure(state="disabled")

        self.ent_cantidad = ctk.CTkEntry(frame_izq, placeholder_text="Cantidad de Producto", width=250, height=45)
        self.ent_cantidad.pack(pady=10)

        self.ent_talla = ctk.CTkEntry(frame_izq, placeholder_text="Talla", width=250, height=45)
        self.ent_talla.pack(pady=10)

        self.ent_precio = ctk.CTkEntry(frame_izq, placeholder_text="Precio $", width=250, height=45)
        self.ent_precio.pack(pady=10)

        self.ent_color = ctk.CTkEntry(frame_izq, placeholder_text="Color", width=250, height=45)
        self.ent_color.pack(pady=10)

        frame_img = ctk.CTkFrame(frame_izq, fg_color="transparent")
        frame_img.pack(pady=20)

        # self.ent_ruta_img = ctk.CTkEntry(frame_img, placeholder_text="Ruta de imagen...", width=160, height=40)
        # self.ent_ruta_img.pack(side="left", padx=5)

        # def seleccionar_archivo():
        #     ruta = filedialog.askopenfilename(initialdir="/", title="Imagen",
        #                                      filetypes=(("Archivos de imagen", "*.jpg *.png *.jpeg"), ("Todos", "*.*")))
        #     self.ent_ruta_img.delete(0, 'end')
        #     self.ent_ruta_img.insert(0, ruta)

        # btn_explorar = ctk.CTkButton(frame_img, text="...", width=40, height=40, command=seleccionar_archivo)
        # btn_explorar.pack(side="left")

        def recupareraDatos():
            CARPETA_DESTINO = "imagenes_productos"
            if not os.path.exists(CARPETA_DESTINO):
                os.mkedir(CARPETA_DESTINO)\

            ruta = self.ent_ruta_img.get()
            if ruta.strip() == ""  or not os.path.exists(ruta):
                ruta = "SIN IMAGEN"
            else:
                nombre_arhivo = os.path.basename(ruta)
                ruta_destino = os.path.join(CARPETA_DESTINO, nombre_arhivo)
                shutil.copy2(ruta, ruta_destino)
                ruta_final = ruta_destino

            try:
                Clave = self.ent_clave.get()
                CantidadPorducto = int(self.ent_cantidad.get())
                Talla = int(self.ent_talla.get())
                Precio = float(self.ent_precio.get())
                color = self.ent_color.get()
                ventana_inv.destroy()
            except:
                from tkinter import messagebox
                messagebox.showinfo("ERORR", "POSIBLE ERROR EN LOS DATOS")

            inventario_SQL.insert(Clave, CantidadPorducto, Talla, Precio, color, ruta_final)

        self.btn_surtir = ctk.CTkButton(frame_izq, text="SURTIR PRODUCTO", fg_color=COLOR_BOTON,
                                       height=60, font=("Arial", 16, "bold"),
                                       command=lambda: recupareraDatos())
        self.btn_surtir.pack(side="bottom", pady=20, fill="x")


        # derecha
        frame_der = ctk.CTkFrame(ventana_inv, fg_color="#FFFFFF", corner_radius=15)
        frame_der.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        colupnas = ("CLAVE", "CANTIDAD DEL PRODUCTO", "TALLA", "FECHA DE INGRESO", "PRECIO", "COLOR")

         # self.frame_tabla_fijo = ctk.CTkFrame(self.frame_contenido, width=800, height=450)
         # self.frame_tabla_fijo.pack_propagate(False) # ¡VITAL! Evita que el frame cambie de tamaño
         # self.frame_tabla_fijo.pack(pady=20)


        self.tablaProductos_editar_inventrio = ttk.Treeview(frame_der, columns=colupnas, show="tree headings")

        for col in colupnas:
            self.tablaProductos_editar_inventrio.heading(col, text=col)

        self.tablaProductos_editar_inventrio.column("#0", width=100, anchor="center")
        self.tablaProductos_editar_inventrio.heading("#0", text="IMAGEN")

        self.tablaProductos_editar_inventrio.column("#0", width=150, stretch=False, anchor="center")
        self.tablaProductos_editar_inventrio.column("CLAVE", width=100, stretch=True, anchor="center")
        self.tablaProductos_editar_inventrio.column("CANTIDAD DEL PRODUCTO", width=200, stretch=True, anchor="center")
        self.tablaProductos_editar_inventrio.column("TALLA", width=100, stretch=True, anchor="center")
        self.tablaProductos_editar_inventrio.column("FECHA DE INGRESO", width=200, stretch=True, anchor="center")
        self.tablaProductos_editar_inventrio.column("PRECIO", width=100, stretch=True, anchor="center")
        self.tablaProductos_editar_inventrio.column("COLOR", width=150, stretch=True, anchor="center")


        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background="#F2F2F2",
                         foreground="black",
                         rowheight=100,
                         fieldbackground="#F2F2F2")

        style.map("Treeview", background=[('selected', '#3E3E3E')])

        self.tablaProductos_editar_inventrio.pack(side="top", fill="both", expand=True)

        self.tablaProductos_editar_inventrio.bind("<<TreeviewSelect>>", self.Rescatar_datos_editar_inventario)


        self.Talba_editar_inventario()


    def Talba_editar_inventario(self):
        self.imagenes_renderizadas.clear()

        for item in self.tablaProductos_editar_inventrio.get_children():
            self.tablaProductos_editar_inventrio.delete(item)

        datos = inventario_SQL.consultar()

        if datos:
            for fila in datos:
                ruta_img = fila[0]
                resto_datos = fila[1:]

                foto_final = self.cargar_y_redimensionar2(ruta_img)
                self.imagenes_renderizadas.append(foto_final)

                self.tablaProductos_editar_inventrio.insert(
                    "",
                    "end",
                    image=foto_final,
                    values=tuple(str(item).strip() for item in resto_datos)
                )
        # print(self.imagenes_renderizadas)

    def cargar_y_redimensionar2(self, ruta):
        try:
            ruta = ruta.strip()
            if ruta == "SIN IMAGEN" or not os.path.exists(ruta):
                img = Image.new('RGB', (90, 90), color=(200, 200, 200))
            else:
                img = Image.open(ruta)

            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        except Exception as e:
            print(f"ERROR CRÍTICO cargando imagen {ruta}: {e}")
            return ImageTk.PhotoImage(Image.new('RGB', (50, 50), color=(255, 0, 0)))

    def Rescatar_datos_editar_inventario(self, event):
        print("Llega a la tabla")
        seleccion = self.tablaProductos_editar_inventrio.selection()
        if seleccion:
            item = self.tablaProductos_editar_inventrio.item(seleccion)
            valores = item['values']
            self.clave_E_I = valores[0]
            self.cantidad_E_I = valores[1]
            self.talla_E_I = valores[2]
            self.precio_E_I = valores[4]
            self.color_E_I = valores[5]


            self.ent_clave.configure(state="normal")
            self.ent_clave.delete(0, "end")
            self.ent_clave.insert(0, self.clave_E_I)
            self.ent_clave.configure(state="disabled")

            self.ent_cantidad.delete(0, "end")
            self.ent_cantidad.insert(0, self.cantidad_E_I)


            self.ent_talla.delete(0, "end")
            self.ent_talla.insert(0, self.talla_E_I)

            self.ent_precio.delete(0, "end")
            self.ent_precio.insert(0, self.precio_E_I)
            self.ent_color.delete(0, "end")
            self.ent_color.insert(0, self.color_E_I)




    def eliminar_inventario(self):
        COLOR_ROSA = "#F8C8DC"
        COLOR_NEGRO = "#1A1A1A"
        COLOR_FONDO = "#F2F2F2"
        COLOR_BLANCO = "#FFFFFF"

        try:
            calve_a_eliminar = self.clave_a_eliminar
            talla = self.talla
            color = self.color



            print(calve_a_eliminar)
            print(talla)
            print(color)

            ventana_mini = ctk.CTkToplevel()
            ventana_mini.title("Confirmar Eliminación")

            ventana_mini.geometry("600x400")
            ventana_mini.resizable(False, False)
            ventana_mini.configure(fg_color=COLOR_FONDO)
        except Exception as e:
            print(f"error {e}")
            from tkinter import messagebox
            messagebox.showinfo("ERORR", "SELECCIONE UN CLIENTE")
            return

        # ventana_mini.grab_set()

        frame = ctk.CTkFrame(ventana_mini, fg_color=COLOR_BLANCO, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        texto = f"¿Quieres eliminar este producto?"
        label = ctk.CTkLabel(frame, text=texto, text_color=COLOR_NEGRO,
                                font=("Arial", 14, "bold"), wraplength=300)
        label.pack(pady=(30, 20))

        def eliminar_cliente():
            print(f"se eliminara: {calve_a_eliminar}")
            inventario_SQL.delate(calve_a_eliminar, talla, color)
            self.llenarTalbaProd()

        btn_aceptar = ctk.CTkButton(frame, text="ACEPTAR",
                                        fg_color=COLOR_NEGRO,
                                        text_color=COLOR_BLANCO,
                                        hover_color="#FF5733",
                                        command=lambda: [eliminar_cliente(), ventana_mini.destroy()])
        btn_aceptar.pack(pady=10)

        btn_aceptar = ctk.CTkButton(frame, text="CANSELAR",
                                        fg_color=COLOR_NEGRO,
                                        text_color=COLOR_BLANCO,
                                        hover_color="#FF5733",
                                        command=lambda: [ventana_mini.destroy()])
        btn_aceptar.pack(pady=10)

    def eliminar_inve(self, event):
        seleccion = self.tablaProductos.selection()
        if seleccion:
            item = self.tablaProductos.item(seleccion)
            valores = item['values']
            self.clave_a_eliminar = valores[0]
            self.talla = valores[2]
            self.color = valores[5]

            # print(self.clave_a_eliminar)
            # print(self.talla)
            # print(self.color)








obj = inventario()
