import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


class ModuloVentas():
    def Iniciar(self,Frame):

        self.Frame_principal=Frame

        self.COLOR_PRIMARIO = "#F8C8DC"
        self.COLOR_SECUNDARIO = "#1A1A1A"
        self.COLOR_TERCIARIO = "#F2F2F2"
        self.COLOR_TEXTO_NEGRO = "#1A1A1A"
        self.COLOR_COMPLEMENTARIO = "#8DCCE3"

        
        self.btn_realizar_venta = ctk.CTkButton(
            self.Frame_principal, text="Realizar Venta", 
            fg_color=self.COLOR_PRIMARIO, text_color=self.COLOR_TEXTO_NEGRO,
            hover_color="#F4A7C5", width=140, height=30,
            command=self.mostrar_interfaz_venta
        )
        self.btn_realizar_venta.place(relx=1/3, rely=0.05, anchor=ctk.CENTER)
        
        self.btn_consultar_ventas = ctk.CTkButton(
            self.Frame_principal, text="Consultar Ventas", 
            fg_color=self.COLOR_TEXTO_NEGRO, border_width=1, border_color=self.COLOR_COMPLEMENTARIO,
            text_color=self.COLOR_COMPLEMENTARIO, hover_color="#333333", width=140, height=30,
            command=self.mostrar_interfaz_historial
        )
        self.btn_consultar_ventas.place(relx=2/3, rely=0.05, anchor=ctk.CENTER)

        self.main_container = ctk.CTkFrame(self.Frame_principal, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.54, relwidth=0.95, relheight=0.85, anchor=ctk.CENTER)

        self.mostrar_interfaz_venta()

    def limpiar_contenedor(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def mostrar_interfaz_venta(self):
        self.limpiar_contenedor()
        
        self.grid_productos = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.grid_productos.place(relx=0.32, rely=0.5, relwidth=0.62, relheight=1.0, anchor=ctk.CENTER)
        
        self.entry_busqueda = ctk.CTkEntry(
            self.grid_productos, placeholder_text="Buscar por modelo, talla o color...",
            width=400, height=35, border_color=self.COLOR_PRIMARIO
        )
        self.entry_busqueda.place(relx=0.5, rely=0.08, anchor=ctk.CENTER)

        self.scroll_productos = ctk.CTkScrollableFrame(self.grid_productos, fg_color="transparent")
        self.scroll_productos.place(relx=0.5, rely=0.55, relwidth=0.95, relheight=0.8, anchor=ctk.CENTER)

        self.crear_tarjeta_producto("Modelo XYZ", "25 MX", "$850.00")
        self.crear_tarjeta_producto("Bota Elegance", "24 MX", "$1,200.00")

    def crear_tarjeta_producto(self, modelo, talla, precio):
        card = ctk.CTkFrame(self.scroll_productos, fg_color=self.COLOR_TERCIARIO, width=180, height=220)
        card.pack(side="left", padx=10, pady=10) # pack se usa solo para el flujo interno del scrollable
        
        lbl_img = ctk.CTkLabel(card, text="[ Imagen ]", width=140, height=100, fg_color="#D1D1D1")
        lbl_img.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)
        
        ctk.CTkLabel(card, text=modelo, font=("Arial", 14, "bold"), text_color=self.COLOR_SECUNDARIO).place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        ctk.CTkLabel(card, text=f"Talla: {talla}", text_color="gray").place(relx=0.5, rely=0.72, anchor=ctk.CENTER)
        ctk.CTkLabel(card, text=precio, font=("Arial", 13), text_color=self.COLOR_SECUNDARIO).place(relx=0.5, rely=0.82, anchor=ctk.CENTER)
        
        btn_seleccionar = ctk.CTkButton(
            card, text="Seleccionar", fg_color=self.COLOR_SECUNDARIO, 
            height=25, width=120, command=self.abrir_detalle_carrito
        )
        btn_seleccionar.place(relx=0.5, rely=0.92, anchor=ctk.CENTER)

    def abrir_detalle_carrito(self):
        if hasattr(self, 'frame_carrito'): self.frame_carrito.destroy()
        
        self.frame_carrito = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.frame_carrito.place(relx=0.82, rely=0.5, relwidth=0.33, relheight=1.0, anchor=ctk.CENTER)
        
        ctk.CTkLabel(self.frame_carrito, text="Resumen de Venta", font=("Arial", 18, "bold")
                     ).place(relx=0.5, rely=0.08, anchor=ctk.CENTER)
        
        self.lista_carrito = ctk.CTkScrollableFrame(self.frame_carrito, fg_color="transparent", height=200, width=200)
        self.lista_carrito.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
        
        item = ctk.CTkLabel(self.lista_carrito, text="1x Modelo XYZ ......... $850.00", anchor="w",text_color=self.COLOR_TEXTO_NEGRO)
        item.pack(fill="x", pady=5)

        self.lbl_subtotal = ctk.CTkLabel(self.frame_carrito, text="Subtotal: $732.75",text_color=self.COLOR_TEXTO_NEGRO)
        self.lbl_subtotal.place(relx=0.8, rely=0.65, anchor="e")
        
        self.lbl_iva = ctk.CTkLabel(self.frame_carrito, text="IVA (16%): $117.25",text_color=self.COLOR_TEXTO_NEGRO)
        self.lbl_iva.place(relx=0.8, rely=0.7, anchor="e")
        
        self.lbl_total = ctk.CTkLabel(self.frame_carrito, text="Total: $850.00", font=("Arial", 16, "bold"), text_color=self.COLOR_SECUNDARIO)
        self.lbl_total.place(relx=0.8, rely=0.76, anchor="e")
        
        btn_pagar = ctk.CTkButton(self.frame_carrito, text="Realizar Venta", fg_color="#4CAF50", text_color="white", height=40, command=self.popup_pago)
        btn_pagar.place(relx=0.5, rely=0.88, relwidth=0.8, anchor=ctk.CENTER)
        
        btn_cancelar = ctk.CTkButton(self.frame_carrito, text="Cancelar", fg_color="#E74C3C", text_color="white", height=30, command=self.mostrar_interfaz_venta)
        btn_cancelar.place(relx=0.5, rely=0.95, relwidth=0.8, anchor=ctk.CENTER)

    def popup_pago(self):
        pago_win = ctk.CTkToplevel(self.Frame_principal)
        pago_win.title("Metodo de Pago")
        pago_win.geometry("400x450")
        pago_win.after(100, lambda: pago_win.focus())
        
        ctk.CTkLabel(pago_win, text="Seleccione Forma de Pago", font=("Arial", 16)).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        tabview = ctk.CTkTabview(pago_win, segmented_button_selected_color=self.COLOR_PRIMARIO, segmented_button_selected_hover_color="#F4A7C5")
        tabview.place(relx=0.5, rely=0.55, relwidth=0.9, relheight=0.8, anchor=ctk.CENTER)
        
        tabview.add("Efectivo")
        tabview.add("Tarjeta")
        
        lbl_total = ctk.CTkLabel(tabview.tab("Efectivo"), text="Total a pagar: $850.00", font=("Arial", 20, "bold"))
        lbl_total.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        
        entry_pago = ctk.CTkEntry(tabview.tab("Efectivo"), placeholder_text="Monto recibido MXN", width=200)
        entry_pago.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)
        
        btn_finalizar = ctk.CTkButton(tabview.tab("Efectivo"), text="Confirmar y Generar Ticket", fg_color=self.COLOR_SECUNDARIO, width=250,
                                      command=lambda: messagebox.showinfo("Venta Exitosa", "Ticket generado en PDF y registro guardado."))
        btn_finalizar.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

    def mostrar_interfaz_historial(self):
        self.limpiar_contenedor()
        ctk.CTkLabel(self.main_container, text="Historial de Ventas", font=("Arial", 24, "bold"), text_color=self.COLOR_SECUNDARIO).place(relx=0.5, rely=0.05, anchor=ctk.CENTER)
        
        filtro_frame = ctk.CTkFrame(self.main_container, fg_color="white", height=60)
        filtro_frame.place(relx=0.5, rely=0.15, relwidth=0.95, anchor=ctk.CENTER)
        
        ctk.CTkOptionMenu(filtro_frame, values=["2024", "2023"], fg_color=self.COLOR_SECUNDARIO, button_color=self.COLOR_SECUNDARIO).place(relx=0.2, rely=0.5, anchor=ctk.CENTER)
        ctk.CTkOptionMenu(filtro_frame, values=["Enero", "Febrero", "Marzo"], fg_color=self.COLOR_SECUNDARIO, button_color=self.COLOR_SECUNDARIO).place(relx=0.4, rely=0.5, anchor=ctk.CENTER)
        
        self.scroll_historial = ctk.CTkScrollableFrame(self.main_container, fg_color="white")
        self.scroll_historial.place(relx=0.5, rely=0.6, relwidth=0.95, relheight=0.7, anchor=ctk.CENTER)
        
        ctk.CTkButton(self.scroll_historial, text="Venta #001 - 03/03/2024 - $1,200.00 - Empleado: Juan", 
                      fg_color="transparent", text_color="black", anchor="w", border_width=1).pack(fill="x", pady=2)

