import customtkinter as ctk
from tkinter import messagebox, ttk
import pyodbc
from datetime import datetime, timedelta
import random
import tkinter as tk

class SistemaApartado():
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Sistema de Apartado de Productos")
        self.ventana.geometry("1400x800")
        
        self.conectar_bd()
        self.crear_interfaz()
        self.mostrar_apartados()
        
        self.ventana.mainloop()
    
    def conectar_bd(self):
        config = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LAPTOP-IGOUCGFU;"
            "DATABASE=Zapateria;"
            "Trusted_Connection=yes;"
        )
        self.conexion = pyodbc.connect(config)
    
    def crear_interfaz(self):
        self.main_frame = ctk.CTkScrollableFrame(self.ventana, fg_color="#F2F2F2")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        titulo = ctk.CTkLabel(self.main_frame, text="SISTEMA DE APARTADO DE PRODUCTOS", font=("Arial", 32, "bold"), text_color="#8DCCE3")
        titulo.pack(pady=(20, 10))
        
        subtitulo = ctk.CTkLabel(self.main_frame, text="Registro y gestión de apartados realizados por clientes", font=("Arial", 16), text_color="gray")
        subtitulo.pack(pady=(0, 20))
        
        frame_form = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#F8C8DC")
        frame_form.pack(fill="x", padx=10, pady=10)
        
        # Columna izquierda
        col1 = ctk.CTkFrame(frame_form, fg_color="transparent")
        col1.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        
        ctk.CTkLabel(col1, text="DATOS DEL CLIENTE", font=("Arial", 18, "bold"), text_color="#1A1A1A").pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(col1, text="Buscar cliente (clave o nombre):", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        
        self.combo_cliente = ctk.CTkEntry(col1, width=300, height=38, fg_color="white", border_color="#F8C8DC", text_color="black", border_width=2, placeholder_text="Escriba para buscar...")
        self.combo_cliente.pack(anchor="w", pady=(5, 10))
        self.combo_cliente.bind("<KeyRelease>", self.autocompletar_cliente)
        
        self.lista_sugerencias = tk.Listbox(col1, height=5, bg="white", fg="black", font=("Arial", 12))
        self.lista_sugerencias.pack(anchor="w", pady=(0, 10))
        self.lista_sugerencias.pack_forget()
        self.lista_sugerencias.bind("<ButtonRelease-1>", self.seleccionar_cliente_lista)
        
        ctk.CTkLabel(col1, text="Nombre del cliente:", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.caja_nombre = ctk.CTkEntry(col1, width=300, height=38, fg_color="#F0F0F0", border_color="#F8C8DC", text_color="black", border_width=2, state="readonly")
        self.caja_nombre.pack(anchor="w", pady=(5, 10))
        
        ctk.CTkLabel(col1, text="Teléfono:", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.caja_telefono = ctk.CTkEntry(col1, width=300, height=38, fg_color="#F0F0F0", border_color="#F8C8DC", text_color="black", border_width=2, state="readonly")
        self.caja_telefono.pack(anchor="w", pady=(5, 10))
        
        ctk.CTkLabel(col1, text="Fecha apartado:", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.caja_fecha = ctk.CTkEntry(col1, width=300, height=38, fg_color="white", border_color="#F8C8DC", text_color="black", border_width=2)
        self.caja_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.caja_fecha.pack(anchor="w", pady=(5, 10))
        
        # Columna derecha
        col2 = ctk.CTkFrame(frame_form, fg_color="transparent")
        col2.pack(side="right", fill="both", expand=True, padx=20, pady=15)
        
        ctk.CTkLabel(col2, text="DETALLES DEL PRODUCTO", font=("Arial", 18, "bold"), text_color="#1A1A1A").pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(col2, text="Producto:", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.combo_producto = ctk.CTkEntry(col2, width=300, height=38, fg_color="white", border_color="#F8C8DC", text_color="black", border_width=2, placeholder_text="Escriba para buscar...")
        self.combo_producto.pack(anchor="w", pady=(5, 10))
        self.combo_producto.bind("<KeyRelease>", self.autocompletar_producto)
        
        self.lista_productos_sug = tk.Listbox(col2, height=5, bg="white", fg="black", font=("Arial", 12))
        self.lista_productos_sug.pack(anchor="w", pady=(0, 10))
        self.lista_productos_sug.pack_forget()
        self.lista_productos_sug.bind("<ButtonRelease-1>", self.seleccionar_producto_lista)
        
        ctk.CTkLabel(col2, text="Talla:", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.caja_talla = ctk.CTkEntry(col2, width=200, height=38, fg_color="white", border_color="#F8C8DC", text_color="black", border_width=2)
        self.caja_talla.pack(anchor="w", pady=(5, 10))
        
        ctk.CTkLabel(col2, text="Color:", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.caja_color = ctk.CTkEntry(col2, width=200, height=38, fg_color="white", border_color="#F8C8DC", text_color="black", border_width=2)
        self.caja_color.pack(anchor="w", pady=(5, 10))
        
        ctk.CTkLabel(col2, text="Cantidad:", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.caja_cantidad = ctk.CTkEntry(col2, width=200, height=38, fg_color="white", border_color="#F8C8DC", text_color="black", border_width=2)
        self.caja_cantidad.pack(anchor="w", pady=(5, 10))
        
        ctk.CTkLabel(col2, text="Precio unitario:", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.caja_precio = ctk.CTkEntry(col2, width=200, height=38, fg_color="white", border_color="#F8C8DC", text_color="black", border_width=2)
        self.caja_precio.pack(anchor="w", pady=(5, 10))
        
        ctk.CTkLabel(col2, text="Importe pagado (20% mínimo):", font=("Arial", 13), text_color="#1A1A1A").pack(anchor="w")
        self.caja_importe = ctk.CTkEntry(col2, width=200, height=38, fg_color="white", border_color="#F8C8DC", text_color="black", border_width=2)
        self.caja_importe.pack(anchor="w", pady=(5, 10))
        
        frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_botones.pack(pady=15)
        
        ctk.CTkButton(frame_botones, text="AGREGAR APARTADO", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=200, height=40, font=("Arial", 12, "bold"), command=self.agregar_apartado).pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text="EDITAR APARTADO", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=200, height=40, font=("Arial", 12, "bold"), command=self.editar_apartado).pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text="ELIMINAR APARTADO", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=200, height=40, font=("Arial", 12, "bold"), command=self.eliminar_apartado).pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text="PAGAR APARTADO", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=200, height=40, font=("Arial", 12, "bold"), command=self.pagar_apartado).pack(side="left", padx=10)
        
        # Tabla
        frame_tabla = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#F8C8DC")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame_tabla, text="LISTADO DE APARTADOS", font=("Arial", 18, "bold"), text_color="#1A1A1A").pack(pady=10)
        
        tree_container = ctk.CTkFrame(frame_tabla, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        scroll_y = ttk.Scrollbar(tree_container)
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = ttk.Scrollbar(tree_container, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        self.tree = ttk.Treeview(tree_container, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tree.pack(fill="both", expand=True)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        columnas = ("Clave", "Cliente ID", "Cliente", "Producto", "Talla", "Color", "Cant.", "Costo Total", "Importe", "Fecha Limite", "Estado")
        self.tree["columns"] = columnas
        self.tree["show"] = "headings"
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        # Total
        frame_total = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_total.pack(fill="x", padx=10, pady=10)
        
        self.label_total = ctk.CTkLabel(frame_total, text="Total en apartados: $0.00", font=("Arial", 20, "bold"), text_color="#8DCCE3")
        self.label_total.pack(side="left")
        
        btn_salir = ctk.CTkButton(frame_total, text="SALIR", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=100, height=35, font=("Arial", 12, "bold"), command=self.ventana.destroy)
        btn_salir.pack(side="right")
        
        self.cargar_clientes()
        self.cargar_productos()
        self.cliente_seleccionado = None
        self.producto_seleccionado = None
    
    def cargar_clientes(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT clave, Nombre, telefono FROM Clientes")
        self.clientes = cursor.fetchall()
        cursor.close()
    
    def cargar_productos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT i.Clave, p.Modelo, i.Precio FROM Inventario i JOIN Productos p ON i.Clave = p.Clave")
        self.productos = cursor.fetchall()
        cursor.close()
    
    def autocompletar_cliente(self, event):
        texto = self.combo_cliente.get().lower()
        
        if texto == "":
            self.lista_sugerencias.pack_forget()
            return
        
        filtrados = []
        for c in self.clientes:
            clave_lower = c[0].lower()
            nombre_lower = c[1].lower()
            
            if texto in clave_lower:
                filtrados.append(c)
            elif texto in nombre_lower:
                filtrados.append(c)
        
        if len(filtrados) > 0:
            self.lista_sugerencias.pack(anchor="w", pady=(0, 10))
            self.lista_sugerencias.delete(0, tk.END)
            contador = 0
            for c in filtrados:
                if contador < 5:
                    self.lista_sugerencias.insert(tk.END, f"{c[0]} - {c[1]}")
                    contador = contador + 1
        else:
            self.lista_sugerencias.pack_forget()
    
    def autocompletar_producto(self, event):
        texto = self.combo_producto.get().lower()
        
        if texto == "":
            self.lista_productos_sug.pack_forget()
            return
        
        filtrados = []
        for p in self.productos:
            clave_lower = p[0].lower()
            nombre_lower = p[1].lower()
            
            if texto in clave_lower:
                filtrados.append(p)
            elif texto in nombre_lower:
                filtrados.append(p)
        
        if len(filtrados) > 0:
            self.lista_productos_sug.pack(anchor="w", pady=(0, 10))
            self.lista_productos_sug.delete(0, tk.END)
            contador = 0
            for p in filtrados:
                if contador < 5:
                    self.lista_productos_sug.insert(tk.END, f"{p[0]} - {p[1]} - ${p[2]:.2f}")
                    contador = contador + 1
        else:
            self.lista_productos_sug.pack_forget()
    
    def seleccionar_cliente_lista(self, event):
        seleccion = self.lista_sugerencias.get(tk.ACTIVE)
        
        if seleccion != "":
            clave = seleccion.split(" - ")[0]
            for c in self.clientes:
                if c[0] == clave:
                    self.combo_cliente.delete(0, tk.END)
                    self.combo_cliente.insert(0, f"{c[0]} - {c[1]}")
                    self.caja_nombre.configure(state="normal")
                    self.caja_nombre.delete(0, tk.END)
                    self.caja_nombre.insert(0, c[1])
                    self.caja_nombre.configure(state="readonly")
                    self.caja_telefono.configure(state="normal")
                    self.caja_telefono.delete(0, tk.END)
                    self.caja_telefono.insert(0, str(c[2]))
                    self.caja_telefono.configure(state="readonly")
                    self.cliente_seleccionado = clave
                    break
        
        self.lista_sugerencias.pack_forget()
    
    def seleccionar_producto_lista(self, event):
        seleccion = self.lista_productos_sug.get(tk.ACTIVE)
        
        if seleccion != "":
            clave = seleccion.split(" - ")[0]
            for p in self.productos:
                if p[0] == clave:
                    self.combo_producto.delete(0, tk.END)
                    self.combo_producto.insert(0, f"{p[0]} - {p[1]}")
                    self.caja_precio.delete(0, tk.END)
                    self.caja_precio.insert(0, str(p[2]))
                    self.producto_seleccionado = clave
                    break
        
        self.lista_productos_sug.pack_forget()
    
    def generar_clave(self):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numeros = "0123456789"
        clave = ""
        for i in range(5):
            if i < 3:
                pos = random.randint(0, 25)
                clave = clave + letras[pos]
            else:
                pos = random.randint(0, 9)
                clave = clave + numeros[pos]
        return clave
    
    def agregar_apartado(self):
        if self.cliente_seleccionado == None or self.producto_seleccionado == None:
            messagebox.showerror("Error", "Seleccione un cliente y un producto")
            return
        
        try:
            clave = self.generar_clave()
            
            # Obtener cantidad
            if self.caja_cantidad.get() == "":
                cantidad = 1
            else:
                cantidad = int(self.caja_cantidad.get())
            
            # Obtener talla
            if self.caja_talla.get() == "":
                talla = 0
            else:
                talla = int(self.caja_talla.get())
            
            # Obtener color
            if self.caja_color.get() == "":
                color = "N/A"
            else:
                color = self.caja_color.get()
            
            # Obtener precio
            if self.caja_precio.get() == "":
                precio = 0
            else:
                precio = float(self.caja_precio.get())
            
            costo_total = precio * cantidad
            
            # Obtener importe
            if self.caja_importe.get() == "":
                importe = 0
            else:
                importe = float(self.caja_importe.get())
            
            minimo = costo_total * 0.20
            if importe < minimo:
                messagebox.showerror("Error", f"El importe mínimo es 20% (${minimo:.2f})")
                return
            
            cursor = self.conexion.cursor()
            cursor.execute("SELECT TOP 1 ClaveAcceso FROM Personal")
            responsable_row = cursor.fetchone()
            
            if responsable_row == None:
                messagebox.showerror("Error", "No hay personal registrado")
                cursor.close()
                return
            
            responsable = responsable_row[0]
            
            fecha_inicial = datetime.now().strftime("%d/%m/%Y")
            fecha_limite = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
            
            cursor.execute("""INSERT INTO Apartado 
                (ClaveDeApartado, Responsable, Beneficiario, ClaveProducto, Cantidad, Talla, Color, FechaInicial, FechaLimite, CostoTotal, Importe) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (clave, responsable, self.cliente_seleccionado, self.producto_seleccionado, cantidad, talla, color,
                 fecha_inicial, fecha_limite, costo_total, importe))
            self.conexion.commit()
            cursor.close()
            
            messagebox.showinfo("Éxito", f"Apartado {clave} registrado")
            self.limpiar_campos()
            self.mostrar_apartados()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def mostrar_apartados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        cursor = self.conexion.cursor()
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        cursor.execute("""
            SELECT a.ClaveDeApartado, a.Beneficiario, c.Nombre, a.ClaveProducto, a.Talla, a.Color, a.Cantidad, a.CostoTotal, a.Importe, a.FechaLimite,
                   CASE WHEN a.FechaLimite < ? THEN 'Vencido' ELSE 'Activo' END as Estado
            FROM Apartado a
            JOIN Clientes c ON a.Beneficiario = c.clave
        """, (fecha_actual,))
        apartados = cursor.fetchall()
        
        total = 0
        total_pendiente = 0
        
        for apt in apartados:
            if apt[10] == "Vencido":
                estado = "Vencido"
            else:
                estado = "Activo"
            
            self.tree.insert("", "end", values=(
                apt[0], apt[1], apt[2], apt[3], apt[4], apt[5], apt[6], f"${apt[7]:.2f}", f"${apt[8]:.2f}", apt[9], estado
            ))
            
            if apt[7] != None:
                total = total + apt[7]
            
            if estado == "Activo":
                if apt[7] != None and apt[8] != None:
                    resto = apt[7] - apt[8]
                    total_pendiente = total_pendiente + resto
        
        self.label_total.configure(text=f"Total apartados: ${total:.2f} | Pendiente: ${total_pendiente:.2f}")
        cursor.close()
    
    def pagar_apartado(self):
        seleccion = self.tree.selection()
        
        if len(seleccion) == 0:
            messagebox.showwarning("Advertencia", "Seleccione un apartado para pagar")
            return
        
        item = self.tree.item(seleccion)
        valores = item['values']
        clave_apartado = valores[0]
        
        costo_total_str = valores[7].replace('$', '')
        importe_pagado_str = valores[8].replace('$', '')
        costo_total = float(costo_total_str)
        importe_pagado = float(importe_pagado_str)
        resto = costo_total - importe_pagado
        
        if resto <= 0:
            messagebox.showinfo("Info", "Este apartado ya está pagado")
            return
        
        respuesta = messagebox.askyesno("Pagar", f"Saldo pendiente: ${resto:.2f}\n¿Desea realizar el pago?")
        
        if respuesta == True:
            nuevo_importe = costo_total
            cursor = self.conexion.cursor()
            cursor.execute("UPDATE Apartado SET Importe = ? WHERE ClaveDeApartado = ?", (nuevo_importe, clave_apartado))
            self.conexion.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Pago realizado correctamente")
            self.mostrar_apartados()
    
    def eliminar_apartado(self):
        seleccion = self.tree.selection()
        
        if len(seleccion) == 0:
            messagebox.showwarning("Advertencia", "Seleccione un apartado para eliminar")
            return
        
        respuesta = messagebox.askyesno("Eliminar", "¿Eliminar este apartado?")
        
        if respuesta == True:
            item = self.tree.item(seleccion)
            clave_apartado = item['values'][0]
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM Apartado WHERE ClaveDeApartado = ?", (clave_apartado,))
            self.conexion.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Apartado eliminado")
            self.mostrar_apartados()
    
    def editar_apartado(self):
        messagebox.showinfo("Info", "Seleccione el apartado y luego modifique los campos")
    
    def limpiar_campos(self):
        self.combo_cliente.delete(0, tk.END)
        self.caja_nombre.configure(state="normal")
        self.caja_nombre.delete(0, tk.END)
        self.caja_nombre.configure(state="readonly")
        self.caja_telefono.configure(state="normal")
        self.caja_telefono.delete(0, tk.END)
        self.caja_telefono.configure(state="readonly")
        self.combo_producto.delete(0, tk.END)
        self.caja_talla.delete(0, tk.END)
        self.caja_color.delete(0, tk.END)
        self.caja_cantidad.delete(0, tk.END)
        self.caja_precio.delete(0, tk.END)
        self.caja_importe.delete(0, tk.END)
        self.caja_fecha.delete(0, tk.END)
        self.caja_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.cliente_seleccionado = None
        self.producto_seleccionado = None
        self.lista_sugerencias.pack_forget()
        self.lista_productos_sug.pack_forget()

SistemaApartado()