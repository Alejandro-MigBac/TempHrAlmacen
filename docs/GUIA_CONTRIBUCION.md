# GUIA_CONTRIBUCION

Tipo de archivo: guia de colaboracion (Markdown)
Objetivo: homogeneizar la forma de contribuir al proyecto.

## Principios

- Mantener separacion por capas (`models`, `repositories`, `services`, `controller`, `view`).
- Evitar mezclar cambios funcionales y de formato en el mismo commit.
- Actualizar documentacion cuando cambie estructura, contratos o despliegue.

## Flujo sugerido

1. Crear rama de trabajo.
2. Implementar cambios pequenos y revisables.
3. Ejecutar validaciones manuales minimas.
4. Actualizar `CHANGELOG.md`.
5. Abrir PR con alcance, riesgos y pruebas realizadas.

## Checklist minimo

- [ ] README y docs actualizados si aplica.
- [ ] Endpoints principales verificados (`/ingest`, `/api/data`, `/dashboard`).
- [ ] Sin secretos en codigo ni en commits.
- [ ] Riesgos conocidos documentados en `docs/ESTADO_ACTUAL.md`.
