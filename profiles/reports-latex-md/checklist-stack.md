# Checklist de PR — Informes LaTeX + Markdown (perfil)

> Complementa [`../../core/checklist-pr.md`](../../core/checklist-pr.md). Marcar en cada PR junto con el checklist core.

---

## Verify — comandos obligatorios

> Gate local antes de open-pr / evidencia de `verify-implementation`. Ejecutar literales de `stack.quality_gates` según lo tocado por el spec.

| Gate | Cuándo | Comando |
| ---- | ------ | ------- |
| markdown_lint | Siempre (si hay Markdown tocado) | `markdownlint "content/**/*.md"` |
| pandoc_pdf | Siempre (si el spec exige PDF vía pandoc) | `pandoc content/manuscript.md -o output/manuscript.pdf` |
| latex_build | Siempre (si el spec exige LaTeX) | `latexmk -pdf content/manuscript.tex` |
| scripts | Siempre (si se tocaron scripts) | `python -m pytest scripts/tests/ -q` |
| Tests (alcance) | Preferir filtro al alcance del spec si el tooling lo permite; si no, suite del gate | p. ej. `python -m pytest scripts/tests/test_foo.py -q` |
| Condicional JS | — | No aplica |

---

## Compilación y formato

- [ ] Manuscrito principal compila a PDF sin errores (`pandoc` o `latexmk`)
- [ ] Export DOCX generado si el spec lo requiere _(o No aplica)_
- [ ] `markdownlint` sin errores en archivos tocados _(o No aplica)_
- [ ] Figuras y tablas referenciadas existen y se ven en el PDF
- [ ] Bibliografía/citas resuelven correctamente _(o No aplica)_

---

## Contenido y trazabilidad

- [ ] Cada cifra o afirmación factual tiene fuente identificable (dato, script, cita)
- [ ] Scripts de análisis ejecutan y producen la misma salida documentada en el spec
- [ ] Fuentes transcritas en `data/transcripts/` referenciadas en el spec si se usaron
- [ ] Alcance del spec respetado (sin secciones no especificadas)
- [ ] Limitaciones y exclusiones del spec reflejadas en el texto

---

## Reglas de negocio del proyecto _(si aplica)_

> Definidas en `.github/docs/business/domain-rules.md` (definiciones, KPIs, confidencialidad).

- [ ] Terminología alineada con glosario de `domain-rules.md` _(o No aplica)_
- [ ] Datos sensibles anonimizados según reglas del dominio _(o No aplica)_
- [ ] Audiencia y tono coherentes con reglas documentadas _(o No aplica)_

---

## Calidad editorial (In Review)

- [ ] Resumen ejecutivo coherente con el cuerpo del informe _(o No aplica)_
- [ ] Sin conclusiones sin evidencia en fuentes o análisis
- [ ] Sin cherry-picking evidente de datos
- [ ] Ortografía y estilo revisados (o paso explícito pospuesto y documentado)

---

## Scripts auxiliares _(si aplica)_

- [ ] Scripts en `scripts/` documentados en el spec (entrada, salida, dependencias)
- [ ] Sin credenciales ni rutas locales hardcodeadas
- [ ] Tests o smoke script ejecutado si el spec lo exige _(o No aplica)_

---

## Post-publicación

- [ ] PDF/DOCX final copiado a `output/` o ruta acordada
- [ ] Entrada planificada en `releases/vX.Y.Z/` si cierra versión del informe
