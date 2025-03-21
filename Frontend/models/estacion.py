# models/estacion.py
import requests

API_URL = "http://127.0.0.1:8000"

class Tren:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad  # Capacidad total del tren
        self.boletos_vendidos = 0

    def vender_boletos(self, cantidad):
        if self.boletos_vendidos + cantidad > self.capacidad:
            raise Exception("Capacidad insuficiente en el tren")
        self.boletos_vendidos += cantidad  # Se incrementan los boletos vendidos

    def capacidad_disponible(self):
        return self.capacidad - self.boletos_vendidos  # Disminuye a medida que se venden boletos

class Estacion:
    def __init__(self, operador, contrasena, nombre, horarios, precio):
        self.operador = operador
        self.contrasena = contrasena
        self.nombre = nombre
        self.horarios = horarios
        self.precio = precio
        self.estado = "Activo"
        self.boletos_vendidos = 0
        self.ventas = []

        self.trenes = [
            Tren("Tren 1", 80),
            Tren("Tren 2", 80),
            Tren("Tren 3", 80)
        ]

"""admin_credentials = {
    "operador": "admin",
    "contrasena": "123"
}"""

"""estaciones = [
    Estacion("operador1", "123", "Centro", ["09:00", "13:00", "17:00"], 1.0),
    Estacion("operador2", "123", "Barrio Obrero", ["10:00", "14:00", "18:00"], 1.0),
    Estacion("operador3", "123", "Barrio 1", ["10:00", "14:00", "18:00"], 1.0)
]""" 


def cargar_estaciones(page):
    global estaciones  # Usar la variable global
    token = page.session.get("token")
    id_estacion = page.session.get("id_estacion")

    if not token:
        print("⚠️ No hay token, no se pueden obtener estaciones.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{API_URL}/estaciones/{id_estacion}" if id_estacion else f"{API_URL}/estaciones"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        estaciones = response.json()  # Actualizar la variable global
        print(f"✅ Estaciones cargadas: {estaciones}")
    else:
        print(f"⚠️ Error al obtener estaciones: {response.status_code}")


estaciones = [] 
   

usuario_actual = None


