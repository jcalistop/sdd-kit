# Metodología — Auditorías (`audits/`)

> Guía reutilizable para mantenedores del kit. **No** es un plan de una corrida ni el [`core/releases/RUNBOOK.md`](../../../../core/releases/RUNBOOK.md) de release de producto.
> Spec: [SDD-026](../specs/docs/SDD-026-metodologia-auditorias-plantillas.md).

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

Metodología de research: ítem aparte en BACKLOG Discovery (no cubierto aquí).

---

## Cuándo auditoría vs spec SDD

- **Auditoría:** evaluación operativa puntual (madurez, dogfood, higiene). Sin `SDD-NNN` obligatorio; los gaps van a Discovery o a un spec nuevo.
- **Spec SDD:** cambio de producto/proceso con ciclo Draft→Released.

---

## Default: un registro

1. Copiar [`core/templates/audit-registro-template.md`](../../../../core/templates/audit-registro-template.md) a `audits/YYYYMMDD-slug.md` (o con hora si hace falta).
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

1. Copiar [`core/templates/audit-plan-template.md`](../../../../core/templates/audit-plan-template.md).
2. Enlazar el registro/informe hermano.
3. Al cerrar, mergear **plan y registro**.

Ejemplo histórico (no migrar): auditoría general `20260905-…` (dual de facto). Dogfood `20260906-…` en el modelo nuevo sería **solo registro**.

---

## Anexo — Dogfood consumidor (variante)

Pasos tipo (rellenar en el registro; no duplicar como segundo producto documental):

0. Decidir consumidor (repo, perfil stack, rama de desarrollo).
1. Baseline: pin al tag bajo prueba; `validate` en verde; anotar `kit.installed_version` / `agent.targets`.
2. Ciclo SDD mínimo en el consumidor (Discovery→verify→PR a su rama de desarrollo) **con aprobación Ready humana**.
3. Upgrade (si venía de tag anterior) + reinstall según targets + `validate`.
4. Evidencia en el kit: registro Ejecutado; gaps → Discovery/SDD; actualizar índice.
5. Cierre: OK/FAIL por paso; sin bloqueos del kit **o** bloqueos documentados.

---

## Stub ≠ fuente de verdad

- Stub en el **tag** (o borrador pre-corrida) = plantilla / intención.
- Registro (y plan, si existe) **mergeados** en `dev` / `main` = **fuente de verdad** post-corrida.
- Si chocan: **gana el registro Ejecutado mergeado**, no el stub del tag.
- No retaguear historia para “arreglar” un stub antiguo.

---

## Checklist de cierre

- [ ] Registro en estado **Ejecutado** (resultados + gaps con severidad P0–P3).
- [ ] Si hubo plan separado: plan actualizado y enlazado.
- [ ] Gaps priorizados en BACKLOG Discovery o specs (o “no hacer” documentado).
- [ ] Índice [../README.md](../README.md) actualizado (tabla Audits).
- [ ] PR / merge a **`dev`**.
- [ ] Llevar a **`main`** a más tardar en el **próximo patch** dual-release (DR-7).
- [ ] No dejar la SoT solo en una rama feature.

---

## Plantillas

| Plantilla | Uso |
| --------- | --- |
| [`audit-registro-template.md`](../../../../core/templates/audit-registro-template.md) | Default — toda corrida |
| [`audit-plan-template.md`](../../../../core/templates/audit-plan-template.md) | Opcional — solo grandes / freeze |

---

## Ejemplos (referencia; no migrar)

- [20260905-1202-auditoria-general-kit.md](20260905-1202-auditoria-general-kit.md) + informe — grande / dual.
- [20260906-dogfood-consumidor-externo.md](20260906-dogfood-consumidor-externo.md) + informe — corta / en modelo nuevo → un registro.
