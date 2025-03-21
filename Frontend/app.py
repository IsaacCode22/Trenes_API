# app.py
import flet as ft
from controllers.main_controller import main
#TEST


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
    #ft.app(target=main)