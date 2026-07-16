#!/usr/bin/env python3
"""Sincroniza bootstrap/cursor-rules/ desde agent-prompts/ y manifest.json."""
from __future__ import annotations

import json
from pathlib import Path

BOOTSTRAP = Path(__file__).resolve().parent
PROMPTS = BOOTSTRAP / "agent-prompts"
OUT = BOOTSTRAP / "cursor-rules"


def main() -> int:
    tpl = (BOOTSTRAP / "adapters" / "cursor-rule.mdc.tpl").read_text(encoding="utf-8")
    manifest = json.loads((PROMPTS / "manifest.json").read_text(encoding="utf-8"))
    stack_desc = json.loads((PROMPTS / "stack-descriptions.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)

    def render(desc: str, body: str, always: bool) -> str:
        return (
            tpl.replace("{{DESCRIPTION}}", desc)
            .replace("{{BODY}}", body)
            .replace("{{ALWAYS_APPLY}}", str(always).lower())
        )

    mapping = {
        "workflow": "sdd-agent-workflow.mdc",
        "reference": "sdd-workflow-reference.mdc",
        "safe_git": "sdd-safe-git.mdc",
    }

    # Two-zone prompt: construir items con cacheZone, ordenar stable primero, luego volatile.
    # Orden determinista dentro de cada zona (por filename) para garantizar mismo cache key.
    core_items = []
    for key, filename in mapping.items():
        entry = manifest[key]
        body = (PROMPTS / entry["file"]).read_text(encoding="utf-8")
        cache_zone = entry.get("cacheZone", "volatile")
        core_items.append((filename, entry["description"], body, bool(entry.get("alwaysApply", True)), cache_zone))

    core_items.sort(key=lambda x: (0 if x[4] == "stable" else 1, x[0]))

    for filename, description, body, always, _cz in core_items:
        (OUT / filename).write_text(
            render(description, body, always),
            encoding="utf-8",
        )

    # Stack rules siempre en zona volatile (orden alfabetico determinista)
    stack_items = []
    for stack in sorted((PROMPTS / "stacks").glob("*.md")):
        profile = stack.stem
        body = stack.read_text(encoding="utf-8")
        desc = stack_desc.get(profile, f"SDD — perfil {profile}")
        stack_items.append((f"sdd-stack-{profile}.mdc", desc, body, False, "volatile"))

    stack_items.sort(key=lambda x: x[0])
    for filename, description, body, always, _cz in stack_items:
        (OUT / filename).write_text(
            render(description, body, always),
            encoding="utf-8",
        )

    # Validacion: verificar que las reglas stable no aparezcan despues de las volatile
    generated_files = sorted(OUT.glob("*.mdc"), key=lambda f: f.name)
    stable_seen = False
    volatile_after_stable = False
    for f in generated_files:
        name = f.name
        is_stable = any(name == item[0] for item in core_items if item[4] == "stable")
        if is_stable:
            if volatile_after_stable:
                print(f"ADVERTENCIA: regla volatile antes de stable '{name}' — cache key roto.", file=sys.stderr)
            stable_seen = True
        else:
            if stable_seen:
                volatile_after_stable = True

    generated_count = len(generated_files)
    print(f"Synced {generated_count} files to {OUT} (two-zone: stable, then volatile)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
