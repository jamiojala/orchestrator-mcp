# orchestrator-mcp

`orchestrator-mcp` is a local-first MCP server for multi-LLM orchestration.

It is built for developers who:

- use multiple coding agents
- want one shared local routing layer
- care about safe defaults
- want better cost control than "just send everything to the most expensive model"

## What it gives you

- model routing across Ollama, Gemini, and NVIDIA-backed providers
- semantic caching and budget-aware fallback
- safe delegation helpers for Codex-style orchestration
- local observability for recent runs and failures
- public-release hygiene scanning

Start with [Quickstart](quickstart.md) or jump straight to [One-Paste Installs](one-paste-installs.md).
