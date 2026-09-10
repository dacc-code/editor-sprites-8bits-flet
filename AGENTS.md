# AGENTS.md — Instrucciones para agentes de IA (editor-sprites-8bits-flet)

> Leer antes de modificar. Rama obligatoria: nunca commitear directo a `main`.

## Descripción

Editor de sprites 8×8 (64 bits) para la materia Electrónica Digital (CUL). Doble superficie: app desktop con Flet (`app.py`, 368 líneas) + demo web estática (`index.html`, GitHub Pages). Convierte framebuffer ↔ hexadecimal de 16 chars (`format(valor,'016X')`, `zfill(64)`).

## Arquitectura

- `app.py::main(page)`: Flet `DARK`, ventana 1000×900 scroll AUTO, `estado=[False]*64` (row-major), grid 8×8 (Column+Rows), `hex_input`/`hex_output`, `page.update()`.
- Dirección 1 (pantalla→hex): 64 toggles → binario 64 chars → hex 16 chars.
- Dirección 2 (hex→pantalla): valida `[0-9A-F]{1,16}` → `zfill(64)` → pinta 64 botones.
- `index.html`: mirror estático para Pages (grid 8×8 + hex 64 bits, sin pago).
- `docs/index.html`: copia publicada en Pages (verificar antes de tocar).

## Comandos

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # flet>=0.26.0 (sin pin)
python app.py                     # desktop 1000×900 según código
flet run app.py                   # alternativo
```

Sin linter, tests ni CI configurados.

## Estructura

```text
├── app.py             # app Flet (único módulo, 368 líneas)
├── index.html         # demo web estática (185 líneas)
├── docs/index.html    # publicado en GitHub Pages
├── requirements.txt   # flet>=0.26.0
├── README.md          # docs (demo vivo + fases 1-4)
├── LICENSE            # MIT
└── AGENTS.md          # este archivo
```

## Convenciones

- Python sin type hints estrictos; colores como constantes (`COLOR_APAGADO` etc.).
- Commits imperativos (`feat:`, `fix:`, `docs:`).
- No inventar demo URLs, guías PDF ni features: lo no verificado va como `TODO`.
- `Practica 2 Digital.pdf` referenciado en README no está en el repo — no afirmar su contenido.

## Reglas de modificación

1. Rama `feat/*`, `fix/*`, `docs/*`, `chore/*`. Jamás a `main`.
2. `git status` + `git branch --show-current` antes de editar.
3. Cambios mínimos; no partir `app.py` en módulos sin aprobación.
4. No tocar `requirements.txt` (pin de versión) sin probar `python app.py`.
5. Si cambia UI/flujo hex, actualizar README + `index.html` + `docs/index.html` en el mismo PR.
6. Sin secretos: no hay backend ni credenciales; no introducir ninguno.

## Testing / Lint / Build

- Sin suite. Verificación mínima: `python app.py` abre ventana + toggle pixel actualiza hex; cargar `00FF00FF00FF00FF` pinta patrón.
- TODO: tests de conversión pura (extraer función bin↔hex). CI: `.github/workflows/ci.yml` (pip install + py_compile + import-check).
- No instalar toolchains pesados (equipo limitado, `/` al 87% el 2026-09-10).

## Deployment

GitHub Pages sirve `docs/` (demo vivo en README). No cambiar rama/carpeta de Pages sin aprobación.

## Variables de entorno

Ninguna (`.env` ya ignorado).

## IA (OpenCode implementa, Codex revisa)

- OpenCode: plan antes de implementar, solo en rama actual.
- Codex: clasificar CRITICAL/HIGH/MEDIUM/LOW/SUGGESTION. Bloquean merge: secretos, `except:` silenciosos que oculten fallos de ventana, validación hex rota, docs falsas, dependencia sin pin añadida sin nota.
