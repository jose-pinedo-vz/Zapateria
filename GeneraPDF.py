from fpdf import FPDF
from datetime import datetime

class PDF_Guachinango(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "BANCO GUACHINANGO S.A. de C.V.", ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.cell(0, 5, "Comprobante Oficial de Operación", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cell(0, 10, f"Generado el: {fecha_hora} - Página {self.page_no()}", align="C")
    