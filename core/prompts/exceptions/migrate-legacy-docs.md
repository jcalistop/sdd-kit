---
id: migrate-legacy-docs
title: Migrar documentación legacy a business/
category: exceptions
adoption_stage: 3
workflow_phase: null
when: Documentación previa fuera de business/; Etapa 3 de adopción
prerequisites:
  - Instancia SDD activa (Etapa 2+)
related:
  - adoption-guide.md#etapa-3
tags: [migration, documentation]
human_approval: true
---

## Cuándo usarlo

Adopción Etapa 3: consolidar documentación de negocio que hoy está en otro lado (READMEs, `docs/`, herramientas externas, etc.) en `business/README.md` y `domain-rules.md`.

## Qué hará el agente

- Inventaria fuentes legacy que indiques (rutas en el repo, URLs, archivos exportados)
- Extrae roles, reglas e invariantes
- Propone contenido para `business/` sin borrar fuentes originales
- Pide aprobación antes de escribir

## Prompt

```
Migra documentación legacy al contexto SDD en business/.

Fuentes: <RUTAS_EN_REPO_O_URLS_O_DESCRIPCION>

Instrucciones:
1. Lee adoption-guide.md Etapa 3 y templates/business-domain-template.md.
2. Inventaria qué hay en las fuentes (roles, reglas, glosario).
3. Propone actualización de business/README.md y business/domain-rules.md.
4. NO eliminar fuentes originales sin confirmación.
5. Registra en BACKLOG qué quedó migrado vs pendiente.

Pide mi aprobación antes de escribir archivos finales.
```

## Después de pegarlo

Revisa propuesta y aprueba escritura. Valida con `sdd validate`.

## Ver también

- [`adoption-guide.md`](../../adoption-guide.md) — Etapa 3
