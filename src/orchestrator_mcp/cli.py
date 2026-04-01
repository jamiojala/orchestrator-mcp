"""CLI entrypoints for serving, diagnostics, benchmarking, and cinematic workflows."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from .config import config_summary, load_project_config
from .content import CODEX_DUAL_MODE_FRAMEWORK
from .marketplace import export_skill_pack, get_marketplace_skill, list_marketplace_skills, marketplace_summary
from .models import ComplexityInput, OrchestrateInput, TaskType
from .routing import build_complexity_payload, build_delegations
from .safety import scan_public_release_tree
from .server import build_server
from .skills import SkillRegistry
from .state import StateStore


def _load_registry(config_path: str | None) -> tuple[object, SkillRegistry]:
    config = load_project_config(Path(config_path) if config_path else None)
    registry = SkillRegistry(config.skills_dir)
    registry.load()
    return config, registry


def _run_dashboard() -> int:
    try:
        from streamlit.web.bootstrap import run as streamlit_run
    except ImportError:
        print("Streamlit is not installed. Install with: pip install 'orchestrator-mcp[dashboard]'", file=sys.stderr)
        return 1

    dashboard_path = Path(__file__).with_name("dashboard.py")
    streamlit_run(str(dashboard_path), "", [], {})
    return 0


def command_serve(args: argparse.Namespace) -> int:
    server = build_server(Path(args.config) if args.config else None)
    server.run()
    return 0


def command_dashboard(_: argparse.Namespace) -> int:
    return _run_dashboard()


def command_doctor(args: argparse.Namespace) -> int:
    config, registry = _load_registry(args.config)
    findings = scan_public_release_tree(config.repo_root)
    payload = config_summary(config)
    payload["skill_count"] = len(registry.all())
    payload["marketplace_skill_count"] = len(list_marketplace_skills())
    payload["public_release_findings"] = findings
    print(json.dumps(payload, indent=2))
    return 0 if not findings else 2


def command_benchmark(args: argparse.Namespace) -> int:
    config = load_project_config(Path(args.config) if args.config else None)
    store = StateStore(config.state_dir / "orchestrator-mcp.sqlite3")
    registry = SkillRegistry(config.skills_dir)
    registry.load()
    tasks = [
        {"task": "Build a new animated pricing page with strong TypeScript types", "file_count": 6, "estimated_changed_lines": 700, "needs_animation": True},
        {"task": "Fix a failing auth hook with a type regression", "file_count": 1, "estimated_changed_lines": 90},
        {"task": "Review a screenshot-based accessibility issue in a dashboard", "needs_visual_analysis": True},
    ]
    results = []
    for task in tasks:
        payload = build_complexity_payload(ComplexityInput.model_validate(task))
        results.append(payload)
    print(
        json.dumps(
            {
                "benchmark": "router-smoke",
                "results": results,
                "skills": registry.summary(),
                "marketplace_skill_count": len(list_marketplace_skills()),
            },
            indent=2,
        )
    )
    return 0


def command_cinematic_upgrade(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    config = load_project_config(Path(args.config) if args.config else None, cwd=target)
    store = StateStore(config.state_dir / "orchestrator-mcp.sqlite3")
    registry = SkillRegistry(config.skills_dir)
    registry.load()
    skill = registry.get("cinematic-upgrade")
    file_paths = [str(path.relative_to(target)) for path in target.rglob("*") if path.suffix in {".tsx", ".ts", ".jsx", ".js", ".css"}][:50]
    task = f"Create a cinematic upgrade plan for {target.name} with emphasis on premium motion and polish."
    plan_input = OrchestrateInput(
        task=task,
        task_type=TaskType.ARCHITECTURE,
        file_count=len(file_paths),
        estimated_changed_lines=len(file_paths) * 80,
        has_unknown_root_cause=False,
        needs_architecture=True,
        needs_animation=True,
        needs_visual_analysis=True,
        needs_copy=False,
        configured_only=True,
        skill_slug="cinematic-upgrade",
        repo_context="\n".join(file_paths[:20]),
        constraints=[
            "Keep the workflow non-mutating until approved.",
            "Prefer GPU-friendly animation guidance.",
            "Preserve user-facing meaning and accessibility.",
        ],
        preferred_mode=None,
    )
    plan = build_delegations(
        plan_input,
        config=config,
        store=store,
        skill_registry=registry,
    )
    payload = {
        "target": str(target),
        "matched_skill": skill.slug if skill else None,
        "files_considered": file_paths,
        "framework": CODEX_DUAL_MODE_FRAMEWORK,
        "delegations": plan,
    }
    print(json.dumps(payload, indent=2))
    return 0


def command_skills_list(args: argparse.Namespace) -> int:
    config, registry = _load_registry(args.config)
    installed = registry.summary() if args.source in {"installed", "all"} else []
    marketplace = marketplace_summary() if args.source in {"marketplace", "all"} else []
    if args.category:
        installed = [item for item in installed if item.get("category") == args.category]
        marketplace = [item for item in marketplace if item.get("category") == args.category]
    payload = {
        "source": args.source,
        "category": args.category,
        "installed_count": len(installed),
        "marketplace_count": len(marketplace),
        "installed": installed,
        "marketplace": marketplace,
        "skills_dir": str(config.skills_dir),
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print(f"Installed skills: {len(installed)}")
    for item in installed:
        print(f"- {item['slug']} ({item.get('category') or 'uncategorized'})")
    print(f"Marketplace skills: {len(marketplace)}")
    for item in marketplace:
        print(f"- {item['skill_id']} ({item['category']})")
    return 0


def command_skills_show(args: argparse.Namespace) -> int:
    _, registry = _load_registry(args.config)
    installed = registry.get(args.skill_id)
    marketplace = get_marketplace_skill(args.skill_id)
    if args.source == "installed" and installed is None:
        print(f"Skill not found in installed registry: {args.skill_id}", file=sys.stderr)
        return 1
    if args.source == "marketplace" and marketplace is None:
        print(f"Skill not found in marketplace: {args.skill_id}", file=sys.stderr)
        return 1
    payload: dict[str, object] = {"skill_id": args.skill_id}
    if installed is not None and args.source in {"installed", "all"}:
        payload["installed"] = installed.model_dump()
    if marketplace is not None and args.source in {"marketplace", "all"}:
        payload["marketplace"] = marketplace.marketplace_manifest()
    print(json.dumps(payload, indent=2))
    return 0


def _copy_installed_skill(skill_root: Path, destination_root: Path) -> Path:
    destination = destination_root / skill_root.name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(skill_root, destination)
    return destination


def command_skills_export(args: argparse.Namespace) -> int:
    config, registry = _load_registry(args.config)
    destination_root = Path(args.to).resolve()
    destination_root.mkdir(parents=True, exist_ok=True)

    if args.source in {"marketplace", "auto"}:
        marketplace_skill = get_marketplace_skill(args.skill_id)
        if marketplace_skill is not None:
            destination = export_skill_pack(marketplace_skill, destination_root)
            print(json.dumps({"source": "marketplace", "skill_id": args.skill_id, "destination": str(destination)}, indent=2))
            return 0

    if args.source in {"installed", "auto"}:
        installed_root = config.skills_dir / args.skill_id
        if installed_root.exists():
            destination = _copy_installed_skill(installed_root, destination_root)
            print(json.dumps({"source": "installed", "skill_id": args.skill_id, "destination": str(destination)}, indent=2))
            return 0

    print(f"Skill not found for export: {args.skill_id}", file=sys.stderr)
    return 1


def command_skills_export_category(args: argparse.Namespace) -> int:
    destination_root = Path(args.to).resolve()
    destination_root.mkdir(parents=True, exist_ok=True)
    skills = list_marketplace_skills(None if args.category == "all" else args.category)
    exported = [str(export_skill_pack(skill, destination_root)) for skill in skills]
    print(
        json.dumps(
            {
                "category": args.category,
                "count": len(exported),
                "destination_root": str(destination_root),
                "exported": exported,
            },
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orchestrator-mcp", description="A local-first multi-LLM orchestration platform.")
    parser.add_argument("--config", help="Path to orchestrator-mcp.yaml", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve = subparsers.add_parser("serve", help="Run the MCP server")
    serve.set_defaults(func=command_serve)

    dashboard = subparsers.add_parser("dashboard", help="Launch the observability dashboard")
    dashboard.set_defaults(func=command_dashboard)

    doctor = subparsers.add_parser("doctor", help="Check local configuration and public-release safety")
    doctor.set_defaults(func=command_doctor)

    benchmark = subparsers.add_parser("benchmark", help="Run a lightweight benchmark and router smoke test")
    benchmark.set_defaults(func=command_benchmark)

    cinematic = subparsers.add_parser("cinematic-upgrade", help="Generate a non-mutating cinematic upgrade plan")
    cinematic.add_argument("--path", required=True, help="Path to the target project")
    cinematic.set_defaults(func=command_cinematic_upgrade)

    skills = subparsers.add_parser("skills", help="Browse and export the built-in portable skill marketplace")
    skills_subparsers = skills.add_subparsers(dest="skills_command", required=True)

    skills_list = skills_subparsers.add_parser("list", help="List installed skills, marketplace skills, or both")
    skills_list.add_argument("--source", choices=["installed", "marketplace", "all"], default="all")
    skills_list.add_argument("--category", default=None)
    skills_list.add_argument("--json", action="store_true")
    skills_list.set_defaults(func=command_skills_list)

    skills_show = skills_subparsers.add_parser("show", help="Show one skill from the installed registry or marketplace")
    skills_show.add_argument("skill_id")
    skills_show.add_argument("--source", choices=["installed", "marketplace", "all"], default="all")
    skills_show.set_defaults(func=command_skills_show)

    skills_export = skills_subparsers.add_parser("export", help="Export one skill as a standalone portable pack")
    skills_export.add_argument("skill_id")
    skills_export.add_argument("--to", required=True, help="Destination directory")
    skills_export.add_argument("--source", choices=["auto", "installed", "marketplace"], default="auto")
    skills_export.set_defaults(func=command_skills_export)

    skills_export_category = skills_subparsers.add_parser("export-category", help="Export a whole marketplace category to standalone packs")
    skills_export_category.add_argument("--category", required=True, help="Marketplace category or 'all'")
    skills_export_category.add_argument("--to", required=True, help="Destination directory")
    skills_export_category.set_defaults(func=command_skills_export_category)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
