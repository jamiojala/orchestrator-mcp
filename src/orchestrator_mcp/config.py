"""Configuration loading and project defaults."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in minimal environments
    yaml = None  # type: ignore[assignment]


DEFAULT_CONFIG_NAME = "orchestrator-mcp.yaml"

DEFAULT_PROVIDER_PRICING: dict[str, dict[str, float]] = {
    "ollama": {"input_per_1k": 0.0, "output_per_1k": 0.0, "relative_cost_weight": 0.05},
    "nvidia": {"input_per_1k": 0.02, "output_per_1k": 0.06, "relative_cost_weight": 0.55},
    "gemini": {"input_per_1k": 0.018, "output_per_1k": 0.05, "relative_cost_weight": 0.45},
}


@dataclass(slots=True)
class BudgetConfig:
    daily_usd: float = 5.0
    weekly_usd: float = 20.0
    poor_mans_mode: bool = False


@dataclass(slots=True)
class ProjectConfig:
    project: str
    repo_root: Path
    config_path: Path | None
    skills_dir: Path
    state_dir: Path
    budgets: BudgetConfig
    pricing: dict[str, dict[str, float]]
    models: dict[str, Any]
    workflows: dict[str, Any]


def default_state_dir(app_name: str = "orchestrator-mcp") -> Path:
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / app_name
    if sys.platform.startswith("win"):
        return Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local")) / app_name
    return home / ".local" / "state" / app_name


def find_repo_root(start: Path | None = None) -> Path:
    cursor = (start or Path.cwd()).resolve()
    for candidate in [cursor, *cursor.parents]:
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return cursor


def _load_yaml(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read orchestrator-mcp.yaml. Install with: pip install PyYAML")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_project_config(config_path: Path | None = None, cwd: Path | None = None) -> ProjectConfig:
    repo_root = find_repo_root(cwd)
    resolved_config_path = config_path or (repo_root / DEFAULT_CONFIG_NAME)
    raw = _load_yaml(resolved_config_path if resolved_config_path.exists() else None)

    budgets_raw = raw.get("budgets", {})
    budgets = BudgetConfig(
        daily_usd=float(budgets_raw.get("daily_usd", 5.0)),
        weekly_usd=float(budgets_raw.get("weekly_usd", 20.0)),
        poor_mans_mode=bool(budgets_raw.get("poor_mans_mode", False)),
    )

    state_dir_value = raw.get("state_dir")
    state_dir = Path(state_dir_value).expanduser() if state_dir_value else default_state_dir()

    skills_dir_value = raw.get("skills_dir", "./skills")
    skills_dir = (repo_root / skills_dir_value).resolve() if not Path(skills_dir_value).is_absolute() else Path(skills_dir_value)

    pricing = DEFAULT_PROVIDER_PRICING | raw.get("pricing", {})

    return ProjectConfig(
        project=str(raw.get("project", "orchestrator-mcp")),
        repo_root=repo_root,
        config_path=resolved_config_path if resolved_config_path.exists() else None,
        skills_dir=skills_dir,
        state_dir=state_dir,
        budgets=budgets,
        pricing=pricing,
        models=raw.get("models", {}),
        workflows=raw.get("workflows", {}),
    )


def provider_env_status() -> dict[str, bool]:
    return {
        "gemini": bool(os.environ.get("GEMINI_API_KEY")),
        "nvidia": bool(os.environ.get("NVIDIA_API_KEY")),
        "ollama": bool(os.environ.get("OLLAMA_API_KEY")),
    }


def config_summary(config: ProjectConfig) -> dict[str, Any]:
    return {
        "project": config.project,
        "repo_root": str(config.repo_root),
        "config_path": str(config.config_path) if config.config_path else None,
        "skills_dir": str(config.skills_dir),
        "state_dir": str(config.state_dir),
        "provider_env": provider_env_status(),
        "budgets": {
            "daily_usd": config.budgets.daily_usd,
            "weekly_usd": config.budgets.weekly_usd,
            "poor_mans_mode": config.budgets.poor_mans_mode,
        },
    }
