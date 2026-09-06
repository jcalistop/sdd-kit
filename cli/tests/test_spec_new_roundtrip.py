"""Round-trip: spec new → archivo + fila Draft."""

from __future__ import annotations

import sys
from argparse import Namespace
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]
if str(CLI_ROOT) not in sys.path:
    sys.path.insert(0, str(CLI_ROOT))

import sdd as sdd_cli  # noqa: E402
from lib.backlog import parse_backlog  # noqa: E402


def test_spec_new_round_trip(sdd_fixture: Path) -> None:
    # next_id en fixture es 1 → SDD-001
    args = Namespace(
        sdd_path=str(sdd_fixture),
        domain="cli",
        title="Round trip pytest",
        type="feature",
        version="v0.1.0",
    )
    code = sdd_cli.cmd_spec_new(args)
    assert code == 0

    spec = sdd_fixture / "specs" / "cli" / "SDD-001-round-trip-pytest.md"
    assert spec.is_file()
    text = spec.read_text(encoding="utf-8")
    assert "SDD-001" in text
    assert "`cli`" in text or "cli" in text

    backlog = parse_backlog(sdd_fixture / "BACKLOG.md")
    draft = [i for i in backlog.sections.get("Draft", []) if i.id == "SDD-001"]
    assert len(draft) == 1
    assert "Round trip pytest" in draft[0].title
    assert backlog.next_id == 2
