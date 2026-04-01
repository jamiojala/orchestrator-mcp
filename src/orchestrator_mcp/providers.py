"""Provider clients and model catalog helpers."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Optional

import httpx

from .models import Provider
from .safety import sanitize_error_text, validated_ollama_base_url

GEMINI_DEFAULT_MODEL = "gemini-2.5-flash"
NVIDIA_DEFAULT_MODEL = "moonshotai/kimi-k2.5"
OLLAMA_DEFAULT_MODEL = "gpt-oss:120b"
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"


@dataclass(slots=True)
class ProviderResponse:
    text: str
    input_tokens: int | None
    output_tokens: int | None
    usage: dict[str, Any]


def provider_is_configured(provider: Provider) -> bool:
    if provider == Provider.GEMINI:
        return bool(os.environ.get("GEMINI_API_KEY"))
    if provider == Provider.NVIDIA:
        return bool(os.environ.get("NVIDIA_API_KEY"))
    if provider == Provider.OLLAMA:
        return bool(os.environ.get("OLLAMA_API_KEY"))
    return any(
        [
            bool(os.environ.get("GEMINI_API_KEY")),
            bool(os.environ.get("NVIDIA_API_KEY")),
            bool(os.environ.get("OLLAMA_API_KEY")),
        ]
    )


def _flatten_content_parts(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return str(content.get("text", ""))
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "".join(parts)
    return ""


def _extract_openai_compatible_response(data: dict[str, Any], provider_name: str) -> ProviderResponse:
    choices = data.get("choices") or []
    if not choices:
        return ProviderResponse(
            text=f"Error: Unexpected {provider_name} response format: no choices",
            input_tokens=None,
            output_tokens=None,
            usage={},
        )
    choice = choices[0]
    message = choice.get("message") or {}
    candidate_texts = [
        _flatten_content_parts(message.get("content")),
        _flatten_content_parts(choice.get("text")),
        _flatten_content_parts(message.get("reasoning_content")),
    ]
    text = next((candidate for candidate in candidate_texts if candidate.strip()), "")
    usage = data.get("usage") or {}
    return ProviderResponse(
        text=text or f"Error: Unexpected {provider_name} response format: no text content",
        input_tokens=usage.get("prompt_tokens"),
        output_tokens=usage.get("completion_tokens"),
        usage=usage,
    )


def _extract_gemini_response(data: dict[str, Any]) -> ProviderResponse:
    candidates = data.get("candidates") or []
    if not candidates:
        prompt_feedback = sanitize_error_text(json.dumps(data.get("promptFeedback") or {}))
        message = "Error: Unexpected Gemini response format: no candidates"
        if prompt_feedback:
            message = f"{message}. {prompt_feedback}"
        return ProviderResponse(text=message, input_tokens=None, output_tokens=None, usage={})
    parts = candidates[0].get("content", {}).get("parts") or []
    text = "".join(part.get("text", "") for part in parts if isinstance(part.get("text"), str))
    usage = data.get("usageMetadata") or {}
    return ProviderResponse(
        text=text or "Error: Unexpected Gemini response format: no text parts",
        input_tokens=usage.get("promptTokenCount"),
        output_tokens=usage.get("candidatesTokenCount"),
        usage=usage,
    )


async def call_gemini(
    messages: list[dict[str, str]],
    model: str,
    system_prompt: Optional[str],
    temperature: Optional[float],
    max_tokens: int,
    timeout_seconds: float,
) -> ProviderResponse:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return ProviderResponse(
            text="Error: GEMINI_API_KEY not set. Get a key at https://aistudio.google.com/apikey",
            input_tokens=None,
            output_tokens=None,
            usage={},
        )

    contents = []
    for message in messages:
        role = "user" if message["role"] in ("user", "system") else "model"
        contents.append({"role": role, "parts": [{"text": message["content"]}]})

    body: dict[str, Any] = {"contents": contents, "generationConfig": {"maxOutputTokens": max_tokens}}
    if system_prompt:
        body["systemInstruction"] = {"parts": [{"text": system_prompt}]}
    if temperature is not None:
        body["generationConfig"]["temperature"] = temperature

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        response = await client.post(url, json=body)
        response.raise_for_status()
        return _extract_gemini_response(response.json())


async def call_openai_compatible(
    messages: list[dict[str, str]],
    model: str,
    system_prompt: Optional[str],
    temperature: Optional[float],
    max_tokens: int,
    base_url: str,
    api_key: str,
    provider_name: str,
    timeout_seconds: float,
) -> ProviderResponse:
    if not api_key:
        return ProviderResponse(
            text=f"Error: API key not set for {provider_name}.",
            input_tokens=None,
            output_tokens=None,
            usage={},
        )

    api_messages = []
    if system_prompt:
        api_messages.append({"role": "system", "content": system_prompt})
    api_messages.extend(messages)
    body: dict[str, Any] = {"model": model, "messages": api_messages, "max_tokens": max_tokens}
    if temperature is not None:
        body["temperature"] = temperature

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    url = f"{base_url.rstrip('/')}/chat/completions"
    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        response = await client.post(url, json=body, headers=headers)
        response.raise_for_status()
        return _extract_openai_compatible_response(response.json(), provider_name=provider_name)


async def call_provider(
    provider: Provider,
    messages: list[dict[str, str]],
    model: str,
    system_prompt: Optional[str],
    temperature: Optional[float],
    max_tokens: int,
    timeout_seconds: float,
) -> ProviderResponse:
    if provider == Provider.GEMINI:
        return await call_gemini(messages, model, system_prompt, temperature, max_tokens, timeout_seconds)
    if provider == Provider.NVIDIA:
        return await call_openai_compatible(
            messages,
            model,
            system_prompt,
            temperature,
            max_tokens,
            NVIDIA_BASE_URL,
            os.environ.get("NVIDIA_API_KEY", ""),
            "nvidia",
            timeout_seconds,
        )
    if provider == Provider.OLLAMA:
        return await call_openai_compatible(
            messages,
            model,
            system_prompt,
            temperature,
            max_tokens,
            validated_ollama_base_url(os.environ.get("OLLAMA_BASE_URL", "https://ollama.com/v1")),
            os.environ.get("OLLAMA_API_KEY", ""),
            "ollama",
            timeout_seconds,
        )
    return ProviderResponse(text=f"Error: Unknown provider '{provider.value}'", input_tokens=None, output_tokens=None, usage={})


async def list_models(provider: Provider) -> str:
    if provider == Provider.AUTO:
        return "Error: provider='auto' is not supported for llm_list_models. Pick a concrete provider."

    if provider == Provider.NVIDIA:
        api_key = os.environ.get("NVIDIA_API_KEY", "")
        if not api_key:
            return "Error: NVIDIA_API_KEY not set. Get one at https://build.nvidia.com/"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://integrate.api.nvidia.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
            )
            response.raise_for_status()
            data = response.json()
        models = []
        for item in data.get("data", []):
            models.append(
                {
                    "id": item.get("id"),
                    "name": item.get("name", item.get("id")),
                    "description": item.get("description", ""),
                    "context_window": item.get("context_window", "unknown"),
                }
            )
        return json.dumps(
            {
                "provider": "nvidia",
                "total_models": len(models),
                "models": models[:50],
                "note": f"Showing first 50 of {len(models)} models.",
            },
            indent=2,
        )

    if provider == Provider.GEMINI:
        return json.dumps(
            {
                "provider": "gemini",
                "models": [
                    {"id": "gemini-2.5-flash", "description": "Fast, cost-efficient for everyday tasks"},
                    {"id": "gemini-2.5-pro", "description": "Best quality for complex tasks and multimodal analysis"},
                    {"id": "gemini-2.5-flash-lite", "description": "Lightweight, very fast"},
                    {"id": "gemini-2.0-flash-thinking-exp", "description": "Experimental reasoning model"},
                ],
            },
            indent=2,
        )

    return json.dumps(
        {
            "provider": "ollama",
            "models": [
                {"id": "gpt-oss:120b", "description": "GPT-OSS 120B parameters"},
                {"id": "gpt-oss:20b-cloud", "description": "GPT-OSS 20B cloud version"},
                {"id": "deepseek-v3.1:671-cloud", "description": "DeepSeek V3.1 671B MoE"},
                {"id": "deepseek-r1:32b-cloud", "description": "DeepSeek R1 32B reasoning"},
                {"id": "qwen3-coder:480b-cloud", "description": "Qwen3 Coder 480B"},
                {"id": "llama4-scout:109b-cloud", "description": "Llama 4 Scout 109B"},
                {"id": "qwen2.5-coder:32b-cloud", "description": "Qwen2.5 Coder 32B"},
            ],
        },
        indent=2,
    )

