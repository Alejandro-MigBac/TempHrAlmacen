# SECURITY

Tipo de archivo: politica de seguridad (Markdown)
Objetivo: definir pautas para reporte responsable y manejo seguro del proyecto.

## Reporte responsable

Reporta vulnerabilidades de forma privada al mantenedor incluyendo:

- Descripcion del hallazgo.
- Pasos de reproduccion.
- Impacto potencial.
- Mitigacion sugerida (si existe).

No publiques detalles tecnicos sensibles antes de corregir.

## Buenas practicas

- No subir secretos (`SUPABASE_KEY`, tokens, credenciales).
- Limitar exposicion de servicios locales.
- Revisar dependencias periodicamente.
- Documentar cambios de seguridad en `CHANGELOG.md`.
