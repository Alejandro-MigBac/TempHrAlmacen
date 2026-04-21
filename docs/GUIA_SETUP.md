# GUIA_SETUP

Tipo de archivo: guia operativa de instalacion (Markdown)
Objetivo: dejar el proyecto listo para ejecucion local.

## Requisitos

- Windows + PowerShell.
- Python 3.11+ (validado con `py -3`).
- Acceso a internet para instalar dependencias.

## Instalacion

1. Crear entorno virtual:
   ```bash
   py -3 -m venv .venv
   ```
2. Activar entorno:
   ```bash
   .\\.venv\\Scripts\\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Variables opcionales (modo nube)

Para activar Supabase en `ConfigDB`:

- `SUPABASE_URL`
- `SUPABASE_KEY`

Si no existen, el sistema usa SQLite local en `application/repositories/sqlite.db`.

## Arranque por componente

- API y dashboard web:
  ```bash
  py -3 app.py
  ```
- Simulador de envio de lecturas:
  ```bash
  py -3 simulator.py
  ```
- GUI escritorio:
  ```bash
  py -3 main.py
  ```
