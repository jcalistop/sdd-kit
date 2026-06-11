"""Parser y escritura de BACKLOG.md."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

SECTIONS_ORDER = [
    "Discovery",
    "Draft",
    "Ready",
    "In Build",
    "Validating",
    "Released",
    "Descartado",
]

TRANSITIONS: dict[str, list[str]] = {
    "Discovery": ["Draft", "Descartado"],
    "Draft": ["Ready", "Discovery", "Descartado"],
    "Ready": ["In Build", "Draft", "Descartado"],
    "In Build": ["Validating", "Ready", "Descartado"],
    "Validating": ["Released", "In Build", "Descartado"],
    "Released": [],
    "Descartado": ["Discovery"],
}


@dataclass
class BacklogItem:
    section: str
    id: str | None = None
    domain: str = ""
    title: str = ""
    version: str = ""
    extra: str = ""
    date: str = ""
    archived: str = ""
    raw_line: str = ""


@dataclass
class Backlog:
    path: Path
    preamble: list[str] = field(default_factory=list)
    sections: dict[str, list[BacklogItem]] = field(default_factory=dict)
    next_id: int = 1

    def all_items(self) -> list[BacklogItem]:
        items: list[BacklogItem] = []
        for sec in SECTIONS_ORDER:
            items.extend(self.sections.get(sec, []))
        return items

    def find_by_id(self, spec_id: str) -> BacklogItem | None:
        for item in self.all_items():
            if item.id == spec_id:
                return item
        return None


def _is_separator_row(line: str) -> bool:
    return bool(re.match(r"^\|\s*[-:]+\s*\|", line))


def _is_dash_token(value: str) -> bool:
    v = value.strip()
    return not v or v in ("—", "-", "–") or bool(re.match(r"^[-—–]+$", v))


def _is_placeholder_row(line: str) -> bool:
    cols = [c.strip() for c in line.strip("|").split("|")]
    return bool(cols) and all(_is_dash_token(c) for c in cols)


def _is_header_row(cols: list[str]) -> bool:
    if not cols:
        return True
    first = cols[0].strip()
    return first in ("Dominio", "ID", "Idea / ID", "Idea / necesidad", "---")


def parse_backlog(path: Path) -> Backlog:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    backlog = Backlog(path=path)

    next_m = re.search(r"Pr[oó]ximo ID disponible:\*\*\s*`SDD-(\d+)`", text, re.I)
    if next_m:
        backlog.next_id = int(next_m.group(1))

    current: str | None = None
    preamble: list[str] = []
    in_body = False

    for line in lines:
        sec_m = re.match(
            r"^##\s+(Discovery|Draft|Ready|In Build|Validating|Released|Descartado)",
            line,
        )
        if sec_m:
            current = sec_m.group(1)
            if "Descartado" in current:
                current = "Descartado"
            backlog.sections.setdefault(current, [])
            in_body = True
            continue

        if not in_body:
            preamble.append(line)
            continue

        if not current or not line.strip().startswith("|"):
            continue
        if _is_separator_row(line) or _is_placeholder_row(line):
            continue

        cols = [c.strip() for c in line.strip("|").split("|")]
        if _is_header_row(cols):
            continue

        if current == "Discovery" and len(cols) >= 2:
            backlog.sections[current].append(
                BacklogItem(
                    section=current,
                    domain=cols[0],
                    title=cols[1],
                    version=cols[2] if len(cols) > 2 else "",
                    extra=cols[3] if len(cols) > 3 else "",
                    raw_line=line,
                )
            )
        elif current == "Descartado":
            backlog.sections[current].append(
                BacklogItem(
                    section=current,
                    title=cols[0],
                    extra=cols[1] if len(cols) > 1 else "",
                    version=cols[2] if len(cols) > 2 else "",
                    raw_line=line,
                )
            )
        elif current == "Released" and cols[0].startswith("SDD-"):
            backlog.sections[current].append(
                BacklogItem(
                    section=current,
                    id=cols[0],
                    domain=cols[1],
                    title=cols[2],
                    version=cols[3],
                    date=cols[4] if len(cols) > 4 else "",
                    archived=cols[5] if len(cols) > 5 else "",
                    raw_line=line,
                )
            )
        elif cols[0].startswith("SDD-"):
            backlog.sections[current].append(
                BacklogItem(
                    section=current,
                    id=cols[0],
                    domain=cols[1],
                    title=cols[2],
                    version=cols[3] if len(cols) > 3 else "",
                    extra=cols[4] if len(cols) > 4 else "",
                    raw_line=line,
                )
            )

    backlog.preamble = preamble
    return backlog


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return s.strip("-")[:60] or "sin-titulo"


def format_id(num: int) -> str:
    return f"SDD-{num:03d}"


def add_draft_item(
    backlog: Backlog, domain: str, title: str, version: str, spec_link: str
) -> str:
    spec_id = format_id(backlog.next_id)
    item = BacklogItem(
        section="Draft",
        id=spec_id,
        domain=domain,
        title=title,
        version=version,
        extra=spec_link,
    )
    backlog.sections.setdefault("Draft", []).append(item)
    backlog.next_id += 1
    return spec_id


def _update_next_id_line(preamble: list[str], next_id: int) -> list[str]:
    out: list[str] = []
    replaced = False
    for line in preamble:
        if re.search(r"Pr[oó]ximo ID disponible", line, re.I):
            out.append(f"**Próximo ID disponible:** `{format_id(next_id)}`.")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.insert(
            min(8, len(out)),
            f"**Próximo ID disponible:** `{format_id(next_id)}`.",
        )
    return out


def write_backlog(backlog: Backlog) -> None:
    lines = _update_next_id_line(backlog.preamble, backlog.next_id)

    lines.append("")
    lines.append("## Discovery")
    lines.append("")
    lines.append("| Dominio | Idea / necesidad | Versión | Notas |")
    lines.append("| ------- | ---------------- | ------- | ----- |")
    disc = backlog.sections.get("Discovery", [])
    if disc:
        for it in disc:
            lines.append(f"| {it.domain} | {it.title} | {it.version} | {it.extra} |")
    else:
        lines.append("| — | — | — | — |")

    for sec in ["Draft", "Ready", "In Build", "Validating"]:
        lines.append("")
        lines.append(f"## {sec}")
        lines.append("")
        lines.append("| ID | Dominio | Título | Versión | Spec |")
        lines.append("| --- | ------- | ------ | ------- | ---- |")
        items = backlog.sections.get(sec, [])
        if items:
            for it in items:
                lines.append(
                    f"| {it.id} | {it.domain} | {it.title} | {it.version} | {it.extra} |"
                )
        else:
            lines.append("| — | — | — | — | — |")

    lines.append("")
    lines.append("## Released")
    lines.append("")
    lines.append("| ID | Dominio | Título | Versión | Fecha | Spec archivado |")
    lines.append("| --- | ------- | ------ | ------- | ----- | -------------- |")
    rel = backlog.sections.get("Released", [])
    if rel:
        for it in rel:
            lines.append(
                f"| {it.id} | {it.domain} | {it.title} | {it.version} | {it.date} | {it.archived} |"
            )
    else:
        lines.append("| — | — | — | — | — | — |")

    lines.append("")
    lines.append("## Descartado / en pausa")
    lines.append("")
    lines.append("| Idea / ID | Razón | Fecha |")
    lines.append("| --------- | ----- | ----- |")
    desc = backlog.sections.get("Descartado", [])
    if desc:
        for it in desc:
            lines.append(f"| {it.title} | {it.extra} | {it.version} |")
    else:
        lines.append("| — | — | — |")

    backlog.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
