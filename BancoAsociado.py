import customtkinter as ctk
from tkinter import messagebox
import random
import ConexionBanco
from decimal import Decimal
from GeneraPDF import PDF_Guachinango
from datetime import datetime
import os
 

class BancoGuachinango():
    def Iniciar(self):
        self.COLOR_ROSA = "#F8C8DC"
        self.COLOR_NEGRO = "#1A1A1A"
        self.COLOR_GUACHINANGO = "#FF5733"
        self.COLOR_FONDO = "#F2F2F2"

        self.Sucursal="Zacatecas Sur"
        self.CuentaSeleccionada=None

        self.CUENTAS_GUACHINANGO = {}

        self.Ventana=ctk.CTk()
        self.Ventana.title("Sistema Bancario GUACHINANGO")
        self.Ventana.geometry("1000x650")
        self.Ventana.configure(fg_color=self.COLOR_FONDO)
        self.setup_ui()
        self.Ventana.mainloop()

    def setup_ui(self):
        self.header = ctk.CTkFrame(self.Ventana, fg_color=self.COLOR_NEGRO, height=80, corner_radius=0)
        self.header.place(relx=0.5, rely=0.06, relwidth=1.0, anchor=ctk.CENTER)
        
        ctk.CTkLabel(self.header, text="BANCO GUACHINANGO", 
                      font=("Arial", 26, "bold"), text_color=self.COLOR_GUACHINANGO).place(relx=0.2, rely=0.5, anchor=ctk.CENTER)
        ctk.CTkLabel(self.header, text="Tu cuenta del ahorro.", 
                      font=("Arial", 12, "italic"), text_color="white").place(relx=0.2, rely=0.85, anchor=ctk.CENTER)

        ctk.CTkButton(self.header, text="Registrar", fg_color=self.COLOR_GUACHINANGO, 
                      text_color="white", font=("Arial", 13, "bold"), height=10,
                      command=self.registrar_cliente).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        ctk.CTkButton(self.header, text="Editar", fg_color="#FFB700", 
                      text_color="white", font=("Arial", 13, "bold"), height=10,
                      command=self.actualizar_cliente).place(relx=0.7, rely=0.5,  anchor=ctk.CENTER)
        
        ctk.CTkButton(self.header, text="Eliminar", fg_color="#FF3503", 
                      text_color="white", font=("Arial", 13, "bold"), height=10,
                      command=self.Eliminar_cliente).place(relx=0.9, rely=0.5,  anchor=ctk.CENTER)
        

        self.main_container = ctk.CTkFrame(self.Ventana, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.55, relwidth=0.95, relheight=0.8, anchor=ctk.CENTER)

        self.frame_reg = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.frame_reg.place(relx=0.2, rely=0.5, relwidth=0.38, relheight=1.0, anchor=ctk.CENTER)


        self.frame_lista = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.frame_lista.place(relx=0.7, rely=0.5, relwidth=0.58, relheight=1.0, anchor=ctk.CENTER)

        ctk.CTkLabel(self.frame_lista, text="Clientes Registrados", font=("Arial", 18, "bold"),text_color="black").place(relx=0.5, rely=0.05, anchor=ctk.CENTER)
        ctk.CTkLabel(self.frame_lista, text=f"Sucursal: {self.Sucursal}", 
                      font=("Arial", 12, "italic"), text_color="black").place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        self.search_bar = ctk.CTkEntry(self.frame_lista, placeholder_text="Buscar por numero de cuenta...", width=300)
        self.search_bar.place(relx=0.5, rely=0.18, anchor=ctk.CENTER)
        btn_buscar=ctk.CTkButton(self.frame_lista,text="🔍", width=10,command=self.Busqueda)
        btn_buscar.place(relx=0.8, rely=0.18, anchor=ctk.CENTER)

        self.scroll_cuentas = ctk.CTkScrollableFrame(self.frame_lista, fg_color="transparent")
        self.scroll_cuentas.place(relx=0.5, rely=0.58, relwidth=0.9, relheight=0.7, anchor=ctk.CENTER)

        self.actualizar_diccionario()
        self.actualizar_lista()
        
    
    def Busqueda(self):
        if self.search_bar.get()!="":
            cuentaa=self.search_bar.get()
            for w in self.scroll_cuentas.winfo_children(): 
                w.destroy()
            if cuentaa in self.CUENTAS_GUACHINANGO:
                for cuenta, datos in self.CUENTAS_GUACHINANGO.items():
                    if cuentaa in cuenta:

                        card = ctk.CTkFrame(self.scroll_cuentas, fg_color=self.COLOR_FONDO, corner_radius=10, height=60)
                        card.pack(fill="x", pady=5, padx=5) 
                    
                        info = f"CUENTA: {cuenta} | {datos['nombre']}"
                        ctk.CTkLabel(card, text=info, font=("Arial", 12, "bold"),text_color="black").place(relx=0.25, rely=0.5, anchor=ctk.CENTER)
                        
                        saldo_lbl = ctk.CTkLabel(card, text=f"${datos['saldo']:,.2f}", text_color=self.COLOR_GUACHINANGO, font=("Arial", 14, "bold"))
                        saldo_lbl.place(relx=0.75, rely=0.5, anchor=ctk.CENTER)
                        
                        ctk.CTkButton(card, text="+", width=30, height=30, fg_color=self.COLOR_NEGRO, 
                                    command=lambda n=cuenta: self.abrir_deposito(n)).place(relx=0.92, rely=0.5, anchor=ctk.CENTER)
                        
            else:
                card = ctk.CTkFrame(self.scroll_cuentas, fg_color=self.COLOR_FONDO, corner_radius=10, height=60)
                card.pack(fill="x", pady=5, padx=5) 
                ctk.CTkLabel(card, text="No se encontro nada", font=("Arial", 12, "bold"),text_color="black").place(relx=0.25, rely=0.5, anchor=ctk.CENTER)
        else:
            self.actualizar_lista()
                

    def crear_campo(self, master, label, y_pos):
        ctk.CTkLabel(master, text=label, font=("Arial", 11),text_color="black").place(relx=0.5, rely=y_pos - 0.05, anchor=ctk.CENTER)
        entry = ctk.CTkEntry(master, height=35)
        entry.place(relx=0.5, rely=y_pos, relwidth=0.8, anchor=ctk.CENTER)
        return entry
    
    def CrearPin(self):
        PIN=""
        for i in range(4):
            PIN+=str(random.randrange(0,10))
        return PIN
    
    def CrearClave(self):
        clave=""
        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()

        cursor.execute("SELECT Nombre_Sucursal,Ciudad_Sucursal FROM Sucursal")
        for fila in cursor:
            if fila.Nombre_Sucursal==self.Sucursal:
                ciudad=fila.Ciudad_Sucursal
            else:
                print("Esa sucursal no existe")
                return None

        ciudad=ciudad.lower()[:2]
        clave+=ciudad+"-"
        cursor.execute("SELECT ClaveCuenta FROM Cuenta")

        for fila in cursor:
            last=fila.ClaveCuenta
        last=int(last[-2:])
        last+=1

        if last<10:
            last="0"+str(last)
        else:
            last=str(last)

        clave=ciudad+"-"+last

        cursor.close()
        conexion.close()

        return clave
    
    def CrearTajeta(self,id_cuenta):
        numero = ''.join([str(random.randint(0, 9)) for _ in range(16)])

        cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()
        
        cursor.execute("""
        INSERT INTO Tarjeta (numero_tarjeta, cvv, id_cuenta_asociada)
        VALUES (?, ?, ?)
        """, (numero, cvv, id_cuenta))
        conexion.commit()
        messagebox.showinfo("Guachinango", f"Tarjeta {numero} creada exitosamente.")

    def registrar_cliente(self):
        self.LimpiarFrame(self.frame_reg)
        ctk.CTkLabel(self.frame_reg, text="Apertura de Cuenta", font=("Arial", 18, "bold"), text_color=self.COLOR_NEGRO).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        self.ent_nombre = self.crear_campo(self.frame_reg, "Nombre del Cliente", 0.2)
        self.ent_apellidop= self.crear_campo(self.frame_reg, "Apellido Paterno", 0.35)
        self.ent_apellidom = self.crear_campo(self.frame_reg, "Apellido Paterno", 0.5)
        self.ent_residencia= self.crear_campo(self.frame_reg, "Ciudad de residencia", 0.65)
        self.ent_deposito = self.crear_campo(self.frame_reg, "Deposito Inicial ($)", 0.8)
        

        ctk.CTkButton(self.frame_reg, text="Registrar Cuenta", fg_color=self.COLOR_GUACHINANGO, 
                      text_color="white", font=("Arial", 13, "bold"), height=40,
                      command=self.registrar).place(relx=0.5, rely=0.9, relwidth=0.8, anchor=ctk.CENTER)

    def registrar(self):
        try:
            nombre = self.ent_nombre.get().strip()
            apellidop = self.ent_apellidop.get().strip()
            apellidom = self.ent_apellidom.get().strip()
            ubicacion = self.ent_residencia.get().strip()
    
            if not all([nombre, apellidop, apellidom, ubicacion]):
                messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
                return
            
            if not all(x.replace(" ", "").isalpha() for x in [nombre, apellidop, apellidom]):
                messagebox.showwarning("Datos inválidos", "Los nombres y apellidos no pueden contener números.")
                return

            ClaveCuenta = self.CrearClave()
            Pin = self.CrearPin()
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
            return
        
        try:
            monto = float(self.ent_deposito.get())
        except:
            messagebox.showerror("Error", "Monto de deposito invalido.")
            return
        
        
        self.GuardarNuevoUsuario(ClaveCuenta,nombre,apellidop,apellidom,Pin,ubicacion,monto)
        self.actualizar_diccionario()
        self.limpiar_campos()
        self.actualizar_lista()
        

    def actualizar_cliente(self):
        try:
            nombre = self.ent_nombre.get().strip()
            apellidop = self.ent_apellidop.get().strip()
            apellidom = self.ent_apellidom.get().strip()
            ubicacion = self.ent_residencia.get().strip()
    
            if not all([nombre, apellidop, apellidom, ubicacion]):
                messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
                return
            
            if not all(x.replace(" ", "").isalpha() for x in [nombre, apellidop, apellidom]):
                messagebox.showwarning("Datos inválidos", "Los nombres y apellidos no pueden contener números.")
                return

            ClaveCuenta = self.CrearClave()
            Pin = self.CrearPin()
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
            return
        
        try:
            monto = float(self.ent_deposito.get())
        except:
            messagebox.showerror("Error", "Monto de deposito invalido.")
            return
        
        
        self.GuardarNuevoUsuario(ClaveCuenta,nombre,apellidop,apellidom,Pin,ubicacion,monto)
        self.actualizar_diccionario()
        self.limpiar_campos()
        self.actualizar_lista()
    
    def Consulta_cliente(self,cuenta):
        self.Emergente= ctk.CTkToplevel()
        self.Emergente.title("Datos del cliente")
        self.Emergente.geometry("500x500")
        self.Emergente.configure(fg_color=self.COLOR_FONDO)
        self.Emergente.grab_set()
        Cliente={"Clave","Saldo","Sucursal"}
        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()
        print(cuenta)
        ctk.CTkLabel(self.Emergente, text=f"Información de la cuenta", font=("Arial", 15, "bold"),text_color="black"
                         ).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        cursor.execute("SELECT distinct Cliente.ClaveCuenta,NombreCliente,ApellidoM,ApeelidoP,Saldo,Sucursal,numero_tarjeta FROM Cuenta,Cliente,Tarjeta WHERE Cliente.ClaveCuenta=Cuenta.ClaveCuenta and  Cliente.ClaveCuenta=id_cuenta_asociada and Cliente.ClaveCuenta=?",
                       (cuenta,))
        for fila in cursor:
            print(fila)
            ctk.CTkLabel(self.Emergente, text=f"Clave:\n{fila.ClaveCuenta}", font=("Arial", 15, "bold"),text_color="black"
                            ).place(relx=0.5, rely=0.25, anchor=ctk.CENTER)
            ctk.CTkLabel(self.Emergente, text=f"Saldo:\n{fila.Saldo}", font=("Arial", 15, "bold"),text_color="black"
                            ).place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
            ctk.CTkLabel(self.Emergente, text=f"Sucursal donde la\ncuenta fue abierta:\n{fila.Sucursal}", font=("Arial", 15, "bold"),text_color="black"
                            ).place(relx=0.5, rely=0.45, anchor=ctk.CENTER)
        
        cursor.close()
        conexion.close()

        

    def Eliminar_cliente(self):
        try:
            nombre = self.ent_nombre.get().strip()
            apellidop = self.ent_apellidop.get().strip()
            apellidom = self.ent_apellidom.get().strip()
            ubicacion = self.ent_residencia.get().strip()
    
            if not all([nombre, apellidop, apellidom, ubicacion]):
                messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
                return
            
            if not all(x.replace(" ", "").isalpha() for x in [nombre, apellidop, apellidom]):
                messagebox.showwarning("Datos inválidos", "Los nombres y apellidos no pueden contener números.")
                return

            ClaveCuenta = self.CrearClave()
            Pin = self.CrearPin()
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
            return
        
        try:
            monto = float(self.ent_deposito.get())
        except:
            messagebox.showerror("Error", "Monto de deposito invalido.")
            return
        
        
        self.GuardarNuevoUsuario(ClaveCuenta,nombre,apellidop,apellidom,Pin,ubicacion,monto)
        self.actualizar_diccionario()
        self.limpiar_campos()
        self.actualizar_lista()

    def GuardarNuevoUsuario(self,ClaveCuenta,nombre,apellidop,apellidom,Pin,ubicacion,monto):
        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()

        cursor.execute("INSERT INTO Cliente (ClaveCuenta, NombreCliente, ApellidoM, ApeelidoP) VALUES (?,?,?,?)",
        (ClaveCuenta,nombre,apellidom,apellidop))

        cursor.execute("INSERT INTO Cuenta (ClaveCuenta,Saldo,Sucursal,PIN) VALUES (?,?,?,?)",
        (ClaveCuenta,monto,self.Sucursal,Pin))

        cursor.execute("INSERT INTO Ubicacion (Nombre,Ciudad,Clave) VALUES (?,?,?)",
        (nombre,ubicacion,ClaveCuenta))
        conexion.commit()
        cursor.close()
        conexion.close()
        messagebox.showinfo("Guachinango", f"Cuenta creada con exito!\nNo. Cuenta: {ClaveCuenta}\nSaldo: ${monto}")
        self.CrearTajeta(ClaveCuenta)
        

        

    def limpiar_campos(self):
        self.ent_nombre.delete(0, 'end')
        self.ent_apellidop.delete(0, 'end')
        self.ent_apellidom.delete(0, 'end')
        self.ent_residencia.delete(0, 'end')
        self.ent_deposito.delete(0, 'end')
    
    def actualizar_diccionario(self):
        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()
        cursor.execute("SELECT Cuenta.ClaveCuenta,Cliente.NombreCliente,Saldo FROM Cuenta,Cliente WHERE Cliente.ClaveCuenta=Cuenta.ClaveCuenta")
        for fila in cursor:
            self.CUENTAS_GUACHINANGO[fila.ClaveCuenta]={
                "nombre": fila.NombreCliente,
                "saldo":fila.Saldo}
        cursor.close()
        conexion.close()
        

    def actualizar_lista(self):
        for w in self.scroll_cuentas.winfo_children(): w.destroy()
        
        for cuenta, datos in self.CUENTAS_GUACHINANGO.items():
            card = ctk.CTkFrame(self.scroll_cuentas, fg_color=self.COLOR_FONDO, corner_radius=10, height=60)
            card.pack(fill="x", pady=5, padx=5) 

            card.bind("<Button-1>", lambda: self.Seleccionado(cuenta))
            
            info = f"CUENTA: {cuenta} | {datos['nombre']}"
            ctk.CTkLabel(card, text=info, font=("Arial", 12, "bold"),text_color="black").place(relx=0.25, rely=0.5, anchor=ctk.CENTER)
            
            saldo_lbl = ctk.CTkLabel(card, text=f"${datos['saldo']:,.2f}", text_color=self.COLOR_GUACHINANGO, font=("Arial", 14, "bold"))
            saldo_lbl.place(relx=0.6, rely=0.5, anchor=ctk.CENTER)
            
            ctk.CTkButton(card, text="+", width=30, height=30, fg_color=self.COLOR_NEGRO, 
                          command=lambda n=cuenta: self.abrir_deposito(n)).place(relx=0.92, rely=0.5, anchor=ctk.CENTER)
            
            ctk.CTkButton(card,text="🔍", width=10,command= lambda: self.Consulta_cliente(cuenta)
                          ).place(relx=0.8, rely=0.5, anchor=ctk.CENTER)

    def abrir_deposito(self, cuenta):
        #dialog1 = ctk.CTkInputDialog(text=f"Monto a depositar:", title="Deposito Guachinango")
        #monto = dialog1.get_input()
        self.Emergente= ctk.CTkToplevel()
        self.Emergente.title("Deposito a cuenta")
        self.Emergente.geometry("500x500")
        self.Emergente.configure(fg_color=self.COLOR_FONDO)
        self.Emergente.grab_set()

        lblTitulo=ctk.CTkLabel(self.Emergente,text="Deposito a cuenta Guachinango",font=("Arial",20,"bold"),text_color=self.COLOR_GUACHINANGO)
        lblTitulo.place(relx=.5,rely=.1,anchor=ctk.CENTER)

        lbl=ctk.CTkLabel(self.Emergente,text="Cantidad a depositar $",font=("Arial",15,"bold"),text_color=self.COLOR_NEGRO
                         ).place(relx=.5,rely=.3,anchor=ctk.CENTER)
        entry_cantidad=ctk.CTkEntry(self.Emergente,font=("Arial",15,"bold"))
        entry_cantidad.place(relx=.5,rely=.4,anchor=ctk.CENTER)

        lbl=ctk.CTkLabel(self.Emergente,text="Destinatario",font=("Arial",15,"bold"),text_color=self.COLOR_NEGRO
                         ).place(relx=.5,rely=.5,anchor=ctk.CENTER)
        entry_destino=ctk.CTkEntry(self.Emergente,font=("Arial",15,"bold"))
        entry_destino.place(relx=.5,rely=.6,anchor=ctk.CENTER)


        def Confirmar():
            try:
                cantidad=Decimal(entry_cantidad.get())
                destino=entry_destino.get()

                deposito=self.Realizar_deposito(cantidad,destino,cuenta)
                if deposito:
                    print("entro")
                    folio_gen = datetime.now().strftime("%Y%m%d%H%M%S")
                    print("1")
                    self.generar_pdf_transferencia(cuenta, destino, cantidad, folio_gen)
                    print("2")
                    self.actualizar_diccionario()
                    self.actualizar_lista()
                    self.Emergente.destroy()
                    messagebox.showinfo("Exito", "Deposito procesado.")
                else:
                    messagebox.showinfo("Error", "Deposito cancelado.")

            except:
                messagebox.showerror("Error", "Valores invalidos.")
            
        aceptar=ctk.CTkButton(self.Emergente, text="Aceptar",
                                command=Confirmar)
        aceptar.place(relx=.35,rely=.7,anchor=ctk.CENTER)

        cancelar=ctk.CTkButton(self.Emergente, text="Cancelar",
                                command=self.Emergente.destroy)
        cancelar.place(relx=.65,rely=.7,anchor=ctk.CENTER)
        
    def Realizar_deposito(self,monto,destino,remitente):
        conexion = None
        try:
            conexion=ConexionBanco.conectar_db()
            cursor=conexion.cursor()
            cursor.execute("UPDATE Cuenta SET Saldo = Saldo - ? WHERE ClaveCuenta = ? AND Saldo >= ?",
                        (monto,remitente,monto))
            cursor.execute("UPDATE Cuenta SET Saldo = Saldo + ? WHERE ClaveCuenta = ?",
                        (monto,destino))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Transacción abortada. Los cambios fueron revertidos: {e}")
            return False
        finally:
            if conexion:
                conexion.close()
    
    def generar_pdf_transferencia(self,remitente, destino, monto, folio):
        pdf = PDF_Guachinango()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título
        pdf.set_fill_color(230, 230, 230) 
        pdf.cell(0, 10, f"DETALLES DE LA TRANSFERENCIA - FOLIO: {folio}", ln=True, align="L", fill=True)
        pdf.ln(5)

        datos = [
            ("Cuenta Emisora:", remitente),
            ("Cuenta Destino:", destino),
            ("Monto de la Operación:", f"${monto:,.2f} MXN"),
            ("Estatus:", "EXITOSO / CONCILIADO")
        ]

        for label, value in datos:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(50, 10, label)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, value, ln=True)

        pdf.ln(20)
        pdf.set_font("Arial", "B", 10)
        pdf.multi_cell(0, 5, "Este documento sirve como comprobante legal de la transferencia realizada. "
                            "Para cualquier duda, contacte a soporte técnico del Tec.")

        nombre_archivo = f"Comprobante_{folio}.pdf"
        carpteda_donde_el_programa_esta_corriendo= os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta = os.path.join(carpteda_donde_el_programa_esta_corriendo, "PDF",nombre_archivo)
        pdf.output(ruta_carpeta)

        print(f"PDF {nombre_archivo} creado con éxito.")
    
    def LimpiarFrame(self,widget):
        for w in widget.winfo_children(): w.destroy()
    
    def Seleccionado(self,event,cuenta):
        self.CuentaSeleccionada=cuenta

obj=BancoGuachinango()
obj.Iniciar()