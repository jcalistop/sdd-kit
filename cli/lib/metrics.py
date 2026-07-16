"""Métricas de salud del proceso SDD y estimación de tokens por spec."""

from __future__ import annotations

import json
import re
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .backlog import parse_backlog

# Heurística documentada (orden de magnitud; no facturación exacta).
# Ratio aproximado Tokenomics: ~54% input / ~24% output / ~22% reasoning.
TOKEN_CHARS_PER = 4
USER_MSG_TOKENS = 200
ASSISTANT_MSG_TOKENS = 800
INPUT_SHARE = 0.539
OUTPUT_SHARE = 0.244
# reasoning share ~0.216 — implícito en el resto
OUTLIER_FACTOR = 2.0
MIN_SAMPLES_FOR_OUTLIER = 3


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


def token_usage_path(sdd_path: Path) -> Path:
    return sdd_path / "metrics" / "token-usage.json"


def load_token_usage(sdd_path: Path) -> dict[str, Any]:
    path = token_usage_path(sdd_path)
    if not path.is_file():
        return {"version": 1, "entries": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "entries": []}
    if not isinstance(data, dict):
        return {"version": 1, "entries": []}
    entries = data.get("entries")
    if not isinstance(entries, list):
        data["entries"] = []
    data.setdefault("version", 1)
    return data


def _entry_by_id(data: dict[str, Any]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for entry in data.get("entries", []):
        if isinstance(entry, dict) and entry.get("spec_id"):
            out[str(entry["spec_id"])] = entry
    return out


def _find_spec_file(sdd_path: Path, spec_id: str) -> Path | None:
    for base in (sdd_path / "specs", sdd_path / "archive"):
        if not base.is_dir():
            continue
        for path in base.rglob(f"{spec_id}-*.md"):
            return path
        for path in base.rglob(f"{spec_id}.md"):
            return path
    return None


def _domain_from_spec(path: Path | None, text: str = "") -> str:
    if path is not None:
        # specs/<dominio>/SDD-... or archive/YYYY/<dominio>/
        parts = path.parts
        for i, part in enumerate(parts):
            if part == "specs" and i + 1 < len(parts):
                return parts[i + 1]
            if part == "archive" and i + 2 < len(parts):
                return parts[i + 2]
    m = re.search(r"\*\*Dominio\*\*\s*\|\s*`?([^`|]+)`?", text)
    if m:
        return m.group(1).strip()
    return "—"


def _heuristic_from_spec_file(spec_path: Path) -> dict[str, Any]:
    """Estima tokens a partir del tamaño del archivo del spec (confidence: low)."""
    text = spec_path.read_text(encoding="utf-8", errors="replace")
    chars = len(text)
    # Spec re-leído muchas veces en review: ~15× tamaño como proxy de sesión mínima
    total = max(1000, int((chars / TOKEN_CHARS_PER) * 15))
    return {
        "estimated_input_tokens": int(total * INPUT_SHARE),
        "estimated_output_tokens": int(total * OUTPUT_SHARE),
        "estimated_total_tokens": total,
        "confidence": "low",
        "source": "heuristic_spec_size",
        "verify_passed_first_attempt": None,
        "costliest_phase": "—",
        "domain": _domain_from_spec(spec_path, text),
        "phases": {},
    }


def _from_usage_entry(entry: dict[str, Any]) -> dict[str, Any]:
    total = int(entry.get("total_estimated_tokens") or 0)
    phases = entry.get("phases") if isinstance(entry.get("phases"), dict) else {}
    if not total and phases:
        total = sum(int(p.get("estimated_tokens") or 0) for p in phases.values() if isinstance(p, dict))
    costliest = "—"
    if phases:
        costliest = max(
            phases.items(),
            key=lambda kv: int(kv[1].get("estimated_tokens") or 0) if isinstance(kv[1], dict) else 0,
        )[0]
    confidence = entry.get("confidence") or "medium"
    if total and not entry.get("estimated_input_tokens"):
        inp = int(total * INPUT_SHARE)
        out = int(total * OUTPUT_SHARE)
    else:
        inp = int(entry.get("estimated_input_tokens") or int(total * INPUT_SHARE))
        out = int(entry.get("estimated_output_tokens") or int(total * OUTPUT_SHARE))
    return {
        "estimated_input_tokens": inp,
        "estimated_output_tokens": out,
        "estimated_total_tokens": total,
        "confidence": confidence,
        "source": "token-usage.json",
        "verify_passed_first_attempt": entry.get("verify_passed_first_attempt"),
        "costliest_phase": costliest,
        "domain": entry.get("domain") or "—",
        "phases": phases,
        "date": entry.get("date"),
    }


def estimate_tokens(sdd_path: Path, spec_id: str) -> dict[str, Any]:
    """Estima consumo de tokens para un SDD-NNN.

    Heurística:
    - Preferir entrada en metrics/token-usage.json (confidence medium/high según registro)
    - Si no hay registro: chars/4 del archivo del spec × 15 (confidence low)
    - No usa APIs de pricing ni counts reales del IDE
    """
    data = load_token_usage(sdd_path)
    by_id = _entry_by_id(data)
    if spec_id in by_id:
        result = _from_usage_entry(by_id[spec_id])
        result["spec_id"] = spec_id
        return result

    spec_path = _find_spec_file(sdd_path, spec_id)
    if spec_path is None:
        raise FileNotFoundError(f"Spec {spec_id} no encontrado en specs/ ni archive/")

    result = _heuristic_from_spec_file(spec_path)
    result["spec_id"] = spec_id
    return result


def list_token_estimates(sdd_path: Path, only_with_usage: bool = False) -> list[dict[str, Any]]:
    data = load_token_usage(sdd_path)
    by_id = _entry_by_id(data)
    ids: set[str] = set(by_id.keys())

    if not only_with_usage:
        for base in (sdd_path / "specs", sdd_path / "archive"):
            if not base.is_dir():
                continue
            for path in base.rglob("SDD-*.md"):
                m = re.match(r"(SDD-\d+[a-z]?)", path.name)
                if m:
                    ids.add(m.group(1))

    rows: list[dict[str, Any]] = []
    for spec_id in sorted(ids, key=lambda s: (int(re.search(r"\d+", s).group()) if re.search(r"\d+", s) else 0, s)):
        try:
            rows.append(estimate_tokens(sdd_path, spec_id))
        except FileNotFoundError:
            if spec_id in by_id:
                row = _from_usage_entry(by_id[spec_id])
                row["spec_id"] = spec_id
                rows.append(row)
    return rows


def summarize_token_estimates(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "count": 0,
            "total": 0,
            "average": 0,
            "median": 0,
            "top_consumer": None,
            "rows": [],
        }
    totals = [int(r.get("estimated_total_tokens") or 0) for r in rows]
    top = max(rows, key=lambda r: int(r.get("estimated_total_tokens") or 0))
    return {
        "count": len(rows),
        "total": sum(totals),
        "average": round(statistics.mean(totals)) if totals else 0,
        "median": round(statistics.median(totals)) if totals else 0,
        "top_consumer": {
            "spec_id": top.get("spec_id"),
            "estimated_total_tokens": top.get("estimated_total_tokens"),
            "domain": top.get("domain"),
        },
        "rows": rows,
    }


def format_token_report(
    rows: list[dict[str, Any]],
    *,
    fmt: str = "table",
    summary: dict[str, Any] | None = None,
) -> str:
    """Formatea reporte: table | text | json."""
    if fmt == "json":
        payload: dict[str, Any] = {"estimates": rows}
        if summary is not None:
            payload["summary"] = {k: v for k, v in summary.items() if k != "rows"}
        return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    if not rows:
        return "Sin datos de métricas de tokens.\n"

    def _verify_cell(v: Any) -> str:
        if v is True:
            return "Sí"
        if v is False:
            return "No"
        return "—"

    lines: list[str] = []
    if summary is not None:
        lines.append("## Resumen tokens (estimado)")
        lines.append(f"  Specs: {summary['count']}")
        lines.append(f"  Total estimado: {summary['total']}")
        lines.append(f"  Promedio: {summary['average']}")
        lines.append(f"  Mediana: {summary['median']}")
        top = summary.get("top_consumer")
        if top:
            lines.append(
                f"  Top consumer: {top.get('spec_id')} "
                f"({top.get('estimated_total_tokens')} tokens, dominio {top.get('domain')})"
            )
        lines.append("")
        lines.append(
            "Nota: valores heurísticos (no facturación exacta). Ver metrics/README.md."
        )
        lines.append("")

    header = (
        f"{'SDD-NNN':<10} {'Dominio':<12} {'Fase cara':<12} "
        f"{'Tokens est.':>12} {'Verify 1er':<10} {'Conf':<6}"
    )
    lines.append(header)
    lines.append("-" * len(header))
    for r in rows:
        lines.append(
            f"{str(r.get('spec_id') or '—'):<10} "
            f"{str(r.get('domain') or '—'):<12} "
            f"{str(r.get('costliest_phase') or '—'):<12} "
            f"{int(r.get('estimated_total_tokens') or 0):>12} "
            f"{_verify_cell(r.get('verify_passed_first_attempt')):<10} "
            f"{str(r.get('confidence') or '—'):<6}"
        )
    return "\n".join(lines) + "\n"


def find_token_outliers(
    rows: list[dict[str, Any]],
    *,
    factor: float = OUTLIER_FACTOR,
    min_samples: int = MIN_SAMPLES_FOR_OUTLIER,
) -> list[tuple[str, str, int, float]]:
    """Retorna (spec_id, domain, tokens, domain_avg) para outliers > factor × promedio del dominio."""
    by_domain: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        if r.get("source") != "token-usage.json":
            continue
        dom = str(r.get("domain") or "—")
        by_domain.setdefault(dom, []).append(r)

    outliers: list[tuple[str, str, int, float]] = []
    for domain, items in by_domain.items():
        if len(items) < min_samples:
            continue
        totals = [int(i.get("estimated_total_tokens") or 0) for i in items]
        avg = statistics.mean(totals)
        if avg <= 0:
            continue
        for i in items:
            t = int(i.get("estimated_total_tokens") or 0)
            if t > factor * avg:
                outliers.append((str(i.get("spec_id")), domain, t, avg))
    return outliers
