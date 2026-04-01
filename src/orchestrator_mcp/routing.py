"""Task typing, mode choice, and route selection."""

from __future__ import annotations

from typing import Any, Optional

from .config import ProjectConfig
from .content import SPECIALIST_REGISTRY
from .costs import order_routes_by_budget
from .models import ComplexityInput, ModelSelectionInput, OrchestrateInput, Provider, TaskType, WorkMode
from .providers import GEMINI_DEFAULT_MODEL, NVIDIA_DEFAULT_MODEL, OLLAMA_DEFAULT_MODEL, provider_is_configured
from .skills import SkillRegistry
from .state import StateStore


def infer_provider_from_model(model: str) -> Provider:
    if model.startswith("gemini-"):
        return Provider.GEMINI
    if ":" in model:
        return Provider.OLLAMA
    return Provider.NVIDIA


def infer_task_type(text: str, explicit: TaskType) -> TaskType:
    if explicit != TaskType.AUTO:
        return explicit
    lowered = text.lower()
    if any(token in lowered for token in ["screenshot", "mockup", "image", "visual", "figma", "a11y", "accessibility"]):
        return TaskType.VISUAL
    if any(token in lowered for token in ["headline", "tagline", "copy", "marketing text", "rewrite text"]):
        return TaskType.CONTENT
    if any(token in lowered for token in ["architecture", "refactor", "multi-file", "project structure", "state management"]):
        return TaskType.ARCHITECTURE
    if any(token in lowered for token in ["review", "audit", "regression", "compliance"]):
        return TaskType.REVIEW
    if any(token in lowered for token in ["debug", "bug", "root cause", "traceback", "failing"]):
        return TaskType.REASONING
    if any(token in lowered for token in ["quick", "fast", "rapid"]):
        return TaskType.SPEED
    return TaskType.CODE


def provider_defaults(provider: Provider, task_type: TaskType) -> list[str]:
    defaults: dict[Provider, dict[TaskType, list[str]]] = {
        Provider.GEMINI: {
            TaskType.AUTO: [GEMINI_DEFAULT_MODEL],
            TaskType.CODE: ["gemini-2.5-flash", "gemini-2.5-pro"],
            TaskType.REVIEW: ["gemini-2.5-pro", "gemini-2.5-flash"],
            TaskType.REASONING: ["gemini-2.5-pro", "gemini-2.5-flash"],
            TaskType.ARCHITECTURE: ["gemini-2.5-pro", "gemini-2.5-flash"],
            TaskType.VISUAL: ["gemini-2.5-pro", "gemini-2.5-flash"],
            TaskType.CONTENT: ["gemini-2.5-flash", "gemini-2.5-flash-lite"],
            TaskType.SPEED: ["gemini-2.5-flash", "gemini-2.5-flash-lite"],
        },
        Provider.NVIDIA: {
            TaskType.AUTO: [NVIDIA_DEFAULT_MODEL],
            TaskType.CODE: ["moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct"],
            TaskType.REVIEW: ["deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5"],
            TaskType.REASONING: ["deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5"],
            TaskType.ARCHITECTURE: ["moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2"],
            TaskType.VISUAL: ["microsoft/phi-4-multimodal-instruct", "moonshotai/kimi-k2.5"],
            TaskType.CONTENT: ["meta/llama-3.3-70b-instruct", "moonshotai/kimi-k2.5"],
            TaskType.SPEED: ["meta/llama-3.3-70b-instruct", "google/gemma-2-9b-it"],
        },
        Provider.OLLAMA: {
            TaskType.AUTO: [OLLAMA_DEFAULT_MODEL],
            TaskType.CODE: ["qwen3-coder:480b-cloud", "qwen2.5-coder:32b-cloud", "gpt-oss:120b"],
            TaskType.REVIEW: ["qwen3-coder:480b-cloud", "gpt-oss:120b"],
            TaskType.REASONING: ["deepseek-v3.1:671-cloud", "deepseek-r1:32b-cloud", "gpt-oss:120b"],
            TaskType.ARCHITECTURE: ["qwen3-coder:480b-cloud", "deepseek-v3.1:671-cloud"],
            TaskType.VISUAL: ["gpt-oss:120b"],
            TaskType.CONTENT: ["gpt-oss:20b-cloud", "gpt-oss:120b"],
            TaskType.SPEED: ["gpt-oss:20b-cloud", "qwen2.5-coder:32b-cloud"],
        },
        Provider.AUTO: {TaskType.AUTO: []},
    }
    return defaults[provider].get(task_type) or defaults[provider][TaskType.AUTO]


def choose_mode(input_data: ComplexityInput, preferred_mode: Optional[WorkMode] = None) -> tuple[WorkMode, list[str], int]:
    if preferred_mode is not None:
        return preferred_mode, [f"Mode pinned to {preferred_mode.value} by caller."], 9

    task_type = infer_task_type(input_data.task, input_data.task_type)
    reasons: list[str] = []
    score = 3
    lowered = input_data.task.lower()

    if input_data.file_count is not None:
        score += min(3, input_data.file_count // 2)
        if input_data.file_count > 3:
            reasons.append("Touches more than 3 files.")
    if input_data.estimated_changed_lines is not None:
        score += min(3, input_data.estimated_changed_lines // 250)
        if input_data.estimated_changed_lines > 500:
            reasons.append("Expected change set is larger than 500 lines.")
    if input_data.has_unknown_root_cause:
        score += 2
        reasons.append("Root cause is not yet known.")
    if input_data.needs_architecture or task_type == TaskType.ARCHITECTURE:
        score += 2
        reasons.append("Task includes architecture or broad refactor concerns.")
    if any(token in lowered for token in ["full page", "complete section", "new page", "new screen"]):
        score += 2
        reasons.append("Task sounds like a full section or page build.")
    if input_data.needs_animation or input_data.needs_visual_analysis:
        score += 1
        reasons.append("Task includes visual or motion work.")

    score = max(1, min(score, 10))
    mode = WorkMode.ORCHESTRATOR if score >= 7 else WorkMode.ENGINEER
    if not reasons:
        reasons.append("Task looks focused enough for direct implementation.")
    return mode, reasons, score


def build_complexity_payload(input_data: ComplexityInput, preferred_mode: Optional[WorkMode] = None) -> dict[str, Any]:
    task_type = infer_task_type(input_data.task, input_data.task_type)
    mode, reasons, score = choose_mode(input_data, preferred_mode)
    return {
        "task_type": task_type.value,
        "complexity_score": score,
        "recommended_mode": mode.value,
        "reasons": reasons,
    }


def curated_candidates(
    task_type: TaskType,
    mode: WorkMode,
    skill_models: list[str] | None = None,
    configured_only: bool = True,
) -> list[dict[str, Any]]:
    configured = {
        Provider.GEMINI.value: provider_is_configured(Provider.GEMINI),
        Provider.NVIDIA.value: provider_is_configured(Provider.NVIDIA),
        Provider.OLLAMA.value: provider_is_configured(Provider.OLLAMA),
    }
    candidates = [
        item
        for item in SPECIALIST_REGISTRY
        if task_type.value in item["task_types"]
        and mode.value in item["modes"]
        and (configured.get(item["provider"], False) or not configured_only)
    ]
    if skill_models:
        prioritized = [item for item in candidates if item["model"] in skill_models]
        others = [item for item in candidates if item["model"] not in skill_models]
        return prioritized + sorted(others, key=lambda item: item["priority"], reverse=True)
    return sorted(candidates, key=lambda item: item["priority"], reverse=True)


def build_route_candidates(
    provider: Provider,
    model: str | None,
    task_type: TaskType,
    task_text: str,
    allow_fallback: bool,
    config: ProjectConfig,
    store: StateStore,
    project_name: str,
    skill_registry: SkillRegistry,
    skill_slug: str | None,
    configured_only: bool = True,
) -> list[dict[str, str]]:
    if model:
        resolved_provider = provider if provider != Provider.AUTO else infer_provider_from_model(model)
        return [{"provider": resolved_provider.value, "model": model, "reason": "explicit model provided by caller"}]

    matched_skill = skill_registry.get(skill_slug) if skill_slug else None
    matched_skills = [matched_skill] if matched_skill else skill_registry.match(task_text, task_type)
    skill_models = matched_skills[0].preferred_models if matched_skills else []

    if provider != Provider.AUTO:
        models = skill_models or provider_defaults(provider, task_type)
        routes = [{"provider": provider.value, "model": item, "reason": f"{provider.value} default for {task_type.value}"} for item in models]
        return routes[: (3 if allow_fallback else 1)]

    mode = WorkMode.ENGINEER if task_type in {TaskType.CODE, TaskType.REASONING, TaskType.SPEED} else WorkMode.ORCHESTRATOR
    candidates = curated_candidates(task_type, mode, skill_models=skill_models, configured_only=configured_only)
    routes = [
        {"provider": candidate["provider"], "model": candidate["model"], "reason": f"specialist match: {candidate['nickname']}"}
        for candidate in candidates
    ]
    if not routes:
        for fallback_provider in [Provider.OLLAMA, Provider.NVIDIA, Provider.GEMINI]:
            if provider_is_configured(fallback_provider) or not configured_only:
                routes.append(
                    {
                        "provider": fallback_provider.value,
                        "model": provider_defaults(fallback_provider, task_type)[0],
                        "reason": f"default fallback for {task_type.value}",
                    }
                )
    budget_status = store.get_budget_status(project_name, config.budgets.daily_usd, config.budgets.weekly_usd)
    routes = order_routes_by_budget(routes, config, budget_status)
    return routes[: (3 if allow_fallback else 1)]


def select_model_payload(
    input_data: ModelSelectionInput,
    config: ProjectConfig,
    store: StateStore,
    skill_registry: SkillRegistry,
    preferred_mode: Optional[WorkMode] = None,
) -> dict[str, Any]:
    task_type = infer_task_type(input_data.task, input_data.task_type)
    mode, _, score = choose_mode(input_data, preferred_mode)
    routes = build_route_candidates(
        provider=Provider.AUTO,
        model=None,
        task_type=task_type,
        task_text=input_data.task,
        allow_fallback=True,
        config=config,
        store=store,
        project_name=config.project,
        skill_registry=skill_registry,
        skill_slug=input_data.skill_slug,
        configured_only=input_data.configured_only,
    )
    recommended = routes[0] if routes else {"provider": "ollama", "model": OLLAMA_DEFAULT_MODEL, "reason": "fallback"}
    explicit_skill = skill_registry.get(input_data.skill_slug) if input_data.skill_slug else None
    matched_skills = [explicit_skill] if explicit_skill is not None else skill_registry.match(input_data.task, task_type)
    return {
        "task_type": task_type.value,
        "mode_suggestion": mode.value,
        "complexity_score": score,
        "recommended": recommended,
        "alternatives": routes[1:4],
        "matched_skills": [skill.slug for skill in matched_skills],
    }


def render_delegation_prompt(
    specialist: dict[str, Any],
    subtask: str,
    repo_context: str | None,
    constraints: list[str],
) -> str:
    context_block = repo_context or "No repo snapshot provided. Work only from the task and constraints."
    lines = [
        "[Delegation]",
        f"Target specialist: {specialist['nickname']} ({specialist['provider']} / {specialist['model']})",
        f"Task: {subtask}",
        "",
        "Repo context:",
        context_block,
        "",
        "Constraints:",
    ]
    for constraint in constraints or [
        "Do not invent files, imports, or APIs.",
        "Return only the bounded result requested for this subtask.",
        "Flag assumptions and edge cases clearly.",
    ]:
        lines.append(f"- {constraint}")
    return "\n".join(lines)


def mode_checklist(mode: WorkMode) -> list[str]:
    if mode == WorkMode.ORCHESTRATOR:
        return [
            "Break work into bounded subproblems before delegating.",
            "Keep Codex responsible for final synthesis and validation.",
            "Use parallel delegation for independent sidecar tasks only.",
            "Verify diffs, preserved copy, and design compliance before presenting results.",
        ]
    return [
        "Keep core implementation local in Codex.",
        "Delegate only specialized sidecars such as motion, visual review, or copy polish.",
        "Validate the final integrated change locally before presenting it.",
    ]


def build_delegations(
    input_data: OrchestrateInput,
    config: ProjectConfig,
    store: StateStore,
    skill_registry: SkillRegistry,
) -> list[dict[str, Any]]:
    task_type = infer_task_type(input_data.task, input_data.task_type)
    mode, _, _ = choose_mode(input_data, preferred_mode=input_data.preferred_mode)
    routes = build_route_candidates(
        provider=Provider.AUTO,
        model=None,
        task_type=task_type,
        task_text=input_data.task,
        allow_fallback=True,
        config=config,
        store=store,
        project_name=config.project,
        skill_registry=skill_registry,
        skill_slug=input_data.skill_slug,
        configured_only=input_data.configured_only,
    )
    registry_by_model = {item["model"]: item for item in SPECIALIST_REGISTRY}
    constraints = list(input_data.constraints)
    delegations: list[dict[str, Any]] = []
    for route in routes[:4]:
        specialist = registry_by_model.get(route["model"], {"nickname": route["model"], "provider": route["provider"], "model": route["model"]})
        subtask = "Produce the best bounded result for the requested slice."
        if task_type == TaskType.ARCHITECTURE:
            subtask = "Design the implementation slice, file structure, and typed interfaces for the requested change."
        elif task_type == TaskType.REASONING:
            subtask = "Stress-test the plan for edge cases, logic risks, and API or data pitfalls."
        elif task_type == TaskType.VISUAL:
            subtask = "Review visual direction, screenshots, layout, accessibility, and motion choices."
        elif task_type == TaskType.CONTENT:
            subtask = "Polish user-facing copy while preserving meaning and product accuracy."
        delegations.append(
            {
                "nickname": specialist["nickname"],
                "provider": route["provider"],
                "model": route["model"],
                "subtask": subtask,
                "prompt": render_delegation_prompt(specialist, subtask, input_data.repo_context, constraints),
            }
        )
    return delegations
