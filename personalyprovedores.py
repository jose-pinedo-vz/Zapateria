import customtkinter as ctk
from tkinter import messagebox
import random
import tkinter as tk
import pyodbc

class Proveedor():
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Personal Y Proveedores")
        self.ventana.state("zoomed")
        self.ventana.resizable(False, False)
        self.ventana.configure(fg_color="#1A1A1A")

        # Conectar a base de datos
        self.conectar_bd()

        self.menu_principal()

        self.ventana.mainloop()

    def conectar_bd(self):
        config = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LAPTOP-IGOUCGFU;"
            "DATABASE=Zapateria;"
            "Trusted_Connection=yes;"
        )
        self.conexion = pyodbc.connect(config)
        print("Conectado a la base de datos")

    def menu_principal(self):
        # Limpiar ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        titulo = ctk.CTkLabel(self.ventana, text="SISTEMA DE GESTIÓN", font=("Arial", 40, "bold"), text_color="#8DCCE3")
        titulo.pack(pady=(150, 30))

        btn_proveedores = ctk.CTkButton(self.ventana, text="PROVEEDORES", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=250, height=60, corner_radius=15, font=("Arial", 18, "bold"), command=self.proveedor_interfaz)
        btn_proveedores.pack(pady=15)

        btn_personal = ctk.CTkButton(self.ventana, text="PERSONAL", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=250, height=60, corner_radius=15, font=("Arial", 18, "bold"), command=self.personal_interfaz)
        btn_personal.pack(pady=15)

    def proveedor_interfaz(self):
        self.ventanapro = ctk.CTkToplevel()
        self.ventanapro.title("Proveedores")
        self.ventanapro.configure(fg_color="#1A1A1A")
        self.ventanapro.geometry("1500x900")

        # Botón volver al menú
        volver = ctk.CTkButton(self.ventanapro, text="← Volver", fg_color="#8DCCE3", hover_color="#F8C8DC", font=("Arial", 18), corner_radius=15, width=100, height=40, command=self.volver_menu_proveedor)
        volver.pack(pady=(20, 10), anchor="w", padx=20)

        marco_principal = ctk.CTkFrame(self.ventanapro, fg_color="transparent")
        marco_principal.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = ctk.CTkLabel(marco_principal, text="Registro de Proveedores", font=("Arial", 26, "bold"), text_color="#8DCCE3")
        titulo.pack(pady=(10, 20))

        marco_registro = ctk.CTkFrame(marco_principal, border_width=2, border_color="#F8C8DC", corner_radius=15, fg_color="white")
        marco_registro.pack(fill="x", padx=20, pady=10)

        # Labels
        frame_labels = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_labels.pack(pady=(15, 5))

        ctk.CTkLabel(frame_labels, text="Empresa:", font=("Arial", 14), text_color="#1A1A1A").pack(side="left", padx=40)
        ctk.CTkLabel(frame_labels, text="Teléfono:", font=("Arial", 14), text_color="#1A1A1A").pack(side="left", padx=40)
        ctk.CTkLabel(frame_labels, text="Dirección:", font=("Arial", 14), text_color="#1A1A1A").pack(side="left", padx=40)
        ctk.CTkLabel(frame_labels, text="Contacto:", font=("Arial", 14), text_color="#1A1A1A").pack(side="left", padx=40)

        # Campos de texto
        frame_campos = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_campos.pack(pady=(5, 15))

        self.caempresa = ctk.CTkEntry(frame_campos, width=180, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caempresa.pack(side="left", padx=30)

        self.catelefono = ctk.CTkEntry(frame_campos, width=180, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.catelefono.pack(side="left", padx=30)

        self.cadireccion = ctk.CTkEntry(frame_campos, width=180, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.cadireccion.pack(side="left", padx=30)

        self.cacontacto = ctk.CTkEntry(frame_campos, width=180, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.cacontacto.pack(side="left", padx=30)

        # Botones
        frame_botones = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_botones.pack(pady=(5, 20))

        boton_agregar = ctk.CTkButton(frame_botones, text="+ Agregar proveedor", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=180, height=40, corner_radius=10, command=self.agregar_proveedor)
        boton_agregar.pack(side="left", padx=15)

        boton_eliminar = ctk.CTkButton(frame_botones, text="- Eliminar proveedor", fg_color="#dc3545", hover_color="#c82333", text_color="white", width=180, height=40, corner_radius=10, command=self.eliminar_proveedor)
        boton_eliminar.pack(side="left", padx=15)

        boton_limpiar = ctk.CTkButton(frame_botones, text="Limpiar campos", fg_color="#6c757d", hover_color="#5a6268", text_color="white", width=180, height=40, corner_radius=10, command=self.limpiar_campos_proveedor)
        boton_limpiar.pack(side="left", padx=15)

        # Tabla
        marco_tabla = ctk.CTkFrame(marco_principal, border_width=2, border_color="#F8C8DC", corner_radius=15, fg_color="white")
        marco_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        frame_encabezados = ctk.CTkFrame(marco_tabla, fg_color="#8DCCE3", corner_radius=10)
        frame_encabezados.pack(pady=(10, 5))

        ctk.CTkLabel(frame_encabezados, text="Empresa", width=200, text_color="white", font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=8)
        ctk.CTkLabel(frame_encabezados, text="Teléfono", width=150, text_color="white", font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=8)
        ctk.CTkLabel(frame_encabezados, text="Dirección", width=200, text_color="white", font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=8)
        ctk.CTkLabel(frame_encabezados, text="Contacto", width=200, text_color="white", font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=8)

        self.frame_datos_proveedores = ctk.CTkFrame(marco_tabla, fg_color="transparent")
        self.frame_datos_proveedores.pack(pady=5)

        # Cargar proveedores desde la base de datos
        self.mostrar_proveedores()

        # Botón salir
        btn_salir = ctk.CTkButton(self.ventanapro, text="Salir", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", corner_radius=20, width=120, height=40, command=self.ventanapro.destroy)
        btn_salir.pack(pady=20)

    def personal_interfaz(self):
        self.ventanapersonal = ctk.CTkToplevel()
        self.ventanapersonal.title("Personal")
        self.ventanapersonal.configure(fg_color="#1A1A1A")
        self.ventanapersonal.geometry("1600x900")

        volver = ctk.CTkButton(self.ventanapersonal, text="← Volver", fg_color="#8DCCE3", hover_color="#F8C8DC", font=("Arial", 18), corner_radius=15, width=100, height=40, command=self.volver_menu_personal)
        volver.pack(pady=(20, 10), anchor="w", padx=20)

        marco_principal = ctk.CTkFrame(self.ventanapersonal, fg_color="transparent")
        marco_principal.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = ctk.CTkLabel(marco_principal, text="Registro de Personal", font=("Arial", 26, "bold"), text_color="#8DCCE3")
        titulo.pack(pady=(10, 20))

        marco_registro = ctk.CTkFrame(marco_principal, border_width=2, border_color="#F8C8DC", corner_radius=15, fg_color="white")
        marco_registro.pack(fill="x", padx=20, pady=10)

        # Labels
        frame_labels = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_labels.pack(pady=(15, 5))

        ctk.CTkLabel(frame_labels, text="Clave:", font=("Arial", 13), text_color="#1A1A1A").pack(side="left", padx=15)
        ctk.CTkLabel(frame_labels, text="Nombre:", font=("Arial", 13), text_color="#1A1A1A").pack(side="left", padx=15)
        ctk.CTkLabel(frame_labels, text="Apellido P:", font=("Arial", 13), text_color="#1A1A1A").pack(side="left", padx=15)
        ctk.CTkLabel(frame_labels, text="Sueldo:", font=("Arial", 13), text_color="#1A1A1A").pack(side="left", padx=15)

        # Campos
        frame_campos = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_campos.pack(pady=(5, 15))

        self.caja_clave = ctk.CTkEntry(frame_campos, width=100, height=35, fg_color="#F0F0F0", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10, state="readonly")
        self.caja_clave.pack(side="left", padx=10)

        self.caja_nombre = ctk.CTkEntry(frame_campos, width=120, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caja_nombre.pack(side="left", padx=10)

        self.caja_apellido = ctk.CTkEntry(frame_campos, width=120, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caja_apellido.pack(side="left", padx=10)

        self.caja_sueldo = ctk.CTkEntry(frame_campos, width=120, height=35, fg_color="white", border_color="#F8C8DC", text_color="#1A1A1A", border_width=2, corner_radius=10)
        self.caja_sueldo.pack(side="left", padx=10)

        # Botón generar clave
        btn_generar_clave = ctk.CTkButton(marco_registro, text="Generar clave", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=120, height=30, corner_radius=10, command=self.generar_clave_personal)
        btn_generar_clave.pack(pady=(5, 10))

        # Botones de acción
        frame_botones = ctk.CTkFrame(marco_registro, fg_color="transparent")
        frame_botones.pack(pady=(5, 20))

        boton_agregar = ctk.CTkButton(frame_botones, text="+ Agregar personal", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", width=180, height=40, corner_radius=10, command=self.agregar_personal)
        boton_agregar.pack(side="left", padx=15)

        boton_eliminar = ctk.CTkButton(frame_botones, text="- Eliminar personal", fg_color="#dc3545", hover_color="#c82333", text_color="white", width=180, height=40, corner_radius=10, command=self.eliminar_personal)
        boton_eliminar.pack(side="left", padx=15)

        boton_limpiar = ctk.CTkButton(frame_botones, text="Limpiar campos", fg_color="#6c757d", hover_color="#5a6268", text_color="white", width=180, height=40, corner_radius=10, command=self.limpiar_campos_personal)
        boton_limpiar.pack(side="left", padx=15)

        # Tabla
        marco_tabla = ctk.CTkFrame(marco_principal, border_width=2, border_color="#F8C8DC", corner_radius=15, fg_color="white")
        marco_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        frame_encabezados = ctk.CTkFrame(marco_tabla, fg_color="#8DCCE3", corner_radius=10)
        frame_encabezados.pack(pady=(10, 5))

        ctk.CTkLabel(frame_encabezados, text="Clave", width=100, text_color="white", font=("Arial", 12, "bold")).pack(side="left", padx=8, pady=6)
        ctk.CTkLabel(frame_encabezados, text="Nombre", width=120, text_color="white", font=("Arial", 12, "bold")).pack(side="left", padx=8, pady=6)
        ctk.CTkLabel(frame_encabezados, text="Apellido P", width=120, text_color="white", font=("Arial", 12, "bold")).pack(side="left", padx=8, pady=6)
        ctk.CTkLabel(frame_encabezados, text="Sueldo", width=120, text_color="white", font=("Arial", 12, "bold")).pack(side="left", padx=8, pady=6)

        self.frame_datos_personal = ctk.CTkFrame(marco_tabla, fg_color="transparent")
        self.frame_datos_personal.pack(pady=5)

        # Cargar personal desde la base de datos
        self.mostrar_personal()

        btn_salir = ctk.CTkButton(self.ventanapersonal, text="Salir", fg_color="#8DCCE3", hover_color="#F8C8DC", text_color="white", corner_radius=20, width=120, height=40, command=self.ventanapersonal.destroy)
        btn_salir.pack(pady=20)

    def generar_clave_personal(self):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numeros = "0123456789"
        
        clave_generada = ""
        for i in range(5):
            if i < 3:
                pos = random.randint(0, 25)
                clave_generada = clave_generada + letras[pos]
            else:
                pos = random.randint(0, 9)
                clave_generada = clave_generada + numeros[pos]
        
        self.caja_clave.configure(state="normal")
        self.caja_clave.delete(0, tk.END)
        self.caja_clave.insert(0, clave_generada)
        self.caja_clave.configure(state="readonly")

    def agregar_proveedor(self):
        empresa = self.caempresa.get().strip()
        telefono = self.catelefono.get().strip()
        direccion = self.cadireccion.get().strip()
        contacto = self.cacontacto.get().strip()

        if empresa == "":
            messagebox.showerror("Error", "Complete el nombre de la empresa")
            return

        try:
            cursor = self.conexion.cursor()
            # Generar un número de cuenta simple
            no_cuenta = "PROV" + str(random.randint(1000, 9999))
            cursor.execute("INSERT INTO Proveedores (NoCuenta, Empresa, Direccion, correoElectronico, telefono) VALUES (?, ?, ?, ?, ?)",
                          (no_cuenta, empresa, None, contacto, telefono if telefono else None))
            self.conexion.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
            self.limpiar_campos_proveedor()
            self.mostrar_proveedores()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def mostrar_proveedores(self):
        # Limpiar tabla
        for widget in self.frame_datos_proveedores.winfo_children():
            widget.destroy()

        cursor = self.conexion.cursor()
        cursor.execute("SELECT Empresa, telefono, correoElectronico FROM Proveedores")
        proveedores = cursor.fetchall()
        cursor.close()

        contador = 0
        for prov in proveedores:
            if contador % 2 == 0:
                color_fila = "white"
            else:
                color_fila = "#F2F2F2"

            fila_frame = ctk.CTkFrame(self.frame_datos_proveedores, fg_color=color_fila, corner_radius=5)
            fila_frame.pack(fill="x", padx=5, pady=2)

            empresa = prov[0] if prov[0] else ""
            telefono = str(prov[1]) if prov[1] else ""
            contacto = prov[2] if prov[2] else ""

            ctk.CTkLabel(fila_frame, text=empresa, width=200, text_color="#1A1A1A", font=("Arial", 12)).pack(side="left", padx=20, pady=5)
            ctk.CTkLabel(fila_frame, text=telefono, width=150, text_color="#1A1A1A", font=("Arial", 12)).pack(side="left", padx=20, pady=5)
            ctk.CTkLabel(fila_frame, text="", width=200, text_color="#1A1A1A", font=("Arial", 12)).pack(side="left", padx=20, pady=5)
            ctk.CTkLabel(fila_frame, text=contacto, width=200, text_color="#1A1A1A", font=("Arial", 12)).pack(side="left", padx=20, pady=5)
            
            contador = contador + 1

    def agregar_personal(self):
        clave = self.caja_clave.get().strip()
        nombre = self.caja_nombre.get().strip()
        apellido = self.caja_apellido.get().strip()
        sueldo = self.caja_sueldo.get().strip()

        if clave == "" or nombre == "":
            messagebox.showerror("Error", "Complete los campos obligatorios")
            return

        sueldo_valor = float(sueldo) if sueldo else 0

        try:
            cursor = self.conexion.cursor()
            # Insertar en Usuario primero
            cursor.execute("INSERT INTO Usuario (Nombre, ApellidoP, ApellidoM) VALUES (?, ?, ?)", (nombre, apellido, ''))
            # Insertar en Personal
            cursor.execute("INSERT INTO Personal (ClaveAcceso, Nombre, ApellidoP, Sueldo) VALUES (?, ?, ?, ?)",
                          (clave, nombre, apellido, sueldo_valor))
            self.conexion.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Personal agregado correctamente")
            self.limpiar_campos_personal()
            self.mostrar_personal()
            self.generar_clave_personal()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def mostrar_personal(self):
        # Limpiar tabla
        for widget in self.frame_datos_personal.winfo_children():
            widget.destroy()

        cursor = self.conexion.cursor()
        cursor.execute("SELECT ClaveAcceso, Nombre, ApellidoP, Sueldo FROM Personal")
        personal = cursor.fetchall()
        cursor.close()

        contador = 0
        for emp in personal:
            if contador % 2 == 0:
                color_fila = "white"
            else:
                color_fila = "#F2F2F2"

            fila_frame = ctk.CTkFrame(self.frame_datos_personal, fg_color=color_fila, corner_radius=5)
            fila_frame.pack(fill="x", padx=5, pady=2)

            sueldo_str = f"${emp[3]:.2f}" if emp[3] else "$0.00"

            ctk.CTkLabel(fila_frame, text=emp[0], width=100, text_color="#1A1A1A", font=("Arial", 12)).pack(side="left", padx=8, pady=5)
            ctk.CTkLabel(fila_frame, text=emp[1], width=120, text_color="#1A1A1A", font=("Arial", 12)).pack(side="left", padx=8, pady=5)
            ctk.CTkLabel(fila_frame, text=emp[2] if emp[2] else "", width=120, text_color="#1A1A1A", font=("Arial", 12)).pack(side="left", padx=8, pady=5)
            ctk.CTkLabel(fila_frame, text=sueldo_str, width=120, text_color="#1A1A1A", font=("Arial", 12)).pack(side="left", padx=8, pady=5)
            
            contador = contador + 1

    def eliminar_proveedor(self):
        messagebox.showinfo("Info", "Seleccione un proveedor de la tabla para eliminar")

    def eliminar_personal(self):
        messagebox.showinfo("Info", "Seleccione un empleado de la tabla para eliminar")

    def limpiar_campos_proveedor(self):
        self.caempresa.delete(0, "end")
        self.catelefono.delete(0, "end")
        self.cadireccion.delete(0, "end")
        self.cacontacto.delete(0, "end")

    def limpiar_campos_personal(self):
        self.caja_nombre.delete(0, "end")
        self.caja_apellido.delete(0, "end")
        self.caja_sueldo.delete(0, "end")

    def volver_menu_proveedor(self):
        self.ventanapro.destroy()
        self.menu_principal()

    def volver_menu_personal(self):
        self.ventanapersonal.destroy()
        self.menu_principal()

Proveedor()