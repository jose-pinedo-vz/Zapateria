import customtkinter as ctk
from tkinter import messagebox

class ModuloFinanzas():
    def Iniciar(self,Frame):

        self.Frame_principal=Frame

        self.COLOR_ROSA = "#F8C8DC"
        self.COLOR_NEGRO = "#1A1A1A"
        self.COLOR_FONDO = "#F2F2F2"
        self.COLOR_BLANCO = "#FFFFFF"
        self.COLOR_COMPLEMENTARIO = "#8DCCE3"



        self.ventas_hoy = 8500.00
        self.egresos_lista = []

        self.setup_ui()


    def setup_ui(self):
        ctk.CTkLabel(self.Frame_principal, text="ADMINISTRACION FINANCIERA",
                      font=("Arial", 20, "bold"),
                      text_color=self.COLOR_ROSA,
                      fg_color=self.COLOR_NEGRO,
                      corner_radius=15
                      ).place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        self.nav_frame = ctk.CTkFrame(self.Frame_principal, fg_color="transparent", height=50)
        self.nav_frame.place(relx=0.5, rely=0.15, relwidth=0.9, anchor=ctk.CENTER)

        ctk.CTkButton(self.nav_frame, text="Corte de Caja", fg_color=self.COLOR_NEGRO,
                      text_color=self.COLOR_ROSA, hover_color="#333", width=150,
                      command=self.mostrar_corte
                      ).place(relx=1/4, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkButton(self.nav_frame, text="Registro Egresos", fg_color=self.COLOR_NEGRO,
                      text_color=self.COLOR_ROSA, hover_color="#333", width=150,
                      command=self.mostrar_egresos
                      ).place(relx=2/4, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkButton(self.nav_frame, text="Nomina Semanal", fg_color=self.COLOR_NEGRO,
                      text_color=self.COLOR_ROSA, hover_color="#333", width=150,
                      command=self.mostrar_nomina
                      ).place(relx=3/4, rely=0.5, anchor=ctk.CENTER)

        self.Frame_resumen = ctk.CTkFrame(self.Frame_principal, fg_color=self.COLOR_BLANCO, corner_radius=15)
        self.Frame_resumen.place(relx=0.5, rely=0.55, relwidth=0.9, relheight=0.7, anchor=ctk.CENTER)

        self.mostrar_corte()

    def limpiar_vista(self):
        for widget in self.Frame_resumen.winfo_children():
            widget.destroy()

    def mostrar_corte(self):
        self.limpiar_vista()

        total_egresos = sum(e['monto'] for e in self.egresos_lista)
        balance = self.ventas_hoy - total_egresos

        ctk.CTkLabel(self.Frame_resumen, text="Resumen de Corte Diario",
                      font=("Arial", 15, "bold"), text_color=self.COLOR_NEGRO
                      ).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        self.crear_metrica(self.Frame_resumen, "ENTRADAS (VENTAS)", f"${self.ventas_hoy:,.2f}", "#2ECC71", 0.2)
        self.crear_metrica(self.Frame_resumen, "SALIDAS (EGRESOS)", f"${total_egresos:,.2f}", "#E74C3C", 0.5)
        self.crear_metrica(self.Frame_resumen, "EFECTIVO EN CAJA", f"${balance:,.2f}", self.COLOR_NEGRO, 0.8)

        ctk.CTkButton(self.Frame_resumen, text="CERRAR TURNO Y GENERAR REPORTE",
                                        fg_color=self.COLOR_COMPLEMENTARIO, text_color=self.COLOR_NEGRO, font=("Arial", 14, "bold"),
                                        height=45, width=400,
                                        command=lambda: messagebox.showinfo("Corte", "Corte guardado en base de datos.")
                                        ).place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

    def crear_metrica(self, master, titulo, valor, color_txt, x_rel):
        etiqueta = ctk.CTkFrame(master, fg_color=self.COLOR_FONDO, width=200, height=100, corner_radius=10)
        etiqueta.place(relx=x_rel, rely=0.4, anchor=ctk.CENTER)

        ctk.CTkLabel(etiqueta, text=titulo, font=("Arial", 12, "bold"), text_color="gray").place(relx=0.5, rely=0.3, anchor=ctk.CENTER)
        ctk.CTkLabel(etiqueta, text=valor, font=("Arial", 28, "bold"), text_color=color_txt).place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

    def mostrar_egresos(self):
        self.limpiar_vista()

        ctk.CTkLabel(self.Frame_resumen, text="Registro de Gastos y Salidas", font=("Arial", 15, "bold"),
                        text_color=self.COLOR_NEGRO
                     ).place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        self.cat_egreso = ctk.CTkOptionMenu(self.Frame_resumen, values=["Renta", "Luz", "Internet", "Proveedores", "Limpieza"],
                                           fg_color=self.COLOR_NEGRO, button_color=self.COLOR_NEGRO, button_hover_color="#333", width=150)
        self.cat_egreso.place(relx=0.3, rely=0.2, anchor=ctk.CENTER)

        self.monto_egreso = ctk.CTkEntry(self.Frame_resumen, placeholder_text="Monto $", width=150)
        self.monto_egreso.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        ctk.CTkButton(self.Frame_resumen, text="Registrar Salida", fg_color=self.COLOR_COMPLEMENTARIO, text_color=self.COLOR_NEGRO, width=150,
                      command=self.registrar_egreso).place(relx=0.7, rely=0.2, anchor=ctk.CENTER)

        self.scroll_egresos = ctk.CTkScrollableFrame(self.Frame_resumen, fg_color=self.COLOR_FONDO, height=200,width=450)
        self.scroll_egresos.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        self.actualizar_lista_egresos()

    def registrar_egreso(self):
        try:
            monto = float(self.monto_egreso.get())
            self.egresos_lista.append({"cat": self.cat_egreso.get(), "monto": monto})
            self.monto_egreso.delete(0, 'end')
            self.actualizar_lista_egresos()
            messagebox.showinfo("Exito", "Gasto registrado correctamente.")
        except:
            messagebox.showerror("Error", "Ingrese un monto valido.")

    def actualizar_lista_egresos(self):
        for w in self.scroll_egresos.winfo_children(): w.destroy()
        for e in reversed(self.egresos_lista):
            f = ctk.CTkFrame(self.scroll_egresos, fg_color="white", height=40)
            f.pack(fill="x", pady=2)

            ctk.CTkLabel(f, text=f"Pago de {e['cat']}", anchor="w",text_color=self.COLOR_NEGRO
                         ).place(relx=0.2, rely=0.5, anchor=ctk.CENTER)

            ctk.CTkLabel(f, text=f"- ${e['monto']:,.2f}", text_color="red", font=("Arial", 12, "bold")
                         ).place(relx=0.8, rely=0.5, anchor=ctk.CENTER)

    def mostrar_nomina(self):
        self.limpiar_vista()

        ctk.CTkLabel(self.Frame_resumen, text="Calculo de Nomina Dinamica", font=("Arial", 20, "bold")).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        calc_frame = ctk.CTkFrame(self.Frame_resumen, fg_color=self.COLOR_FONDO, corner_radius=15, height=400)
        calc_frame.place(relx=0.5, rely=0.5, relwidth=0.7, anchor=ctk.CENTER)

        ctk.CTkLabel(calc_frame, text="Sueldo Base Semanal:",text_color=self.COLOR_NEGRO
                     ).place(relx=0.3, rely=0.2, anchor=ctk.CENTER)
        self.s_base = ctk.CTkEntry(calc_frame, width=200)
        self.s_base.insert(0, "1500")
        self.s_base.place(relx=0.7, rely=0.2, anchor=ctk.CENTER)

        ctk.CTkLabel(calc_frame, text="Ventas por Empleado:",text_color=self.COLOR_NEGRO
                     ).place(relx=0.3, rely=0.4, anchor=ctk.CENTER)
        self.v_emp = ctk.CTkEntry(calc_frame, width=200)
        self.v_emp.place(relx=0.7, rely=0.4, anchor=ctk.CENTER)

        ctk.CTkLabel(calc_frame, text="% Comision (ej. 0.03):",text_color=self.COLOR_NEGRO
                     ).place(relx=0.3, rely=0.6, anchor=ctk.CENTER)
        self.p_comision = ctk.CTkEntry(calc_frame, width=200)
        self.p_comision.insert(0, "0.03")
        self.p_comision.place(relx=0.7, rely=0.6, anchor=ctk.CENTER)

        self.lbl_resultado_nomina = ctk.CTkLabel(calc_frame, text="PAGO TOTAL: $0.00", font=("Arial", 18, "bold"), text_color=self.COLOR_NEGRO)
        self.lbl_resultado_nomina.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

        ctk.CTkButton(calc_frame, text="Calcular Sueldo", fg_color=self.COLOR_NEGRO, text_color=self.COLOR_ROSA, width=300,
                      command=self.calcular_nomina).place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

    def calcular_nomina(self):
        try:
            base = float(self.s_base.get())
            ventas = float(self.v_emp.get())
            porcentaje = float(self.p_comision.get())
            total = base + (ventas * porcentaje)
            self.lbl_resultado_nomina.configure(text=f"PAGO TOTAL: ${total:,.2f} MXN")
        except:
            messagebox.showerror("Error", "Verifique los datos de entrada.")
