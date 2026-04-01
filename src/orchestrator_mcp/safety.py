"""Safety, redaction, rate limiting, and public-release scanning."""

from __future__ import annotations

import asyncio
import re
import time
from collections import deque
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from .models import SafetyMode

DEFAULT_OLLAMA_BASE_URL = "https://ollama.com/v1"
LOCALHOST_HOSTS = {"localhost", "127.0.0.1", "::1"}
OLLAMA_ALLOWED_HOSTS = {"ollama.com", "api.ollama.com", *LOCALHOST_HOSTS}
MAX_MODEL_NAME_LENGTH = 160
SAFE_MODEL_PATTERN = re.compile(r"^[A-Za-z0-9._:/-]{1,160}$")
MAX_REQUESTS_PER_MINUTE = 24

REQUEST_LOG: deque[float] = deque()
REQUEST_LOG_LOCK = asyncio.Lock()

SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"sk-ant-[A-Za-z0-9\-_]{16,}"), "[REDACTED_ANTHROPIC_KEY]"),
    (re.compile(r"sk-[A-Za-z0-9]{16,}"), "[REDACTED_API_KEY]"),
    (re.compile(r"AIza[0-9A-Za-z\-_]{20,}"), "[REDACTED_GEMINI_KEY]"),
    (re.compile(r"nvapi-[A-Za-z0-9\-_]{20,}"), "[REDACTED_NVIDIA_KEY]"),
    (re.compile(r"eyJ[A-Za-z0-9_\-]+=*\.[A-Za-z0-9_\-]+=*\.([A-Za-z0-9_\-]+=*)"), "[REDACTED_JWT]"),
    (
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----",
            re.MULTILINE,
        ),
        "[REDACTED_PRIVATE_KEY]",
    ),
    (
        re.compile(r"(?im)\b([A-Z][A-Z0-9_]{2,})\s*=\s*(['\"]?)([^'\"\s]{20,})\2"),
        r"\1=[REDACTED]",
    ),
]

HARMFUL_REQUEST_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(keylogger|credential stuffing|botnet|ransomware|stealer|phishing kit)\b", re.I),
    re.compile(r"\b(generate|write|build|create|produce|develop)\b.{0,80}\b(malware|ransomware|keylogger|stealer|phishing|botnet)\b", re.I),
    re.compile(r"\b(steal|exfiltrat(?:e|ion)|dump|harvest)\b.{0,80}\b(token|password|credential|cookie|session|secret|api key)\b", re.I),
    re.compile(r"\b(bypass|evade|disable)\b.{0,60}\b(authentication|authorization|mfa|2fa|waf|rate limit|sandbox|edr|xdr)\b", re.I),
    re.compile(
        r"\b(reveal|print|show|dump|list|expose)\b.{0,80}\b(api keys?|secrets?|tokens?|environment variables?|system prompts?)\b",
        re.I,
    ),
]
DEFENSIVE_CONTEXT_PATTERN = re.compile(
    r"\b(defend|defensive|detect|prevent|mitigate|review|audit|patch|fix|harden|secure|sanitize|monitor|test)\b",
    re.I,
)

PUBLIC_RELEASE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"/Users/[^/\s]+"), "Found absolute local user path."),
    (re.compile(r"\.codex/config\.toml"), "Found private Codex config reference."),
    (re.compile(r"AIza[0-9A-Za-z\-_]{20,}"), "Found Google API key pattern."),
    (re.compile(r"nvapi-[A-Za-z0-9\-_]{20,}"), "Found NVIDIA API key pattern."),
    (re.compile(r"sk-ant-[A-Za-z0-9\-_]{16,}"), "Found Anthropic API key pattern."),
    (re.compile(r"sk-[A-Za-z0-9]{16,}"), "Found generic API key pattern."),
    (
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----",
            re.MULTILINE,
        ),
        "Found a private key block.",
    ),
]


def validated_ollama_base_url(base_url: str) -> str:
    parsed = urlparse(base_url)
    host = parsed.hostname or ""
    if parsed.scheme == "https" and host in OLLAMA_ALLOWED_HOSTS:
        return base_url.rstrip("/")
    if parsed.scheme == "http" and host in LOCALHOST_HOSTS:
        return base_url.rstrip("/")
    return DEFAULT_OLLAMA_BASE_URL


def redact_sensitive_text(text: str) -> str:
    redacted = text
    for pattern, replacement in SECRET_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def redact_messages(messages: list[dict[str, str]]) -> tuple[list[dict[str, str]], bool]:
    redacted_any = False
    sanitized: list[dict[str, str]] = []
    for message in messages:
        original = message.get("content", "")
        cleaned = redact_sensitive_text(original)
        redacted_any = redacted_any or cleaned != original
        sanitized.append({"role": message["role"], "content": cleaned})
    return sanitized, redacted_any


def sanitize_error_text(text: str) -> str:
    return redact_sensitive_text(text or "")[:300]


def request_block_reason(text: str, safety_mode: SafetyMode) -> Optional[str]:
    if safety_mode == SafetyMode.OFF:
        return None

    for pattern in HARMFUL_REQUEST_PATTERNS:
        if pattern.search(text):
            if DEFENSIVE_CONTEXT_PATTERN.search(text) and safety_mode == SafetyMode.BALANCED:
                return None
            if DEFENSIVE_CONTEXT_PATTERN.search(text) and safety_mode == SafetyMode.STRICT:
                return "Request blocked by strict safety policy due to high-risk wording."
            return "Request blocked by safety policy because it appears to involve secrets, malware, phishing, or unauthorized access."
    return None


def validate_model_name(model: str) -> str:
    if len(model) > MAX_MODEL_NAME_LENGTH:
        raise ValueError("Model name is too long")
    if not SAFE_MODEL_PATTERN.fullmatch(model):
        raise ValueError("Model name contains disallowed characters")
    return model


async def reserve_request_slots(count: int) -> Optional[str]:
    async with REQUEST_LOG_LOCK:
        now = time.monotonic()
        while REQUEST_LOG and now - REQUEST_LOG[0] > 60:
            REQUEST_LOG.popleft()
        if len(REQUEST_LOG) + count > MAX_REQUESTS_PER_MINUTE:
            return "Error: Local safety rate limit hit for external delegation. Please wait a minute and try again."
        for _ in range(count):
            REQUEST_LOG.append(now)
    return None


def scan_public_release_tree(root: Path) -> list[str]:
    findings: list[str] = []
    ignore_dirs = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
    ignore_files = {"safety.py"}
    text_suffixes = {
        ".py",
        ".md",
        ".toml",
        ".yaml",
        ".yml",
        ".txt",
        ".json",
        ".cfg",
        ".ini",
        ".env",
        ".sh",
    }

    for path in root.rglob("*"):
        if any(part in ignore_dirs for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name in ignore_files:
            continue
        if path.suffix and path.suffix.lower() not in text_suffixes:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern, message in PUBLIC_RELEASE_PATTERNS:
            if pattern.search(content):
                findings.append(f"{path.relative_to(root)}: {message}")
    return findings
