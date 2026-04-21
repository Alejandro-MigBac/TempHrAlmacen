# ESTADO_ACTUAL

Tipo de archivo: informe tecnico de estado (Markdown)
Objetivo: dejar trazados hallazgos del estado actual del repo tras la actualizacion.

## Hallazgos relevantes

1. La estructura principal usa paquete `application/`.
2. Existen imports heredados con prefijo `app` dentro de:
   - `application/controller/controlador_ppal.py`
   - `application/view/ventana_ppal.py`
3. Existe `app.py` en raiz; esto puede colisionar semanticamente con imports `app.*`.
4. `simulator.py` apunta por defecto a endpoint remoto en Vercel.
5. `ConfigDB` soporta dos backends: SQLite local y Supabase por variables de entorno.

## Impacto documental

La documentacion de este repo ya contempla estos puntos en:

- `docs/GUIA_SETUP.md`
- `docs/GUIA_ARQUITECTURA.md`
- `docs/GUIA_OPERACION.md`
- `docs/GUIA_TROUBLESHOOTING.md`
