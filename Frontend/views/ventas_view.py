# views/ventas_view.py
import flet as ft
import threading, time
from datetime import datetime
import models.estacion as modelo_estacion 
from utils.helpers import mostrar_mensaje

def construir_horarios(horarios):
    colores_pastel = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
    elementos_horarios = []
    for i, horario in enumerate(horarios):
        color = colores_pastel[i % len(colores_pastel)]
        elementos_horarios.append(
            ft.Container(
                content=ft.Text(horario, color="black"),
                bgcolor=color,
                padding=5,
                border_radius=5,
                margin=ft.Margin(left=0, top=0, right=5, bottom=0)
            )
        )
    return ft.Row(elementos_horarios, wrap=True)

def vista_ventas(page):
    print(f"🔍 Usuario actual en ventas: {modelo_estacion.usuario_actual}")  # Depuración

    # Validar si usuario_actual existe
    if not modelo_estacion.usuario_actual:
        print("⚠️ Error: usuario_actual es None, revisa la asignación después del login.")
        mostrar_mensaje(page, "Error: usuario no autenticado", tipo="error")
        page.go("/login")
        return
    
    # Ajuste: Revisar si usuario_actual ya es la estación directamente
    usuario_actual = modelo_estacion.usuario_actual
    
    if "nombre" in usuario_actual and "boletos_vendidos" in usuario_actual:
        estacion = usuario_actual  # Si tiene estos campos, ya es la estación
    else:
        estacion = usuario_actual.get("estacion", None)  # Si hay una estructura con "estacion", úsala

    # Validar si realmente tenemos una estación
    if estacion is None:
        print("⚠️ Error: No se encontró la estación para el usuario.")
        print(f"📌 Contenido de usuario_actual: {usuario_actual}")  # Depuración
        mostrar_mensaje(page, "Error: no tiene una estación asignada", tipo="error")
        page.go("/login")
        return

    # Validar que estacion realmente es un diccionario antes de intentar acceder a sus claves
    if not isinstance(estacion, dict):
        print("⚠️ Error: estacion no es un diccionario.")
        mostrar_mensaje(page, "Error: datos de estación incorrectos", tipo="error")
        page.go("/login")
        return

    boletos_vendidos = estacion.get("boletos_vendidos", 0)  # Evitar error si no existe la clave

    print(f"✅ Estación asignada: {estacion['nombre']} con {boletos_vendidos} boletos vendidos")  # Depuración


    def actualizar_hora_fecha():
        while True:
            texto_hora.value = datetime.now().strftime("%H:%M:%S")
            texto_fecha.value = datetime.now().strftime("%d/%m/%Y")
            page.update()
            time.sleep(1)


    texto_hora = ft.Text("00:00:00", size=48, weight=ft.FontWeight.BOLD)
    texto_fecha = ft.Text("00/00/0000", size=24)
    threading.Thread(target=actualizar_hora_fecha, daemon=True).start()
    
    sidebar = ft.Container(
    content=ft.Column(
        [
            ft.Text(estacion["nombre"], size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Row([ft.Text(f"Hola, {estacion['operador']}", size=18, color=ft.colors.WHITE)]),  # ❌ Eliminada lista dentro de ft.Text
            ft.Text("Estado: Activo", size=14, color=ft.colors.GREY_400),
            ft.Divider(color="#4511ED"),
            ft.Text("Horarios:", size=14, color=ft.colors.GREY_400),
            construir_horarios(estacion["horarios"]),  # ✅ Ahora accede como diccionario correctamente
            ft.Divider(color="#4511ED"),
            ft.ElevatedButton(
                "Generar PDF",
                icon=ft.icons.PICTURE_AS_PDF,
                bgcolor="#A7107F",
                color=ft.colors.WHITE,
                on_click=lambda e: mostrar_mensaje(page, "PDF generado", tipo="pdf")
            ),
            ft.ElevatedButton(
                "Gestionar Horarios",
                icon=ft.icons.SCHEDULE,
                bgcolor="#A7107F",
                color=ft.colors.WHITE,
                on_click=lambda e: page.go("/horarios")
            ),
            texto_boletos := ft.Text(f"Boletos vendidos: {boletos_vendidos}")
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    ),
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

    destino = ft.Dropdown(
        label="Destino",
        label_style=ft.TextStyle(color="#F4F9FA", size=20),
        filled=True,
        border_color="#F4F9FA",
        bgcolor="#574E55",
        elevation=8,               
        width=270,
        height=50,
        border_radius=7,
            options=[
        ft.dropdown.Option(e["nombre"]) for e in modelo_estacion.estaciones if e["nombre"] != estacion["nombre"]
    ]

    )

    horario = ft.Dropdown(
        label="Horario",
        label_style=ft.TextStyle(color="#F4F9FA", size=20),
        filled=True,
        border_color="#F4F9FA",
        bgcolor="#C95670",
        width=170,
        height=50,
        border_radius=7,
        options=[ft.dropdown.Option(h) for h in estacion["horarios"]]
    )
    

    dropdown_tren = ft.Dropdown(
        label="Tren",
        label_style=ft.TextStyle(color="#F4F9FA", size=20),
        filled=True,
        border_color="#F4F9FA",
        bgcolor="#C95670",
        width=100,
        height=50,
        border_radius=7,
        options=[ft.dropdown.Option(tren["nombre"]) for tren in estacion.get("trenes", [])]
    )

    capacidad_preview = ft.Text("80", size=15, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)


    def actualizar_capacidad(e):
        if dropdown_tren.value:
            selected_train = next((t for t in estacion.trenes if t.nombre == dropdown_tren.value), None)
            if selected_train:
                capacidad_preview.value = str(selected_train.capacidad_disponible())
        else:
            capacidad_preview.value = "N/A"
        page.update()

    dropdown_tren.on_change = actualizar_capacidad


    tren_column = ft.Column(
        controls=[dropdown_tren, capacidad_preview],
        spacing=5
    )


    cantidad_adultos = ft.TextField(
        label="Adultos",
        label_style=ft.TextStyle(color="#F4F9FA", size=20),
        text_style=ft.TextStyle(color=ft.colors.WHITE),
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=100,
        height=50,
        border_radius=7,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="0"
    )
    cantidad_niños = ft.TextField(
        label="Niños",
        label_style=ft.TextStyle(color="#F4F9FA", size=20),
        text_style=ft.TextStyle(color=ft.colors.WHITE),
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=100,
        height=50,
        border_radius=7,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="0"
    )
    cantidad_adultos_mayores = ft.TextField(
        label="Adultos Mayores",
        label_style=ft.TextStyle(color="#F4F9FA", size=20),
        text_style=ft.TextStyle(color=ft.colors.WHITE),
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=100,
        height=50,
        border_radius=7,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="0"
    )
    fila_precios = ft.Row(
        [
            ft.Column(
                [
                    cantidad_adultos,
                    ft.Text(f"${estacion.get('precio', 0):.2f}", size=15, weight=ft.FontWeight.BOLD)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(
                [
                    cantidad_niños,
                    ft.Text(f"${(estacion.get('precio', 0) * 0.5):.2f}", size=15, weight=ft.FontWeight.BOLD)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(
                [
                    cantidad_adultos_mayores,
                    ft.Text(f"${(estacion.get('precio', 0) * 0.4):.2f}", size=15, weight=ft.FontWeight.BOLD)

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(
                [
                    dropdown_tren,
                    capacidad_preview
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        spacing=20
    )

    encabezado = ft.Container(
        content=ft.Row(
            [ft.IconButton(ft.icons.LOGOUT, icon_color="#A7107F", on_click=lambda e: page.go("/login"))],
            alignment=ft.MainAxisAlignment.END
        ),
        alignment=ft.alignment.top_right,
        padding=ft.Padding(left=10, top=50, right=10, bottom=0)
    )

    total = ft.Text("Total: $0.00", size=20, weight=ft.FontWeight.BOLD)

    def calcular_total(e):
        try:
            num_adultos = float(cantidad_adultos.value) if cantidad_adultos.value else 0
            num_niños = float(cantidad_niños.value) if cantidad_niños.value else 0
            num_adultos_mayores = float(cantidad_adultos_mayores.value) if cantidad_adultos_mayores.value else 0
            total_valor = (num_adultos * estacion.precio) + \
                          (num_niños * estacion.precio * 0.5) + \
                          (num_adultos_mayores * estacion.precio * 0.4)
            total.value = f"Total: ${total_valor:.2f}"
            page.update()
        except Exception as ex:
            print(ex)

    cantidad_adultos.on_change = calcular_total
    cantidad_niños.on_change = calcular_total
    cantidad_adultos_mayores.on_change = calcular_total

    reloj_container = ft.Container(
        content=ft.Column(
            [
                texto_hora,
                texto_fecha
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=30,
        margin=ft.Margin(top=0, left=0, right=0, bottom=0),
        width=800,
        height=155,
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


    contenido_ventas = ft.Column(
        [
            ft.Text("Venta de Boletos", size=24),
            ft.Row([destino, horario, ], spacing=20),
            fila_precios,
            total,
            ft.ElevatedButton(
                "Generar Boleto",
                icon=ft.icons.CONFIRMATION_NUM_OUTLINED,
                bgcolor="#A7107F",
                color=ft.colors.WHITE,
                on_click=lambda e: vender_boleto()
            )
        ],
        spacing=20,
        expand=True
    )

    contenido_ventas = ft.Container(
        content=contenido_ventas,
        padding=30,
        margin=ft.Margin(top=0, left=0, right=0, bottom=0),  
        width=800,
        height=400,
        border_radius=16,
        alignment=ft.alignment.top_center,
        blur=ft.Blur(sigma_x=15, sigma_y=15),
        border=ft.Border(
            left=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            top=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            right=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            bottom=ft.BorderSide(color=ft.colors.WHITE12, width=1.5)
        )
    )

    def vender_boleto():
        nonlocal boletos_vendidos
        try:
            if not all([destino.value, horario.value, dropdown_tren.value]) or (
                cantidad_adultos.value == "" and
                cantidad_niños.value == "" and
                cantidad_adultos_mayores.value == ""
            ):
                raise Exception("Complete todos los campos")

            selected_train = next((t for t in estacion.trenes if t.nombre == dropdown_tren.value), None)
            if selected_train is None:
                raise Exception("Seleccione un tren válido")

            num_adultos = int(cantidad_adultos.value) if cantidad_adultos.value else 0
            num_niños = int(cantidad_niños.value) if cantidad_niños.value else 0
            num_adultos_mayores = int(cantidad_adultos_mayores.value) if cantidad_adultos_mayores.value else 0

            total_boletos = num_adultos + num_niños + num_adultos_mayores
            if total_boletos == 0:
                raise Exception("La cantidad de boletos no puede ser 0")

            if total_boletos > selected_train.capacidad_disponible():
                raise Exception("Capacidad insuficiente en el tren seleccionado")

            # Registrar la venta en el tren
            selected_train.vender_boletos(total_boletos)
            boletos_vendidos += total_boletos
            texto_boletos.value = f"Boletos vendidos: {boletos_vendidos}"
            texto_boletos.color = ft.colors.RED

            estacion.ventas.append({
                'destino': destino.value,
                'horario': horario.value,
                'tren': selected_train.nombre,
                'adultos': num_adultos,
                'niños': num_niños,
                'adultos_mayores': num_adultos_mayores,
                'total_boletos': total_boletos
            })

            # Limpiar los campos
            destino.value = ""
            horario.value = ""
            dropdown_tren.value = ""
            cantidad_adultos.value = "0"
            cantidad_niños.value = "0"
            cantidad_adultos_mayores.value = "0"
            total.value = "Total: $0.00"

            # Actualizar capacidad
            actualizar_capacidad(None)

            # Mostrar mensaje de éxito
            mostrar_mensaje(page, f"{total_boletos} boleto(s) vendido(s) en {selected_train.nombre}!", tipo="success")
            page.update()

        except Exception as ex:
            mostrar_mensaje(page, f"Error: {str(ex)}", tipo="error")
            
    return ft.View(
        "/ventas",
        [
            ft.Container(
                padding=30,  
                content=ft.Row(
                    [
                        sidebar,
                        ft.VerticalDivider(),
                        ft.Column(
                            [
                                contenido_ventas,
                                reloj_container
                            ],
                            spacing=20,
                            expand=True
                        ),
                        ft.VerticalDivider(),
                        encabezado
                    ],
                    expand=True
                ),
                expand=True,
                alignment=ft.alignment.center,
                image_src="https://iili.io/3ncZ0gI.png",
                image_fit=ft.ImageFit.COVER,
                border_radius=16,
            )
        ]
    )
