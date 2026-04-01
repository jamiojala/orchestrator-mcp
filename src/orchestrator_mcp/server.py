"""FastMCP server assembly and tool registration."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .analysis import (
    design_audit_payload,
    generate_diff_text,
    git_code_review_payload,
    git_commit_message_payload,
    git_pr_description_payload,
    verify_text_unchanged_payload,
)
from .config import ProjectConfig, load_project_config, provider_env_status
from .content import CODEX_DUAL_MODE_FRAMEWORK, SAFETY_POLICY_TEXT
from .dispatch import dispatch_with_routing, format_dispatch_output
from .marketplace import get_marketplace_skill, marketplace_summary
from .models import (
    AskInput,
    ChatInput,
    ComplexityInput,
    DesignAuditInput,
    DiffInput,
    GitDiffInput,
    ModelSelectionInput,
    OrchestrateInput,
    ParallelDispatchInput,
    Provider,
    TaskType,
    TextPreservationInput,
    WorkMode,
)
from .providers import list_models
from .routing import build_complexity_payload, build_delegations, mode_checklist, select_model_payload
from .skills import SkillRegistry
from .state import StateStore


@dataclass(slots=True)
class AppContext:
    config: ProjectConfig
    store: StateStore
    skill_registry: SkillRegistry


def build_app_context(config_path: Path | None = None) -> AppContext:
    config = load_project_config(config_path)
    store = StateStore(config.state_dir / "orchestrator-mcp.sqlite3")
    skill_registry = SkillRegistry(config.skills_dir)
    skill_registry.load()
    return AppContext(config=config, store=store, skill_registry=skill_registry)


def build_server(config_path: Path | None = None) -> FastMCP:
    app = build_app_context(config_path)
    mcp = FastMCP("orchestrator_mcp")

    @mcp.resource(
        "llm://frameworks/codex-dual-mode-v3",
        name="codex_dual_mode_framework",
        title="Codex Dual-Mode Framework",
        description="Codex-focused orchestration framework with verified specialist mappings and safety constraints.",
        mime_type="text/plain",
    )
    def codex_dual_mode_framework_resource() -> str:
        return CODEX_DUAL_MODE_FRAMEWORK

    @mcp.resource(
        "llm://policies/safety",
        name="llm_safety_policy",
        title="LLM Delegator Safety Policy",
        description="The local safety constraints enforced by this MCP.",
        mime_type="text/plain",
    )
    def safety_policy_resource() -> str:
        return SAFETY_POLICY_TEXT

    @mcp.resource(
        "llm://registry/specialists",
        name="specialist_registry",
        title="Specialist Model Registry",
        description="Curated model registry for coding, reasoning, vision, and copy tasks.",
        mime_type="application/json",
    )
    def specialist_registry_resource() -> str:
        payload = {
            "configured_providers": provider_env_status(),
            "skills": app.skill_registry.summary(),
        }
        return json.dumps(payload, indent=2)

    @mcp.resource(
        "llm://registry/marketplace-skills",
        name="skill_marketplace",
        title="Skill Marketplace",
        description="Summary of the built-in 100-skill marketplace catalog.",
        mime_type="application/json",
    )
    def skill_marketplace_resource() -> str:
        payload = {
            "marketplace_count": len(marketplace_summary()),
            "skills": marketplace_summary(),
        }
        return json.dumps(payload, indent=2)

    @mcp.prompt(
        name="codex_dual_mode_orchestrator",
        title="Codex Dual-Mode Orchestrator Prompt",
        description="Build a reusable system/user prompt pair for Codex-style orchestration.",
    )
    def codex_dual_mode_orchestrator_prompt(task: str, repo_context: str = "", constraints: str = "") -> list[dict[str, str]]:
        user_prompt = "\n".join(
            [
                f"Task:\n{task}",
                "",
                "Repo context:",
                repo_context or "No repo context provided.",
                "",
                "Constraints:",
                constraints or "No extra constraints provided.",
            ]
        )
        return [
            {"role": "system", "content": CODEX_DUAL_MODE_FRAMEWORK},
            {"role": "user", "content": user_prompt},
        ]

    @mcp.prompt(
        name="specialist_delegation_brief",
        title="Specialist Delegation Brief",
        description="Create a scoped prompt for a specialist model subtask.",
    )
    def specialist_delegation_brief_prompt(
        specialist_name: str,
        subtask: str,
        repo_context: str = "",
        constraints: str = "",
    ) -> list[dict[str, str]]:
        skill_lines = [line.strip() for line in constraints.splitlines() if line.strip()]
        constraint_lines = [f"- {line}" for line in skill_lines] or ["- No extra constraints provided."]
        content = "\n".join(
            [
                f"Specialist: {specialist_name}",
                f"Subtask: {subtask}",
                "",
                "Repo context:",
                repo_context or "No repo context provided.",
                "",
                "Constraints:",
                *constraint_lines,
            ]
        )
        return [{"role": "user", "content": content}]

    @mcp.tool(
        name="llm_ask",
        annotations={
            "title": "Ask External LLM",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": True,
        },
    )
    async def llm_ask(params: AskInput) -> str:
        result = await dispatch_with_routing(
            provider=params.provider,
            messages=[{"role": "user", "content": params.prompt}],
            model=params.model,
            system_prompt=params.system_prompt,
            temperature=params.temperature,
            max_tokens=params.max_tokens or 4096,
            task_type=params.task_type,
            timeout_seconds=params.timeout_seconds,
            allow_fallback=params.allow_fallback,
            safety_mode=params.safety_mode,
            use_cache=params.use_cache,
            project_name=params.project_name or app.config.project,
            skill_slug=params.skill_slug,
            tool_name="llm_ask",
            config=app.config,
            store=app.store,
            skill_registry=app.skill_registry,
        )
        return format_dispatch_output(result, include_metadata=params.include_metadata)

    @mcp.tool(
        name="llm_chat",
        annotations={
            "title": "Chat with External LLM",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": True,
        },
    )
    async def llm_chat(params: ChatInput) -> str:
        result = await dispatch_with_routing(
            provider=params.provider,
            messages=[{"role": message.role, "content": message.content} for message in params.messages],
            model=params.model,
            system_prompt=params.system_prompt,
            temperature=params.temperature,
            max_tokens=params.max_tokens or 4096,
            task_type=params.task_type,
            timeout_seconds=params.timeout_seconds,
            allow_fallback=params.allow_fallback,
            safety_mode=params.safety_mode,
            use_cache=params.use_cache,
            project_name=params.project_name or app.config.project,
            skill_slug=params.skill_slug,
            tool_name="llm_chat",
            config=app.config,
            store=app.store,
            skill_registry=app.skill_registry,
        )
        return format_dispatch_output(result, include_metadata=params.include_metadata)

    @mcp.tool(
        name="dispatch_parallel",
        annotations={
            "title": "Dispatch Parallel Delegations",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": True,
        },
    )
    async def dispatch_parallel(params: ParallelDispatchInput) -> str:
        semaphore = asyncio.Semaphore(params.max_concurrency)

        async def run_request(request: object) -> dict[str, object]:
            from .models import ParallelRequest

            assert isinstance(request, ParallelRequest)
            messages = (
                [{"role": "user", "content": request.prompt or ""}]
                if request.prompt is not None
                else [{"role": message.role, "content": message.content} for message in request.messages or []]
            )
            async with semaphore:
                result = await dispatch_with_routing(
                    provider=request.provider,
                    messages=messages,
                    model=request.model,
                    system_prompt=request.system_prompt,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens or 4096,
                    task_type=request.task_type,
                    timeout_seconds=request.timeout_seconds,
                    allow_fallback=request.allow_fallback,
                    safety_mode=request.safety_mode,
                    use_cache=request.use_cache,
                    project_name=request.project_name or app.config.project,
                    skill_slug=request.skill_slug,
                    tool_name="dispatch_parallel",
                    config=app.config,
                    store=app.store,
                    skill_registry=app.skill_registry,
                )
            result["id"] = request.id
            return result

        results = []
        for request in params.requests:
            result = await run_request(request)
            results.append(result)
            if params.stop_on_error and not result.get("ok"):
                break

        payload = {
            "ok": all(bool(result.get("ok")) for result in results),
            "results": results,
            "summary": {
                "requested": len(params.requests),
                "succeeded": sum(1 for result in results if result.get("ok")),
                "failed": sum(1 for result in results if not result.get("ok")),
            },
        }
        return json.dumps(payload, indent=2)

    @mcp.tool(
        name="estimate_complexity",
        annotations={
            "title": "Estimate Task Complexity",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def estimate_complexity(params: ComplexityInput) -> str:
        return json.dumps(build_complexity_payload(params), indent=2)

    @mcp.tool(
        name="llm_pick_model",
        annotations={
            "title": "Pick Specialist Model",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def llm_pick_model(params: ModelSelectionInput) -> str:
        payload = select_model_payload(params, config=app.config, store=app.store, skill_registry=app.skill_registry)
        return json.dumps(payload, indent=2)

    @mcp.tool(
        name="llm_orchestrate",
        annotations={
            "title": "Create Orchestration Plan",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def llm_orchestrate(params: OrchestrateInput) -> str:
        complexity = build_complexity_payload(params, preferred_mode=params.preferred_mode)
        model_selection = select_model_payload(params, config=app.config, store=app.store, skill_registry=app.skill_registry, preferred_mode=params.preferred_mode)
        delegations = build_delegations(params, config=app.config, store=app.store, skill_registry=app.skill_registry)
        resolved_mode = params.preferred_mode or WorkMode(complexity["recommended_mode"])
        payload = {
            "task_type": complexity["task_type"],
            "complexity_score": complexity["complexity_score"],
            "mode": complexity["recommended_mode"],
            "decision_reasons": complexity["reasons"],
            "recommended_primary_model": model_selection["recommended"],
            "alternative_models": model_selection["alternatives"],
            "matched_skills": model_selection["matched_skills"],
            "delegations": delegations,
            "checklist": mode_checklist(resolved_mode),
        }
        return json.dumps(payload, indent=2)

    @mcp.tool(
        name="generate_diff",
        annotations={
            "title": "Generate Unified Diff",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def generate_diff(params: DiffInput) -> str:
        return generate_diff_text(params.original, params.revised, params.path, params.context_lines)

    @mcp.tool(
        name="verify_text_unchanged",
        annotations={
            "title": "Verify Text Is Unchanged",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def verify_text_unchanged(params: TextPreservationInput) -> str:
        payload = verify_text_unchanged_payload(
            params.original,
            params.candidate,
            params.normalize_whitespace,
            params.ignore_case,
        )
        return json.dumps(payload, indent=2)

    @mcp.tool(
        name="audit_design_compliance",
        annotations={
            "title": "Audit Design Compliance",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def audit_design_compliance(params: DesignAuditInput) -> str:
        return json.dumps(design_audit_payload(params.code, params.profile), indent=2)

    @mcp.tool(
        name="git_delegate_commit_message",
        annotations={
            "title": "Generate Commit Message",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def git_delegate_commit_message(params: GitDiffInput) -> str:
        payload = git_commit_message_payload(params.diff_text, params.context)
        return json.dumps(payload, indent=2) if params.include_metadata else payload["conventional_commit"]

    @mcp.tool(
        name="git_delegate_pr_description",
        annotations={
            "title": "Generate PR Description",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def git_delegate_pr_description(params: GitDiffInput) -> str:
        payload = git_pr_description_payload(params.diff_text, params.context)
        return json.dumps(payload, indent=2) if params.include_metadata else payload["body"]

    @mcp.tool(
        name="git_delegate_code_review",
        annotations={
            "title": "Review Diff",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def git_delegate_code_review(params: GitDiffInput) -> str:
        payload = git_code_review_payload(params.diff_text, params.context)
        return json.dumps(payload, indent=2)

    @mcp.tool(
        name="llm_list_models",
        annotations={
            "title": "List Available Models",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    )
    async def llm_list_models(provider: Provider) -> str:
        return await list_models(provider)

    @mcp.tool(
        name="llm_list_providers",
        annotations={
            "title": "List Available LLM Providers",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def llm_list_providers() -> str:
        providers = [
            {
                "id": "gemini",
                "configured": provider_env_status()["gemini"],
                "default_model": "gemini-2.5-flash",
                "strengths": ["multimodal", "analysis", "visual review"],
            },
            {
                "id": "nvidia",
                "configured": provider_env_status()["nvidia"],
                "default_model": "moonshotai/kimi-k2.5",
                "strengths": ["reasoning", "logic", "architecture"],
            },
            {
                "id": "ollama",
                "configured": provider_env_status()["ollama"],
                "default_model": "gpt-oss:120b",
                "strengths": ["coding", "open models", "cost efficiency"],
            },
        ]
        return json.dumps(providers, indent=2)

    @mcp.tool(
        name="skill_marketplace_list",
        annotations={
            "title": "List Marketplace Skills",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def skill_marketplace_list() -> str:
        return json.dumps({"marketplace_count": len(marketplace_summary()), "skills": marketplace_summary()}, indent=2)

    @mcp.tool(
        name="skill_marketplace_show",
        annotations={
            "title": "Show One Marketplace Skill",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def skill_marketplace_show(skill_id: str) -> str:
        skill = get_marketplace_skill(skill_id)
        if skill is None:
            return json.dumps({"error": f"Marketplace skill not found: {skill_id}"}, indent=2)
        return json.dumps(skill.marketplace_manifest(), indent=2)

    return mcp


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()
