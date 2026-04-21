import customtkinter as ctk

class cliente:
    def __init__(self):
        self.ventana = ctk.CTkToplevel()
        self.ventana.title("APARTADO DE CLUENTES - ZAPATERIA")
        self.ventana.config(bg="#1A1A1A")

        try: self.ventana.state("zoomed")
        except: self.ventana.attributes("-zoomed", True)

        self.ventana.grid_columnconfigure(0, weight=0)
        self.ventana.grid_columnconfigure(1, weight=1)
        self.ventana.grid_rowconfigure(0, weight=1)  

        self.frame_menu = ctk.CTkFrame(self.ventana, fg_color="#2B2B2B", corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="ns", padx=0, pady=0)

        # Frame ixquierdo
        self.btn_listaInventario = ctk.CTkButton(
            self.frame_menu, 
            text="ClIENTES", 
            fg_color="#3E3E3E", 
            text_color="#F2F2F2",
            hover_color="#505050",
            command=lambda: self.frameCentral()
        )
        self.btn_listaInventario.grid(row=0, column=0, padx=20, pady=20)

        self.frame_contenido = ctk.CTkFrame(self.ventana, fg_color="#D1D1D1", corner_radius=0)
        self.frame_contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.frameCentral()
        self.ventana.mainloop()

    def limpiar_frame_central(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
    
    


if __name__ == "__main__":
    obj = cliente()
