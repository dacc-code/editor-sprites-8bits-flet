import flet as ft

# Colores según guía
COLOR_APAGADO = "#1e293b"  # azul noche / gris oscuro
COLOR_APAGADO_BORDER = "#334155"
COLOR_ENCENDIDO = "#22c55e"  # verde neón
# Alternative: "#eab308" amarillo, "#38bdf8" azul
COLOR_BG = "#0f172a"
COLOR_CARD = "#1e293b"

def main(page: ft.Page):
    page.title = "Editor de Sprites 8x8 - CUL | Electrónica Digital"
    page.bgcolor = COLOR_BG
    page.theme_mode = ft.ThemeMode.DARK
    # Ventana y scroll - fijado para 8x8 completo sin recorte
    try:
        page.window.width = 1000
        page.window.height = 900
        page.window.min_width = 900
        page.window.min_height = 800
        page.window.resizable = True
    except:
        try:
            page.window_width = 1000
            page.window_height = 900
        except:
            pass
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.START

    # Estado interno: 64 bits (False=apagado, True=encendido)
    # Fila-major order: index = fila*8 + columna
    estado = [False] * 64
    botones = []  # lista de refs a los botones/containers

    # --- Componentes de UI que se actualizarán ---
    hex_input = ft.TextField(
        label="Código Hexadecimal (16 caracteres)",
        hint_text="Ej: 00FF00FF00FF00FF",
        max_length=16,
        width=340,
        border_radius=8,
        bgcolor="#0f172a",
        border_color="#334155",
        text_size=14,
        capitalization=ft.TextCapitalization.CHARACTERS,
    )

    hex_output = ft.Text(
        value="0000000000000000",
        size=22,
        weight=ft.FontWeight.BOLD,
        color="#38bdf8",
        font_family="Consolas",
        selectable=True,
    )

    mensaje = ft.Text("", size=12, color="#94a3b8")

    # --- Funciones de conversión ---

    def bin_to_hex(bin_str: str) -> str:
        """Convierte cadena binaria 64 bits a hex 16 chars mayúsculas, padded"""
        # Manual: dividir en grupos de 4 bits, mapear
        # Pero usamos int->hex para simplicidad y luego formatear, equivalante a división sucesiva
        if len(bin_str) != 64:
            raise ValueError("Binario debe tener 64 caracteres")
        # Validar
        for c in bin_str:
            if c not in "01":
                raise ValueError("Binario inválido")
        valor = 0
        for c in bin_str:
            valor = (valor << 1) | (1 if c == "1" else 0)
        hex_str = format(valor, '016X')  # 16 chars, mayúsculas, padded con ceros
        return hex_str

    def hex_to_bin(hex_str: str) -> str:
        """Convierte hex 1-16 chars a binario 64 chars padded"""
        hex_str = hex_str.strip().upper()
        if not hex_str:
            raise ValueError("Ingrese código hexadecimal")
        if len(hex_str) > 16:
            raise ValueError("Máximo 16 caracteres hexadecimales")
        for c in hex_str:
            if c not in "0123456789ABCDEF":
                raise ValueError(f"Carácter inválido '{c}' - solo 0-9 y A-F")
        # Conversión manual: cada hex -> 4 bits
        bin_str = ""
        for c in hex_str:
            val = int(c, 16)
            bin_str += format(val, '04b')
        # Pad a 64
        bin_str = bin_str.zfill(64)
        if len(bin_str) > 64:
            # Si hex era >16 ya habría error, pero por seguridad
            bin_str = bin_str[-64:]
        return bin_str

    def actualizar_hex_output():
        """Fase 3: Lee matriz -> binario 64 -> hex 16"""
        # Lectura secuencial fila por fila (ya en orden)
        bin_str = ""
        for i in range(64):
            bin_str += "1" if estado[i] else "0"
        hex_str = bin_to_hex(bin_str)
        hex_output.value = hex_str
        hex_output.update()

    def actualizar_matriz_desde_hex(hex_str: str):
        """Fase 4: Hex -> binario 64 -> renderiza en botones"""
        bin_str = hex_to_bin(hex_str)
        for i in range(64):
            estado[i] = (bin_str[i] == "1")
            # Actualizar visual
            btn = botones[i]
            # btn es Container con on_click
            is_on = estado[i]
            btn.bgcolor = COLOR_ENCENDIDO if is_on else COLOR_APAGADO
            btn.border = ft.Border.all(1, COLOR_ENCENDIDO if is_on else COLOR_APAGADO_BORDER)
            # Añadir brillo si encendido
            btn.shadow = ft.BoxShadow(blur_radius=8, spread_radius=1, color="#22c55e55") if is_on else None
        # Refrescar
        grid.update()
        hex_output.value = bin_to_hex(bin_str)  # normalizado
        hex_output.update()

    # --- Handlers ---

    def on_pixel_click(e):
        idx = e.control.data  # índice 0-63
        # Toggle estado
        estado[idx] = not estado[idx]
        is_on = estado[idx]
        e.control.bgcolor = COLOR_ENCENDIDO if is_on else COLOR_APAGADO
        e.control.border = ft.Border.all(1, COLOR_ENCENDIDO if is_on else COLOR_APAGADO_BORDER)
        e.control.shadow = ft.BoxShadow(blur_radius=8, spread_radius=1, color="#22c55e55") if is_on else None
        grid.update()
        # Fase 3: Dirección 1 - Pantalla -> Hex
        try:
            actualizar_hex_output()
            mensaje.value = f"Pixel {idx//8},{idx%8} -> {'ENCENDIDO' if is_on else 'APAGADO'} | Binario actualizado"
            mensaje.color = "#86efac"
        except Exception as ex:
            mensaje.value = str(ex)
            mensaje.color = "#f87171"
        mensaje.update()

    def on_cargar_hex(e):
        hex_str = hex_input.value or ""
        hex_str = hex_str.strip().upper()
        # Validación
        if not hex_str:
            mensaje.value = "Ingrese un código hexadecimal"
            mensaje.color = "#f87171"
            mensaje.update()
            return
        if len(hex_str) > 16:
            mensaje.value = "Error: máximo 16 caracteres (64 bits)"
            mensaje.color = "#f87171"
            mensaje.update()
            return
        for c in hex_str:
            if c not in "0123456789ABCDEF":
                mensaje.value = f"Error: carácter inválido '{c}' - solo 0-9 A-F"
                mensaje.color = "#f87171"
                mensaje.update()
                return
        # Pad visual
        hex_str_padded = hex_str.zfill(16).upper()
        try:
            actualizar_matriz_desde_hex(hex_str_padded)
            mensaje.value = f"Cargado: {hex_str_padded} -> matriz actualizada"
            mensaje.color = "#86efac"
            hex_input.value = hex_str_padded
            hex_input.update()
            mensaje.update()
        except Exception as ex:
            mensaje.value = str(ex)
            mensaje.color = "#f87171"
            mensaje.update()

    def on_limpiar(e):
        for i in range(64):
            estado[i] = False
            btn = botones[i]
            btn.bgcolor = COLOR_APAGADO
            btn.border = ft.Border.all(1, COLOR_APAGADO_BORDER)
            btn.shadow = None
        grid.update()
        actualizar_hex_output()
        mensaje.value = "Matriz limpiada (64 bits en 0)"
        mensaje.color = "#94a3b8"
        mensaje.update()

    def on_invertir(e):
        for i in range(64):
            estado[i] = not estado[i]
            btn = botones[i]
            is_on = estado[i]
            btn.bgcolor = COLOR_ENCENDIDO if is_on else COLOR_APAGADO
            btn.border = ft.Border.all(1, COLOR_ENCENDIDO if is_on else COLOR_APAGADO_BORDER)
            btn.shadow = ft.BoxShadow(blur_radius=8, spread_radius=1, color="#22c55e55") if is_on else None
        grid.update()
        actualizar_hex_output()
        mensaje.value = "Matriz invertida"
        mensaje.color = "#86efac"
        mensaje.update()

    def on_llenar(e):
        for i in range(64):
            estado[i] = True
            btn = botones[i]
            btn.bgcolor = COLOR_ENCENDIDO
            btn.border = ft.Border.all(1, COLOR_ENCENDIDO)
            btn.shadow = ft.BoxShadow(blur_radius=8, spread_radius=1, color="#22c55e55")
        grid.update()
        actualizar_hex_output()
        mensaje.value = "Matriz llena (FFFF FFFF FFFF FFFF)"
        mensaje.color = "#86efac"
        mensaje.update()

    # --- Construcción de la cuadrícula 8x8 (Fase 1: Framebuffer) ---
    # Bucle anidado for filas y for columnas como exige la guía
    grid_controls = []
    for fila in range(8):
        for col in range(8):
            idx = fila * 8 + col
            # Container actúa como pixel
            pixel = ft.Container(
                width=50,
                height=50,
                bgcolor=COLOR_APAGADO,
                border=ft.Border.all(1, COLOR_APAGADO_BORDER),
                border_radius=6,
                alignment=ft.Alignment.CENTER,
                data=idx,  # guardar índice para el handler
                on_click=on_pixel_click,
                ink=True,
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            )
            botones.append(pixel)
            grid_controls.append(pixel)

    # --- Grid 8x8 garantizado con Rows/Columns (más fiable que GridView) ---
    # GridView cumple la guía pero Rows garantiza 8x8 exacto sin recorte
    # Usamos Column con 8 Rows, cada Row con 8 Containers (bucle anidado exigido)
    rows = []
    for fila in range(8):
        row_controls = []
        for col in range(8):
            idx = fila*8+col
            row_controls.append(botones[idx])
        rows.append(ft.Row(controls=row_controls, spacing=4, alignment=ft.MainAxisAlignment.CENTER, tight=True))
    grid = ft.Column(controls=rows, spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

    # --- Panel de control (Fase 2) ---
    panel_hex = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Panel de Control - Hex Editor", size=14, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text("Cada pixel = 1 bit. 8x8 = 64 bits = 16 hex. Clickeá los píxeles o carga un código.", size=11, color="#94a3b8"),
                ft.Divider(height=1, color="#334155"),
                ft.Row(
                    controls=[
                        hex_input,
                        ft.ElevatedButton(
                            content="Cargar Hex",
                            icon=ft.Icons.DOWNLOAD,
                            bgcolor="#38bdf8",
                            color="white",
                            height=42,
                            on_click=on_cargar_hex,
                        ),
                    ],
                    spacing=12,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Valor actual:", size=12, color="#94a3b8"),
                        hex_output,
                        ft.IconButton(icon=ft.Icons.COPY, icon_size=16, tooltip="Copiar", on_click=lambda e: page.set_clipboard(hex_output.value)),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                mensaje,
                ft.Row(
                    controls=[
                        ft.FilledButton("Limpiar", icon=ft.Icons.CLEAR, bgcolor="#334155", color="white", on_click=on_limpiar),
                        ft.FilledButton("Invertir", icon=ft.Icons.INVERT_COLORS, bgcolor="#475569", color="white", on_click=on_invertir),
                        ft.FilledButton("Llenar", icon=ft.Icons.GRID_ON, bgcolor="#22c55e", color="white", on_click=on_llenar),
                    ],
                    spacing=8,
                ),
            ],
            spacing=10,
        ),
        bgcolor=COLOR_CARD,
        padding=16,
        border_radius=12,
        border=ft.Border.all(1, "#334155"),
        width=520,
    )

    # --- Layout principal ---
    titulo = ft.Column(
        controls=[
            ft.Text("EDITOR DE SPRITES 8-BITS", size=24, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
            ft.Text("Electrónica Digital · CUL · Sistemas de Numeración Binario ↔ Hexadecimal · 64 bits", size=11, color="#94a3b8", text_align=ft.TextAlign.CENTER),
        ],
        spacing=2,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Contenedor framebuffer con borde - tamaño fijo para 8x8
    frame = ft.Container(
        content=grid,
        bgcolor="#0f172a",
        padding=14,
        border_radius=12,
        border=ft.Border.all(2, "#334155"),
        shadow=ft.BoxShadow(blur_radius=20, color="#00000066"),
        alignment=ft.Alignment.CENTER,
        width=520,
    )

    # Info de ayuda
    ayuda = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Cómo usar:", weight=ft.FontWeight.BOLD, size=12, color="white"),
                ft.Text("• Click en un pixel: alterna APAGADO (gris) ↔ ENCENDIDO (verde neón) y actualiza el hex automáticamente (Dirección 1).", size=11, color="#cbd5e1"),
                ft.Text("• Escribe hex (0-9, A-F, max 16) y presiona 'Cargar Hex': la matriz se pinta según los bits (Dirección 2).", size=11, color="#cbd5e1"),
                ft.Text("• Ejemplo: 00FF00FF00FF00FF = patrón de rayas. FFFFFFFFFFFFFFFF = todo encendido. 0000000000000000 = todo apagado.", size=11, color="#94a3b8"),
            ],
            spacing=4,
        ),
        bgcolor="#1e293b",
        padding=12,
        border_radius=8,
        width=520,
    )

    page.add(
        ft.Column(
            controls=[
                titulo,
                ft.Divider(height=10, color="transparent"),
                frame,
                panel_hex,
                ayuda,
                ft.Text("CUL · Ingeniería de Sistemas · Python + Flet · 8×8=64 bits = 16 hex · page.update() tras cada cambio", size=9, color="#64748b", text_align=ft.TextAlign.CENTER),
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )
    )

    # Inicializar salida
    actualizar_hex_output()

if __name__ == "__main__":
    ft.app(target=main)
