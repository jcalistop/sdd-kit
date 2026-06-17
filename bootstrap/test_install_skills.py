#!/usr/bin/env python3
"""Tests mínimos para instalación de skills SDD."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

BOOTSTRAP = Path(__file__).resolve().parent
sys.path.insert(0, str(BOOTSTRAP))

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "install_agents",
    BOOTSTRAP / "install-agents.py",
)
assert _spec and _spec.loader
ia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ia)


class InstallSkillsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.target = Path(self._tmp.name)
        (self.target / ".github" / "docs" / "sdd").mkdir(parents=True)
        (self.target / ".github" / "docs" / "sdd" / "sdd.config.yaml").write_text(
            "project:\n  development_branch: dev\n",
            encoding="utf-8",
        )
        (self.target / ".cursor" / "skills" / "laravel-best-practices").mkdir(parents=True)
        (self.target / ".cursor" / "skills" / "laravel-best-practices" / "SKILL.md").write_text(
            "boost skill",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_install_cursor_skills_renders_placeholders(self) -> None:
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)

        skill_file = self.target / ".cursor" / "skills" / "sdd-draft-spec" / "SKILL.md"
        self.assertTrue(skill_file.is_file())
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn(".github/docs/sdd", content)
        self.assertNotIn("{{SDD_PATH}}", content)
        self.assertNotIn("Backoffice v2", content)

    def test_install_does_not_remove_non_sdd_skills(self) -> None:
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)

        boost_skill = self.target / ".cursor" / "skills" / "laravel-best-practices" / "SKILL.md"
        self.assertTrue(boost_skill.is_file())
        self.assertEqual(boost_skill.read_text(encoding="utf-8"), "boost skill")

    def test_manifest_marker_written(self) -> None:
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)

        marker = self.target / ".cursor" / "skills" / ".sdd-kit-manifest.json"
        self.assertTrue(marker.is_file())
        data = json.loads(marker.read_text(encoding="utf-8"))
        self.assertIn("sdd-draft-spec", data["managed_skills"])

    def test_build_skills_map_table(self) -> None:
        table = ia.build_skills_map_table()
        self.assertIn("sdd-build-spec", table)
        self.assertIn("build-spec", table)

    def test_update_sdd_config_preserves_kit_block(self) -> None:
        config_path = self.target / ".github" / "docs" / "sdd" / "sdd.config.yaml"
        config_path.write_text(
            "project:\n  name: Test\n\n"
            "agent:\n  targets: [claude]\n  install_mode: auto\n\n"
            'kit:\n  installed_version: "v1.2.0"\n  installed_at: "2026-06-15"\n',
            encoding="utf-8",
        )

        ia.update_sdd_config(self.target, ".github/docs/sdd", ["cursor"], "explicit")

        content = config_path.read_text(encoding="utf-8")
        self.assertIn('installed_version: "v1.2.0"', content)
        self.assertIn('installed_at: "2026-06-15"', content)
        self.assertIn("targets: [cursor]", content)
        self.assertIn("install_mode: explicit", content)
        self.assertNotIn("targets: [claude]", content)


if __name__ == "__main__":
    unittest.main()
