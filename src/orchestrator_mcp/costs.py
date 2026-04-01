"""Cost estimation and budget-aware routing helpers."""

from __future__ import annotations

from typing import Any

from .config import ProjectConfig


def estimate_tokens_from_text(text: str) -> int:
    return max(1, (len(text) + 3) // 4)


def estimate_message_tokens(messages: list[dict[str, str]], system_prompt: str | None = None) -> int:
    total = sum(estimate_tokens_from_text(message.get("content", "")) for message in messages)
    if system_prompt:
        total += estimate_tokens_from_text(system_prompt)
    return total


def resolve_provider_pricing(config: ProjectConfig, provider: str) -> dict[str, float]:
    return dict(config.pricing.get(provider, {}))


def estimate_run_cost(
    config: ProjectConfig,
    provider: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    pricing = resolve_provider_pricing(config, provider)
    input_per_1k = float(pricing.get("input_per_1k", 0.0))
    output_per_1k = float(pricing.get("output_per_1k", 0.0))
    return round((input_tokens / 1000.0) * input_per_1k + (output_tokens / 1000.0) * output_per_1k, 6)


def relative_cost_weight(config: ProjectConfig, provider: str) -> float:
    pricing = resolve_provider_pricing(config, provider)
    return float(pricing.get("relative_cost_weight", 1.0))


def order_routes_by_budget(
    routes: list[dict[str, Any]],
    config: ProjectConfig,
    budget_status: dict[str, float],
) -> list[dict[str, Any]]:
    if config.budgets.poor_mans_mode or budget_status.get("daily_remaining", 0.0) <= 0:
        return sorted(routes, key=lambda route: (route["provider"] != "ollama", relative_cost_weight(config, route["provider"])))
    return sorted(routes, key=lambda route: relative_cost_weight(config, route["provider"]))

