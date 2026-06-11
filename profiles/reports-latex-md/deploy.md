# Publicación — Informes LaTeX + Markdown

Perfil de **publicación de documentos** (no despliegue de aplicación). El entregable final vive en `output/` y/o se adjunta al release SDD.

## Principio

La rama de producción (`main` por defecto) contiene las fuentes versionadas; la **publicación** es compilar y publicar el PDF/DOCX de una versión etiquetada.

| Capa        | Dónde                          | Qué valida                                    |
| ----------- | ------------------------------ | --------------------------------------------- |
| CI          | GitHub Actions (`docs-ci.yml`) | Lint MD, compilación PDF, scripts de análisis |
| Publicación | `output/` + release SDD        | Entregable final con versión SemVer           |

## Pasos (alineados con Fase 4 del runbook)

1. Revisar `releases/vX.Y.Z/release_vX.Y.Z.md` — informes incluidos, fuentes, scripts one-off.
2. Confirmar CI en verde para el commit de la versión.
3. **Compilar** manuscrito(s) afectados:

```bash
pandoc content/manuscript.md -o output/manuscript-vX.Y.Z.pdf
pandoc content/manuscript.md -o output/manuscript-vX.Y.Z.docx
# o, si LaTeX directo:
latexmk -pdf -outdir=output content/manuscript.tex
```

4. **Ejecutar scripts** de análisis/figuras en el orden documentado en el spec.
5. Copiar PDF/DOCX a `output/` con nombre que incluya versión.
6. Registrar hash o ruta del artefacto en la nota de release.

## Smoke post-publicación

- [ ] PDF abre sin errores; índice y referencias correctos
- [ ] DOCX abre en Word/LibreOffice si aplica
- [ ] Cifras en PDF coinciden con salida de scripts (muestra aleatoria)
- [ ] Metadatos (título, autor, fecha) correctos en portada
- [ ] Archivo en `output/` referenciado en release

## Rollback

- Revertir commit o tag anterior; republicar PDF de la versión previa desde `output/` archivado o tag Git.
- Si el error es factual: spec `bugfix` + nueva versión patch (vX.Y.Z+1).
