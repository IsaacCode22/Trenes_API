import flet as ft
import models.estacion as modelo_estacion
from models.estacion import estaciones

def vista_horarios(page):
    pastel_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]

    rows = []
    for idx, est in enumerate(estaciones):
        color = pastel_colors[idx % len(pastel_colors)]
        horarios_str = ", ".join(est.horarios) if est.horarios else "Sin Horarios"
        
        station_cell = ft.DataCell(
            ft.Container(
                content=ft.Text(est.nombre, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                bgcolor=color,
                padding=ft.Padding(8, 8, 8, 8),
                border_radius=8
            )
        )
        
        horarios_cell = ft.DataCell(
            ft.Container(
                content=ft.Text(horarios_str),
                padding=ft.Padding(8, 8, 8, 8)
            )
        )

        rows.append(
            ft.DataRow(
                cells=[station_cell, horarios_cell]
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Container(
                    bgcolor="#A7107F",
                    content=ft.Text("Estación", weight=ft.FontWeight.BOLD)
                )
            ),
            ft.DataColumn(
                ft.Container(
                    bgcolor="#A7107F",
                    content=ft.Text("Horarios", weight=ft.FontWeight.BOLD)
                )
            ),
        ],
        rows=rows,
        heading_row_color="#A7107F",
        border=ft.border.all(1, ft.colors.BLUE_GREY),
        divider_thickness=1,
        expand=True
    )

    main_container = ft.Container(
        padding=ft.Padding(30, 30, 30, 30),
        content=ft.Column(
            [
                ft.Container(
                    alignment=ft.alignment.top_right,
                    padding=ft.Padding(10, 10, 10, 10)
                ),
                ft.Text("HORARIOS", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Container(
                    content=table,
                    padding=ft.Padding(20, 20, 20, 20),
                    blur=ft.Blur(sigma_x=15, sigma_y=15),
                    border=ft.Border(
                        left=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
                        top=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
                        right=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
                        bottom=ft.BorderSide(color=ft.colors.WHITE12, width=1.5)
                    ),
                    border_radius=16,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        image_fit=ft.ImageFit.COVER,
        border_radius=16,
        expand=True
    )

    back_container = ft.Container(
        padding=ft.Padding(30, 30, 30, 30),
        alignment=ft.alignment.center,
        image_src="https://iili.io/3ncZ0gI.png",
        image_fit=ft.ImageFit.COVER,
        border_radius=16,
        expand=True,
        content=ft.Row(
            [
                ft.VerticalDivider(),
                main_container,
                ft.VerticalDivider(),
                ft.Container(
                    content=ft.IconButton(
                        ft.icons.ARROW_BACK,
                        on_click=lambda e: page.go("/panel") if modelo_estacion.usuario_actual.operador == "admin" else page.go("/ventas")
                    ),
                    alignment=ft.alignment.top_right
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START 
        )
    )

    return ft.View("/horarios", [back_container])


