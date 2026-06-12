#!/usr/bin/env python3
"""Detección de versión del kit para init-sdd y validate-sdd."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def detect_kit_ref(kit_dir: Path) -> str:
    git_dir = kit_dir / ".git"
    if not git_dir.exists():
        return "unknown"
    try:
        exact = subprocess.run(
            ["git", "-C", str(kit_dir), "describe", "--tags", "--exact-match"],
            capture_output=True,
            text=True,
            check=False,
        )
        if exact.returncode == 0 and exact.stdout.strip():
            return exact.stdout.strip()
        desc = subprocess.run(
            ["git", "-C", str(kit_dir), "describe", "--tags", "--always"],
            capture_output=True,
            text=True,
            check=True,
        )
        return desc.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def resolve_kit_dir(project_root: Path) -> Path | None:
    submodule = project_root / "sdd-kit"
    if submodule.is_dir() and (submodule / "core").is_dir():
        return submodule.resolve()
    if (project_root / "core").is_dir() and (project_root / "bootstrap").is_dir():
        return project_root.resolve()
    return None


def parse_installed_version(config_text: str) -> str | None:
    in_kit = False
    for line in config_text.splitlines():
        if re.match(r"^\s*kit:\s*$", line):
            in_kit = True
            continue
        if in_kit and re.match(r"^\S", line) and not line.strip().startswith("#"):
            in_kit = False
        if in_kit:
            m = re.match(r'^\s*installed_version:\s*["\']?([^"\'\s#]+)', line)
            if m:
                value = m.group(1).strip()
                if value and not value.startswith("{{"):
                    return value
    return None


def versions_match(installed: str, detected: str) -> bool:
    if not installed or not detected or detected == "unknown":
        return True
    if installed == detected:
        return True
    return detected.startswith(installed)


def cmd_detect(kit_dir: str) -> int:
    print(detect_kit_ref(Path(kit_dir).resolve()))
    return 0


def cmd_check(sdd_path: str, project_root: str | None = None) -> int:
    sdd = Path(sdd_path).resolve()
    root = Path(project_root).resolve() if project_root else sdd.parent.parent.parent.resolve()
    config_path = sdd / "sdd.config.yaml"
    if not config_path.is_file():
        return 0

    installed = parse_installed_version(config_path.read_text(encoding="utf-8"))
    if not installed:
        return 0

    kit_dir = resolve_kit_dir(root)
    if not kit_dir:
        return 0

    detected = detect_kit_ref(kit_dir)
    if not versions_match(installed, detected):
        print(
            f"WARN:  kit.installed_version ({installed}) difiere del kit en disco ({detected})"
        )
        return 0

    print(f"OK:    kit.installed_version coherente con kit en disco ({detected})")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: kit-version.py detect <kit-dir> | check <sdd-path> [project-root]", file=sys.stderr)
        return 1
    cmd = sys.argv[1]
    if cmd == "detect" and len(sys.argv) >= 3:
        return cmd_detect(sys.argv[2])
    if cmd == "check" and len(sys.argv) >= 3:
        root = sys.argv[3] if len(sys.argv) >= 4 else None
        return cmd_check(sys.argv[2], root)
    print("Comando desconocido o argumentos insuficientes", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
