import customtkinter as ctk
from Ventas import ModuloVentas
from Corte_caja import ModuloFinanzas
import os
#pip install pyodbc
#pip install fpdf2 Pillow
class Ventana_GUI():
    def Iniciar(self):
        self.COLOR_PRIMARIO = "#F8C8DC"
        self.COLOR_SECUNDARIO = "#1A1A1A"
        self.COLOR_TERCIARIO = "#FFB0CC"
        self.COLOR_COMPLEMENTARIO = "#8DCCE3"
        self.COLOR_FONDO_BLANCO= "#F2F2F2"
        self.COLOR_TEXTO_NEGRO = "#1A1A1A"

        """A quien le toque: esto es para tomar al responsable o quien entro al sistema"""
        clave="E001"
        import pyodbc

        conexion=(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=Zapateria;"
        "Trusted_Connection=yes;")
        try:
            conexion=pyodbc.connect(conexion)
            print("Conexión exitosa")
        except Exception as e:
            print(f"Error al conectar: {e}")
            try:
                DB_CONFIG = (
                        "DRIVER={ODBC Driver 18 for SQL Server};"
                        "SERVER=localhost;"
                        "DATABASE=Zapateria;"
                        "UID=sa;"
                        "PWD=JitlerSQL2026!;"
                        "Encrypt=yes;"
                        "TrustServerCertificate=yes;"
                )
                conexion = pyodbc.connect(DB_CONFIG)
                print("coneccion exitosa")
            except:
                print("Ubo un error2")





        cursor=conexion.cursor()
        cursor.execute("""
            SELECT ClaveAcceso,Nombre,ApellidoP
            FROM Personal
            WHERE ClaveAcceso=?
            """,(clave,))

        fila=cursor.fetchone()
        self.Responsable_turno=(fila.Nombre+" "+fila.ApellidoP)
        cursor.close()
        conexion.close()
        print("Responsable: ",self.Responsable_turno)


        self.Ventana=ctk.CTk()
        self.Ventana.geometry("1000x700")
        self.Ventana.title("Menu Principal")
        self.Ventana.configure(fg_color=self.COLOR_SECUNDARIO)
        self.Ventana.after(200,lambda:self.Ventana.state('zoomed'))


        self.Frame_principal=ctk.CTkFrame(self.Ventana,
                                          fg_color=self.COLOR_FONDO_BLANCO,

                                          )
        self.Frame_principal.place(relx=0.5, rely=0.6, relheight=.75,relwidth=.9,anchor=ctk.CENTER)

        btn_Finanzas=ctk.CTkButton(self.Ventana,text="Area financiera",
                                   fg_color=self.COLOR_COMPLEMENTARIO,
                                   text_color=self.COLOR_TEXTO_NEGRO,
                                   command=self.Llama_Modulo_Finanzas)
        btn_Finanzas.place(relx=.1,rely=.15,anchor=ctk.CENTER)

        btn_Venta=ctk.CTkButton(self.Ventana,text="Ventas",
                                fg_color=self.COLOR_COMPLEMENTARIO,
                                text_color=self.COLOR_TEXTO_NEGRO,
                                command=self.Llama_Modulo_Ventas)
        btn_Venta.place(relx=.25,rely=.15,anchor=ctk.CENTER)

        btn_extra1 = ctk.CTkButton(
                    self.Ventana,
                    text="Clientes",
                    fg_color=self.COLOR_COMPLEMENTARIO,
                    text_color=self.COLOR_TEXTO_NEGRO,
                    command=self.llamar_modulo_clientes
                )
        btn_extra1.place(relx=.4, rely=.15, anchor=ctk.CENTER)

        btn_extra2=ctk.CTkButton(self.Ventana,text="Productos",
                                   fg_color=self.COLOR_COMPLEMENTARIO,
                                   text_color=self.COLOR_TEXTO_NEGRO,
                                   command=self.llamar_modulo_inventario)
        btn_extra2.place(relx=.55,rely=.15,anchor=ctk.CENTER)

        btn_extra3=ctk.CTkButton(self.Ventana,text="Extra 3",
                                   fg_color=self.COLOR_COMPLEMENTARIO,
                                   text_color=self.COLOR_TEXTO_NEGRO)
        btn_extra3.place(relx=.7,rely=.15,anchor=ctk.CENTER)

        btn_extra4=ctk.CTkButton(self.Ventana,text="Extra 4",
                                   fg_color=self.COLOR_COMPLEMENTARIO,
                                   text_color=self.COLOR_TEXTO_NEGRO)
        btn_extra4.place(relx=.85,rely=.15,anchor=ctk.CENTER)



        lblTitulo=ctk.CTkLabel(self.Ventana,text="Zapateria Los Dos Hermanos\nS.A de C.V.",
                               font=("Arial", 20,"bold"),
                               text_color=self.COLOR_PRIMARIO)
        lblTitulo.place(relx=.5,rely=.05,anchor=ctk.CENTER)

        self.Ventana.mainloop()

    def BorraFrame(self):
        for widget in self.Frame_principal.winfo_children():
            widget.destroy()

    def Llama_Modulo_Ventas(self):
        self.BorraFrame()
        Ventas=ModuloVentas()
        Ventas.Iniciar(self.Frame_principal,self.Responsable_turno)

    def Llama_Modulo_Finanzas(self):
        self.BorraFrame()
        Finanzas=ModuloFinanzas()
        Finanzas.Iniciar(self.Frame_principal,self.Responsable_turno)

    def llamar_modulo_clientes(self):
        self.BorraFrame()
        from clientes import cliente
        obj = cliente()

    def llamar_modulo_inventario(self):
        self.BorraFrame()
        from inventario import inventario
        obj = inventario()


obj=Ventana_GUI()
obj.Iniciar()
