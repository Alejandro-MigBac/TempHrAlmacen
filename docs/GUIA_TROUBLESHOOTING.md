# GUIA_TROUBLESHOOTING

Tipo de archivo: guia de resolucion de incidencias (Markdown)
Objetivo: resolver errores frecuentes de ejecucion e integracion.

## Error de dependencias (`ModuleNotFoundError`)

Sintoma:

- Falla al ejecutar `app.py` o `main.py` por paquetes faltantes.

Accion:

- Activar venv e instalar `requirements.txt`.

## Error de imports `app` vs `application`

Sintoma:

- Al abrir GUI, aparecen errores relacionados con `from app...`.

Causa:

- Parte del codigo fue movido a `application/`, pero algunos imports conservan prefijo `app`.

Accion:

- Revisar `application/controller/controlador_ppal.py` y `application/view/ventana_ppal.py`.
- Alinear imports al namespace real (`application...`) en una tarea de refactor.

## Simulador no envia a entorno local

Sintoma:

- `simulator.py` no impacta al servidor local.

Causa:

- `API_URL` esta apuntando por defecto a Vercel.

Accion:

- Cambiar `API_URL` a `http://127.0.0.1:5000/ingest` para pruebas locales.

## Dashboard sin datos

Sintoma:

- `/dashboard` carga, pero no dibuja curvas.

Accion:

- Confirmar que hay lecturas insertadas.
- Probar `/api/data` directamente.
- Ejecutar simulador para poblar datos.
