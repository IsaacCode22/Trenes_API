import flet as ft
from utils.pdf_generator import generar_pdf
from models.estacion import Estacion
from models.estacion import estaciones
from utils.helpers import mostrar_mensaje

import requests 
import json
API_URL = "http://127.0.0.1:8000"

def vista_panel_admin(page, token):
     
    headers = {"Authorization": f"Bearer {token}"}
    def generar_reporte_pdf(page):
        token = page.session.get("token")
        if not token:
            mostrar_mensaje(page, "Error: No hay token disponible", tipo="error")
            return

        try:
            generar_pdf(token)
            mostrar_mensaje(page, "Reporte PDF generado exitosamente", tipo="success")
        except Exception as e:
            mostrar_mensaje(page, f"Error al generar el PDF: {str(e)}", tipo="error")
    def obtener_estaciones():
        try:
            response = requests.get(f"{API_URL}/estaciones", headers=headers)
            if response.status_code == 200:
                return response.json()  # Devuelve la lista de estaciones desde el backend
            else:
                mostrar_mensaje(page, "Error al obtener estaciones", tipo="error")
                return []
        except Exception as ex:
            mostrar_mensaje(page, f"Error: {str(ex)}", tipo="error")
            return []
        
    def eliminar_estacion(est):
        try:
            response = requests.delete(f"{API_URL}/estaciones/{est['id']}", headers=headers)
            if response.status_code == 200:
                mostrar_mensaje(page, f"Estación '{est['nombre']}' eliminada.", tipo="success")
                actualizar_sidebar(lista_estaciones, page)
            else:
                mostrar_mensaje(page, "Error al eliminar la estación.", tipo="error")
        except Exception as ex:
            mostrar_mensaje(page, f"Error: {str(ex)}", tipo="error")
    
    def crear_estacion(e):
        nueva_estacion = {
            "operador": campo_operador.value,
            "contrasena": campo_contrasena_nueva.value,
            "nombre": campo_nombre_estacion.value,
            "horarios": [h.strip() for h in campo_horarios.value.split(",")],
            "precio": float(campo_precio.value),
            "estado": "activo",  # ✅ Valor por defecto
            "boletos_vendidos": 0  # ✅ Valor por defecto
        }

        print("JSON a enviar:", json.dumps(nueva_estacion, indent=2))  # 📌 Depuración

        try:
            response = requests.post(f"{API_URL}/estaciones", json=nueva_estacion, headers=headers)
            if response.status_code == 201:
                mostrar_mensaje(page, "¡Estación creada!", tipo="success")
                actualizar_sidebar(lista_estaciones, page)  # ✅ Esto debería actualizar la lista
            else:
                mostrar_mensaje(page, f"Error al crear estación: {response.text}", tipo="error")
        except Exception as ex:
            mostrar_mensaje(page, f"Error: {str(ex)}", tipo="error")

        try:
            nueva_est = Estacion(
                operador=campo_operador.value,
                contrasena=campo_contrasena_nueva.value,
                nombre=campo_nombre_estacion.value,
                horarios=[h.strip() for h in campo_horarios.value.split(",")],
                precio=float(campo_precio.value)
            )
            estaciones.append(nueva_est)
            generar_archivo_ventas(nueva_est)
            mostrar_mensaje(page, "¡Estación creada!", tipo="success")
            limpiar_formulario()
            actualizar_sidebar(lista_estaciones, page)
        except Exception as ex:
            mostrar_mensaje(page, f"Error: {str(ex)}", tipo="error")
    
    def limpiar_formulario():
        campo_operador.value = ""
        campo_contrasena_nueva.value = ""
        campo_nombre_estacion.value = ""
        campo_horarios.value = ""
        campo_precio.value = "1.0"
        page.update()
    
    def actualizar_sidebar(lista_estaciones, page):
        estaciones = obtener_estaciones()
        lista_estaciones.controls.clear()  # Vaciar la lista antes de actualizarla

        for est in estaciones:
            lista_estaciones.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(est["nombre"], color=ft.colors.WHITE),
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            icon_color=ft.colors.RED,
                            tooltip="Eliminar estación",
                            on_click=lambda e, st=est: eliminar_estacion(st)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
        page.update()

    # 💡 Definir lista_estaciones antes de usarla
    lista_estaciones = ft.Column()  # Asegurar que lista_estaciones está definida

    # 🔄 Llamar a actualizar_sidebar después de definir lista_estaciones
    actualizar_sidebar(lista_estaciones, page)

    # Resto del código (Sidebar, Formulario, etc.)


    # ----------------------------------------------------------------
    # barra lateral
    # ----------------------------------------------------------------
    total_boletos = sum(est.boletos_vendidos for est in estaciones)
    texto_total_boletos = ft.Text(f"Total Boletos Vendidos: {total_boletos}", color=ft.colors.WHITE)
    active_operators = sum(1 for est in estaciones if est.estado == "Activo")
    inactive_operators = sum(1 for est in estaciones if est.estado != "Activo")
    lista_estaciones = ft.Column(spacing=5)
    actualizar_sidebar(lista_estaciones, page) 
    
    sidebar = ft.Container(
        content=ft.Column([
            ft.Text("Información General", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Divider(color="#4511ED"),
            texto_total_boletos,
            ft.Text("Estaciones Registradas:", color=ft.colors.WHITE),
            lista_estaciones,
            ft.Divider(color="#4511ED"),
            ft.Text(f"Operadores Activos: {active_operators}", color=ft.colors.WHITE),
            ft.Text(f"Operadores Inactivos: {inactive_operators}", color=ft.colors.WHITE),
            ft.Row([
                ft.IconButton(ft.icons.LOGOUT, icon_color=ft.colors.RED_400, on_click=lambda e: page.go("/login")),
                ft.IconButton(ft.icons.PRINT, icon_color=ft.colors.WHITE, on_click=lambda e: generar_reporte_pdf(page)
            )])
        ], spacing=15),
        padding=30,
        width=300,
        height=600,
        border_radius=16,
        alignment=ft.alignment.center,
        blur=ft.Blur(sigma_x=15, sigma_y=15),
        border=ft.Border(
            left=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            top=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            right=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            bottom=ft.BorderSide(color=ft.colors.WHITE12, width=1.5)
        )
    )
    
    # ----------------------------------------------------------------
    # Formulario
    # ----------------------------------------------------------------
    campo_operador = ft.TextField(
        label="Nombre del operador",
        label_style=ft.TextStyle(color="#F4F9FA", size=16),
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        border_radius=7
    )
    campo_contrasena_nueva = ft.TextField(
        label="Contraseña",
        label_style=ft.TextStyle(color="#F4F9FA", size=16),
        password=True,
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        border_radius=7
    )
    campo_nombre_estacion = ft.TextField(
        label="Nombre de la estación",
        label_style=ft.TextStyle(color="#F4F9FA", size=16),
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        border_radius=7
    )
    campo_horarios = ft.TextField(
        label="Horarios (separar por comas)",
        label_style=ft.TextStyle(color="#F4F9FA", size=16),
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        border_radius=7
    )
    campo_precio = ft.TextField(
        label="Precio",
        label_style=ft.TextStyle(color="#F4F9FA", size=16),
        value="1.0",
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        border_radius=7
    )
    
    create_station_form = ft.Container(
        content=ft.Column([
            ft.Text("Crear Nueva Estación", size=24, weight=ft.FontWeight.BOLD, color="#F4F9FA"),
            ft.Column([
                campo_operador,
                campo_contrasena_nueva,
                campo_nombre_estacion,
                campo_horarios,
                campo_precio,
                ft.ElevatedButton(
                    "Crear Estación", 
                    on_click=crear_estacion, 
                    bgcolor="#A7107F", 
                    color=ft.colors.WHITE
                )
            ], spacing=15),
        ], spacing=20),
        padding=30,
        width=400,
        border_radius=16,
        blur=ft.Blur(sigma_x=15, sigma_y=15),
        border=ft.Border(
            left=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            top=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            right=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            bottom=ft.BorderSide(color=ft.colors.WHITE12, width=1.5)
        ),
    )
    
    # ----------------------------------------------------------------
    # Contenedor
    # ----------------------------------------------------------------
    content = ft.Container(
        content=ft.Row([
            sidebar,
            ft.VerticalDivider(width=20),
            create_station_form
        ], expand=True),
        padding=30,
        alignment=ft.alignment.center,
        image_src="https://iili.io/3ncZ0gI.png",
        image_fit=ft.ImageFit.COVER,
        border_radius=16,
        blur=ft.Blur(sigma_x=15, sigma_y=15),
        border=ft.Border(
            left=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            top=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            right=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            bottom=ft.BorderSide(color=ft.colors.WHITE12, width=1.5)
        )
    )
    
    return ft.View("/panel", [content])