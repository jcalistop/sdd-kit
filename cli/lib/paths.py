"""Resolución de rutas del kit y la instancia SDD."""

from __future__ import annotations

import os
from pathlib import Path


def kit_root() -> Path:
    """Raíz del repositorio sdd-kit (padre de cli/)."""
    return Path(__file__).resolve().parent.parent.parent


def find_sdd_path(start: Path | None = None) -> Path:
    """Busca la instancia SDD: env SDD_PATH, .github/docs/sdd o ascendente."""
    if env := os.environ.get("SDD_PATH"):
        p = Path(env)
        if p.is_dir():
            return p.resolve()

    cwd = (start or Path.cwd()).resolve()
    candidates = [
        cwd / ".github" / "docs" / "sdd",
        cwd / "sdd",
    ]
    for c in candidates:
        if (c / "BACKLOG.md").is_file():
            return c.resolve()

    for parent in [cwd, *cwd.parents]:
        c = parent / ".github" / "docs" / "sdd"
        if (c / "BACKLOG.md").is_file():
            return c.resolve()

    return (cwd / ".github" / "docs" / "sdd").resolve()


def business_path(sdd_path: Path) -> Path:
    return sdd_path.parent.parent / "business"
