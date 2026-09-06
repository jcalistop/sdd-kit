"""CLI wrapper: prompt show id inexistente."""

from __future__ import annotations

import sys
from argparse import Namespace
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]
if str(CLI_ROOT) not in sys.path:
    sys.path.insert(0, str(CLI_ROOT))

import sdd as sdd_cli  # noqa: E402


def test_prompt_show_cli_unknown_exits_1(sdd_fixture: Path, capsys) -> None:
    args = Namespace(sdd_path=str(sdd_fixture), prompt_id="no-existe-xyz", full=False)
    code = sdd_cli.cmd_prompt_show(args)
    assert code == 1
    err = capsys.readouterr().err
    assert "no encontrado" in err.lower() or "no-existe" in err
