"""One-off helper to extract agent-prompts from .mdc (run once, then delete)."""
from __future__ import annotations

import re
from pathlib import Path


def strip_mdc(text: str) -> str:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3 :].lstrip("\n")
    return text


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    meta: dict[str, str] = {}
    for line in block.strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()
    return meta


def main() -> None:
    kit = Path(__file__).parent / "cursor-rules"
    out = Path(__file__).parent / "agent-prompts"
    stacks_out = out / "stacks"
    stacks_out.mkdir(parents=True, exist_ok=True)

    mappings = {
        "sdd-core.mdc": "sdd-core.md",
        "sdd-agent-workflow.mdc": "sdd-agent-workflow.md",
    }
    meta_out: dict[str, str] = {}
    for src_name, dest_name in mappings.items():
        src = kit / src_name
        text = src.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        meta_out[dest_name] = meta.get("description", "")
        (out / dest_name).write_text(strip_mdc(text), encoding="utf-8")

    stack_meta: dict[str, str] = {}
    for stack in sorted(kit.glob("sdd-stack-*.mdc")):
        profile = stack.stem.replace("sdd-stack-", "")
        text = stack.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        stack_meta[profile] = meta.get("description", "")
        (stacks_out / f"{profile}.md").write_text(strip_mdc(text), encoding="utf-8")

    # Write stack descriptions for install-agents.py
    desc_path = out / "stack-descriptions.json"
    import json

    desc_path.write_text(json.dumps(stack_meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote prompts to {out}")


if __name__ == "__main__":
    main()
