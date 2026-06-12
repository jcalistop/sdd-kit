#!/usr/bin/env python3
"""CLI SDD — Spec-Driven Development toolkit."""

from __future__ import annotations

import argparse
import platform
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backlog import (  # noqa: E402
    TRANSITIONS,
    add_draft_item,
    format_id,
    parse_backlog,
    slugify,
    write_backlog,
)
from lib.changelog import generate_changelog  # noqa: E402
from lib.github_sync import pull_from_github, push_to_github  # noqa: E402
from lib.metrics import collect_metrics, format_metrics_report  # noqa: E402
from lib.paths import find_sdd_path, kit_root  # noqa: E402
from lib.prompts import (  # noqa: E402
    format_prompt_list,
    format_prompt_show,
    get_prompt,
    load_all_prompts,
)


def cmd_init(args: argparse.Namespace) -> int:
    root = kit_root()
    agent = "cursor" if args.cursor else args.agent
    if platform.system() == "Windows":
        script = root / "bootstrap" / "init-sdd.ps1"
        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
            "-Profile",
            args.profile,
            "-Project",
            args.project,
            "-Agent",
            agent,
        ]
        if args.cursor:
            cmd.append("-Cursor")
        if args.no_prompt:
            cmd.append("-NoPrompt")
        if args.sdd_path:
            cmd.extend(["-SddPath", args.sdd_path])
    else:
        script = root / "bootstrap" / "init-sdd.sh"
        cmd = [
            str(script),
            "--profile",
            args.profile,
            "--project",
            args.project,
            "--agent",
            agent,
        ]
        if args.cursor:
            cmd.append("--cursor")
        if args.no_prompt:
            cmd.append("--no-prompt")
        if args.sdd_path:
            cmd.extend(["--sdd-path", args.sdd_path])
    return subprocess.call(cmd, cwd=Path.cwd())


def cmd_validate(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    root = kit_root()
    if platform.system() == "Windows":
        script = root / "bootstrap" / "validate-sdd.ps1"
        return subprocess.call(
            ["powershell", "-NoProfile", "-File", str(script), "-SddPath", str(sdd)]
        )
    script = root / "bootstrap" / "validate-sdd.sh"
    return subprocess.call([str(script), str(sdd)])


def cmd_backlog_list(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    backlog = parse_backlog(sdd / "BACKLOG.md")

    print(f"BACKLOG — {backlog.path}")
    print(f"Próximo ID: {format_id(backlog.next_id)}\n")

    for item in backlog.all_items():
        if args.state and item.section.lower() != args.state.lower().replace("-", " "):
            if item.section.lower() != args.state.lower():
                continue
        if args.domain and item.domain.lower() != args.domain.lower():
            continue
        sid = item.id or "—"
        print(f"  [{item.section:12}] {sid:10} {item.domain:8} {item.title}")

    return 0


def cmd_backlog_sync(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    backlog_path = sdd / "BACKLOG.md"
    code = 0
    if args.direction in ("push", "both"):
        code |= push_to_github(backlog_path, dry_run=args.dry_run)
    if args.direction in ("pull", "both"):
        code |= pull_from_github(backlog_path, dry_run=args.dry_run)
    return code


def cmd_spec_new(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    backlog_path = sdd / "BACKLOG.md"
    backlog = parse_backlog(backlog_path)

    cfg_path = sdd / "sdd.config.yaml"
    if cfg_path.is_file() and args.domain not in cfg_path.read_text(encoding="utf-8"):
        print(f"WARN: dominio '{args.domain}' no aparece en sdd.config.yaml")

    spec_id = format_id(backlog.next_id)
    slug = slugify(args.title)
    rel_spec = f"specs/{args.domain}/{spec_id}-{slug}.md"
    spec_path = sdd / rel_spec

    if spec_path.exists():
        print(f"ERROR: ya existe {spec_path}")
        return 1

    template = sdd / "templates" / "spec-template.md"
    if not template.is_file():
        template = kit_root() / "core" / "templates" / "spec-template.md"

    content = template.read_text(encoding="utf-8")
    today = __import__("datetime").date.today().isoformat()
    content = content.replace("SDD-NNN", spec_id)
    content = content.replace("YYYY-MM-DD", today)
    content = re.sub(
        r"\| \*\*Dominio\*\*.*\|",
        f"| **Dominio**           | `{args.domain}`                                               |",
        content,
        count=1,
    )
    content = re.sub(
        r"\| \*\*Tipo\*\*.*\|",
        f"| **Tipo**              | `{args.type}` |",
        content,
        count=1,
    )
    content = re.sub(
        r"\| \*\*Versión objetivo\*\*.*\|",
        f"| **Versión objetivo**  | {args.version}                                            |",
        content,
        count=1,
    )
    content = re.sub(
        r"\| \*\*Estado\*\*.*\|",
        "| **Estado**            | `Draft` |",
        content,
        count=1,
    )

    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(content, encoding="utf-8")

    link = f"[{rel_spec}]({rel_spec})"
    add_draft_item(backlog, args.domain, args.title, args.version, link)
    write_backlog(backlog)

    print(f"Spec creado: {spec_path}")
    print(f"BACKLOG actualizado: {spec_id} en Draft")
    return 0


def cmd_spec_status(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    backlog = parse_backlog(sdd / "BACKLOG.md")
    item = backlog.find_by_id(args.spec_id.upper())

    if not item:
        print(f"ERROR: {args.spec_id} no encontrado en BACKLOG")
        return 1

    print(f"ID:      {item.id}")
    print(f"Estado:  {item.section}")
    print(f"Dominio: {item.domain}")
    print(f"Título:  {item.title}")
    print(f"Versión: {item.version}")

    spec_files = list((sdd / "specs").rglob(f"{item.id}-*.md")) if (sdd / "specs").is_dir() else []
    arch_files = list((sdd / "archive").rglob(f"{item.id}-*.md")) if (sdd / "archive").is_dir() else []
    if spec_files:
        print(f"Spec:    {spec_files[0].relative_to(sdd)}")
    elif arch_files:
        print(f"Archivo: {arch_files[0].relative_to(sdd)}")

    next_states = TRANSITIONS.get(item.section, [])
    if next_states:
        print(f"\nTransiciones posibles: {', '.join(next_states)}")
    else:
        print("\nSin transiciones (estado terminal).")

    return 0


def cmd_release_changelog(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    out = Path(args.output) if args.output else None
    path = generate_changelog(sdd, out)
    print(f"CHANGELOG generado: {path}")
    return 0


def cmd_release_close(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    version = args.version if args.version.startswith("v") else f"v{args.version}"
    release_dir = sdd / "releases" / version
    note = release_dir / f"release_{version}.md"

    errors: list[str] = []
    if not release_dir.is_dir():
        errors.append(f"Falta carpeta {release_dir}")
    if not note.is_file():
        errors.append(f"Falta nota {note}")

    backlog = parse_backlog(sdd / "BACKLOG.md")
    active = sum(
        len(backlog.sections.get(s, []))
        for s in ["Draft", "Ready", "In Build", "Validating"]
    )
    if active > 0 and not args.force:
        errors.append(f"Hay {active} ítem(s) activos en BACKLOG (usa --force para ignorar)")

    specs_active = list((sdd / "specs").rglob("SDD-*.md")) if (sdd / "specs").is_dir() else []
    if specs_active and not args.force:
        errors.append(
            f"Hay {len(specs_active)} spec(s) en specs/ sin archivar "
            "(mueve a archive/ antes del PR de campaña)"
        )

    if errors:
        print("Checklist de cierre — ERRORES:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1

    print(f"Checklist de cierre {version} — OK")
    if args.changelog:
        path = generate_changelog(sdd)
        print(f"CHANGELOG actualizado: {path}")
    return 0


def cmd_prompt_list(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    prompts = load_all_prompts(sdd)
    print(format_prompt_list(prompts, category=args.category, phase=args.phase))
    return 0


def cmd_prompt_show(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    meta = get_prompt(args.prompt_id, sdd)
    if meta is None:
        print(f"Error: prompt '{args.prompt_id}' no encontrado.", file=sys.stderr)
        print("Usa `sdd prompt list` para ver IDs disponibles.", file=sys.stderr)
        return 1
    print(format_prompt_show(meta, full=args.full), end="")
    return 0


def cmd_metrics(args: argparse.Namespace) -> int:
    sdd = Path(args.sdd_path) if args.sdd_path else find_sdd_path()
    metrics = collect_metrics(sdd, stagnant_days=args.stagnant_days)
    report = format_metrics_report(metrics, markdown=args.markdown)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Métricas guardadas: {args.output}")
    else:
        print(report)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sdd",
        description="SDD Kit CLI — Spec-Driven Development",
    )
    p.add_argument(
        "--sdd-path",
        help="Ruta instancia SDD (default: .github/docs/sdd o SDD_PATH)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init", help="Inicializar SDD en el proyecto")
    init_p.add_argument("--profile", default="laravel-filament")
    init_p.add_argument("--project", default="Mi Proyecto")
    init_p.add_argument(
        "--agent",
        default="auto",
        help="auto | none | cursor | claude | codex | copilot | lista separada por comas",
    )
    init_p.add_argument(
        "--no-prompt",
        action="store_true",
        help="Sin menú interactivo de agente (CI)",
    )
    init_p.add_argument(
        "--cursor",
        action="store_true",
        help="Alias de --agent cursor (retrocompat)",
    )
    init_p.set_defaults(func=cmd_init)

    val_p = sub.add_parser("validate", help="Validar coherencia documental")
    val_p.set_defaults(func=cmd_validate)

    bl_p = sub.add_parser("backlog", help="Listar BACKLOG o subcomandos list/sync")
    bl_p.add_argument("--state", help="Filtrar por estado")
    bl_p.add_argument("--domain", help="Filtrar por dominio")
    bl_sub = bl_p.add_subparsers(dest="backlog_cmd")

    bl_sync = bl_sub.add_parser("sync", help="Sincronizar con GitHub Issues (gh)")
    bl_sync.add_argument(
        "--direction",
        choices=["push", "pull", "both"],
        default="both",
    )
    bl_sync.add_argument("--dry-run", action="store_true")
    bl_sync.set_defaults(func=cmd_backlog_sync)

    bl_p.set_defaults(func=cmd_backlog_list, backlog_cmd=None)

    sp_p = sub.add_parser("spec", help="Operaciones sobre specs")
    sp_sub = sp_p.add_subparsers(dest="spec_cmd", required=True)

    sp_new = sp_sub.add_parser("new", help="Crear spec Draft + entrada BACKLOG")
    sp_new.add_argument("--domain", required=True)
    sp_new.add_argument("--type", default="feature")
    sp_new.add_argument("--title", required=True)
    sp_new.add_argument("--version", default="v0.1.0")
    sp_new.set_defaults(func=cmd_spec_new)

    sp_st = sp_sub.add_parser("status", help="Estado y transiciones de un spec")
    sp_st.add_argument("spec_id", help="SDD-NNN")
    sp_st.set_defaults(func=cmd_spec_status)

    rel_p = sub.add_parser("release", help="Operaciones de release")
    rel_sub = rel_p.add_subparsers(dest="release_cmd", required=True)

    rel_cl = rel_sub.add_parser("changelog", help="Generar CHANGELOG.md")
    rel_cl.add_argument("-o", "--output", help="Ruta salida CHANGELOG.md")
    rel_cl.set_defaults(func=cmd_release_changelog)

    rel_close = rel_sub.add_parser("close", help="Verificar cierre de release")
    rel_close.add_argument("version", help="vX.Y.Z")
    rel_close.add_argument("--changelog", action="store_true", help="Regenerar CHANGELOG")
    rel_close.add_argument("--force", action="store_true")
    rel_close.set_defaults(func=cmd_release_close)

    met_p = sub.add_parser("metrics", help="Métricas de salud del proceso SDD")
    met_p.add_argument("--markdown", action="store_true")
    met_p.add_argument("-o", "--output", help="Guardar reporte en archivo")
    met_p.add_argument("--stagnant-days", type=int, default=14)
    met_p.set_defaults(func=cmd_metrics)

    pr_p = sub.add_parser("prompt", help="Catálogo de prompts copy-paste")
    pr_sub = pr_p.add_subparsers(dest="prompt_cmd", required=True)

    pr_list = pr_sub.add_parser("list", help="Listar prompts del catálogo")
    pr_list.add_argument(
        "--category",
        choices=["adoption", "workflow", "exceptions"],
        help="Filtrar por categoría",
    )
    pr_list.add_argument(
        "--phase",
        help="Filtrar por fase SDD (Draft, Ready, In Build, Validating, Released)",
    )
    pr_list.set_defaults(func=cmd_prompt_list)

    pr_show = pr_sub.add_parser("show", help="Mostrar prompt copy-paste")
    pr_show.add_argument("prompt_id", help="ID del prompt (ej. adopt-existing)")
    pr_show.add_argument(
        "--full",
        action="store_true",
        help="Mostrar ficha completa con contexto",
    )
    pr_show.set_defaults(func=cmd_prompt_show)

    return p


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "backlog" and getattr(args, "backlog_cmd", None) == "sync":
        return cmd_backlog_sync(args)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
