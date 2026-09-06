"""Tests backlog: parse y filtrado."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

CLI_ROOT = Path(__file__).resolve().parents[1]
if str(CLI_ROOT) not in sys.path:
    sys.path.insert(0, str(CLI_ROOT))

from lib.backlog import parse_backlog  # noqa: E402


def test_parse_backlog_lists_draft_and_discovery(sdd_fixture: Path) -> None:
    backlog = parse_backlog(sdd_fixture / "BACKLOG.md")
    assert backlog.next_id == 1
    draft_ids = [i.id for i in backlog.sections.get("Draft", [])]
    assert "SDD-010" in draft_ids
    disc = backlog.sections.get("Discovery", [])
    assert any(i.domain == "docs" for i in disc)


def test_filter_by_domain(sdd_fixture: Path) -> None:
    backlog = parse_backlog(sdd_fixture / "BACKLOG.md")
    cli_items = [
        i
        for i in backlog.all_items()
        if i.domain.lower() == "cli" and i.id
    ]
    assert len(cli_items) >= 1
    assert all(i.domain.lower() == "cli" for i in cli_items)


def test_malformed_draft_row_does_not_crash(malformed_backlog: Path) -> None:
    """Fila sin ID SDD- se ignora o no aborta el parseo."""
    backlog = parse_backlog(malformed_backlog / "BACKLOG.md")
    assert backlog.path.name == "BACKLOG.md"
    # No debe haber ítem con id inventado desde "not-an-id"
    assert all(
        (i.id is None or i.id.startswith("SDD-"))
        for i in backlog.all_items()
    )
