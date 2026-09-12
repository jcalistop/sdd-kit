# Guía — Auditorías (`audits/`)

> Metodología canónica del kit (producto). **No** es un plan de una corrida ni el [`releases/RUNBOOK.md`](../releases/RUNBOOK.md) de release de producto.
> Carpeta de corridas: opcional bajo `paths.sdd/audits/` de cada instancia. Plantillas: [`templates/`](../templates/).

---

## Glosario

| Término | Qué es |
| ------- | ------ |
| **Metodología** | Esta guía (reutilizable) |
| **Registro** | Artefacto de *esta* corrida (alcance + resultados + gaps + cierre). **Default.** |
| **Plan** | Alcance congelado *antes* de ejecutar. Solo si la auditoría es **grande** o requiere freeze/aprobación previa |
| **Stub** | Borrador en un tag/rama previo a la corrida («Pendiente»). No es fuente de verdad post-corrida |

---

## Audits vs research

| | **audits/** | **research/** |
| --- | --- | --- |
| Pregunta | ¿Está sano y qué hay que arreglar? | ¿Qué aprendimos o qué marco adoptamos? |
| Forma | Corrida con alcance, evidencias, cierre | Nota / ensayo |
| Tablero | Alimenta Discovery / specs | No es cola operativa (puede orientar un ADR) |

Metodología de research: [research.md](research.md).

---

## Cuándo auditoría vs spec SDD

- **Auditoría:** evaluación operativa puntual (madurez, dogfood, higiene). Sin `SDD-NNN` obligatorio; los gaps van a Discovery o a un spec nuevo.
- **Spec SDD:** cambio de producto/proceso con ciclo Draft→Released.

---

## Default: un registro

1. Copiar [`templates/audit-registro-template.md`](../templates/audit-registro-template.md) a `paths.sdd/audits/YYYYMMDD-slug.md` (o con hora si hace falta).
2. Completar alcance y método **antes o al inicio**; resultados y gaps **durante/al cierre**.
3. Estados sugeridos: `Pendiente` → `En curso` → `Ejecutado`.
4. Corrida corta (dogfood típico): **no** crear plan hermano.

---

## Excepción: plan separado (solo grandes)

Usar plan aparte si aplica **alguno**:

- varios días de trabajo;
- muchos ámbitos;
- varios ejecutores;
- el humano debe **congelar/aprobar** el alcance antes de ejecutar.

Entonces:

1. Copiar [`templates/audit-plan-template.md`](../templates/audit-plan-template.md).
2. Enlazar el registro/informe hermano.
3. Al cerrar, mergear **plan y registro**.

---

## Anexo — Dogfood consumidor (variante)

Pasos tipo (rellenar en el registro; no duplicar como segundo producto documental):

0. Decidir consumidor (repo, perfil stack, rama de desarrollo).
1. Baseline: pin al tag bajo prueba; `validate` en verde; anotar `kit.installed_version` / `agent.targets`.
2. Ciclo SDD mínimo en el consumidor (Discovery→verify→PR a su rama de desarrollo) **con aprobación Ready humana**.
3. Upgrade (si venía de tag anterior) + reinstall según targets + `validate`.
4. Evidencia: registro Ejecutado; gaps → Discovery/SDD; actualizar índice de la instancia.
5. Cierre: OK/FAIL por paso; sin bloqueos del kit **o** bloqueos documentados.

---

## Stub ≠ fuente de verdad

- Stub en el **tag** (o borrador pre-corrida) = plantilla / intención.
- Registro (y plan, si existe) **mergeados** en la rama de desarrollo / producción = **fuente de verdad** post-corrida.
- Si chocan: **gana el registro Ejecutado mergeado**, no el stub del tag.
- No retaguear historia para “arreglar” un stub antiguo.

---

## Checklist de cierre

- [ ] Registro en estado **Ejecutado** (resultados + gaps con severidad P0–P3).
- [ ] Si hubo plan separado: plan actualizado y enlazado.
- [ ] Gaps priorizados en BACKLOG Discovery o specs (o “no hacer” documentado).
- [ ] Índice de `paths.sdd` actualizado (tabla Audits, si existe).
- [ ] Merge a la rama de desarrollo del proyecto.
- [ ] Llevar a producción/`main` a más tardar en el **próximo patch** dual-release cuando aplique (DR-7 en el kit).
- [ ] No dejar la SoT solo en una rama feature.

---

## Plantillas

| Plantilla | Uso |
| --------- | --- |
| [`audit-registro-template.md`](../templates/audit-registro-template.md) | Default — toda corrida |
| [`audit-plan-template.md`](../templates/audit-plan-template.md) | Opcional — solo grandes / freeze |

---

## Consumidores

No se exige carpeta `audits/` en proyectos consumidores. Guía y plantillas viven en el kit para adopción voluntaria.
