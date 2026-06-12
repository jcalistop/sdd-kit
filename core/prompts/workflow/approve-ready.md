---
id: approve-ready
title: "DEPRECADO — usar build-spec"
category: workflow
adoption_stage: 2
workflow_phase: Ready
deprecated: true
replaced_by: build-spec
when: Ver build-spec.md
prerequisites: []
related:
  - prompts/workflow/build-spec.md
tags: [deprecated]
human_approval: true
---

> **Deprecado desde v1.2.0.** Usa [`build-spec.md`](build-spec.md) (`sdd prompt show build-spec --full`).

## Migración

`approve-ready` fusionó con `implement-spec` en **`build-spec`**: aprueba el spec, implementa en local y no publica en Git hasta `verify-implementation`.
