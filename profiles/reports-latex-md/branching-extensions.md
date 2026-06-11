# Extensiones de ramas — Documentos

Convenciones opcionales para repos cuyo producto principal es informes.

## Ramas sugeridas

| Rama                   | Uso                                                                     |
| ---------------------- | ----------------------------------------------------------------------- |
| `main`                 | Versiones publicadas; PDFs en `output/` de releases                     |
| `dev`                  | Integración de specs en progreso                                        |
| `draft/<SDD-NNN-slug>` | Borrador de manuscrito ligado al spec (alias de `feature/SDD-NNN-slug`) |

El prefijo `feature/` del core sigue siendo válido; `draft/` es alias semántico para este perfil.

## Reglas

1. Un spec activo → una rama de trabajo (`feature/SDD-NNN-*` o `draft/SDD-NNN-*`).
2. No mezclar dos informes no relacionados en la misma rama.
3. Merge a `dev` solo con PR en estado Validating (In Review) y checklist del perfil completo.
4. Tag SemVer en `main` al publicar versión del informe.

## Actualizaciones de plantillas y dependencias

- Cambios en plantilla Pandoc/LaTeX global → spec o ADR según alcance.
- Bump de herramientas (Pandoc, TinyTeX) → ID `—` en release si no afecta contenido.

## Trazabilidad SDD

Sync de plantillas y bumps de toolchain **no requieren** spec. Registrar en release con ID `—` si aplica.
