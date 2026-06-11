# Impacto técnico — Informes LaTeX + Markdown

> Sección obligatoria en todo spec de este perfil. Copiar al crear `SDD-NNN` o referenciar desde la plantilla de la instancia.
> Contexto de negocio: `.github/docs/business/domain-rules.md`.

## Impacto técnico _(obligatorio)_

Responder cada ítem. Si no aplica: "No aplica — [razón]".

| Pregunta                                                                             | Respuesta |
| ------------------------------------------------------------------------------------ | --------- |
| ¿Cuál es la **audiencia** y el **propósito** del entregable?                         |           |
| ¿Qué **formato(s) de salida**? (PDF, DOCX, `.tex`, HTML)                             |           |
| ¿Qué archivos de **contenido** se crean o modifican? (`content/`, rutas)             |           |
| ¿Qué **fuentes de datos** se usan? (CSV, APIs, entrevistas, docs en `data/sources/`) |           |
| ¿Requiere **transcripción** previa? Listar archivos en `data/sources/`               |           |
| ¿Incluye **análisis de datos** con scripts? Listar `scripts/` y salidas esperadas    |           |
| ¿Incluye **visualizaciones** (figuras, tablas)? ¿Generadas por script o estáticas?   |           |
| ¿Afecta **plantilla** Pandoc/LaTeX o estructura global del informe? → posible ADR    |           |
| ¿Requiere **bibliografía** nueva o cambios en `.bib`?                                |           |
| ¿Afecta reglas en `business/domain-rules.md`? Si sí, listar cuáles.                  |           |
| ¿Introduce decisión metodológica o de estructura **transversal**? Si sí → ADR.       |           |

## Reglas de este perfil

- Fuente canónica preferida: **Markdown** en `content/`; LaTeX directo solo si el proyecto lo exige.
- Transcripciones en `data/transcripts/` — no editar fuentes binarias en el repo sin copia en `data/sources/`.
- Scripts solo como apoyo; el entregable del spec es el **documento**, no el script.
- Toda cifra en el informe debe ser trazable a fuente o script versionado en el repo.
