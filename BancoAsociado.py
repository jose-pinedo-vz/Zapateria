import customtkinter as ctk
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
import random
import ConexionBanco
from decimal import Decimal
from GeneraPDF import PDF_Guachinango
from datetime import datetime
import os
 

class BancoGuachinango():
    def Iniciar(self):
        self.COLOR_ROSA="#F8C8DC"
        self.COLOR_NEGRO="#1A1A1A"
        self.COLOR_GUACHINANGO="#FF5733"
        self.COLOR_FONDO="#F2F2F2"

        self.Sucursal="Zacatecas Sur"
        self.CuentaSeleccionada=None

        self.CUENTAS_GUACHINANGO={}

        self.Ventana=ctk.CTk()
        self.Ventana.title("Sistema Bancario GUACHINANGO")
        self.Ventana.geometry("1000x700")
        self.Ventana.configure(fg_color=self.COLOR_FONDO)
        self.setup_ui()
        self.Ventana.mainloop()

    def setup_ui(self):
        self.header=ctk.CTkFrame(self.Ventana, fg_color=self.COLOR_NEGRO, height=80, corner_radius=0)
        self.header.place(relx=0.5, rely=0.06, relwidth=1.0, anchor=ctk.CENTER)
        
        ctk.CTkLabel(self.header, text="BANCO GUACHINANGO", 
                      font=("Arial", 26, "bold"), text_color=self.COLOR_GUACHINANGO).place(relx=0.2, rely=0.5, anchor=ctk.CENTER)
        ctk.CTkLabel(self.header, text="Tu cuenta del ahorro.", 
                      font=("Arial", 12, "italic"), text_color="white").place(relx=0.2, rely=0.85, anchor=ctk.CENTER)

        

        self.main_container=ctk.CTkFrame(self.Ventana, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.55, relwidth=0.95, relheight=0.8, anchor=ctk.CENTER)

        self.frame_reg=ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.frame_reg.place(relx=0.2, rely=0.5, relwidth=0.38, relheight=1.0, anchor=ctk.CENTER)


        self.frame_lista=ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.frame_lista.place(relx=0.7, rely=0.5, relwidth=0.58, relheight=1.0, anchor=ctk.CENTER)

        ctk.CTkLabel(self.frame_lista, text="Clientes Registrados", font=("Arial", 18, "bold"),text_color="black").place(relx=0.5, rely=0.05, anchor=ctk.CENTER)
        ctk.CTkLabel(self.frame_lista, text=f"Sucursal: {self.Sucursal}", 
                      font=("Arial", 12, "italic"), text_color="black").place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        ctk.CTkButton(self.frame_lista, text="Registrar", fg_color=self.COLOR_GUACHINANGO, 
                      text_color="white", font=("Arial", 13, "bold"), height=10,
                      command=self.registrar_cliente).place(relx=0.8, rely=0.1, anchor=ctk.CENTER)
        
        self.search_bar=ctk.CTkEntry(self.frame_lista, placeholder_text="Buscar por numero de cuenta...", width=300)
        self.search_bar.place(relx=0.5, rely=0.18, anchor=ctk.CENTER)
        btn_buscar=ctk.CTkButton(self.frame_lista,text="🔍", width=10,command=self.Busqueda)
        btn_buscar.place(relx=0.8, rely=0.18, anchor=ctk.CENTER)

        self.scroll_cuentas=ctk.CTkScrollableFrame(self.frame_lista, fg_color="transparent")
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

                        card=ctk.CTkFrame(self.scroll_cuentas, fg_color=self.COLOR_FONDO, corner_radius=10, height=60)
                        card.pack(fill="x", pady=5, padx=5) 
                    
                        info=f"CUENTA: {cuenta} | {datos['nombre']}"
                        ctk.CTkLabel(card, text=info, font=("Arial", 12, "bold"),text_color="black").place(relx=0.25, rely=0.5, anchor=ctk.CENTER)
                        
                        saldo_lbl=ctk.CTkLabel(card, text=f"${datos['saldo']:,.2f}", text_color=self.COLOR_GUACHINANGO, font=("Arial", 14, "bold"))
                        saldo_lbl.place(relx=0.75, rely=0.5, anchor=ctk.CENTER)
                        
                        ctk.CTkButton(card, text="+", width=30, height=30, fg_color=self.COLOR_NEGRO, 
                                    command=lambda n=cuenta: self.abrir_deposito(n)).place(relx=0.92, rely=0.5, anchor=ctk.CENTER)
                        
            else:
                card=ctk.CTkFrame(self.scroll_cuentas, fg_color=self.COLOR_FONDO, corner_radius=10, height=60)
                card.pack(fill="x", pady=5, padx=5) 
                ctk.CTkLabel(card, text="No se encontro nada", font=("Arial", 12, "bold"),text_color="black").place(relx=0.25, rely=0.5, anchor=ctk.CENTER)
        else:
            self.actualizar_lista()
                

    def crear_campo(self, master, label, y_pos):
        ctk.CTkLabel(master, text=label, font=("Arial", 11),text_color="black").place(relx=0.5, rely=y_pos - 0.05, anchor=ctk.CENTER)
        entry=ctk.CTkEntry(master, height=30)
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
        numero=''.join([str(random.randint(0, 9)) for _ in range(16)])

        cvv=''.join([str(random.randint(0, 9)) for _ in range(3)])
        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()
        
        cursor.execute("""
        INSERT INTO Tarjeta (numero_tarjeta, cvv, id_cuenta_asociada)
        VALUES (?, ?, ?)
        """, (numero, cvv, id_cuenta))
        conexion.commit()
        messagebox.showinfo("Guachinango", f"Tarjeta {numero} creada exitosamente.")
        cursor.close()
        conexion.close()

    def registrar_cliente(self):
        self.LimpiarFrame(self.frame_reg)
        ctk.CTkLabel(self.frame_reg, text="Apertura de Cuenta", font=("Arial", 15, "bold"), text_color=self.COLOR_NEGRO).place(relx=0.5, rely=1/10, anchor=ctk.CENTER)
        
        self.ent_nombre=self.crear_campo(self.frame_reg, "Nombre del Cliente", 2/10)
        self.ent_apellidop= self.crear_campo(self.frame_reg, "Apellido Paterno", 3/10)
        self.ent_apellidom=self.crear_campo(self.frame_reg, "Apellido Materno", 4/10)
        self.ent_residencia= self.crear_campo(self.frame_reg, "Ciudad de residencia", 5/10)
        self.ent_telefono=self.crear_campo(self.frame_reg, "Teléfono", 6/10) 
        self.ent_email=self.crear_campo(self.frame_reg, "Correo Electrónico", 7/10) 
        self.ent_deposito=self.crear_campo(self.frame_reg, "Deposito Inicial ($)", 8/10)
        

        ctk.CTkButton(self.frame_reg, text="Registrar Cuenta", fg_color=self.COLOR_GUACHINANGO, 
                      text_color="white", font=("Arial", 13, "bold"), height=30,
                      command=self.registrar).place(relx=0.5, rely=9/10, relwidth=0.8, anchor=ctk.CENTER)

    def registrar(self):
        try:
            nombre=self.ent_nombre.get().strip()
            apellidop=self.ent_apellidop.get().strip()
            apellidom=self.ent_apellidom.get().strip()
            ubicacion=self.ent_residencia.get().strip()
            telefono=self.ent_telefono.get().strip()
            email=self.ent_email.get().strip()
    
            if not all([nombre, apellidop, apellidom, ubicacion, telefono, email]):
                CTkMessagebox(title="Error", message="Todos los campos son obligatorios.", icon="cancel")
                return
            
            if not all(x.replace(" ", "").isalpha() for x in [nombre, apellidop, apellidom]):
                CTkMessagebox(title="Error", message="Los nombres y apellidos no pueden contener números.", icon="cancel")
                return
            
            if not telefono.replace(" ", "").isdigit():
                CTkMessagebox(title="Error", message="El teléfono debe contener solo dígitos numéricos", icon="cancel")
                return
            
            if "@" not in email or "." not in email:
                CTkMessagebox(title="Error", message="El correo electrónico no es válido", icon="cancel")
                return
            ClaveCuenta=self.CrearClave()
            Pin=self.CrearPin()
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
            return
        
        try:
            monto=float(self.ent_deposito.get())
        except:
            messagebox.showerror("Error", "Monto de deposito invalido.")
            return
        
        
        self.GuardarNuevoUsuario(ClaveCuenta, nombre, apellidop, apellidom, Pin, ubicacion, monto, telefono, email)
        self.actualizar_diccionario()
        self.limpiar_campos()
        self.actualizar_lista()
        

    def actualizar_cliente(self,cuenta):
        if hasattr(self, 'Emergente'):
            self.Emergente.destroy()
        self.LimpiarFrame(self.frame_reg)
        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()

        cursor.execute("""
                SELECT distinct Cliente.ClaveCuenta, NombreCliente, ApellidoM, ApellidoP, ciudad, Telefono, Email
                FROM Cuenta, Cliente, Ubicacion
                WHERE Cliente.ClaveCuenta=Cuenta.ClaveCuenta
                AND Cliente.ClaveCuenta=Ubicacion.Clave
                AND Cliente.ClaveCuenta=? 
                AND Cliente.Activo=1
            """, (cuenta,))
        
        fila=cursor.fetchone()
        if fila:
            self.ent_nombre=self.crear_campo(self.frame_reg, "Nombre del Cliente", 1/8)
            self.ent_apellidop= self.crear_campo(self.frame_reg, "Apellido Paterno", 2/8)
            self.ent_apellidom=self.crear_campo(self.frame_reg, "Apellido Materno", 3/8)
            self.ent_residencia= self.crear_campo(self.frame_reg, "Ciudad de residencia", 4/8)
            self.ent_telefono=self.crear_campo(self.frame_reg, "Teléfono", 5/8) 
            self.ent_email=self.crear_campo(self.frame_reg, "Correo Electrónico", 6/8) 

            self.ent_nombre.insert(0,fila.NombreCliente)
            self.ent_apellidop.insert(0, fila.ApellidoP)
            self.ent_apellidom.insert(0, fila.ApellidoM)
            self.ent_residencia.insert(0,fila.ciudad)
            self.ent_telefono.insert(0, fila.Telefono)
            self.ent_email.insert(0,fila.Email)

            ctk.CTkButton(self.frame_reg, text="Aceptar cambios", fg_color=self.COLOR_GUACHINANGO, 
                        text_color="white", font=("Arial", 13, "bold"), height=40,
                        command=lambda:self.Actualizar(cuenta)).place(relx=0.25, rely=6/7, relwidth=0.4, anchor=ctk.CENTER)
            
            ctk.CTkButton(self.frame_reg, text="Cancelar", fg_color="#FFAB03", 
                        text_color="white", font=("Arial", 13, "bold"), height=40,
                        command=lambda: self.LimpiarFrame(self.frame_reg)).place(relx=0.75, rely=7/8, relwidth=0.4, anchor=ctk.CENTER)

        else:
            CTkMessagebox(title="Error", message="El cliente no existe en la base de datos", icon="cancel")
        cursor.close()
        conexion.close()

       
    def Actualizar(self,cuenta):
        band=self.mostrar_confirmacion()
        if band: 
            try:
                nombre=self.ent_nombre.get().strip()
                apellidop=self.ent_apellidop.get().strip()
                apellidom=self.ent_apellidom.get().strip()
                ubicacion=self.ent_residencia.get().strip()
                telefono=self.ent_telefono.get().strip()
                email=self.ent_email.get().strip()
                if not all([nombre, apellidop, apellidom, ubicacion]):
                    CTkMessagebox(title="Error", message="Todos los campos son obligatorios.", icon="cancel")
                    return
                
                if not all(x.replace(" ", "").isalpha() for x in [nombre, apellidop, apellidom]):
                    CTkMessagebox(title="Error", message="Los nombres y apellidos no pueden contener números.", icon="cancel")
                    return
                
                if not telefono.replace(" ", "").isdigit():
                    CTkMessagebox(title="Error", message="El teléfono debe contener solo dígitos numéricos", icon="cancel")
                    return
                
                if "@" not in email or "." not in email:
                    CTkMessagebox(title="Error", message="El correo electrónico no es válido", icon="cancel")
                    return
                
                conexion=ConexionBanco.conectar_db()
                cursor=conexion.cursor()

                cursor.execute("""UPDATE Cliente
                           SET NombreCliente=?, ApellidoM=? , ApellidoP=?, Telefono=?, Email=?
                           WHERE ClaveCuenta=?""",
                           (nombre,apellidom,apellidop,cuenta,telefono,email))
                
                cursor.execute("""UPDATE Ubicacion
                           SET Ciudad=?
                           WHERE Clave=?""",
                           (ubicacion,cuenta))
                conexion.commit()
                cursor.close()
                conexion.close()
                self.actualizar_diccionario()
                self.actualizar_lista()
                self.LimpiarFrame(self.frame_reg)
                CTkMessagebox(title="Éxito", message="Cuenta modificada correctamente.", icon="check")
                
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Ocurrió un error inesperado: {e}", icon="cancel")
                return
        else:
            self.LimpiarFrame(self.frame_reg)
            CTkMessagebox(title="Cancelado", message="Operacion cancelada", icon="cancel")
            
        
    
        
    def Consulta_cliente(self,cuenta):
        self.Emergente= ctk.CTkToplevel()
        self.Emergente.title("Datos del cliente")
        self.Emergente.geometry("500x500")
        self.Emergente.configure(fg_color=self.COLOR_FONDO)
        self.Emergente.grab_set()

        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()
        print(cuenta)
        frame=ctk.CTkFrame(master=self.Emergente,bg_color=self.COLOR_FONDO,corner_radius=50)
        frame.pack(fill="both", expand=True,pady=10, padx=10)

        ctk.CTkLabel(frame, text=f"Información de la cuenta: {cuenta}", font=("Arial", 15, "bold"),text_color=self.COLOR_FONDO
                         ).place(relx=0.5, rely=1/9, anchor=ctk.CENTER)

        cursor.execute("""
                SELECT distinct Cliente.ClaveCuenta, NombreCliente, ApellidoM, ApellidoP, Saldo, Sucursal, numero_tarjeta, ciudad, Telefono, Email
                FROM Cuenta, Cliente, Tarjeta ,Ubicacion
                WHERE Cliente.ClaveCuenta=Cuenta.ClaveCuenta 
                AND Clave=Cuenta.ClaveCuenta
                AND Cliente.ClaveCuenta=id_cuenta_asociada 
                AND Cliente.ClaveCuenta=? 
                AND Cliente.Activo=1
            """, (cuenta,))
        
        fila=cursor.fetchone()

        if fila:
            
            ctk.CTkLabel(frame, text=f"A nombre de:\n{fila.NombreCliente} {fila.ApellidoP} {fila.ApellidoM}", font=("Arial", 15, "bold"),text_color=self.COLOR_FONDO
                            ).place(relx=0.5, rely=2/9, anchor=ctk.CENTER)
            
            ctk.CTkLabel(frame, text=f"Numero telefonico:\n{fila.Telefono}", font=("Arial", 15, "bold"),text_color=self.COLOR_FONDO
                            ).place(relx=0.5, rely=3/9, anchor=ctk.CENTER)
            
            ctk.CTkLabel(frame, text=f"Email:\n{fila.Email}", font=("Arial", 15, "bold"),text_color=self.COLOR_FONDO
                            ).place(relx=0.5, rely=4/9, anchor=ctk.CENTER)
            
            ctk.CTkLabel(frame, text=f"Saldo:\n{fila.Saldo}", font=("Arial", 15, "bold"),text_color=self.COLOR_FONDO
                            ).place(relx=0.5, rely=5/9, anchor=ctk.CENTER)
            
            ctk.CTkLabel(frame, text=f"Sucursal donde la\ncuenta fue abierta:\n{fila.Sucursal}", font=("Arial", 15, "bold"),text_color=self.COLOR_FONDO
                            ).place(relx=0.5, rely=6/9, anchor=ctk.CENTER)
            
            ctk.CTkLabel(frame, text=f"Clabe de tarjeta:\n{fila.numero_tarjeta}", font=("Arial", 15, "bold"),text_color=self.COLOR_FONDO
                            ).place(relx=0.5, rely=7/9, anchor=ctk.CENTER)
            
            ctk.CTkButton(frame, text="Editar", fg_color="#FFB700", 
                      text_color="white", font=("Arial", 13, "bold"), height=10,
                      command=lambda: self.actualizar_cliente(cuenta)).place(relx=0.25, rely=8/9,  anchor=ctk.CENTER)
        
            ctk.CTkButton(frame, text="Eliminar", fg_color="#FF3503", 
                      text_color="white", font=("Arial", 13, "bold"), height=10,
                      command=lambda: self.Eliminar_cliente(cuenta)).place(relx=0.75, rely=8/9,  anchor=ctk.CENTER)
        else:
            CTkMessagebox(title="Error", message="El cliente no existe en la base de datos", icon="cancel")


        cursor.close()
        conexion.close()

        

    def Eliminar_cliente(self,cuenta):
        band=self.mostrar_confirmacion()
        if band: 
            try:
                conexion=ConexionBanco.conectar_db()
                cursor=conexion.cursor()

                cursor.execute("UPDATE Cliente SET Activo=0 WHERE ClaveCuenta=?", (cuenta,))
                
                conexion.commit()
                cursor.close()
                conexion.close()

                if hasattr(self, 'Emergente'):
                    self.Emergente.destroy()

                self.actualizar_diccionario()
                self.actualizar_lista()
                
                CTkMessagebox(title="Éxito", message="Cuenta desactivada correctamente.", icon="check")

            except Exception as e:
                CTkMessagebox(title="Error", message=f"No se pudo desactivar la cuenta: {e}", icon="cancel")
        else:
            CTkMessagebox(title="Cancelado", message="Operacion cancelada", icon="cancel")

    def GuardarNuevoUsuario(self,ClaveCuenta,nombre,apellidop,apellidom,Pin,ubicacion,monto,telefono, email):
        conexion=None
        try:
            conexion=ConexionBanco.conectar_db()
            cursor=conexion.cursor()

            cursor.execute("""
            INSERT INTO Cliente (ClaveCuenta, NombreCliente, ApellidoM, ApellidoP, Telefono, Email) 
            VALUES (?,?,?,?,?,?)""",
            (ClaveCuenta, nombre, apellidom, apellidop, telefono, email))

            cursor.execute("INSERT INTO Cuenta (ClaveCuenta, Saldo, Sucursal, PIN) VALUES (?,?,?,?)",
                        (ClaveCuenta, monto, self.Sucursal, Pin))

            cursor.execute("INSERT INTO Ubicacion (Ciudad, Clave) VALUES (?,?)",
                        (ubicacion, ClaveCuenta))

            conexion.commit()
            CTkMessagebox(title="Guachinango", message="Cuenta creada con éxito.", icon="check")
            self.CrearTajeta(ClaveCuenta)

        except Exception as e:
            if conexion: conexion.rollback()
            CTkMessagebox(title="Error", message=f"No se pudo guardar: {e}", icon="cancel")

        finally:
            if conexion:
                cursor.close() 
                conexion.close() 
        

        

    def limpiar_campos(self):
        self.ent_nombre.delete(0, 'end')
        self.ent_apellidop.delete(0, 'end')
        self.ent_apellidom.delete(0, 'end')
        self.ent_residencia.delete(0, 'end')
        self.ent_deposito.delete(0, 'end')
        self.ent_telefono.delete(0, 'end')
        self.ent_email.delete(0, 'end')
    
    def actualizar_diccionario(self):
        self.CUENTAS_GUACHINANGO={} 
        conexion=ConexionBanco.conectar_db()
        cursor=conexion.cursor()
        cursor.execute("""
            SELECT Cuenta.ClaveCuenta, Cliente.NombreCliente, Saldo 
            FROM Cuenta 
            JOIN Cliente ON Cliente.ClaveCuenta=Cuenta.ClaveCuenta 
            WHERE Cliente.Activo=1
        """)
        for fila in cursor:
            self.CUENTAS_GUACHINANGO[fila.ClaveCuenta]={
                "nombre": fila.NombreCliente,
                "saldo": fila.Saldo
            }
        cursor.close()
        conexion.close()
            

    def actualizar_lista(self):
        for w in self.scroll_cuentas.winfo_children(): w.destroy()
        
        for cuenta, datos in self.CUENTAS_GUACHINANGO.items():
            card=ctk.CTkFrame(self.scroll_cuentas, fg_color=self.COLOR_FONDO, corner_radius=10, height=60)
            card.pack(fill="x", pady=5, padx=5) 

            card.bind("<Button-1>", lambda e, c=cuenta: self.Seleccionado(c))
            card.bind("<Enter>", lambda e, c=card: c.configure(fg_color="#A5A5A5"))
            card.bind("<Leave>", lambda e, c=card: c.configure(fg_color=self.COLOR_FONDO))
            
            info=f"CUENTA: {cuenta} | {datos['nombre']}"
            ctk.CTkLabel(card, text=info, font=("Arial", 12, "bold"),text_color="black").place(relx=0.25, rely=0.5, anchor=ctk.CENTER)
            
            saldo_lbl=ctk.CTkLabel(card, text=f"${datos['saldo']:,.2f}", text_color=self.COLOR_GUACHINANGO, font=("Arial", 14, "bold"))
            saldo_lbl.place(relx=0.6, rely=0.5, anchor=ctk.CENTER)
            
            ctk.CTkButton(card, text="-", width=30, height=30, fg_color="#E74C3C", hover_color="#C0392B",
                          command=lambda c=cuenta: self.abrir_retiro(c)).place(relx=0.85, rely=0.5, anchor=ctk.CENTER)
            
            ctk.CTkButton(card, text="+", width=30, height=30, fg_color=self.COLOR_NEGRO, 
                          command=lambda c=cuenta: self.abrir_deposito(c)).place(relx=0.93, rely=0.5, anchor=ctk.CENTER)
            

    def abrir_deposito(self, cuenta):
        #dialog1=ctk.CTkInputDialog(text=f"Monto a depositar:", title="Deposito Guachinango")
        #monto=dialog1.get_input()
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

        ctk.CTkLabel(self.Emergente,text="CVV",font=("Arial",15,"bold"),text_color=self.COLOR_NEGRO
                         ).place(relx=.5,rely=.7,anchor=ctk.CENTER)
        entry_clave=ctk.CTkEntry(self.Emergente,font=("Arial",15,"bold"))
        entry_clave.place(relx=.5,rely=.8,anchor=ctk.CENTER)


        def Confirmar():
            try:
                cantidad=Decimal(entry_cantidad.get())
                destino=entry_destino.get()
                cvv=entry_clave.get().strip()

                deposito=self.Realizar_deposito(cantidad,destino,cuenta)
                if deposito:
                    print("entro")
                    folio_gen=datetime.now().strftime("%Y%m%d%H%M%S")
                    print("1")
                    self.generar_pdf_transferencia(cuenta, destino, cantidad, folio_gen)
                    print("2")
                    self.actualizar_diccionario()
                    self.actualizar_lista()
                    self.Emergente.destroy()
                    
                    CTkMessagebox(title="Éxito", message="Deposito procesado.", icon="check")
                else:
                    messagebox.showinfo("Error", "Deposito cancelado.")

            except:
                CTkMessagebox(title="Error", message="Valores invalidos.", icon="cancel")
            
        aceptar=ctk.CTkButton(self.Emergente, text="Aceptar",
                                command=Confirmar)
        aceptar.place(relx=.35,rely=.7,anchor=ctk.CENTER)

        cancelar=ctk.CTkButton(self.Emergente, text="Cancelar",
                                command=self.Emergente.destroy)
        cancelar.place(relx=.65,rely=.7,anchor=ctk.CENTER)
        
    def Realizar_deposito(self, monto, destino, remitente,cvv):
        conexion=None
        cursor=None
        try:
            conexion=ConexionBanco.conectar_db()
            cursor=conexion.cursor()
            if len(destino)!=16:
                cursor.execute("SELECT numero_tarjeta from Tarjeta WHERE id_cuenta_asociada=?",
                                    (destino))
                fila=cursor.fetchone()
                tarjeta_destino=fila.numero_tarjeta
            else:
                tarjeta_destino=destino

            cursor.execute("SELECT numero_tarjeta from Tarjeta WHERE id_cuenta_asociada=?",
                                (remitente))
            fila=cursor.fetchone()
            tarjeta_remitente=fila.numero_tarjeta
            

            if tarjeta_destino==tarjeta_remitente:
                cursor.execute("""UPDATE Cuenta SET Saldo=Saldo + ?
                                where exists(select 1 from Tarjeta where  numero_tarjeta=? and Cuenta.ClaveCuenta=Tarjeta.id_cuenta_asociada,and cvv=?)
                                and exists(select 1 from Cliente where  Cuenta.ClaveCuenta=Cliente.ClaveCuenta and Cliente.Activo=1)""",
                                (monto, tarjeta_destino,cvv))
            
            else:
                cursor.execute("""UPDATE Cuenta SET Saldo=Saldo - ?
                        where Saldo >= ?
                        and exists(select 1 from Tarjeta where  numero_tarjeta=? and Cuenta.ClaveCuenta=Tarjeta.id_cuenta_asociada)
                        and exists(select 1 from Cliente where  Cuenta.ClaveCuenta=Cliente.ClaveCuenta and Cliente.Activo=1)""",
                                (monto, monto, tarjeta_remitente,cvv))
                
                cursor.execute("""UPDATE Cuenta SET Saldo=Saldo + ?
                                where exists(select 1 from Tarjeta where  numero_tarjeta=? and Cuenta.ClaveCuenta=Tarjeta.id_cuenta_asociada)
                                and exists(select 1 from Cliente where  Cuenta.ClaveCuenta=Cliente.ClaveCuenta and Cliente.Activo=1)""",
                                (monto, tarjeta_destino))
            
            conexion.commit()
            return True
        except Exception as e:
            if conexion: conexion.rollback()
            return False
        finally:
            if conexion: conexion.close()
            
    def abrir_retiro(self, cuenta):
        self.Emergente_Retiro = ctk.CTkToplevel(self.Ventana)
        self.Emergente_Retiro.title("Retiro de Efectivo")
        self.Emergente_Retiro.geometry("300x200")
        self.Emergente_Retiro.grab_set() # Bloquea la ventana principal

        ctk.CTkLabel(self.Emergente_Retiro, text=f"Retirar de cuenta: {cuenta}", font=("Arial", 12)).pack(pady=10)
        
        ent_monto = ctk.CTkEntry(self.Emergente_Retiro, placeholder_text="Monto a retirar")
        ent_monto.pack(pady=10)

        ctk.CTkButton(self.Emergente_Retiro, text="Confirmar Retiro", fg_color="#E74C3C",
                      command=lambda: self.confirmar_ejecucion_retiro(cuenta, ent_monto.get())).pack(pady=10)

    def confirmar_ejecucion_retiro(self, cuenta, monto_str):
        try:
            monto = Decimal(monto_str)
            if monto <= 0: raise ValueError
            
            if self.mostrar_confirmacion():
                exito = self.Procesar_retiro_db(monto, cuenta)
                
                if exito:
                    self.Emergente_Retiro.destroy()
                    self.actualizar_diccionario()
                    self.actualizar_lista()
                    CTkMessagebox(title="Éxito", message=f"Retiro de ${monto:,.2f} realizado.", icon="check")
                else:
                    CTkMessagebox(title="Error", message="Saldo insuficiente.", icon="cancel")
        except:
            CTkMessagebox(title="Error", message="Ingrese un monto válido.", icon="cancel")
    
    def Procesar_retiro_db(self, monto, cuenta):
        conexion = None
        try:
            conexion = ConexionBanco.conectar_db()
            cursor = conexion.cursor()
            cursor.execute("UPDATE Cuenta SET Saldo = Saldo - ? WHERE ClaveCuenta = ? AND Saldo >= ?", 
                           (monto, cuenta, monto))
            count = cursor.rowcount
            conexion.commit()
            return count > 0
        except Exception as e:
            if conexion: conexion.rollback()
            return False
        finally:
            if conexion: conexion.close()
        
    def generar_pdf_transferencia(self,remitente, destino, monto, folio):
        pdf=PDF_Guachinango()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título
        pdf.set_fill_color(230, 230, 230) 
        pdf.cell(0, 10, f"DETALLES DE LA TRANSFERENCIA - FOLIO: {folio}", ln=True, align="L", fill=True)
        pdf.ln(5)

        datos=[
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

        nombre_archivo=f"Comprobante_{folio}.pdf"
        carpteda_donde_el_programa_esta_corriendo= os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta=os.path.join(carpteda_donde_el_programa_esta_corriendo, "PDF",nombre_archivo)
        pdf.output(ruta_carpeta)

        print(f"PDF {nombre_archivo} creado con éxito.")
    
    def LimpiarFrame(self,widget):
        for w in widget.winfo_children(): w.destroy()
    
    def Seleccionado(self,cuenta):
        self.CuentaSeleccionada=cuenta
        self.Consulta_cliente(cuenta)
    
    def mostrar_confirmacion(self):
        msg=CTkMessagebox(
            title="Confirmar Acción",
            message="¿Estás seguro de que deseas realizar esta operación en Banco Guachinango?",
            icon="question",
            option_1="Cancelar",
            option_2="Confirmar"
        )
        respuesta=msg.get()
        
        if respuesta=="Confirmar":
            return True
        else:
            msg.destroy()
            return False
        

obj=BancoGuachinango()
obj.Iniciar()