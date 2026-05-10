import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import pyodbc
from decimal import Decimal,ROUND_HALF_UP
from datetime import datetime
import os
class ModuloVentas():
    def Iniciar(self,Frame,Responsable):

        self.Frame_principal=Frame
        self.Responsable=Responsable
        self.COLOR_PRIMARIO="#F8C8DC"
        self.COLOR_SECUNDARIO="#1A1A1A"
        self.COLOR_TERCIARIO="#F2F2F2"
        self.COLOR_TEXTO_NEGRO="#1A1A1A"
        self.COLOR_COMPLEMENTARIO="#8DCCE3"

        
        self.btn_realizar_venta=ctk.CTkButton(
            self.Frame_principal, text="Realizar Venta", 
            fg_color=self.COLOR_PRIMARIO, text_color=self.COLOR_TEXTO_NEGRO,
            hover_color="#F4A7C5", width=140, height=30,
            command=self.mostrar_lista_productos
        )
        self.btn_realizar_venta.place(relx=1/3, rely=0.05, anchor=ctk.CENTER)
        
        self.btn_consultar_ventas=ctk.CTkButton(
            self.Frame_principal, text="Consultar Ventas", 
            fg_color=self.COLOR_TEXTO_NEGRO, border_width=1, border_color=self.COLOR_COMPLEMENTARIO,
            text_color=self.COLOR_COMPLEMENTARIO, hover_color="#333333", width=140, height=30,
            command=self.mostrar_interfaz_historial
        )
        self.btn_consultar_ventas.place(relx=2/3, rely=0.05, anchor=ctk.CENTER)

        self.main_container=ctk.CTkFrame(self.Frame_principal, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.54, relwidth=0.95, relheight=0.85, anchor=ctk.CENTER)
        self.carrito={}
        self.mostrar_lista_productos()

    def limpiar_contenedor(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
    def actualizar_diccionario(self):
        self.Productos={} 
        conexion=self.conectar_db()
        cursor=conexion.cursor()
        cursor.execute("""
            SELECT Productos.Clave, Modelo, Talla, Precio, RutaImagen
            FROM Productos,Inventario
            WHERE Productos.Clave=Inventario.Clave
        """)
        for fila in cursor:
            self.Productos[fila.Clave]={
                "Modelo": fila.Modelo,
                "Talla": fila.Talla,
                "Precio":fila.Precio,
                "imagen":fila.RutaImagen
                }
        cursor.close()
        conexion.close()
        print(self.Productos)

    def mostrar_lista_productos(self):
        self.limpiar_contenedor()
        self.actualizar_diccionario()
        self.grid_productos=ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.grid_productos.place(relx=0.32, rely=0.5, relwidth=0.62, relheight=1.0, anchor=ctk.CENTER)
        
        self.entry_busqueda=ctk.CTkEntry(
            self.grid_productos, placeholder_text="Buscar por modelo, talla o color...",
            width=400, height=35, border_color=self.COLOR_PRIMARIO
        )
        self.entry_busqueda.place(relx=0.5, rely=0.08, anchor=ctk.CENTER)
        self.scroll_productos=ctk.CTkScrollableFrame(self.grid_productos, fg_color="transparent")
        self.scroll_productos.place(relx=0.5, rely=0.55, relwidth=0.95, relheight=0.8, anchor=ctk.CENTER)

        for i, (producto, datos) in enumerate(self.Productos.items()):
            self.crear_tarjeta_producto(producto,datos["Modelo"], datos["Talla"], datos["Precio"], datos["imagen"], i)
       

    def CargarImagen(self,ruta):
        ruta_imagen=os.path.join(os.path.dirname(__file__),ruta)

        try:
            img_pil=Image.open(ruta_imagen)
            img_ctk=ctk.CTkImage(light_image=img_pil, 
                                dark_image=img_pil, 
                                size=(100, 100))
            return img_ctk
        except Exception as e:
            print("error")

    def crear_tarjeta_producto(self, clave, modelo, talla, precio, ruta, indice):
        card=ctk.CTkFrame(self.scroll_productos, fg_color=self.COLOR_TERCIARIO, width=180, height=220)
        fila=indice // 3
        print("fila",fila)
        columna=indice % 3
        print("Columna",columna)
        
        card.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")
        
        img=self.CargarImagen(ruta)
        lbl_img=ctk.CTkLabel(card,text="", image=img, width=140, height=100, fg_color="#D1D1D1")
        lbl_img.image=img
        lbl_img.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)
        
        ctk.CTkLabel(card, text=modelo, font=("Arial", 14, "bold"), text_color=self.COLOR_SECUNDARIO).place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        ctk.CTkLabel(card, text=f"Talla: {talla}", text_color="gray").place(relx=0.5, rely=0.72, anchor=ctk.CENTER)
        ctk.CTkLabel(card, text=precio, font=("Arial", 13), text_color=self.COLOR_SECUNDARIO).place(relx=0.5, rely=0.82, anchor=ctk.CENTER)
        
        btn_seleccionar=ctk.CTkButton(
            card, text="Seleccionar", fg_color=self.COLOR_SECUNDARIO, 
            height=25, width=120, command= lambda c=clave: self.Agregar_a_carrito(c)
        )
        btn_seleccionar.place(relx=0.5, rely=0.92, anchor=ctk.CENTER)
        
    def Agregar_a_carrito(self,producto):
        if producto not in self.carrito:
            print("simon")
            self.carrito[producto]={"Modelo":self.Productos[producto]["Modelo"],
                                    "Talla": self.Productos[producto]["Talla"],
                                    "Precio":self.Productos[producto]["Precio"]}
            print(self.carrito)
        else:
            print("nel")
        self.abrir_detalle_carrito()

    def Vaciar_carrito(self):
        self.carrito={}
        self.mostrar_lista_productos()

    def Eliminar_prod_carrito(self,producto):
        del self.carrito[producto]
        if len(self.carrito)<1:
            self.mostrar_lista_productos()
        else:
            self.abrir_detalle_carrito()
        
    def Calcular_total(self,sub):
        self.IVA=Decimal("0.16")
        sub_decimal=Decimal(str(sub))
        iva = sub_decimal * self.IVA
        total = sub_decimal + iva
        
        # 4. Redondear a 2 decimales exactos
        centavos = Decimal("0.01")
        iva_final = iva.quantize(centavos, rounding=ROUND_HALF_UP)
        total_final = total.quantize(centavos, rounding=ROUND_HALF_UP)
        return iva_final,total_final
    
    def abrir_detalle_carrito(self):
        if hasattr(self, 'frame_carrito'): self.frame_carrito.destroy()
        subtotal=0
        total=0
        self.frame_carrito=ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.frame_carrito.place(relx=0.82, rely=0.5, relwidth=0.33, relheight=1.0, anchor=ctk.CENTER)
        
        ctk.CTkLabel(self.frame_carrito, text="Resumen de Venta", font=("Arial", 18, "bold"),
                     text_color=self.COLOR_TEXTO_NEGRO
                     ).place(relx=0.5, rely=0.05, anchor=ctk.CENTER)
        
        self.lista_carrito=ctk.CTkScrollableFrame(self.frame_carrito, fg_color="transparent")
        self.lista_carrito.place(relx=0.5, rely=0.35,relheight=.5, relwidth=.9, anchor=ctk.CENTER)

        for producto,datos in self.carrito.items():
            fila = ctk.CTkFrame(self.lista_carrito, fg_color="transparent")
            fila.pack(fill="x", pady=5, padx=10)

            item=ctk.CTkLabel(fila,
                              text=f"{datos["Modelo"]}...${datos["Precio"]}",
                              anchor="w",
                              text_color=self.COLOR_TEXTO_NEGRO)
            item.pack(side="left", padx=10, expand=True, fill="x")

            ctk.CTkButton(fila, text="🗑", width=10,fg_color="#FF4848", command=lambda p=producto: self.Eliminar_prod_carrito(p)
                           ).pack(side="right", padx=10)
            
            subtotal+=datos["Precio"]

        self.lbl_subtotal=ctk.CTkLabel(self.frame_carrito, text=f"Subtotal: {subtotal}",text_color=self.COLOR_TEXTO_NEGRO)
        self.lbl_subtotal.place(relx=0.8, rely=0.65, anchor="e")
        
        iva,total=self.Calcular_total(subtotal)

        self.lbl_iva=ctk.CTkLabel(self.frame_carrito, text=f"IVA({self.IVA}): {iva}",text_color=self.COLOR_TEXTO_NEGRO)
        self.lbl_iva.place(relx=0.8, rely=0.7, anchor="e")
        
        self.lbl_total=ctk.CTkLabel(self.frame_carrito, text=f"Total: {total}", font=("Arial", 16, "bold"), text_color=self.COLOR_SECUNDARIO)
        self.lbl_total.place(relx=0.8, rely=0.76, anchor="e")
        
        btn_pagar=ctk.CTkButton(self.frame_carrito, text="Realizar Venta", fg_color="#4CAF50", text_color="white", height=30,
                                command= lambda: self.popup_pago(total))
        btn_pagar.place(relx=0.5, rely=0.88, relwidth=0.8, anchor=ctk.CENTER)
        
        btn_cancelar=ctk.CTkButton(self.frame_carrito, text="Cancelar", fg_color="#E74C3C", text_color="white", height=30,
                                   command=self.Vaciar_carrito)
        btn_cancelar.place(relx=0.5, rely=0.95, relwidth=0.8, anchor=ctk.CENTER)

    def popup_pago(self,total):
        pago_win=ctk.CTkToplevel(self.Frame_principal)
        pago_win.title("Metodo de Pago")
        pago_win.geometry("400x450")
        pago_win.after(100, lambda: pago_win.focus())
        
        ctk.CTkLabel(pago_win, text="Seleccione Forma de Pago", font=("Arial", 16)).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        tabview=ctk.CTkTabview(pago_win, segmented_button_selected_color=self.COLOR_PRIMARIO, segmented_button_selected_hover_color="#F4A7C5")
        tabview.place(relx=0.5, rely=0.55, relwidth=0.9, relheight=0.8, anchor=ctk.CENTER)
        
        tabview.add("Efectivo")
        tabview.add("Tarjeta")
        
        lbl_total=ctk.CTkLabel(tabview.tab("Efectivo"), text=f"Total a pagar: ${total}", font=("Arial", 20, "bold"))
        lbl_total.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        
        entry_pago=ctk.CTkEntry(tabview.tab("Efectivo"), placeholder_text="Monto recibido MXN", width=200)
        entry_pago.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        btn_finalizar=ctk.CTkButton(tabview.tab("Efectivo"), text="Confirmar y Generar Ticket", fg_color=self.COLOR_SECUNDARIO, width=250,
                                      command=lambda:self.Pago_efectivo(total) )
        btn_finalizar.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

        lbl_total=ctk.CTkLabel(tabview.tab("Tarjeta"), text=f"Total a pagar: ${total}", font=("Arial", 20, "bold"))
        lbl_total.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        
        entry_pago=ctk.CTkEntry(tabview.tab("Tarjeta"), width=200)
        entry_pago.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)
        
        btn_finalizar=ctk.CTkButton(tabview.tab("Tarjeta"), text="Confirmar y Generar Ticket", fg_color=self.COLOR_SECUNDARIO, width=250,
                                      command=lambda:self.Pago_tarjeta(total) )
        btn_finalizar.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)
    
    def Pago_tarjeta(self,total):
        pass
    def Pago_efectivo(self,total):
        messagebox.showinfo("Venta Exitosa", "Ticket generado en PDF y registro guardado.")

    def mostrar_interfaz_historial(self):
        self.limpiar_contenedor()
        ctk.CTkLabel(self.main_container, text="Historial de Ventas", font=("Arial", 24, "bold"), text_color=self.COLOR_SECUNDARIO).place(relx=0.5, rely=0.05, anchor=ctk.CENTER)
        
        filtro_frame=ctk.CTkFrame(self.main_container, fg_color="white", height=60)
        filtro_frame.place(relx=0.5, rely=0.15, relwidth=0.95, anchor=ctk.CENTER)
        
        ctk.CTkOptionMenu(filtro_frame, values=["2024", "2023"], fg_color=self.COLOR_SECUNDARIO, button_color=self.COLOR_SECUNDARIO).place(relx=0.2, rely=0.5, anchor=ctk.CENTER)
        ctk.CTkOptionMenu(filtro_frame, values=["Enero", "Febrero", "Marzo"], fg_color=self.COLOR_SECUNDARIO, button_color=self.COLOR_SECUNDARIO).place(relx=0.4, rely=0.5, anchor=ctk.CENTER)
        
        self.scroll_historial=ctk.CTkScrollableFrame(self.main_container, fg_color="white")
        self.scroll_historial.place(relx=0.5, rely=0.6, relwidth=0.95, relheight=0.7, anchor=ctk.CENTER)
        
        ctk.CTkButton(self.scroll_historial, text="Venta #001 - 03/03/2024 - $1,200.00 - Empleado: Juan", 
                      fg_color="transparent", text_color="black", anchor="w", border_width=1).pack(fill="x", pady=2)
    
    def conectar_db(self):
        conexion=(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=Zapateria;"
        "Trusted_Connection=yes;")
        try:
            conexion=pyodbc.connect(conexion)
            print("Conexión exitosa")
            return conexion
        except Exception as e:
            print(f"Error al conectar: {e}")
            return None

