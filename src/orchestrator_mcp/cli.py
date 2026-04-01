"""CLI entrypoints for serving, diagnostics, benchmarking, and cinematic workflows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import config_summary, load_project_config
from .content import CODEX_DUAL_MODE_FRAMEWORK
from .models import ComplexityInput, OrchestrateInput, TaskType
from .routing import build_complexity_payload, build_delegations
from .safety import scan_public_release_tree
from .server import build_server
from .skills import SkillRegistry
from .state import StateStore


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
    config = load_project_config(Path(args.config) if args.config else None)
    registry = SkillRegistry(config.skills_dir)
    registry.load()
    findings = scan_public_release_tree(config.repo_root)
    payload = config_summary(config)
    payload["skill_count"] = len(registry.all())
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
    print(json.dumps({"benchmark": "router-smoke", "results": results, "skills": registry.summary()}, indent=2))
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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
