# orchestrator-mcp

`orchestrator-mcp` is a local-first orchestration layer for developers who use more than one coding model or coding agent. It gives Codex, Claude Code, Kimi Code, and other MCP-capable clients a shared MCP server for safe delegation, smart routing, semantic caching, budget-aware fallbacks, and observability.

If your workflow already spans Ollama, Gemini, NVIDIA-hosted models, or multiple agent subscriptions, this repo turns that stack into one reusable local tool instead of scattered editor-specific prompt glue.

## Suggested GitHub positioning

- Repository description: `Local-first MCP server for multi-LLM orchestration across Codex, Claude Code, Kimi Code, Ollama, Gemini, and NVIDIA models.`
- Suggested topics: `mcp`, `model-context-protocol`, `llm`, `multi-agent`, `ollama`, `claude-code`, `codex`, `kimi-code`, `developer-tools`, `ai-tooling`

## Why this exists

Most coding agents are excellent inside one model silo. Real developer setups are not:

- Codex for repo-native implementation
- Claude Code for long-form reasoning and planning
- Kimi Code for IDE-first iteration and MCP-rich tooling
- Ollama or Ollama Pro for cheap open-model capacity
- Gemini or NVIDIA-hosted specialists for multimodal review and fallback reasoning

`orchestrator-mcp` gives those workflows one consistent local server surface.

## Core features

- Backward-compatible MCP tools including `llm_ask`, `llm_chat`, `dispatch_parallel`, `estimate_complexity`, and `llm_orchestrate`
- Safety guardrails for secret redaction, malicious prompt blocking, model-name validation, and public-release scanning
- Cost-aware routing with fallback chains, daily and weekly budget pressure, and Ollama-first "poor man's mode"
- Semantic caching with local SQLite persistence
- Streamlit dashboard for recent runs, failures, cache hits, and estimated project spend
- YAML skill registry for reusable routing rules and validation logic
- Safe git-analysis helpers for commit messages, PR descriptions, and review summaries without mutating the repo

## Cheapest default recommendation

For most developers, the best cost-to-capability starting point is:

1. Local Ollama or Ollama Pro for the bulk of coding and parallel delegation
2. Gemini for multimodal review and fast cloud fallback
3. NVIDIA-hosted Kimi or DeepSeek models for reasoning-heavy sidecars

If budget matters most, enable `poor_mans_mode` and route to local/Ollama models first.

## Install

### Python package

```bash
pip install "orchestrator-mcp[dashboard]"
```

For contributors:

```bash
pip install -e ".[dashboard,docs,dev]"
```

## One-paste installs

### Codex

If you want a direct command:

```bash
codex mcp add orchestrator -- python -m orchestrator_mcp.cli serve
```

Config-file snippet:

```toml
[mcp_servers.orchestrator]
command = "python"
args = ["-m", "orchestrator_mcp.cli", "serve"]
```

OpenAI documents `codex mcp add` and config-file MCP setup in the Codex docs. Source: [OpenAI Docs MCP quickstart](https://developers.openai.com/learn/docs-mcp).

### Claude Code

```bash
claude mcp add orchestrator -- python -m orchestrator_mcp.cli serve
```

Project config example:

```json
{
  "mcpServers": {
    "orchestrator": {
      "command": "python",
      "args": ["-m", "orchestrator_mcp.cli", "serve"]
    }
  }
}
```

Anthropic documents `claude mcp add`, `claude mcp list`, scopes, and project-level `.mcp.json` usage in the Claude Code MCP docs.

### Kimi Code

Kimi Code currently documents local MCP servers through its MCP Servers UI with `stdio` transport.

Paste these values into the Kimi Code MCP server form:

- Name: `orchestrator`
- Transport: `stdio`
- Command: `python`
- Args: `-m orchestrator_mcp.cli serve`

If your Kimi setup exposes raw JSON for local stdio servers, use the same command and args from the examples in [`examples/kimi-stdio.json`](examples/kimi-stdio.json).

Source: [Kimi Code MCP setup docs](https://www.kimi.com/code/docs/en/kimi-code-for-vscode/guides/getting-started.html)

### Generic MCP client

Any stdio-capable MCP client can launch:

```bash
python -m orchestrator_mcp.cli serve
```

## Quick start

```bash
cp .env.example .env
cp orchestrator-mcp.yaml.example orchestrator-mcp.yaml
orchestrator-mcp doctor
orchestrator-mcp serve
```

Launch the dashboard:

```bash
orchestrator-mcp dashboard
```

## Configuration

Important settings in `orchestrator-mcp.yaml`:

- `budgets.daily_usd` and `budgets.weekly_usd`: keeps model usage under control
- `budgets.poor_mans_mode`: aggressively prefers cheap/local routes
- `skills_dir`: loads reusable community skills
- `pricing`: override the default provider cost table if your pricing differs
- `models` and `workflows`: project-specific routing policy

## Safety model

`orchestrator-mcp` is intentionally narrower than a shell-capable coding agent.

- It does not execute shell commands
- It does not crawl your filesystem for context
- It redacts obvious secrets before outbound model calls
- It blocks clear malware, phishing, and credential-exfiltration requests
- It includes a release scanner for common leaks such as API keys and absolute local paths

Run the public-release scan:

```bash
orchestrator-mcp doctor
```

## CLI

```bash
orchestrator-mcp serve
orchestrator-mcp dashboard
orchestrator-mcp doctor
orchestrator-mcp benchmark
orchestrator-mcp cinematic-upgrade --path ./your-project
```

## Skill registry

Skills live in `skills/<slug>/skill.yaml` and can define:

- trigger keywords
- preferred models
- prompt templates
- validation steps

The repo also ships a first-party downloadable skill library. Newer skills include portable `SKILL.md` packs so they can be copied into other agent ecosystems, not just this MCP.

## Repository contents

- `src/orchestrator_mcp/`: core package
- `skills/`: skill manifests
- `examples/`: copy-paste client config examples
- `docs/`: MkDocs site content
- `tests/`: regression and safety coverage
- `scripts/check_public_repo.py`: release-time hygiene scan

## Development

```bash
pytest
python -m py_compile llm_delegator_mcp.py src/orchestrator_mcp/*.py
python scripts/check_public_repo.py
```

## Documentation

See [`docs/index.md`](docs/index.md) or serve the site locally:

```bash
mkdocs serve
```

## License

Apache-2.0
