# Extensiones de workflow — Informes (perfil `reports-latex-md`)

> Complementa [`../../core/workflow.md`](../../core/workflow.md). El ciclo base SDD se mantiene; este perfil **renombra y extiende** etapas para documentos.

## Ciclo adaptado

```
Discovery → Transcription → Draft → Ready → In Progress → In Review → Released
```

| Etapa SDD core | Etapa en este perfil | Artefacto                                | Criterio de salida                                 |
| -------------- | -------------------- | ---------------------------------------- | -------------------------------------------------- |
| Discovery      | **Discovery**        | Nota en BACKLOG                          | Pregunta/objetivo definido, fuentes identificadas  |
| _(opcional)_   | **Transcription**    | `.md` en `data/transcripts/`             | Fuentes no legibles convertidas a Markdown         |
| Draft          | **Draft**            | `specs/<dominio>/SDD-NNN-slug.md`        | DoR cumplida (estructura, metodología, fuentes)    |
| Ready          | **Ready**            | Spec `Estado: Ready`                     | Humano aprueba enfoque y outline                   |
| In Build       | **In Progress**      | Rama + `content/*.md` / `.tex` + scripts | Manuscrito compila; scripts de análisis ejecutan   |
| Validating     | **In Review**        | PR + checklist del perfil                | Contenido, cifras, citas y compilación verificados |
| Released       | **Released**         | Spec archivado + PDF/DOCX en `output/`   | Entregable publicado y versionado                  |

**Mapeo de estados en cabecera del spec:** usar los estados del core (`Draft`, `Ready`, `In Build`, `Validating`, `Released`). En comunicación con el humano se puede decir "In Progress" / "In Review" como alias.

## Cuándo usar Transcription

| Situación                                                   | Acción                                                         |
| ----------------------------------------------------------- | -------------------------------------------------------------- |
| Fuentes ya en `.md` o `.tex` legibles                       | Saltar Transcription                                           |
| PDF, DOCX, PPTX, imágenes escaneadas, audio (transcripción) | Spec tipo `transcription` o fase Transcription antes del Draft |
| Grupo de documentos relacionados                            | Un spec puede cubrir el lote; listar cada archivo en alcance   |

**Salida de Transcription:** archivo en `data/transcripts/<slug>.md` con metadatos (fuente original, fecha, método: pandoc / script / manual).

## Tipos de spec en este perfil

| Tipo core       | Uso en informes                                     |
| --------------- | --------------------------------------------------- |
| `feature`       | Informe nuevo o sección mayor                       |
| `documentation` | Anexo, glosario, nota metodológica                  |
| `refactor`      | Reestructuración mayor del manuscrito               |
| `transcription` | Convertir fuente(s) a Markdown para el agente       |
| `bugfix`        | Corrección factual (cifra errónea, cita incorrecta) |

Combinaciones: `feature + transcription`, `feature + documentation`.

## ADR en proyectos de informes

Crear ADR cuando la decisión es **transversal** entre informes o specs:

- Estructura de capítulos / plantilla Pandoc global
- Metodología de análisis (ej. siempre reproducible con scripts versionados)
- Fuentes de datos oficiales y política de citación
- Formato de entrega (solo PDF vs PDF + DOCX)
- Exclusión de secciones o público objetivo

No crear ADR por decisiones locales de un solo informe (van en el spec).

## Scripts permitidos

| Permitido                                                    | Prohibido como producto final                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Transcripción (`pandoc`, `python` + librerías de extracción) | Aplicación web o API de entrega                              |
| Análisis de datos (pandas, polars, etc.)                     | Base de datos operativa del informe                          |
| Generación de figuras/tablas                                 | Lógica de negocio embebida en scripts sin documentar en spec |
| Validación (lint, checksums de fuentes)                      | Pipeline sin trazabilidad en spec/release                    |

## Referencias

- [`spec-impact.md`](spec-impact.md) — tabla para specs
- [`checklist-stack.md`](checklist-stack.md) — DoD en In Review
- [`deploy.md`](deploy.md) — publicación del PDF/DOCX final
