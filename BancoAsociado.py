import customtkinter as ctk
from tkinter import messagebox
import random

 

class BancoGuachinango():
    def Iniciar(self):
        self.COLOR_ROSA = "#F8C8DC"
        self.COLOR_NEGRO = "#1A1A1A"
        self.COLOR_GUACHINANGO = "#FF5733"
        self.COLOR_FONDO = "#F2F2F2"

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
                      font=("Arial", 12, "italic"), text_color="white").place(relx=0.45, rely=0.5, anchor=ctk.CENTER)

        self.main_container = ctk.CTkFrame(self.Ventana, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.55, relwidth=0.95, relheight=0.8, anchor=ctk.CENTER)

        self.frame_reg = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.frame_reg.place(relx=0.2, rely=0.5, relwidth=0.38, relheight=1.0, anchor=ctk.CENTER)

        ctk.CTkLabel(self.frame_reg, text="Apertura de Cuenta", font=("Arial", 18, "bold"), text_color=self.COLOR_NEGRO).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        self.ent_nombre = self.crear_campo(self.frame_reg, "Nombre Completo del Cliente", 0.25)
        self.ent_pin = self.crear_campo(self.frame_reg, "PIN de Seguridad (4 digitos)", 0.45)
        self.ent_deposito = self.crear_campo(self.frame_reg, "Deposito Inicial ($)", 0.65)

        ctk.CTkButton(self.frame_reg, text="Registrar en Guachinango", fg_color=self.COLOR_GUACHINANGO, 
                      text_color="white", font=("Arial", 13, "bold"), height=40,
                      command=self.registrar_cliente).place(relx=0.5, rely=0.85, relwidth=0.8, anchor=ctk.CENTER)

        self.frame_lista = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15)
        self.frame_lista.place(relx=0.7, rely=0.5, relwidth=0.58, relheight=1.0, anchor=ctk.CENTER)

        ctk.CTkLabel(self.frame_lista, text="Clientes Registrados", font=("Arial", 18, "bold"),text_color="black").place(relx=0.5, rely=0.08, anchor=ctk.CENTER)

        self.search_bar = ctk.CTkEntry(self.frame_lista, placeholder_text="Buscar por numero de cuenta...", width=300)
        self.search_bar.place(relx=0.5, rely=0.18, anchor=ctk.CENTER)

        self.scroll_cuentas = ctk.CTkScrollableFrame(self.frame_lista, fg_color="transparent")
        self.scroll_cuentas.place(relx=0.5, rely=0.58, relwidth=0.9, relheight=0.7, anchor=ctk.CENTER)

        self.actualizar_lista()

    def crear_campo(self, master, label, y_pos):
        ctk.CTkLabel(master, text=label, font=("Arial", 11),text_color="black").place(relx=0.5, rely=y_pos - 0.05, anchor=ctk.CENTER)
        entry = ctk.CTkEntry(master, height=35)
        entry.place(relx=0.5, rely=y_pos, relwidth=0.8, anchor=ctk.CENTER)
        return entry

    def registrar_cliente(self):
        nombre = self.ent_nombre.get()
        pin = self.ent_pin.get()
        try:
            monto = float(self.ent_deposito.get())
        except:
            messagebox.showerror("Error", "Monto de deposito invalido.")
            return

        if nombre and len(pin) == 4:
            n_cuenta = str(random.randint(100000, 999999))
            
            self.CUENTAS_GUACHINANGO[n_cuenta] = {
                "nombre": nombre,
                "pin": pin,
                "saldo": monto
            }
            
            messagebox.showinfo("Guachinango", f"Cuenta creada con exito!\nNo. Cuenta: {n_cuenta}\nSaldo: ${monto}")
            self.limpiar_campos()
            self.actualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Complete todos los campos correctamente.")

    def limpiar_campos(self):
        self.ent_nombre.delete(0, 'end')
        self.ent_pin.delete(0, 'end')
        self.ent_deposito.delete(0, 'end')

    def actualizar_lista(self):
        for w in self.scroll_cuentas.winfo_children(): w.destroy()
        
        y_offset = 0.1
        for num, datos in self.CUENTAS_GUACHINANGO.items():
            card = ctk.CTkFrame(self.scroll_cuentas, fg_color=self.COLOR_FONDO, corner_radius=10, height=60)
            card.pack(fill="x", pady=5, padx=5) # Nota: pack se mantiene solo dentro del ScrollableFrame para permitir el scroll dinamico
            
            info = f"CTA: {num} | {datos['nombre']}"
            ctk.CTkLabel(card, text=info, font=("Arial", 12, "bold"),text_color="black").place(relx=0.25, rely=0.5, anchor=ctk.CENTER)
            
            saldo_lbl = ctk.CTkLabel(card, text=f"${datos['saldo']:,.2f}", text_color=self.COLOR_GUACHINANGO, font=("Arial", 14, "bold"))
            saldo_lbl.place(relx=0.75, rely=0.5, anchor=ctk.CENTER)
            
            ctk.CTkButton(card, text="+", width=30, height=30, fg_color=self.COLOR_NEGRO, 
                          command=lambda n=num: self.abrir_deposito(n)).place(relx=0.92, rely=0.5, anchor=ctk.CENTER)

    def abrir_deposito(self, n_cuenta):
        dialog = ctk.CTkInputDialog(text=f"Monto a depositar en cuenta {n_cuenta}:", title="Deposito Guachinango")
        monto = dialog.get_input()
        if monto:
            try:
                self.CUENTAS_GUACHINANGO[n_cuenta]['saldo'] += float(monto)
                self.actualizar_lista()
                messagebox.showinfo("Exito", "Deposito procesado.")
            except:
                messagebox.showerror("Error", "Monto invalido.")

obj=BancoGuachinango()
obj.Iniciar()