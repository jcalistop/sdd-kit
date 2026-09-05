"""Métricas de salud del proceso SDD."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path

from .backlog import parse_backlog


def collect_metrics(sdd_path: Path, stagnant_days: int = 14) -> dict:
    backlog = parse_backlog(sdd_path / "BACKLOG.md")
    by_state: dict[str, int] = {}
    for item in backlog.all_items():
        by_state[item.section] = by_state.get(item.section, 0) + 1

    specs_dir = sdd_path / "specs"
    stagnant: list[str] = []
    types_count: dict[str, int] = {}
    cutoff = datetime.now() - timedelta(days=stagnant_days)

    if specs_dir.is_dir():
        for spec_file in specs_dir.rglob("SDD-*.md"):
            mtime = datetime.fromtimestamp(spec_file.stat().st_mtime)
            if mtime < cutoff:
                stagnant.append(f"{spec_file.name} (sin cambios {stagnant_days}+ días)")

            text = spec_file.read_text(encoding="utf-8", errors="replace")
            tm = re.search(r"\*\*Tipo\*\*\s*\|\s*`?(\w+)`?", text)
            if tm:
                t = tm.group(1)
                types_count[t] = types_count.get(t, 0) + 1

    releases = list((sdd_path / "releases").glob("v*/")) if (sdd_path / "releases").is_dir() else []

    return {
        "by_state": by_state,
        "stagnant": stagnant,
        "types": types_count,
        "release_count": len([r for r in releases if r.is_dir()]),
        "active_specs": sum(
            len(backlog.sections.get(s, [])) for s in ["Draft", "Ready", "In Build", "Validating"]
        ),
        "next_id": backlog.next_id,
    }


def format_metrics_report(metrics: dict, markdown: bool = False) -> str:
    lines: list[str] = []
    if markdown:
        lines.append("# Métricas SDD")
        lines.append("")

    lines.append("## Resumen por estado")
    for state, count in sorted(metrics["by_state"].items()):
        lines.append(f"  {state}: {count}")

    lines.append("")
    lines.append(f"Specs activos (Draft a Validating): {metrics['active_specs']}")
    lines.append(f"Releases documentados: {metrics['release_count']}")
    lines.append(f"Próximo ID: SDD-{metrics['next_id']:03d}")

    if metrics["types"]:
        lines.append("")
        lines.append("## Tipos de spec activos")
        for t, c in sorted(metrics["types"].items()):
            lines.append(f"  {t}: {c}")

    if metrics["stagnant"]:
        lines.append("")
        lines.append("## Specs estancados")
        for s in metrics["stagnant"]:
            lines.append(f"  ! {s}")

    return "\n".join(lines)
