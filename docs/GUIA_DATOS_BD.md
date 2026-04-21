# GUIA_DATOS_BD

Tipo de archivo: documento de modelo de datos (Markdown)
Objetivo: describir entidades persistidas y consultas de diagnostico.

## Backend de datos

- Local: SQLite (`application/repositories/sqlite.db`).
- Nube: Supabase (tabla `lecturas` y `alarmas`).

## Tabla `lecturas`

- `id` (PK)
- `temperatura` (REAL)
- `humedad` (REAL)
- `fecha` (TEXT)
- `hora` (TEXT)
- `id_almacen` (INTEGER)

## Tabla `alarmas`

- `id` (PK)
- `fecha` (TEXT)
- `hora` (TEXT)
- `valor_alarma` (REAL)
- `almacen` (INTEGER)

## Consultas SQL utiles (SQLite)

Ultimas lecturas:

```sql
SELECT * FROM lecturas ORDER BY fecha DESC, hora DESC LIMIT 20;
```

Ultimas alarmas:

```sql
SELECT * FROM alarmas ORDER BY fecha DESC, hora DESC LIMIT 20;
```

Conteo diario de alarmas:

```sql
SELECT fecha, COUNT(*) AS total
FROM alarmas
GROUP BY fecha
ORDER BY fecha DESC;
```
