"""Static content and curated specialist registry."""

from __future__ import annotations

from typing import Any

CODEX_DUAL_MODE_FRAMEWORK = """LLM MCP v3.1 Unified - Codex Dual-Mode Orchestrator

Dual identity:
- Orchestrator mode: choose when work spans many files, the blast radius is unclear, or the task needs decomposition.
- Engineer mode: choose when the change is focused and Codex should own the implementation directly.

Mode triggers:
- Use Orchestrator when a task touches more than 3 files, changes more than 500 lines, asks for a full page/section, or has an unknown root cause.
- Use Engineer when the task is focused, code-heavy, or mostly an integration/debugging problem inside a small slice.

Verified specialist registry:
- Qwen3-Coder (ollama / qwen3-coder:480b-cloud): strong TypeScript, React, component structure.
- Qwen2.5-Coder (ollama / qwen2.5-coder:32b-cloud): fast coding and utility work.
- Kimi-K2.5 (nvidia / moonshotai/kimi-k2.5): long-context reasoning, orchestration, plan synthesis.
- DeepSeek-V3.2 (nvidia / deepseek-ai/deepseek-v3.2): logic, API work, debugging, edge cases.
- Gemini 2.5 Pro (gemini / gemini-2.5-pro): multimodal analysis, screenshots, design review.
- Gemini 2.5 Flash (gemini / gemini-2.5-flash): fast analysis and rapid iteration.
- Phi-4 Multimodal (nvidia / microsoft/phi-4-multimodal-instruct): vision-language fallback.
- GPT-OSS 20B (ollama / gpt-oss:20b-cloud): copy polish and lightweight synthesis.

Safety posture:
- This MCP redacts obvious secrets before outbound delegation.
- This MCP blocks clearly malicious credential theft, malware, phishing, and prompt-exfiltration requests.
- This MCP does not run shell commands or read arbitrary files. Keep local validation and repo inspection in Codex's normal local toolchain.

Recommended workflow:
1. Run estimate_complexity to select Engineer vs Orchestrator mode.
2. Run llm_pick_model or llm_orchestrate to choose specialists and prepare delegation prompts.
3. Run dispatch_parallel for sidecar model work.
4. Use generate_diff, verify_text_unchanged, and audit_design_compliance to review outputs before integrating locally.
"""

SAFETY_POLICY_TEXT = """Safety policy

This MCP is intentionally narrower than a general local agent.

Allowed:
- Delegating text-only prompts to configured model providers.
- Comparing or auditing text/code that the caller explicitly provides.
- Producing orchestration plans, diffs, compliance reports, and safe git-review summaries.

Blocked or intentionally excluded:
- Shell execution.
- Arbitrary filesystem crawling or project exfiltration.
- Returning provider API keys or raw secrets from environment/config.
- Clearly malicious requests involving malware, phishing, credential theft, or prompt/secret exfiltration.

Additional protections:
- Obvious secrets are redacted before outbound requests.
- Error payloads are sanitized before returning to the client.
- Requests are rate-limited in-process.
- Provider/model routing only uses an allowlisted set of endpoints and validated model names.
"""

SPECIALIST_REGISTRY: list[dict[str, Any]] = [
    {
        "nickname": "Qwen3-Coder",
        "provider": "ollama",
        "model": "qwen3-coder:480b-cloud",
        "tier": "coding",
        "specialty": "TypeScript, React, component architecture, multi-file implementation",
        "task_types": ["code", "review", "architecture"],
        "modes": ["engineer", "orchestrator"],
        "priority": 100,
    },
    {
        "nickname": "Qwen2.5-Coder",
        "provider": "ollama",
        "model": "qwen2.5-coder:32b-cloud",
        "tier": "coding",
        "specialty": "fast coding, focused utilities, low-latency implementation",
        "task_types": ["code", "speed"],
        "modes": ["engineer"],
        "priority": 90,
    },
    {
        "nickname": "Kimi-K2.5",
        "provider": "nvidia",
        "model": "moonshotai/kimi-k2.5",
        "tier": "strategy",
        "specialty": "long-context reasoning, orchestration, task synthesis",
        "task_types": ["architecture", "reasoning", "review"],
        "modes": ["engineer", "orchestrator"],
        "priority": 95,
    },
    {
        "nickname": "DeepSeek-V3.2",
        "provider": "nvidia",
        "model": "deepseek-ai/deepseek-v3.2",
        "tier": "logic",
        "specialty": "algorithms, debugging, API integration, edge-case analysis",
        "task_types": ["reasoning", "review", "architecture"],
        "modes": ["engineer", "orchestrator"],
        "priority": 93,
    },
    {
        "nickname": "Gemini 2.5 Pro",
        "provider": "gemini",
        "model": "gemini-2.5-pro",
        "tier": "vision",
        "specialty": "multimodal analysis, screenshots, UI/accessibility review",
        "task_types": ["visual", "review", "reasoning"],
        "modes": ["engineer", "orchestrator"],
        "priority": 96,
    },
    {
        "nickname": "Gemini 2.5 Flash",
        "provider": "gemini",
        "model": "gemini-2.5-flash",
        "tier": "fast",
        "specialty": "rapid analysis and quick turnaround",
        "task_types": ["speed", "content", "reasoning"],
        "modes": ["engineer", "orchestrator"],
        "priority": 92,
    },
    {
        "nickname": "Phi-4 Multimodal",
        "provider": "nvidia",
        "model": "microsoft/phi-4-multimodal-instruct",
        "tier": "vision",
        "specialty": "vision-language fallback and screenshot interpretation",
        "task_types": ["visual", "review"],
        "modes": ["engineer", "orchestrator"],
        "priority": 88,
    },
    {
        "nickname": "GPT-OSS 20B",
        "provider": "ollama",
        "model": "gpt-oss:20b-cloud",
        "tier": "content",
        "specialty": "copy polish, concise synthesis, text cleanup",
        "task_types": ["content", "speed"],
        "modes": ["engineer", "orchestrator"],
        "priority": 84,
    },
]

