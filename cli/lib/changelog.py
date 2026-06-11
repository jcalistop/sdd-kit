"""Generación de CHANGELOG.md desde releases/."""

from __future__ import annotations

import re
from pathlib import Path


def _parse_version(path: Path) -> tuple[str, int, int, int] | None:
    m = re.match(r"v?(\d+)\.(\d+)\.(\d+)", path.name)
    if not m:
        return None
    ver = path.name if path.name.startswith("v") else f"v{path.name}"
    return ver, int(m.group(1)), int(m.group(2)), int(m.group(3))


def _extract_section(text: str, heading: str) -> str:
    pattern = rf"###?\s*{re.escape(heading)}[^\n]*\n(.*?)(?=\n###|\n## |\Z)"
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _extract_specs_table(text: str) -> list[str]:
    items: list[str] = []
    in_table = False
    for line in text.splitlines():
        if "Specs incluidos" in line or "| ID" in line and "SDD" in line:
            in_table = True
            continue
        if in_table and line.startswith("|") and "SDD-" in line:
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) >= 4 and cols[0].startswith("SDD-"):
                items.append(f"- **{cols[0]}** ({cols[2]}): {cols[3]}")
        elif in_table and line.startswith("##"):
            break
    return items


def generate_changelog(sdd_path: Path, output: Path | None = None) -> str:
    releases_dir = sdd_path / "releases"
    out_path = output or (sdd_path.parent.parent.parent / "CHANGELOG.md")

    versions: list[tuple[tuple[int, int, int], str, Path]] = []
    if releases_dir.is_dir():
        for d in releases_dir.iterdir():
            if not d.is_dir():
                continue
            parsed = _parse_version(d)
            if not parsed:
                continue
            ver, ma, mi, pa = parsed
            note = d / f"release_{d.name}.md"
            if not note.is_file():
                notes = list(d.glob("release_*.md"))
                note = notes[0] if notes else None
            if note and note.is_file():
                versions.append(((ma, mi, pa), ver, note))

    versions.sort(key=lambda x: x[0], reverse=True)

    lines = [
        "# Changelog",
        "",
        "Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).",
        "Generado por `sdd release changelog`.",
        "",
    ]

    for (_, ver, note_path) in versions:
        text = note_path.read_text(encoding="utf-8")
        date_m = re.search(r"\*\*Fecha\*\*\s*\|\s*(\d{4}-\d{2}-\d{2})", text)
        date = date_m.group(1) if date_m else ""

        lines.append(f"## [{ver}] - {date}")
        lines.append("")

        general = _extract_section(text, "En qué consiste esta versión")
        if not general:
            general = _extract_section(text, "Información general")
        if general:
            lines.append(general)
            lines.append("")

        novedades = _extract_section(text, "Novedades visibles")
        if novedades:
            lines.append("### Added")
            lines.append("")
            for bullet in re.findall(r"^-\s+.+", novedades, re.MULTILINE):
                lines.append(bullet)
            lines.append("")

        specs = _extract_specs_table(text)
        if specs:
            lines.append("### Specs")
            lines.append("")
            lines.extend(specs)
            lines.append("")

        limitaciones = _extract_section(text, "Limitaciones o pendientes")
        if limitaciones:
            lines.append("### Known issues")
            lines.append("")
            for bullet in re.findall(r"^-\s+.+", limitaciones, re.MULTILINE):
                lines.append(bullet)
            lines.append("")

    if len(lines) <= 5:
        lines.append("## [Unreleased]")
        lines.append("")
        lines.append("_Sin releases documentados aún._")
        lines.append("")

    content = "\n".join(lines)
    out_path.write_text(content, encoding="utf-8")
    return str(out_path)
