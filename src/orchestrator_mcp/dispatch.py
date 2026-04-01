"""Routing, caching, logging, and provider dispatch."""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Optional

from .config import ProjectConfig
from .costs import estimate_message_tokens, estimate_run_cost
from .models import Provider, SafetyMode, TaskType
from .providers import ProviderResponse, call_provider
from .routing import build_route_candidates, infer_task_type, infer_provider_from_model
from .safety import (
    redact_messages,
    redact_sensitive_text,
    request_block_reason,
    reserve_request_slots,
    sanitize_error_text,
    validate_model_name,
)
from .skills import SkillRegistry
from .state import StateStore


def normalize_for_cache(text: str) -> str:
    return " ".join(text.lower().split())


def build_cache_key(
    messages: list[dict[str, str]],
    system_prompt: str | None,
    task_type: TaskType,
    project_name: str,
    skill_slug: str | None,
) -> str:
    payload = {
        "messages": messages,
        "system_prompt": system_prompt,
        "task_type": task_type.value,
        "project_name": project_name,
        "skill_slug": skill_slug,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


async def dispatch_once(
    provider: Provider,
    messages: list[dict[str, str]],
    model: str,
    system_prompt: Optional[str],
    temperature: Optional[float],
    max_tokens: int,
    timeout_seconds: float,
) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        response: ProviderResponse = await call_provider(
            provider=provider,
            messages=messages,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout_seconds=timeout_seconds,
        )
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        if response.text.startswith("Error:"):
            return {
                "ok": False,
                "provider": provider.value,
                "model": model,
                "error": sanitize_error_text(response.text),
                "elapsed_ms": elapsed_ms,
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
            }
        return {
            "ok": True,
            "provider": provider.value,
            "model": model,
            "result": redact_sensitive_text(response.text),
            "elapsed_ms": elapsed_ms,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "usage": response.usage,
        }
    except Exception as exc:
        return {
            "ok": False,
            "provider": provider.value,
            "model": model,
            "error": sanitize_error_text(f"Error: Unexpected error calling {provider.value}: {type(exc).__name__}: {exc}"),
            "elapsed_ms": int((time.perf_counter() - started) * 1000),
            "input_tokens": None,
            "output_tokens": None,
        }


def format_dispatch_output(result: dict[str, Any], include_metadata: bool) -> str:
    if include_metadata:
        return json.dumps(result, indent=2)
    if result.get("ok"):
        return result.get("result", "")
    return result.get("error", "Error: Unknown failure")


async def dispatch_with_routing(
    *,
    provider: Provider,
    messages: list[dict[str, str]],
    model: str | None,
    system_prompt: str | None,
    temperature: float | None,
    max_tokens: int,
    task_type: TaskType,
    timeout_seconds: float | None,
    allow_fallback: bool,
    safety_mode: SafetyMode,
    use_cache: bool,
    project_name: str,
    skill_slug: str | None,
    tool_name: str,
    config: ProjectConfig,
    store: StateStore,
    skill_registry: SkillRegistry,
) -> dict[str, Any]:
    timeout_value = timeout_seconds or 120.0
    joined_text = "\n".join([system_prompt or "", *(message["content"] for message in messages)])
    block_reason = request_block_reason(joined_text, safety_mode)
    if block_reason:
        return {"ok": False, "blocked": True, "error": f"Error: {block_reason}", "attempts": []}

    rate_limit_error = await reserve_request_slots(1)
    if rate_limit_error:
        return {"ok": False, "blocked": False, "error": rate_limit_error, "attempts": []}

    resolved_task_type = infer_task_type(joined_text, task_type)
    cache_key = build_cache_key(messages, system_prompt, resolved_task_type, project_name, skill_slug)
    sanitized_messages, message_redacted = redact_messages(messages)
    sanitized_system_prompt = redact_sensitive_text(system_prompt or "") if system_prompt else None
    system_redacted = (sanitized_system_prompt or "") != (system_prompt or "")
    normalized_prompt = normalize_for_cache("\n".join([sanitized_system_prompt or "", *(message["content"] for message in sanitized_messages)]))

    if use_cache:
        hit = store.find_similar_cache(normalized_prompt, resolved_task_type.value, threshold=0.92)
        if hit is not None:
            payload = {
                "ok": True,
                "provider": hit.provider,
                "model": hit.model,
                "result": hit.response_text,
                "task_type": resolved_task_type.value,
                "redacted_input": message_redacted or system_redacted,
                "cached": True,
                "cache_key": hit.cache_key,
                "attempts": [],
                "project_name": project_name,
                "tool_name": tool_name,
                "estimated_input_tokens": estimate_message_tokens(sanitized_messages, sanitized_system_prompt),
                "estimated_output_tokens": len(hit.response_text) // 4,
                "estimated_cost": 0.0,
                "summary": "Served from semantic cache",
            }
            store.record_run(payload)
            return payload

    routes = build_route_candidates(
        provider=provider,
        model=validate_model_name(model) if model else None,
        task_type=resolved_task_type,
        task_text=joined_text,
        allow_fallback=allow_fallback,
        config=config,
        store=store,
        project_name=project_name,
        skill_registry=skill_registry,
        skill_slug=skill_slug,
    )

    attempts: list[dict[str, Any]] = []
    last_error = "Error: Delegation failed before any provider could be called."
    for route in routes:
        attempt = await dispatch_once(
            provider=Provider(route["provider"]),
            messages=sanitized_messages,
            model=validate_model_name(route["model"]),
            system_prompt=sanitized_system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout_seconds=timeout_value,
        )
        attempt["route_reason"] = route["reason"]
        attempts.append(attempt)
        input_tokens = attempt.get("input_tokens") or estimate_message_tokens(sanitized_messages, sanitized_system_prompt)
        output_tokens = attempt.get("output_tokens") or (len(attempt.get("result", "")) // 4 if attempt.get("result") else 0)
        estimated_cost = estimate_run_cost(config, route["provider"], input_tokens, output_tokens)

        if attempt["ok"]:
            payload = {
                "ok": True,
                "provider": attempt["provider"],
                "model": attempt["model"],
                "result": attempt["result"],
                "task_type": resolved_task_type.value,
                "redacted_input": message_redacted or system_redacted,
                "cached": False,
                "cache_key": cache_key,
                "attempts": attempts,
                "project_name": project_name,
                "tool_name": tool_name,
                "estimated_input_tokens": input_tokens,
                "estimated_output_tokens": output_tokens,
                "estimated_cost": estimated_cost,
                "elapsed_ms": attempt["elapsed_ms"],
                "summary": route["reason"],
            }
            store.record_run(payload)
            if use_cache:
                store.record_cache_entry(
                    cache_key=cache_key,
                    normalized_prompt=normalized_prompt,
                    task_type=resolved_task_type.value,
                    provider=attempt["provider"],
                    model=attempt["model"],
                    response_text=attempt["result"],
                    metadata={"route_reason": route["reason"], "project_name": project_name, "skill_slug": skill_slug},
                )
            return payload

        payload = {
            "ok": False,
            "provider": attempt["provider"],
            "model": attempt["model"],
            "task_type": resolved_task_type.value,
            "redacted_input": message_redacted or system_redacted,
            "cached": False,
            "cache_key": cache_key,
            "attempts": attempts,
            "project_name": project_name,
            "tool_name": tool_name,
            "estimated_input_tokens": input_tokens,
            "estimated_output_tokens": output_tokens,
            "estimated_cost": estimated_cost,
            "elapsed_ms": attempt["elapsed_ms"],
            "summary": route["reason"],
            "error": attempt["error"],
        }
        store.record_run(payload)
        last_error = attempt["error"]
        if not allow_fallback:
            break

    return {
        "ok": False,
        "task_type": resolved_task_type.value,
        "redacted_input": message_redacted or system_redacted,
        "error": last_error,
        "attempts": attempts,
    }

