"""Catálogo de prompts SDD — lectura y filtrado."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from lib.paths import find_sdd_path, kit_root

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_PROMPT_BLOCK_RE = re.compile(
    r"## Prompt\s*\n+```(?:\w+)?\s*\n(.*?)```",
    re.DOTALL,
)


@dataclass
class PromptMeta:
    id: str
    title: str
    category: str
    adoption_stage: int | None = None
    workflow_phase: str | None = None
    when: str = ""
    prerequisites: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    cli_alternative: str | None = None
    tags: list[str] = field(default_factory=list)
    human_approval: bool = False
    deprecated: bool = False
    replaced_by: str | None = None
    path: Path | None = None


def _parse_scalar(value: str) -> str | int | bool | None:
    value = value.strip()
    if value in ("null", "~", ""):
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.isdigit():
        return int(value)
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def _parse_yaml_list(block: str) -> list[str]:
    items: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if item.startswith("[") and item.endswith("]"):
                inner = item[1:-1]
                return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
            items.append(str(_parse_scalar(item) or item))
    return items


def parse_frontmatter(text: str) -> dict[str, object]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}

    raw = match.group(1)
    data: dict[str, object] = {}
    current_key: str | None = None
    list_buffer: list[str] = []

    def flush_list() -> None:
        nonlocal current_key, list_buffer
        if current_key is not None:
            data[current_key] = list_buffer
            list_buffer = []

    for line in raw.splitlines():
        if line.strip().startswith("- ") and current_key is not None:
            list_buffer.append(line.strip()[2:].strip().strip("'\""))
            continue
        flush_list()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            current_key = key
            list_buffer = []
            continue
        current_key = None
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            data[key] = [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
        else:
            data[key] = _parse_scalar(value)

    flush_list()
    return data


def _meta_from_file(path: Path) -> PromptMeta:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    adoption = fm.get("adoption_stage")
    return PromptMeta(
        id=str(fm.get("id", path.stem)),
        title=str(fm.get("title", path.stem)),
        category=str(fm.get("category", "unknown")),
        adoption_stage=int(adoption) if isinstance(adoption, int) else None,
        workflow_phase=(
            str(fm["workflow_phase"])
            if fm.get("workflow_phase") not in (None, "null")
            else None
        ),
        when=str(fm.get("when", "")),
        prerequisites=[str(x) for x in (fm.get("prerequisites") or [])],
        related=[str(x) for x in (fm.get("related") or [])],
        cli_alternative=(
            str(fm["cli_alternative"])
            if fm.get("cli_alternative") not in (None, "null")
            else None
        ),
        tags=[str(x) for x in (fm.get("tags") or [])],
        human_approval=bool(fm.get("human_approval")),
        deprecated=bool(fm.get("deprecated")),
        replaced_by=(
            str(fm["replaced_by"])
            if fm.get("replaced_by") not in (None, "null")
            else None
        ),
        path=path,
    )


def find_prompts_dir(sdd_path: Path | None = None) -> Path:
    """Prioriza prompts en instancia SDD; fallback al kit."""
    if sdd_path is None:
        sdd_path = find_sdd_path()
    local = sdd_path / "prompts"
    if local.is_dir() and any(local.rglob("*.md")):
        return local
    return kit_root() / "core" / "prompts"


def load_all_prompts(sdd_path: Path | None = None) -> list[PromptMeta]:
    prompts_dir = find_prompts_dir(sdd_path)
    items: list[PromptMeta] = []
    for path in sorted(prompts_dir.rglob("*.md")):
        if path.name.startswith("."):
            continue
        items.append(_meta_from_file(path))
    return sorted(items, key=lambda p: (p.category, p.id))


def get_prompt(prompt_id: str, sdd_path: Path | None = None) -> PromptMeta | None:
    for meta in load_all_prompts(sdd_path):
        if meta.id == prompt_id:
            return meta
    return None


def extract_prompt_body(text: str) -> str:
    match = _PROMPT_BLOCK_RE.search(text)
    if match:
        return match.group(1).rstrip() + "\n"
    return ""


def format_prompt_list(
    prompts: list[PromptMeta],
    *,
    category: str | None = None,
    phase: str | None = None,
) -> str:
    filtered = prompts
    if category:
        filtered = [p for p in filtered if p.category == category]
    if phase:
        filtered = [
            p for p in filtered if p.workflow_phase and p.workflow_phase.lower() == phase.lower()
        ]

    if not filtered:
        return "No hay prompts que coincidan con los filtros."

    id_w = max(len(p.id) for p in filtered)
    title_w = min(40, max(len(p.title) for p in filtered))
    lines = [
        f"{'ID':<{id_w}}  {'TÍTULO':<{title_w}}  CATEGORÍA  FASE",
        "-" * (id_w + title_w + 24),
    ]
    for p in filtered:
        phase_col = p.workflow_phase or "—"
        title = p.title if len(p.title) <= title_w else p.title[: title_w - 1] + "…"
        lines.append(f"{p.id:<{id_w}}  {title:<{title_w}}  {p.category:<9}  {phase_col}")
    lines.append(f"\nTotal: {len(filtered)} — `sdd prompt show <id>` para copiar")
    return "\n".join(lines)


def _replacement_prompt(
    meta: PromptMeta, sdd_path: Path | None, *, seen: frozenset[str]
) -> PromptMeta | None:
    if not meta.replaced_by or meta.replaced_by in seen:
        return None
    return get_prompt(meta.replaced_by, sdd_path)


def format_prompt_show(
    meta: PromptMeta,
    *,
    full: bool = False,
    sdd_path: Path | None = None,
) -> str:
    if meta.path is None or not meta.path.is_file():
        return f"Error: no se encontró archivo para prompt '{meta.id}'"

    text = meta.path.read_text(encoding="utf-8")
    body = extract_prompt_body(text)

    if not full:
        if not body:
            replacement = _replacement_prompt(meta, sdd_path, seen=frozenset({meta.id}))
            if replacement and replacement.path:
                replacement_body = extract_prompt_body(
                    replacement.path.read_text(encoding="utf-8")
                )
                if replacement_body:
                    return (
                        f"# Nota: '{meta.id}' está deprecado → usa '{replacement.id}'.\n\n"
                        f"{replacement_body}"
                    )
            return f"Error: prompt '{meta.id}' no tiene bloque ## Prompt"
        if meta.deprecated and meta.replaced_by:
            return (
                f"# Nota: '{meta.id}' está deprecado → usa '{meta.replaced_by}'.\n\n"
                f"{body}"
            )
        return body

    return text.strip() + "\n"
