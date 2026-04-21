# GUIA_API

Tipo de archivo: especificacion de API HTTP (Markdown)
Objetivo: documentar contratos para clientes y pruebas manuales.

Base URL local: `http://127.0.0.1:5000`

## POST `/ingest`

Inserta una lectura y genera alarma si temperatura > 25.0.

Body JSON:

```json
{
  "temperatura": 24.5,
  "humedad": 51.2
}
```

Respuestas:

- `201` -> `{"status":"success"}`
- `400` -> error por parametros faltantes
- `500` -> error interno

## GET `/dashboard`

Devuelve dashboard web con Plotly.js y refresco periodico.

## GET `/api/data`

Devuelve JSON con serie de 24h, estadisticas y alertas.

Campos esperados:

- `timestamp[]`
- `temperatura[]`
- `humedad[]`
- `stats` (`max_t`, `min_t`, `max_h`, `min_h`)
- `alerts[]`

## GET `/api/static?window=<valor>`

Vista estatica por ventana temporal.

Valores validos:

- `5m`
- `1h`
- `24h`
- `1w`
