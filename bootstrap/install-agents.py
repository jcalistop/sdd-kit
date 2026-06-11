#!/usr/bin/env python3
"""Instala adaptadores de agente IA para SDD Kit (Cursor, Claude, Codex, Copilot)."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

VALID_AGENTS = ("cursor", "claude", "codex", "copilot")
DETECTION_THRESHOLD = 30
MARKER_START = "<!-- sdd-kit:agent-instructions:start -->"
MARKER_END = "<!-- sdd-kit:agent-instructions:end -->"


def kit_dir_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def bootstrap_dir() -> Path:
    return Path(__file__).resolve().parent


def load_template(name: str) -> str:
    path = bootstrap_dir() / "adapters" / name
    return path.read_text(encoding="utf-8")


def load_manifest() -> dict:
    path = bootstrap_dir() / "agent-prompts" / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_stack_descriptions() -> dict[str, str]:
    path = bootstrap_dir() / "agent-prompts" / "stack-descriptions.json"
    return json.loads(path.read_text(encoding="utf-8"))


def read_prompt(filename: str) -> str:
    path = bootstrap_dir() / "agent-prompts" / filename
    if not path.is_file():
        raise FileNotFoundError(f"Prompt no encontrado: {path}")
    return path.read_text(encoding="utf-8")


def read_stack_prompt(profile: str) -> str | None:
    path = bootstrap_dir() / "agent-prompts" / "stacks" / f"{profile}.md"
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def render_template(tpl: str, **kwargs: str) -> str:
    result = tpl
    for key, value in kwargs.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def combined_body(profile: str) -> str:
    manifest = load_manifest()
    parts = [
        read_prompt(manifest["core"]["file"]),
        read_prompt(manifest["workflow"]["file"]),
    ]
    stack = read_stack_prompt(profile)
    if stack:
        parts.append(stack)
    return "\n\n---\n\n".join(parts)


def merge_marked_block(existing: str, new_block: str) -> str:
    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        re.DOTALL,
    )
    if pattern.search(existing):
        return pattern.sub(new_block.strip(), existing)
    if existing.strip():
        return existing.rstrip() + "\n\n" + new_block
    return new_block


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def install_cursor(target: Path, profile: str) -> None:
    manifest = load_manifest()
    stack_desc = load_stack_descriptions()
    rules_dir = target / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    tpl = load_template("cursor-rule.mdc.tpl")

    items = [
        ("sdd-core.mdc", manifest["core"]["description"], manifest["core"]["file"]),
        (
            "sdd-agent-workflow.mdc",
            manifest["workflow"]["description"],
            manifest["workflow"]["file"],
        ),
    ]
    stack_body = read_stack_prompt(profile)
    if stack_body:
        desc = stack_desc.get(profile, f"SDD — perfil {profile}")
        items.append((f"sdd-stack-{profile}.mdc", desc, None))

    for filename, description, prompt_file in items:
        body = read_prompt(prompt_file) if prompt_file else stack_body or ""
        content = render_template(tpl, DESCRIPTION=description, BODY=body)
        write_file(rules_dir / filename, content)


def install_marked_file(
    target: Path,
    rel_path: str,
    preamble_tpl: str,
    profile: str,
    sdd_path: str,
) -> None:
    file_path = target / rel_path
    preamble = render_template(preamble_tpl, SDD_PATH=sdd_path)
    body = combined_body(profile)
    section_tpl = load_template("marked-section.tpl")
    new_block = render_template(section_tpl, PREAMBLE=preamble.strip(), BODY=body.strip())
    existing = file_path.read_text(encoding="utf-8") if file_path.is_file() else ""
    write_file(file_path, merge_marked_block(existing, new_block))


def install_claude(target: Path, profile: str, sdd_path: str) -> None:
    install_marked_file(
        target,
        "CLAUDE.md",
        load_template("preamble-claude.tpl"),
        profile,
        sdd_path,
    )


def install_codex(target: Path, profile: str, sdd_path: str) -> None:
    install_marked_file(
        target,
        "AGENTS.md",
        load_template("preamble-codex.tpl"),
        profile,
        sdd_path,
    )


def install_copilot(target: Path, profile: str, sdd_path: str) -> None:
    install_marked_file(
        target,
        ".github/copilot-instructions.md",
        load_template("preamble-copilot.tpl"),
        profile,
        sdd_path,
    )


def detect_agents(target: Path) -> dict[str, int]:
    scores = {name: 0 for name in VALID_AGENTS}

    if any(k.startswith("CURSOR_") for k in os.environ):
        scores["cursor"] += 40
    if (target / ".cursor").is_dir():
        scores["cursor"] += 25
    if shutil.which("cursor"):
        scores["cursor"] += 10

    if os.environ.get("CLAUDE_CODE"):
        scores["claude"] += 40
    if shutil.which("claude"):
        scores["claude"] += 15
    if (target / ".claude").is_dir():
        scores["claude"] += 20
    if (target / "CLAUDE.md").is_file():
        scores["claude"] += 15

    if (target / "AGENTS.md").is_file():
        scores["codex"] += 25
    if os.environ.get("CODEX_HOME") or os.environ.get("OPENAI_CODEX"):
        scores["codex"] += 35

    vscode = target / ".vscode"
    if vscode.is_dir():
        scores["copilot"] += 20
        ext = vscode / "extensions.json"
        if ext.is_file():
            text = ext.read_text(encoding="utf-8").lower()
            if "copilot" in text or "github.copilot" in text:
                scores["copilot"] += 25

    if scores["cursor"] >= 25:
        scores["copilot"] = max(0, scores["copilot"] - 15)

    return scores


def parse_agent_list(value: str) -> list[str]:
    if not value or value == "none":
        return []
    agents = [a.strip().lower() for a in value.split(",") if a.strip()]
    invalid = [a for a in agents if a not in VALID_AGENTS]
    if invalid:
        raise ValueError(f"Agentes no válidos: {', '.join(invalid)}. Opciones: {', '.join(VALID_AGENTS)}")
    return list(dict.fromkeys(agents))


def candidates_from_scores(scores: dict[str, int]) -> list[str]:
    return [name for name, score in scores.items() if score >= DETECTION_THRESHOLD]


def prompt_user(scores: dict[str, int]) -> list[str]:
    print("\nSDD Kit — selección de agente IA\n")
    if any(scores.values()):
        print("Detección (puntuación):")
        for name in VALID_AGENTS:
            if scores[name]:
                print(f"  {name}: {scores[name]}")
        print()

    options = list(VALID_AGENTS) + ["none"]
    for i, name in enumerate(options, 1):
        label = "Omitir instalación de reglas" if name == "none" else name
        print(f"  {i}. {label}")
    print("  6. Varios (separados por coma, ej. cursor,copilot)")
    print()

    detected = candidates_from_scores(scores)
    default_hint = ",".join(detected) if detected else "none"
    try:
        raw = input(f"Elige opción [1-6] o agentes (default: {default_hint}): ").strip()
    except EOFError:
        return detected

    if not raw:
        return detected

    if raw in {"1", "2", "3", "4", "5"}:
        choice = options[int(raw) - 1]
        return [] if choice == "none" else [choice]

    if raw == "6":
        try:
            multi = input("Agentes (cursor,claude,codex,copilot): ").strip()
        except EOFError:
            return detected
        return parse_agent_list(multi) if multi else detected

    return parse_agent_list(raw)


def resolve_agents(
    agent_arg: str,
    target: Path,
    no_prompt: bool,
) -> tuple[list[str], str]:
    if agent_arg == "none":
        return [], "none"

    if agent_arg != "auto":
        return parse_agent_list(agent_arg), "explicit"

    scores = detect_agents(target)
    winners = candidates_from_scores(scores)

    if len(winners) == 1:
        return winners, "auto"

    if no_prompt or not sys.stdin.isatty():
        if len(winners) == 1:
            return winners, "auto"
        if winners:
            print(
                "SDD Kit: detección ambigua; use --agent cursor,claude,... o ejecute sin --no-prompt.",
                file=sys.stderr,
            )
        else:
            print(
                "SDD Kit: no se detectó agente; use --agent o ejecute en terminal interactiva.",
                file=sys.stderr,
            )
        return [], "auto"

    selected = prompt_user(scores)
    return selected, "auto"


def update_sdd_config(target: Path, sdd_path: str, agents: list[str], install_mode: str) -> None:
    config_path = target / sdd_path / "sdd.config.yaml"
    if not config_path.is_file():
        return

    lines = config_path.read_text(encoding="utf-8").splitlines()
    agent_block = [
        "",
        "agent:",
        f"  targets: [{', '.join(agents)}]" if agents else "  targets: []",
        f"  install_mode: {install_mode}",
    ]

    out: list[str] = []
    skip = False
    has_agent = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("agent:"):
            has_agent = True
            skip = True
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                i += 1
            continue
        if not skip:
            out.append(line)
        i += 1

    if has_agent:
        out.extend(agent_block)
    else:
        out.extend(agent_block)

    config_path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


def install_agents(
    target: Path,
    kit: Path,
    profile: str,
    agents: list[str],
    sdd_path: str,
    install_mode: str,
) -> None:
    if not agents:
        print("SDD Kit: sin adaptadores de agente instalados.")
        return

    stack_path = bootstrap_dir() / "agent-prompts" / "stacks" / f"{profile}.md"
    if not stack_path.is_file():
        print(f"Advertencia: sin prompt de stack para perfil '{profile}'.", file=sys.stderr)

    installers = {
        "cursor": lambda: install_cursor(target, profile),
        "claude": lambda: install_claude(target, profile, sdd_path),
        "codex": lambda: install_codex(target, profile, sdd_path),
        "copilot": lambda: install_copilot(target, profile, sdd_path),
    }

    for name in agents:
        installers[name]()
        print(f"SDD Kit: adaptador '{name}' instalado.")

    update_sdd_config(target, sdd_path, agents, install_mode)


def cmd_install(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    kit = Path(args.kit).resolve() if args.kit else kit_dir_from_script()
    agent_arg = args.agent
    if args.cursor:
        agent_arg = "cursor"

    try:
        agents, install_mode = resolve_agents(agent_arg, target, args.no_prompt)
        install_agents(target, kit, args.profile, agents, args.sdd_path, install_mode)
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


def cmd_detect(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    scores = detect_agents(target)
    for name in VALID_AGENTS:
        print(f"{name}: {scores[name]}")
    winners = candidates_from_scores(scores)
    if winners:
        print(f"candidatos: {', '.join(winners)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Instalador multi-agente SDD Kit")
    sub = parser.add_subparsers(dest="command", required=True)

    install_p = sub.add_parser("install", help="Instalar adaptadores de agente")
    install_p.add_argument("--target", default=".", help="Raíz del proyecto destino")
    install_p.add_argument("--kit", default=None, help="Ruta al sdd-kit")
    install_p.add_argument("--profile", default="laravel-filament", help="Perfil stack")
    install_p.add_argument(
        "--agent",
        default="auto",
        help="auto | none | cursor | claude | codex | copilot | lista separada por comas",
    )
    install_p.add_argument("--sdd-path", default=".github/docs/sdd", help="Ruta instancia SDD")
    install_p.add_argument("--no-prompt", action="store_true", help="Sin menú interactivo (CI)")
    install_p.add_argument(
        "--cursor",
        action="store_true",
        help="Alias de --agent cursor (retrocompat)",
    )
    install_p.set_defaults(func=cmd_install)

    detect_p = sub.add_parser("detect", help="Mostrar puntuación de detección")
    detect_p.add_argument("--target", default=".", help="Raíz del proyecto destino")
    detect_p.set_defaults(func=cmd_detect)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
