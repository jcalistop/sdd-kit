"""Tests prompt list / show."""

from __future__ import annotations

import sys
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]
if str(CLI_ROOT) not in sys.path:
    sys.path.insert(0, str(CLI_ROOT))

from lib.prompts import (  # noqa: E402
    format_prompt_list,
    format_prompt_show,
    get_prompt,
    load_all_prompts,
)


def test_prompt_list_non_empty(sdd_fixture: Path) -> None:
    prompts = load_all_prompts(sdd_fixture)
    assert len(prompts) > 0
    text = format_prompt_list(prompts)
    assert "Total:" in text
    assert "discovery-to-draft" in text or any(p.id for p in prompts)


def test_prompt_show_known_id(sdd_fixture: Path) -> None:
    meta = get_prompt("discovery-to-draft", sdd_fixture)
    assert meta is not None
    out = format_prompt_show(meta, full=False, sdd_path=sdd_fixture)
    assert out
    assert "Error:" not in out[:20]


def test_prompt_show_unknown_id_returns_none(sdd_fixture: Path) -> None:
    meta = get_prompt("no-existe-este-prompt-xyz", sdd_fixture)
    assert meta is None
