# Upgrade log — SDD Kit

> Trazabilidad de actualizaciones del **kit SDD** en esta instancia (dogfooding).
> No confundir con releases de iniciativas SDD del proyecto (`releases/`).

| Fecha      | Desde  | Hacia  | Archivos mergeados                                                                                  | Validación      | Notas                                      |
| ---------- | ------ | ------ | --------------------------------------------------------------------------------------------------- | --------------- | ------------------------------------------ |
| 2026-09-11 | v1.4.1 | v1.5.0 | reinstall agents (skills+rules); `branching_mode: solo-push-dev`; sin submodule (repo = kit) | validate-sdd OK (0E) | Dogfood productor post-tag v1.5.0 — SDD-023 |
| 2026-07-15 | v1.2.2 | v1.3.0 | safe-git, harness, validate-sdd, dual-release, cost-governance, metrics, upgrade-kit alineado       | validate-sdd OK (0E) | SDD-007…014 — campaña v1.3.0               |
| 2026-06-12 | v1.0.0 | v1.1.0 | upgrade-guide, upgrade-kit, kit-version, workflow, build-spec, verify-implementation, agent-prompts | validate-sdd OK | SDD-001, SDD-002, SDD-003 — campaña v1.1.0 |
