# SDD-001 — Informe trimestral de indicadores operacionales Q1 2026

> **Spec de ejemplo** para el perfil `reports-latex-md`. Referencia de nivel de detalle esperado.

---

## Cabecera

| Campo                 | Valor                                        |
| --------------------- | -------------------------------------------- |
| **ID**                | `SDD-001`                                    |
| **Dominio**           | `informes`                                   |
| **Tipo**              | `feature`                                    |
| **Fecha**             | 2026-06-11                                   |
| **Estado**            | `Draft`                                      |
| **Versión objetivo**  | v1.0.0                                       |
| **Owner**             | equipo                                       |
| **Prioridad**         | `P1`                                         |
| **ADRs relacionados** | —                                            |
| **Dependencias**      | `SDD-002` (transcripción de actas de comité) |

---

## Problema y objetivo

**Problema:**

La dirección recibe datos dispersos (Excel, correos, actas en PDF) sin un informe consolidado trimestral. Las decisiones se retrasan por falta de una narrativa única con cifras trazables.

**Objetivo:**

Publicar informe trimestral en PDF (y DOCX para revisión interna) con indicadores clave, tendencias Q1 vs Q4 2025 y recomendaciones accionables para el comité directivo.

---

## Alcance

**Incluye:**

- Manuscrito `content/informe-q1-2026.md` con secciones: resumen ejecutivo, indicadores, análisis, recomendaciones, anexos
- Script `scripts/aggregate_kpis.py` — lee `data/sources/kpis_q1.csv` y genera `content/tables/kpis.tex` (o tabla MD)
- Transcripciones previas en `data/transcripts/actas-comite.md` (spec `SDD-002`) citadas en metodología
- Export PDF vía Pandoc + plantilla `templates/informe-corporativo.tex`
- Export DOCX para revisión de gerencia

**Excluye explícitamente:**

- Dashboard interactivo o aplicación web
- Proyecciones financieras a 12 meses (informe futuro)
- Datos de sucursal internacional (sin fuente validada en Q1)

---

## Impacto técnico

| Pregunta                 | Respuesta                                                                   |
| ------------------------ | --------------------------------------------------------------------------- |
| Audiencia y propósito    | Comité directivo; soporte de decisiones trimestrales                        |
| Formatos de salida       | PDF (oficial), DOCX (revisión)                                              |
| Archivos de contenido    | `content/informe-q1-2026.md`, `content/tables/kpis.md`                      |
| Fuentes de datos         | `data/sources/kpis_q1.csv`, actas transcritas `SDD-002`                     |
| Transcripción previa     | Sí — depende de `SDD-002` para actas PDF                                    |
| Análisis con scripts     | Sí — `scripts/aggregate_kpis.py`                                            |
| Visualizaciones          | Tabla de KPIs; gráfico de tendencia `content/figures/trend_q1.png` (script) |
| Plantilla global         | Usa `templates/informe-corporativo.tex` existente — no ADR                  |
| Bibliografía             | No aplica — fuentes internas                                                |
| Reglas `domain-rules.md` | Sí — KPIs según glosario; datos agregados sin identificación personal       |
| ADR                      | No                                                                          |

---

## Reglas de negocio

- Indicadores deben usar definiciones del glosario en `business/domain-rules.md`.
- Cifras comparativas solo entre Q1 2026 y Q4 2025 (misma metodología de cálculo).
- No incluir nombres de personas en el cuerpo del informe (solo roles).

---

## Criterios de aceptación

**Happy path:**

- [ ] PDF compila sin errores y tiene las 5 secciones del outline
- [ ] Tabla de KPIs coincide con salida de `aggregate_kpis.py` (verificación con diff o checksum)
- [ ] Resumen ejecutivo ≤ 2 páginas
- [ ] DOCX abre y mantiene estructura de headings

**Error path / calidad:**

- [ ] Si falta `kpis_q1.csv`, el script falla con mensaje claro (no genera cifras inventadas)
- [ ] Si `SDD-002` no está Released, el spec no pasa a Ready (dependencia bloqueante)
- [ ] Revisor encuentra al menos una fuente por afirmación factual en cuerpo y anexos

---

## Diseño técnico

| Archivo                             | Cambio                   |
| ----------------------------------- | ------------------------ |
| `content/informe-q1-2026.md`        | Manuscrito principal     |
| `scripts/aggregate_kpis.py`         | Agregación CSV → tabla   |
| `content/figures/trend_q1.png`      | Figura generada          |
| `templates/informe-corporativo.tex` | Sin cambios (reutilizar) |
| `output/informe-q1-2026-v1.0.0.pdf` | Entregable final         |

---

## Verificación técnica

```bash
python scripts/aggregate_kpis.py
markdownlint "content/informe-q1-2026.md"
pandoc content/informe-q1-2026.md -o output/informe-q1-2026.pdf --template=templates/informe-corporativo.tex
pandoc content/informe-q1-2026.md -o output/informe-q1-2026.docx
```

---

## Riesgos y rollback

| Riesgo                                         | Probabilidad | Impacto | Mitigación                                                   |
| ---------------------------------------------- | ------------ | ------- | ------------------------------------------------------------ |
| Retraso en transcripción de actas (`SDD-002`)  | Media        | Alto    | Publicar informe sin sección de actas; anexo en patch v1.0.1 |
| CSV con columnas renombradas                   | Baja         | Medio   | Validar schema en script; documentar en spec                 |
| Plantilla LaTeX rompe con nueva versión Pandoc | Baja         | Medio   | Fijar versión Pandoc en CI                                   |

---

## Notas post-implementación

-
