---
id: upgrade-kit
title: Actualizar kit SDD en instancia consumidora
category: exceptions
adoption_stage: null
workflow_phase: null
when: Nueva versión del kit publicada; actualizar submodule e instancia sin perder customizaciones
prerequisites:
  - sdd-kit/ como submodule (o copia con ruta equivalente)
  - Instancia SDD en .github/docs/sdd/
related:
  - guides/upgrade-guide.md
  - INSTALL.md
tags: [maintenance, submodule, upgrade]
human_approval: true
---

## Cuándo usarlo

Sale una versión nueva del kit (tag SemVer en `docs/releases/`) y quieres actualizar tu proyecto: submodule, documentación SDD local, adaptadores de agente y registro de versión.

## Qué hará el agente

- Lee **`sdd-kit/core/guides/upgrade-guide.md`** (canónico tras el bump; no exige copia previa en la instancia) y el changelog `sdd-kit/docs/releases/<VERSION>.md`
- Detecta `kit.installed_version` en `sdd.config.yaml` y la ref actual del submodule
- Actualiza el submodule al tag indicado
- Si destino ≥ v1.6.0: migra guías de la raíz de `paths.sdd` a `guides/` con OK humano; compara `sdd-kit/core/guides/` con `paths.sdd/guides/`
- Reinstala adaptadores si cambió `bootstrap/agent-prompts/` **o** `bootstrap/agent-skills/`
- Ejecuta checklist post-upgrade (`sdd-upgrade-kit/reference.md`) — p. ej. safe-git en v1.3.0+; v1.3.2+ sin cost-governance; v1.5+/v1.6 paths y branching
- Ejecuta `validate-sdd` y reporta errores vs advertencias
- Actualiza `UPGRADE-LOG.md` y `kit.installed_version` solo si el upgrade quedó completo

## Prompt

```
Actualiza el kit SDD de este proyecto a la versión <VERSION>.

Sigue sdd-kit/core/guides/upgrade-guide.md de punta a punta (fuente canónica del kit tras el bump).

Instrucciones:
1. Lee kit.installed_version en .github/docs/sdd/sdd.config.yaml y git -C sdd-kit describe --tags --always.
2. Lee el changelog en sdd-kit/docs/releases/ para <VERSION>.
3. Actualiza el submodule sdd-kit al tag <VERSION> (git fetch --tags; checkout tag).
4. Si <VERSION> ≥ v1.6.0 y hay guías sueltas en la raíz de .github/docs/sdd/: con confirmación humana, muévelas a .github/docs/sdd/guides/ (git mv). No toques BACKLOG.md, specs/, archive/ ni business/.
5. Compara sdd-kit/core/guides/ con .github/docs/sdd/guides/ — lista archivos nuevos y modificados. No uses solo diff de core/ plano como único paso.
6. NO sobrescribas BACKLOG.md, specs/, archive/ ni business/ sin petición explícita.
7. Para cada archivo de instancia modificado en ambos lados: muestra diff y pide confirmación humana antes de escribir.
8. Si hay prompts/ o prompt-catalog.md nuevos, incorpora solo lo faltante.
9. Si cambió bootstrap/agent-prompts/ O bootstrap/agent-skills/, ejecuta install-agents.py según sdd.config.yaml → agent.targets y stack.profile (prompts + skills).
10. Ejecuta el checklist post-upgrade de sdd-kit/bootstrap/agent-skills/sdd-upgrade-kit/reference.md (safe-git, v1.3.2+ sin cost-governance ni metrics tokens; v1.5+/v1.6 branching, profile, guides).
11. Ejecuta python sdd-kit/cli/sdd.py validate — corrige ERROR; explica WARN.
12. Si el humano aprobó todos los merges: actualiza kit.installed_version y kit.installed_at en sdd.config.yaml y añade fila en UPGRADE-LOG.md.
13. Si el humano rechazó algún merge: registra pendientes en UPGRADE-LOG.md (Notas) y NO marques installed_version como <VERSION>.

Salto largo (p. ej. desde v1.2): un solo checkout a <VERSION>; aplica checklists del upgrade-guide en orden. No hagas N bumps intermedios obligatorios.

Commits separados: primero submodule, luego instancia/adaptadores.
```

## Después de pegarlo

Revisa diff de adaptadores. Si quedaron archivos pendientes, agenda otro pase o deja constancia en UPGRADE-LOG.

## Ver también

- [`guides/upgrade-guide.md`](../../guides/upgrade-guide.md) (en el kit: `core/guides/upgrade-guide.md`)
- [`update-submodule.md`](update-submodule.md) — atajo legacy; preferir este prompt
- [`guides/agent-setup.md`](../../guides/agent-setup.md)
