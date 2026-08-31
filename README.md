# Editor de Sprites 8-BITS con Flet — CUL Electrónica Digital

**Repo:** https://github.com/dacc-code/editor-sprites-8bits-flet — `git clone https://github.com/dacc-code/editor-sprites-8bits-flet.git`

Proyecto académico: Editor de Sprites de 8×8 píxeles (64 bits) con Flet. Aplica sistemas de numeración Binario ↔ Hexadecimal con flujos de 64 bits sin pérdida de precisión.

**Guía:** `Practica 2 Digital.pdf` (3 páginas) — Fases 1 a 4.

## 🚀 Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# o: flet run app.py
```

Se abre ventana desktop 950×720, tema oscuro, 8×8 framebuffer.

## 🧩 Fases Implementadas

**Fase 1 — Arquitectura UI con Flet:**
- `ft.app` con título, tamaño fijo y `theme_mode = ft.ThemeMode.DARK`
- Framebuffer: bucle anidado `for fila in range(8): for col in range(8):` → `ft.GridView(runs_count=8, max_extent=58)` dinámico 64 elementos
- Estados de color: APAGADO `#1e293b` (gris oscuro/azul noche) / ENCENDIDO `#22c55e` (verde neón) con sombra y `page.update()`

**Fase 2 — Panel de Control y Eventos:**
- `ft.Column`/`ft.Row`, `ft.TextField` (hex input), `ft.ElevatedButton` ("Cargar Hex"), `ft.Text` dinámico con valor hex actual
- `on_click` en cada pixel: toggle color, conmutación, `page.update()` para refrescar

**Fase 3 — Dirección 1 (Pantalla → Hex):**
- Lectura secuencial 64 elementos → cadena binaria exactamente 64 caracteres (1=ENCENDIDO, 0=APAGADO)
- Conversión binario → hex con `format(valor,'016X')` → salida 16 chars mayúsculas, padded con ceros a la izquierda

**Fase 4 — Dirección 2 (Hex → Pantalla):**
- Captura `ft.TextField`, validación: max 16 chars, solo 0-9 A-F
- Expansión: hex → binario `zfill(64)` exactamente 64 caracteres
- Renderizado visual: recorre 64 bits en paralelo con 64 botones, cambia color según bit, `page.update()` al final

## 🧮 Lógica

- Binario massivo 64 bits nativo sin pérdida (int + bit shift)
- Inyección/extracción bidireccional entre estados lógicos y componentes visuales
- Grid/Rows/Columns dinámicos

## 📦 Entregable

Incluye `app.py`, `requirements.txt`. Compatible Python 3.x + Flet.

## 🔗 Proyectos relacionados

- Calculadora conversiones (Flask): https://github.com/dacc-code/calculadora-conversiones-cul
- Demo estática: https://dacc-code.github.io/calculadora-conversiones-cul/
