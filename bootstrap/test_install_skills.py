#!/usr/bin/env python3
"""Tests mínimos para instalación de skills SDD."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_default_branching_mode_feature_pr_dev(self) -> None:
        """Sin branching_mode: fragmento feature-pr-dev; sin placeholder crudo."""
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)

        for rel in (
            "sdd-build-spec/SKILL.md",
            "sdd-build-spec/reference.md",
            "sdd-open-pr/SKILL.md",
            "sdd-open-pr/reference.md",
        ):
            content = (self.target / ".cursor" / "skills" / rel).read_text(encoding="utf-8")
            self.assertIn("feature-pr-dev", content, rel)
            self.assertNotIn("{{BRANCHING_RULES}}", content, rel)
            self.assertIn("confirmación escrita", content, rel)

    def test_solo_push_dev_branching_mode(self) -> None:
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        config = self.target / sdd_path / "sdd.config.yaml"
        config.write_text(
            "project:\n  development_branch: develop\n"
            "agent:\n  branching_mode: solo-push-dev\n",
            encoding="utf-8",
        )
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)

        content = (
            self.target / ".cursor" / "skills" / "sdd-build-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("solo-push-dev", content)
        self.assertIn("develop", content)
        self.assertNotIn("{{BRANCHING_RULES}}", content)
        self.assertNotIn("{{DEV_BRANCH}}", content)

    def test_removes_global_managed_preserves_other(self) -> None:
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        with tempfile.TemporaryDirectory() as home_tmp:
            fake_home = Path(home_tmp)
            global_skills = fake_home / ".cursor" / "skills"
            managed = global_skills / "sdd-draft-spec"
            managed.mkdir(parents=True)
            (managed / "SKILL.md").write_text("global stale", encoding="utf-8")
            other = global_skills / "other-skill"
            other.mkdir()
            (other / "SKILL.md").write_text("keep me", encoding="utf-8")

            with patch.object(ia.Path, "home", return_value=fake_home):
                ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)

            self.assertFalse(managed.exists(), "managed global debió borrarse")
            self.assertTrue(other.is_dir())
            self.assertEqual((other / "SKILL.md").read_text(encoding="utf-8"), "keep me")

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
        self.assertEqual(data["profile"], "laravel-filament")
        self.assertEqual(data["kit_path"], kit_path)

    def test_profile_rendered_no_placeholders(self) -> None:
        """Install perfil A deja A en skills y sin placeholders crudos."""
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        ia.install_cursor_skills(self.target, "laravel-voyager", sdd_path, kit_path)

        content = (
            self.target / ".cursor" / "skills" / "sdd-build-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("sdd-stack-laravel-voyager", content)
        self.assertNotIn("{{PROFILE}}", content)
        self.assertNotIn("{{STACK_PROFILE}}", content)

        ctx = ia.skill_render_context(self.target, "laravel-voyager", sdd_path, kit_path)
        self.assertEqual(ctx["PROFILE"], "laravel-voyager")
        self.assertEqual(ctx["STACK_PROFILE"], "laravel-voyager")

    def test_profile_change_forces_reinstall(self) -> None:
        """Re-install con perfil B distinto fuerza rewrite a B."""
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)
        content_a = (
            self.target / ".cursor" / "skills" / "sdd-build-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("sdd-stack-laravel-filament", content_a)

        ia.install_cursor_skills(self.target, "laravel-voyager", sdd_path, kit_path)
        content_b = (
            self.target / ".cursor" / "skills" / "sdd-build-spec" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("sdd-stack-laravel-voyager", content_b)
        self.assertNotIn("sdd-stack-laravel-filament", content_b)
        marker = json.loads(
            (self.target / ".cursor" / "skills" / ".sdd-kit-manifest.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(marker["profile"], "laravel-voyager")

    def test_legacy_marker_without_profile_rerenders(self) -> None:
        """Marcador sin campo profile (legado) no hace skip."""
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)

        marker_path = self.target / ".cursor" / "skills" / ".sdd-kit-manifest.json"
        data = json.loads(marker_path.read_text(encoding="utf-8"))
        del data["profile"]
        marker_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        skill_file = self.target / ".cursor" / "skills" / "sdd-draft-spec" / "SKILL.md"
        skill_file.unlink()
        self.assertFalse(skill_file.is_file())

        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)
        self.assertTrue(
            skill_file.is_file(),
            "Marcador legado sin profile debió forzar re-render",
        )
        refreshed = json.loads(marker_path.read_text(encoding="utf-8"))
        self.assertEqual(refreshed["profile"], "laravel-filament")

    def test_templates_source_use_profile_placeholder(self) -> None:
        """Plantillas fuente no hardcodean sdd-stack-<perfil> concreto."""
        skills_root = BOOTSTRAP / "agent-skills"
        for skill_dir in skills_root.iterdir():
            if not skill_dir.is_dir() or skill_dir.name == "stacks":
                continue
            for src in skill_dir.iterdir():
                if not src.is_file():
                    continue
                text = src.read_text(encoding="utf-8")
                if "sdd-stack-" in text:
                    self.assertIn(
                        "sdd-stack-{{PROFILE}}",
                        text,
                        f"{src} debe usar placeholder, no perfil hardcodeado",
                    )
                    self.assertNotRegex(
                        text,
                        r"sdd-stack-(?!\{\{PROFILE\}\})[a-z0-9-]+",
                        f"{src} no debe hardcodear un perfil concreto",
                    )

    def test_install_skills_skips_if_already_installed(self) -> None:
        """Skills no deben reinstalarse si ya existen en el proyecto."""
        sdd_path = ".github/docs/sdd"
        kit_path = ".github/docs/sdd-kit"

        # Primera instalación
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)
        marker = self.target / ".cursor" / "skills" / ".sdd-kit-manifest.json"
        self.assertTrue(marker.is_file())

        # Borramos una skill para verificar que NO se reinstala
        skill_file = self.target / ".cursor" / "skills" / "sdd-draft-spec" / "SKILL.md"
        skill_file.unlink()
        self.assertFalse(skill_file.is_file())

        # Segunda instalación — debe saltar porque el marcador ya existe
        ia.install_cursor_skills(self.target, "laravel-filament", sdd_path, kit_path)
        self.assertFalse(
            skill_file.is_file(),
            "La skill no debió reinstalarse: el marcador ya existía",
        )

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

    def test_install_cursor_emits_safe_git_rule(self) -> None:
        ia.install_cursor(self.target, "laravel-filament")
        rule = self.target / ".cursor" / "rules" / "sdd-safe-git.mdc"
        self.assertTrue(rule.is_file(), "sdd-safe-git.mdc debe emitirse")
        text = rule.read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", text)
        self.assertIn("Safe-Git", text)
        self.assertIn("safe_git", ia.load_manifest())


if __name__ == "__main__":
    unittest.main()
