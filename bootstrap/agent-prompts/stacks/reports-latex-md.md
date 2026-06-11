# SDD Stack — Informes LaTeX + Markdown

Perfil activo cuando `sdd.config.yaml` → `stack.profile: reports-latex-md`.

**Producto final:** documento (`.md` / `.tex` → PDF/DOCX). **Scripts** (Python, Pandoc) solo como apoyo para transcripción, análisis y figuras.

## Workflow extendido

Seguir [`profiles/reports-latex-md/workflow-extensions.md`](profiles/reports-latex-md/workflow-extensions.md):

```
Discovery → Transcription (opcional) → Draft → Ready → In Progress → In Review → Released
```

Estados en cabecera del spec: usar los del core (`Draft`, `Ready`, `In Build`, `Validating`, `Released`).

## Quality gates

- Lint: `markdownlint` en manuscritos tocados
- Compilación: `pandoc` → PDF y/o `latexmk` si hay `.tex`
- Scripts: ejecutar análisis/figuras documentados en el spec sin error
- CI: `.github/workflows/docs-ci.yml` en verde antes de merge (si existe)

## Estructura típica

- `content/` — manuscritos `.md` / `.tex`
- `data/sources/` — archivos originales (PDF, DOCX, CSV)
- `data/transcripts/` — fuentes transcritas a `.md` (legibles por el agente)
- `scripts/` — Python: transcripción, análisis, figuras
- `templates/` — plantillas Pandoc/LaTeX
- `output/` — PDF/DOCX finales versionados

## Transcripción

Cuando el humano aporta PDF, DOCX, PPTX u otros no legibles directamente:

1. Crear spec tipo `transcription` (o fase Transcription antes del Draft del informe).
2. Convertir a Markdown en `data/transcripts/<slug>.md` (Pandoc, script Python, o extracción documentada).
3. Registrar en el spec: archivo fuente, método, fecha, limitaciones de la transcripción.
4. **No** asumir contenido de fuentes no transcritas.

Un spec puede cubrir **un archivo o un grupo** relacionado; listar todos en alcance.

## Specs e impacto técnico

- Completar `profiles/reports-latex-md/spec-impact.md` en cada spec
- Tipos habituales: `feature` (informe), `transcription`, `documentation` (anexo), `refactor` (reestructuración), `bugfix` (corrección factual)

## ADR

Crear ADR para decisiones **transversales**: plantilla global, metodología de análisis, política de fuentes, formatos de entrega, público objetivo. Decisiones de un solo informe van en el spec.

## Reglas de negocio del proyecto

- Fuente única: `.github/docs/business/domain-rules.md` (KPIs, glosario, confidencialidad)
- Si estado plantilla: no asumir definiciones; sesión guiada (`sdd-agent-workflow.mdc`)
- Toda cifra en el informe debe ser trazable a fuente o script versionado

## Publicación

- Ver `profiles/reports-latex-md/deploy.md`
- Artefacto final en `output/` + entrada en release SDD

## Antipatrones de informes (evitar)

| Señal                                   | Acción                                                             |
| --------------------------------------- | ------------------------------------------------------------------ |
| Conclusión sin fuente o script trazable | Detener; citar fuente o marcar como hipótesis                      |
| Cherry-picking de datos                 | Alertar al humano; documentar criterio de selección                |
| Informe genérico "por si acaso"         | YAGNI; acotar audiencia y alcance en spec                          |
| Script que se convierte en "la app"     | Recordar: entregable es el documento                               |
| Reescritura total del manuscrito        | Preferir spec `refactor` incremental                               |
| Ignorar dependencia de transcripción    | Bloquear Ready hasta `transcription` Released o excluir en alcance |

## Prohibido

- Entregar aplicación web/API como sustituto del informe
- Inventar cifras o citas no presentes en fuentes/transcripts
- Omitir compilación PDF antes de Validating si el spec promete PDF
- Hardcodear rutas locales o credenciales en scripts
