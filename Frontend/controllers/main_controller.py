# controllers/main_controller.py
import flet as ft
from views.login_view import vista_login
from views.admin_panel_view import vista_panel_admin
from views.ventas_view import vista_ventas
from views.horarios_view import vista_horarios  

def main(page: ft.Page):
    page.title = "Sistema de Trenes"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto"}
    
    def cambio_ruta(route):
        page.views.clear()

        if page.route == "/login":
            page.views.append(vista_login(page))

        elif page.route == "/panel":
            token = page.session.get("token")
            print(f"Token recuperado en /panel: {token}")  # Debugging

            if token:
                page.views.append(vista_panel_admin(page, token=token))
            else:
                print("Error: No se encontró un token. Redirigiendo a login.")
                page.go("/login")  # Si no hay token, redirigir al login

        elif page.route == "/ventas":
            page.views.append(vista_ventas(page))

        elif page.route == "/horarios":
            page.views.append(vista_horarios(page))

        page.update()
    
    page.on_route_change = cambio_ruta
    page.go("/login")