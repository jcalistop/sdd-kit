# Perfil: Informes LaTeX + Markdown

Extensión del SDD core para **producción de informes y documentos**: fuente en Markdown (`.md`) y/o LaTeX (`.tex`), exportación a PDF/DOCX, scripts Python solo como apoyo (transcripción, análisis de datos).

| Archivo                                                                          | Uso                                              |
| -------------------------------------------------------------------------------- | ------------------------------------------------ |
| [checklist-stack.md](checklist-stack.md)                                         | DoD de contenido, compilación y trazabilidad     |
| [spec-impact.md](spec-impact.md)                                                 | Tabla "Impacto técnico" para specs de documentos |
| [workflow-extensions.md](workflow-extensions.md)                                 | Ciclo adaptado (Transcription → In Review)       |
| [deploy.md](deploy.md)                                                           | Publicación del entregable final                 |
| [branching-extensions.md](branching-extensions.md)                               | Convenciones de ramas para documentos            |
| [release-deploy-section.md](release-deploy-section.md)                           | Bloque para notas de release                     |
| [examples/SDD-001-informe-trimestral.md](examples/SDD-001-informe-trimestral.md) | Spec de ejemplo (referencia de calidad)          |

## Herramientas requeridas

| Herramienta                   | Uso                                                  |
| ----------------------------- | ---------------------------------------------------- |
| **Pandoc**                    | Conversión MD → PDF/DOCX/LaTeX                       |
| **LaTeX** (TinyTeX, TeX Live) | Compilación de `.tex` y salida PDF                   |
| **markdownlint**              | Lint de fuentes Markdown                             |
| **Python 3.10+** (opcional)   | Transcripción de fuentes, análisis de datos, figuras |

## Estructura típica del proyecto consumidor

```
proyecto/
├── content/              # Manuscritos .md / .tex
├── data/
│   ├── sources/          # PDF, DOCX, PPTX, CSV originales
│   └── transcripts/      # Fuentes transcritas a .md (legibles por agente)
├── scripts/              # Python: transcripción, análisis, figuras
├── templates/            # Plantillas Pandoc/LaTeX
├── output/               # PDF/DOCX finales (versionados o en release)
└── .github/docs/sdd/     # Instancia SDD
```

## Quality gates por defecto

- `markdownlint "**/*.md"` (o ruta del manuscrito)
- `pandoc content/manuscript.md -o output/manuscript.pdf` (compilación)
- `latexmk -pdf content/manuscript.tex` (si hay fuente LaTeX directa)
- Scripts de análisis ejecutan sin error (`python scripts/...`)
- CI: workflow de compilación en verde si está configurado

## Principio del perfil

**El producto final es el documento**, no una aplicación. Los scripts existen solo para transcripción, análisis reproducible y generación de figuras/tablas.
