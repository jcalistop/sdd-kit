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
        "core": "sdd-core.mdc",
        "workflow": "sdd-agent-workflow.mdc",
        "reference": "sdd-workflow-reference.mdc",
    }
    for key, filename in mapping.items():
        entry = manifest[key]
        body = (PROMPTS / entry["file"]).read_text(encoding="utf-8")
        (OUT / filename).write_text(
            render(entry["description"], body, bool(entry.get("alwaysApply", True))),
            encoding="utf-8",
        )

    for stack in sorted((PROMPTS / "stacks").glob("*.md")):
        profile = stack.stem
        body = stack.read_text(encoding="utf-8")
        desc = stack_desc.get(profile, f"SDD — perfil {profile}")
        (OUT / f"sdd-stack-{profile}.mdc").write_text(
            render(desc, body, False),
            encoding="utf-8",
        )

    print(f"Synced {len(list(OUT.glob('*.mdc')))} files to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
