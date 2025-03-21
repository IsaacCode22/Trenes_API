import flet as ft
import models.estacion as modelo_estacion 
from utils.helpers import mostrar_mensaje
import requests

API_URL = "http://127.0.0.1:8000"

def vista_login(page):
    page.theme_mode = ft.ThemeMode.DARK

    def validar_ingreso(e):
        url = f"{API_URL}/login"
        data = {
            "operador": campo_usuario.value,
            "contrasena": campo_contrasena.value
        }

        try:
            response = requests.post(url, json=data)
            print(f"🔹 Código de estado: {response.status_code}")  
            print(f"🔹 Respuesta completa: {response.text}")  

            if response.status_code == 200:
                resultado = response.json()
                token = resultado.get("token")  
                rol = resultado.get("rol")
                operador = data["operador"]  # Guarda el operador autenticado

                print(f"✅ Token recibido: {token}")  
                print(f"✅ Rol recibido: {rol}")  

                if token:
                    page.session.set("token", token)
                    page.session.set("rol", rol)

                    print(f"🔹 Token guardado: {page.session.get('token')}")
                    print(f"🔹 Rol guardado: {page.session.get('rol')}")


                    # Cargar las estaciones desde la api
                    modelo_estacion.cargar_estaciones(page)

                    # 🔥 Buscar la estación del operador autenticado
                    operador = data["operador"]
                    print(f"🔍 Buscando estación para operador: {operador}")

                    estacion_usuario = next((e for e in modelo_estacion.estaciones if e["operador"] == operador), None)

                    if estacion_usuario:
                        modelo_estacion.usuario_actual = estacion_usuario
                        print(f"✅ Usuario autenticado: {modelo_estacion.usuario_actual['operador']}, Estación asignada: {modelo_estacion.usuario_actual['nombre']}")
                    else:
                        modelo_estacion.usuario_actual = None
                        print(f"⚠️ No se encontró estación para el operador: {operador}")

                # Redirigir según el rol
                    if rol == "admin":
                        page.go("/panel")
                    elif "operador" in rol and estacion_usuario:
                        page.go("/ventas")
                    else:
                        mostrar_mensaje(page, "Rol desconocido o sin estación asignada", tipo="error")
                else:
                    mostrar_mensaje(page, "No se recibió un token válido", tipo="error")
            else:
                mostrar_mensaje(page, "Credenciales incorrectas", tipo="error")
        except requests.exceptions.RequestException as ex:
            print(f"⚠️ Error de conexión: {ex}")
            mostrar_mensaje(page, "Error de conexión con el servidor", tipo="error")
            


    logo = ft.Text(
        "Trenes Venezuela",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="#F4F9FA",
        font_family="Arial Black italic"
    )
    bienvenido = ft.Text(
        "¡Bienvenido de vuelta!",
        weight=ft.FontWeight.BOLD,
        size=20,
        color="#F4F9FA"
    )

    # ----------------------------------------------------------------
    # Campos de entrada para el usuario y la contraseña
    # ----------------------------------------------------------------
    campo_usuario = ft.TextField(
        label="Usuario",
        label_style=ft.TextStyle(color="#F4F9FA", size=20), 
        text_style=ft.TextStyle(color=ft.colors.WHITE),  
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=300,
        height=50,
        border_radius=7,
        prefix_icon=ft.icons.LOGIN,
        focused_border_color="#A7107F",
        focus_color="#A7107F",      
    )

    campo_contrasena = ft.TextField(
        label="Contraseña",
        label_style=ft.TextStyle(color="#F4F9FA", size=20),
        text_style=ft.TextStyle(color=ft.colors.WHITE),  
        password=True,
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=300,
        height=50,
        border_radius=7,
        can_reveal_password=True,
        prefix_icon=ft.icons.PASSWORD,
        focused_border_color="#A7107F",
        focus_color="#A7107F",     
    )

    # ----------------------------------------------------------------
    # Botón para iniciar sesión
    # ----------------------------------------------------------------
    login_btn = ft.ElevatedButton(
        text="INICIAR",
        on_click=validar_ingreso,
        bgcolor="#A7107F",
        color=ft.colors.WHITE,
    )

    # ----------------------------------------------------------------
    # Contenedor del formulario de inicio de sesión
    # ----------------------------------------------------------------
    login_container = ft.Container(
        content=ft.Column(
            [
                logo,
                ft.Container(height=30), 
                bienvenido,
                ft.Container(height=20),  
                campo_usuario,
                campo_contrasena,
                ft.Row([login_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=30,
        width=500,
        height=600,
        border_radius=16,
        alignment=ft.alignment.center,
        blur=ft.Blur(sigma_x=15, sigma_y=15),  
        border=ft.Border(
            left=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            top=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            right=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            bottom=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
        ),
    )

    # ----------------------------------------------------------------
    # Contenedor principal con imagen de fondo
    # ----------------------------------------------------------------
    background_container = ft.Container(
        content=ft.Stack(
            [
                ft.Column(
                    [
                        ft.Container(expand=1),  
                        ft.Row([login_container], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(expand=1), 
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ]
        ),
        expand=True,
        alignment=ft.alignment.center,
        image_src="https://iili.io/3ncZ0gI.png",
        image_fit=ft.ImageFit.COVER,
        border_radius=16,
        blur=ft.Blur(sigma_x=50, sigma_y=10),  
    )

    return ft.View(
        "/login",
        [background_container],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )