# GUIA_OPERACION

Tipo de archivo: runbook operativo (Markdown)
Objetivo: guiar la operacion diaria y validaciones funcionales.

## Secuencia recomendada de pruebas

1. Levantar servidor web (`py -3 app.py`).
2. Abrir `http://127.0.0.1:5000/dashboard`.
3. Ejecutar simulador (`py -3 simulator.py`).
4. Confirmar llegada de datos y alertas en dashboard.

## Validaciones de salud

- Endpoint `/ingest` retorna `201` en envios correctos.
- `/api/data` entrega arrays no vacios tras simulacion.
- Tabla `lecturas` incrementa registros.
- Tabla `alarmas` crece cuando hay temperatura > 25.0.

## Operacion de GUI

- Iniciar monitoreo desde boton principal.
- Verificar refresco cada 30 segundos.
- Usar botones de intervalo para graficos historicos.

## Modo remoto del simulador

`simulator.py` viene configurado por defecto contra URL Vercel. Si se quiere entorno local, ajustar `API_URL` al host local.
