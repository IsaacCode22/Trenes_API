from fpdf import FPDF
import requests

API_URL = "http://127.0.0.1:8000"

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Reporte de Trenes', border=0, ln=1, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

def generar_pdf(token):
    response = requests.get(f"{API_URL}/reportes", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        raise Exception("Error al obtener los datos del reporte")

    data = response.json()
    pdf = PDF()
    pdf.add_page()

    # Operadores
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Lista de Operadores:', ln=1)
    pdf.set_font('Arial', '', 10)
    for operador in data["operadores"]:
        pdf.cell(0, 10, f"- {operador['operador']} ({operador['nombre']})", ln=1)

    # Trenes
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Lista de Trenes:', ln=1)
    pdf.set_font('Arial', '', 10)
    for tren in data["trenes"]:
        pdf.cell(0, 10, f"- {tren['nombre']}", ln=1)

    # Estaciones
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Lista de Estaciones:', ln=1)
    pdf.set_font('Arial', '', 10)
    for estacion in data["estaciones"]:
        horarios = estacion['horarios']
        pdf.cell(0, 10, f"- {estacion['nombre']} (Boletos vendidos: {estacion['boletos_vendidos']})", ln=1)
        pdf.cell(0, 10, f"  Horarios: {horarios}", ln=1)

    pdf.output("reporte_trenes.pdf")
    print("PDF generado: reporte_trenes.pdf")