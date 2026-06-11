"""Sincronización BACKLOG ↔ GitHub Issues vía gh CLI."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .backlog import Backlog, BacklogItem, parse_backlog, write_backlog

LABEL_PREFIX = "sdd:"
STATE_LABELS = {
    "Discovery": f"{LABEL_PREFIX}discovery",
    "Draft": f"{LABEL_PREFIX}draft",
    "Ready": f"{LABEL_PREFIX}ready",
    "In Build": f"{LABEL_PREFIX}in-build",
    "Validating": f"{LABEL_PREFIX}validating",
    "Released": f"{LABEL_PREFIX}released",
}


def _gh_available() -> bool:
    try:
        subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            check=True,
            timeout=10,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def _run_gh(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        timeout=60,
    )


def _issue_title(item: BacklogItem) -> str:
    if item.id:
        return f"[{item.id}] {item.title}"
    return f"[Discovery] {item.title}"


def _issue_body(item: BacklogItem) -> str:
    lines = [
        "<!-- sdd-sync -->",
        f"**Estado SDD:** {item.section}",
        f"**Dominio:** {item.domain}",
        f"**Versión objetivo:** {item.version}",
    ]
    if item.extra:
        lines.append(f"**Spec:** {item.extra}")
    return "\n".join(lines)


def _parse_issue_state(labels: list[str]) -> str | None:
    for label in labels:
        if label.startswith(LABEL_PREFIX):
            slug = label[len(LABEL_PREFIX) :]
            mapping = {
                "discovery": "Discovery",
                "draft": "Draft",
                "ready": "Ready",
                "in-build": "In Build",
                "validating": "Validating",
                "released": "Released",
            }
            return mapping.get(slug)
    return None


def push_to_github(backlog_path: Path, dry_run: bool = False) -> int:
    if not _gh_available():
        print("ERROR: gh CLI no encontrado. Instala GitHub CLI y autentica con `gh auth login`.")
        return 1

    backlog = parse_backlog(backlog_path)
    created = updated = 0

    result = _run_gh(["issue", "list", "--limit", "200", "--json", "number,title,labels,body"])
    if result.returncode != 0:
        print(f"ERROR: {result.stderr.strip()}")
        return 1

    existing = json.loads(result.stdout or "[]")
    by_id: dict[str, dict] = {}
    for issue in existing:
        m = re.search(r"\[(SDD-\d+)\]", issue.get("title", ""))
        if m:
            by_id[m.group(1)] = issue

    for item in backlog.all_items():
        if item.section == "Descartado":
            continue
        if not item.id and item.section != "Discovery":
            continue

        title = _issue_title(item)
        body = _issue_body(item)
        labels = [STATE_LABELS.get(item.section, f"{LABEL_PREFIX}draft"), "sdd"]

        if item.id and item.id in by_id:
            issue = by_id[item.id]
            num = issue["number"]
            if dry_run:
                print(f"UPDATE issue #{num}: {title}")
            else:
                _run_gh(["issue", "edit", str(num), "--title", title, "--body", body])
                _run_gh(["issue", "edit", str(num), "--add-label", ",".join(labels)])
            updated += 1
        else:
            if dry_run:
                print(f"CREATE: {title}")
            else:
                r = _run_gh(
                    [
                        "issue",
                        "create",
                        "--title",
                        title,
                        "--body",
                        body,
                        "--label",
                        labels[0],
                    ]
                )
                if r.returncode != 0:
                    print(f"WARN: {r.stderr.strip()}")
                else:
                    _run_gh(["issue", "edit", "--add-label", "sdd"])
            created += 1

    print(f"Sync push: {created} creados, {updated} actualizados")
    return 0


def pull_from_github(backlog_path: Path, dry_run: bool = False) -> int:
    if not _gh_available():
        print("ERROR: gh CLI no encontrado.")
        return 1

    backlog = parse_backlog(backlog_path)
    result = _run_gh(["issue", "list", "--label", "sdd", "--limit", "200", "--json", "title,labels,state"])
    if result.returncode != 0:
        print(f"ERROR: {result.stderr.strip()}")
        return 1

    issues = json.loads(result.stdout or "[]")
    changes = 0

    for issue in issues:
        m = re.search(r"\[(SDD-\d+)\]", issue.get("title", ""))
        if not m:
            continue
        spec_id = m.group(1)
        labels = [lb["name"] for lb in issue.get("labels", [])]
        new_state = _parse_issue_state(labels)
        if not new_state:
            continue

        item = backlog.find_by_id(spec_id)
        if item and item.section != new_state and new_state != "Released":
            print(f"  {spec_id}: {item.section} -> {new_state}")
            if not dry_run:
                backlog.sections[item.section] = [
                    i for i in backlog.sections.get(item.section, []) if i.id != spec_id
                ]
                item.section = new_state
                backlog.sections.setdefault(new_state, []).append(item)
            changes += 1

    if changes and not dry_run:
        write_backlog(backlog)
    print(f"Sync pull: {changes} cambio(s) de estado")
    return 0
