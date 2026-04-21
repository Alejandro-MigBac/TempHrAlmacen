# GUIA_ARQUITECTURA

Tipo de archivo: documento tecnico de arquitectura (Markdown)
Objetivo: describir estructura, capas y flujo de datos real del repositorio.

## Capas

- `application/models`: entidades de dominio (`almacen`, `alarma`).
- `application/repositories`: acceso a datos (`ConfigDB`) con backend SQLite/Supabase.
- `application/services`: generacion de graficos y utilidades de negocio.
- `application/controller`: orquestacion MVC de la GUI.
- `application/view`: interfaz Tkinter y componentes.

## Entradas del sistema

- `main.py`: arranque de la GUI escritorio.
- `app.py`: servidor Flask con endpoints y dashboard HTML.
- `simulator.py`: emisor periodico de lecturas por HTTP.

## Flujo funcional

1. Se genera una lectura (GUI o simulador).
2. `ConfigDB.insertar_lectura` persiste en SQLite o Supabase.
3. Si `temperatura > 25.0`, se registra alarma.
4. Dashboard (`/api/data`) y GUI consultan lecturas para mostrar estado.

## Persistencia

- Modo local: SQLite en `application/repositories/sqlite.db`.
- Modo nube: Supabase cuando hay credenciales de entorno.

## Riesgo tecnico observado

Hay referencias de imports `from app...` dentro de `application/` pese al cambio de estructura a `application/...`. Esto se detalla en `docs/ESTADO_ACTUAL.md`.
