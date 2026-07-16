# SDD — Instrucciones para el agente (Codex)

Metodología Spec-Driven Development instalada por **sdd-kit**. Documentación del proyecto en `{{SDD_PATH}}/`.

Sigue estas reglas en iniciativas no triviales. El humano aprueba specs (Ready) y merges (PR).

**Safe-git:** no ejecutes Git destructivo (`reset --hard`, force-push, `clean -fd`, etc.) sin instrucción escrita. Inspecciona divergencia local/remoto antes de pull/merge/reset en la rama de desarrollo. Detalle: `sdd-kit/core/safe-git-contract.md`.
