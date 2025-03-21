# utils/helpers.py
import flet as ft

def mostrar_mensaje(page, mensaje, tipo="info"):
    if tipo == "error":
        bgcolor = ft.colors.RED_800
        text_color = ft.colors.WHITE
    elif tipo == "success":
        bgcolor = ft.colors.GREEN
        text_color = ft.colors.WHITE
    elif tipo == "pdf":
        bgcolor = "#4511ED"
        text_color = ft.colors.WHITE
    else:
        bgcolor = ft.colors.BLUE_GREY
        text_color = ft.colors.WHITE

    snack = ft.SnackBar(
        content=ft.Text(mensaje, color=text_color),
        bgcolor=bgcolor,
        open=True
    )
    page.open(snack)
    page.update()

def toggle_theme(page):
    #modo claro y oscuro
    page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
    page.update()

def generar_archivo_ventas(estacion):
    pass
