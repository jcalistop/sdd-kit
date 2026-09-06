"""Fixtures para tests de la CLI SDD."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

# Raíz del repo sdd-kit (cli/tests/ → parents[2])
KIT_ROOT = Path(__file__).resolve().parents[2]
CLI_ROOT = KIT_ROOT / "cli"


@pytest.fixture
def kit_root() -> Path:
    return KIT_ROOT


@pytest.fixture
def sdd_fixture(tmp_path: Path) -> Path:
    """Mini instancia SDD válida para parse_backlog / spec new."""
    sdd = tmp_path / ".github" / "docs" / "sdd"
    (sdd / "specs" / "cli").mkdir(parents=True)
    (sdd / "templates").mkdir(parents=True)

    backlog = textwrap.dedent(
        """\
        # Backlog SDD — fixture

        **Próximo ID disponible:** `SDD-001`.

        ---

        ## Discovery

        | Dominio | Idea / necesidad | Versión | Notas |
        | ------- | ---------------- | ------- | ----- |
        | docs | Idea discovery | — | nota |

        ## Draft

        | ID | Dominio | Título | Versión | Spec |
        | --- | ------- | ------ | ------- | ---- |
        | SDD-010 | cli | Spec draft fixture | v0.1.0 | [specs/cli/SDD-010-x.md](specs/cli/SDD-010-x.md) |

        ## Ready

        | ID | Dominio | Título | Versión | Spec |
        | --- | ------- | ------ | ------- | ---- |
        | — | — | — | — | — |

        ## In Build

        | ID | Dominio | Título | Versión | Spec |
        | --- | ------- | ------ | ------- | ---- |
        | — | — | — | — | — |

        ## Validating

        | ID | Dominio | Título | Versión | Spec |
        | --- | ------- | ------ | ------- | ---- |
        | — | — | — | — | — |

        ## Released

        | ID | Dominio | Título | Versión | Fecha | Spec archivado |
        | --- | ------- | ------ | ------- | ----- | -------------- |
        | — | — | — | — | — | — |

        ## Descartado / en pausa

        | ID | Dominio | Título | Razón | Fecha | Spec |
        | --- | ------- | ------ | ----- | ----- | ---- |
        | — | — | — | — | — | — |
        """
    )
    (sdd / "BACKLOG.md").write_text(backlog, encoding="utf-8")

    (sdd / "sdd.config.yaml").write_text(
        textwrap.dedent(
            """\
            project:
              name: "Fixture"
            domains:
              - cli
              - docs
            ids:
              next_sdd: 1
            """
        ),
        encoding="utf-8",
    )

    # Plantilla mínima para spec new
    (sdd / "templates" / "spec-template.md").write_text(
        textwrap.dedent(
            """\
            # Spec Template

            | Campo | Valor |
            | --- | --- |
            | **ID** | `SDD-NNN` |
            | **Dominio** | _(dominio)_ |
            | **Tipo** | `feature` |
            | **Fecha** | YYYY-MM-DD |
            | **Estado** | `Draft` |
            | **Versión objetivo** | vX.Y.Z |
            """
        ),
        encoding="utf-8",
    )

    # Spec referenciado en Draft (archivo opcional)
    (sdd / "specs" / "cli" / "SDD-010-x.md").write_text("# SDD-010 fixture\n", encoding="utf-8")

    return sdd


@pytest.fixture
def malformed_backlog(tmp_path: Path) -> Path:
    """BACKLOG con fila Draft sin columnas suficientes — parseable sin crash."""
    sdd = tmp_path / "sdd"
    sdd.mkdir()
    (sdd / "BACKLOG.md").write_text(
        textwrap.dedent(
            """\
            # Backlog

            **Próximo ID disponible:** `SDD-001`.

            ## Draft

            | ID | Dominio | Título | Versión | Spec |
            | --- | ------- | ------ | ------- | ---- |
            | not-an-id | x |
            """
        ),
        encoding="utf-8",
    )
    return sdd
