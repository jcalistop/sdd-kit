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
  - upgrade-guide.md
  - INSTALL.md
tags: [maintenance, submodule, upgrade]
human_approval: true
---

## Cuándo usarlo

Sale una versión nueva del kit (tag SemVer en `docs/releases/`) y quieres actualizar tu proyecto: submodule, documentación SDD local, adaptadores de agente y registro de versión.

## Qué hará el agente

- Lee `sdd-kit/core/upgrade-guide.md` y el changelog `sdd-kit/docs/releases/<VERSION>.md`
- Detecta `kit.installed_version` en `sdd.config.yaml` y la ref actual del submodule
- Actualiza el submodule al tag indicado
- Compara `sdd-kit/core/` con `.github/docs/sdd/` y propone merge archivo a archivo
- Reinstala adaptadores si cambió `bootstrap/agent-prompts/`
- Ejecuta `validate-sdd` y reporta errores vs advertencias
- Actualiza `UPGRADE-LOG.md` y `kit.installed_version` solo si el upgrade quedó completo

## Prompt

```
Actualiza el kit SDD de este proyecto a la versión <VERSION>.

Sigue sdd-kit/core/upgrade-guide.md de punta a punta.

Instrucciones:
1. Lee kit.installed_version en .github/docs/sdd/sdd.config.yaml y git -C sdd-kit describe --tags --always.
2. Lee el changelog en sdd-kit/docs/releases/ para <VERSION>.
3. Actualiza el submodule sdd-kit al tag <VERSION> (git fetch --tags; checkout tag).
4. Compara sdd-kit/core/ con .github/docs/sdd/ — lista archivos nuevos y modificados.
5. NO sobrescribas BACKLOG.md, specs/, archive/ ni business/ sin petición explícita.
6. Para cada archivo de instancia modificado en ambos lados: muestra diff y pide confirmación humana antes de escribir.
7. Si hay prompts/ o prompt-catalog.md nuevos, incorpora solo lo faltante.
8. Si cambió bootstrap/agent-prompts/, ejecuta install-agents.py según sdd.config.yaml → agent.targets y stack.profile.
9. Ejecuta python sdd-kit/cli/sdd.py validate — corrige ERROR; explica WARN.
10. Si el humano aprobó todos los merges: actualiza kit.installed_version y kit.installed_at en sdd.config.yaml y añade fila en UPGRADE-LOG.md.
11. Si el humano rechazó algún merge: registra pendientes en UPGRADE-LOG.md (Notas) y NO marques installed_version como <VERSION>.

Commits separados: primero submodule, luego instancia/adaptadores.
```

## Después de pegarlo

Revisa diff de adaptadores. Si quedaron archivos pendientes, agenda otro pase o deja constancia en UPGRADE-LOG.

## Ver también

- [`upgrade-guide.md`](../../upgrade-guide.md)
- [`update-submodule.md`](update-submodule.md) — atajo legacy; preferir este prompt
- [`agent-setup.md`](../../agent-setup.md)
