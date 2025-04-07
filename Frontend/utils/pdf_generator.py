from fpdf import FPDF
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

class PDF(FPDF):
    def header(self):
        # Logo (si tuvieras uno)
        # self.image('logo.png', 10, 8, 33)
        
        # Título y fecha
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte de Trenes', border=0, ln=1, align='C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', border=0, ln=1, align='C')
        
        # Línea separadora
        self.line(10, 25, 200, 25)
        self.ln(10)  # Espacio después del encabezado

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(230, 230, 230)  # Color gris claro
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(5)
    
    def chapter_body(self):
        self.set_font('Arial', '', 11)
        self.ln(5)

def generar_pdf(token):
    response = requests.get(f"{API_URL}/reportes", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        raise Exception("Error al obtener los datos del reporte")

    data = response.json()
    pdf = PDF()
    
    # Configuraciones generales
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(left=10, top=10, right=10)
    
    # PÁGINA 1: PORTADA
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(60)  # Espacio desde la parte superior
    pdf.cell(0, 20, 'REPORTE COMPLETO', ln=1, align='C')
    pdf.cell(0, 20, 'SISTEMA DE TRENES', ln=1, align='C')
    pdf.set_font('Arial', 'I', 14)
    pdf.cell(0, 10, f'Fecha: {datetime.now().strftime("%d de %B de %Y")}', ln=1, align='C')
    
    # PÁGINA 2: OPERADORES
    pdf.add_page()
    pdf.chapter_title('Lista de Operadores')
    pdf.chapter_body()
    
    # Tabla de operadores
    col_width = 95
    row_height = 10
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(col_width, row_height, "Operador", 1, 0, 'C')
    pdf.cell(col_width, row_height, "Nombre Completo", 1, 1, 'C')
    
    pdf.set_font('Arial', '', 10)
    for operador in data["operadores"]:
        pdf.cell(col_width, row_height, operador['operador'], 1, 0, 'L')
        pdf.cell(col_width, row_height, operador['nombre'], 1, 1, 'L')
    
    # PÁGINA 3: TRENES
    pdf.add_page()
    pdf.chapter_title('Lista de Trenes')
    pdf.chapter_body()
    
    # Tabla de trenes
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, row_height, "Nombre del Tren", 1, 1, 'C')
    
    pdf.set_font('Arial', '', 10)
    for tren in data["trenes"]:
        pdf.cell(0, row_height, tren['nombre'], 1, 1, 'L')
    
    # PÁGINA 4: ESTACIONES
    pdf.add_page()
    pdf.chapter_title('Lista de Estaciones')
    pdf.chapter_body()
    
    # Tabla de estaciones
    pdf.set_font('Arial', 'B', 11)
    headers = ["Nombre", "Operador", "Boletos", "Estado", "Precio"]
    widths = [60, 40, 30, 30, 30]
    
    # Encabezados
    for i in range(len(headers)):
        pdf.cell(widths[i], row_height, headers[i], 1, 0, 'C')
    pdf.ln()
    
    pdf.set_font('Arial', '', 10)
    for estacion in data["estaciones"]:
        # Si una fila es demasiado larga, añadir parámetro para dividir el contenido
        # o calcular el alto de la fila dinámicamente
        pdf.cell(widths[0], row_height, estacion['nombre'], 1, 0, 'L')
        pdf.cell(widths[1], row_height, estacion.get('operador', 'N/A'), 1, 0, 'L')
        pdf.cell(widths[2], row_height, str(estacion['boletos_vendidos']), 1, 0, 'C')
        pdf.cell(widths[3], row_height, estacion.get('estado', 'N/A'), 1, 0, 'C')
        pdf.cell(widths[4], row_height, f"${estacion.get('precio', 0):.2f}", 1, 1, 'R')
    
    # PÁGINA 5: DETALLE DE HORARIOS
    pdf.add_page()
    pdf.chapter_title('Detalle de Horarios por Estación')
    pdf.chapter_body()
    
    for estacion in data["estaciones"]:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, f"{estacion['nombre']}", 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        
        horarios = estacion.get('horarios', 'No disponible')
        pdf.multi_cell(0, 8, f"Horarios: {horarios}", 0, 'L')
        pdf.cell(0, 5, f"Precio del boleto: ${estacion.get('precio', 0):.2f}", 0, 1)
        pdf.cell(0, 5, f"Boletos vendidos: {estacion['boletos_vendidos']}", 0, 1)
        pdf.cell(0, 5, f"Estado: {estacion.get('estado', 'N/A')}", 0, 1)
        pdf.ln(5)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(5)
    
    # PÁGINA 6: ESTADÍSTICAS (opcional)
    pdf.add_page()
    pdf.chapter_title('Estadísticas del Sistema')
    pdf.chapter_body()
    
    # Calcular algunas estadísticas básicas
    total_boletos = sum(estacion['boletos_vendidos'] for estacion in data["estaciones"])
    total_estaciones = len(data["estaciones"])
    total_operadores = len(data["operadores"])
    total_trenes = len(data["trenes"])
    
    # Mostrar estadísticas
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Resumen General:', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    stats = [
        f"Total de boletos vendidos: {total_boletos}",
        f"Total de estaciones: {total_estaciones}",
        f"Total de operadores: {total_operadores}",
        f"Total de trenes: {total_trenes}",
        f"Promedio de boletos por estación: {total_boletos/total_estaciones if total_estaciones > 0 else 0:.2f}"
    ]
    
    for stat in stats:
        pdf.cell(0, 8, stat, 0, 1)
    
    # Guardar el PDF
    pdf.output("reporte_trenes.pdf")
    print("PDF generado: reporte_trenes.pdf")
    return "reporte_trenes.pdf"