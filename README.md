# orchestrator-mcp

Local-first MCP server and portable skill marketplace for serious multi-model coding workflows.

`orchestrator-mcp` gives Codex, Claude Code, Kimi Code, and other MCP-capable clients one shared local orchestration layer for safe delegation, model routing, semantic caching, budget-aware fallbacks, and observability.

If your workflow already jumps between Codex, Claude Code, Kimi Code, Ollama, Gemini, or NVIDIA-backed reasoning models, this repo turns that stack into one reusable local tool instead of scattered client-specific prompt glue.

> Docs: **https://jamiojala.github.io/orchestrator-mcp/**

## Why this exists

Most coding agents are strong inside one environment. Real-world developer setups are messier.

- Codex for repo-native implementation
- Claude Code for deeper planning and review
- Kimi Code for IDE-first iteration and MCP-heavy workflows
- Ollama for cheap local capacity
- Gemini or NVIDIA-backed models for multimodal review and specialist fallback

`orchestrator-mcp` gives those workflows one consistent local server surface.

## What it is

This repo works in two modes:

### 1. Local-first MCP server

Run one shared orchestration layer for multiple coding clients and model providers.

### 2. Portable skill marketplace

Browse, inspect, and export standalone skill packs even if you do not want to run the MCP runtime itself.

## Core features

- Backward-compatible MCP tools including `llm_ask`, `llm_chat`, `dispatch_parallel`, `estimate_complexity`, and `llm_orchestrate`
- Cost-aware model routing with fallback chains and budget pressure
- Semantic caching with local SQLite persistence
- Safety guardrails for secret redaction, malicious prompt blocking, model-name validation, and public-release scanning
- Streamlit dashboard for recent runs, cache hits, failures, and estimated spend
- YAML skill registry for reusable routing rules and validation logic
- Safe git-analysis helpers for commit messages, PR descriptions, and review summaries without mutating the repo
- 120 real on-disk skill packs with a 100-skill global marketplace plus 20 advanced first-party packs for teams that want the skills without the full MCP runtime

## Why it matters

Without a shared orchestration layer, multi-model setups usually turn into:

- duplicated prompts
- inconsistent routing logic
- no cost controls
- no portable skill layer
- no unified safety checks
- editor-specific configuration drift

`orchestrator-mcp` fixes that by making orchestration local, inspectable, reusable, and portable.

## Install

### Standard install

```bash
pip install "orchestrator-mcp[dashboard]"
```

### Contributor install

```bash
pip install -e ".[dashboard,dev]"
```

Use the Python executable that installed the package. If your machine exposes `python3` instead of `python`, substitute that in the snippets below.

## One-paste installs

### Codex

```bash
codex mcp add orchestrator -- python -m orchestrator_mcp.cli serve
```

Config alternative:

```toml
[mcp_servers.orchestrator]
command = "python"
args = ["-m", "orchestrator_mcp.cli", "serve"]
```

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

### Kimi Code

Use a local MCP server with:

- Transport: `stdio`
- Command: `python`
- Args: `-m orchestrator_mcp.cli serve`

A raw example is also included in [`examples/kimi-stdio.json`](examples/kimi-stdio.json).

### Generic MCP client

Any `stdio`-capable MCP client can launch:

```bash
python -m orchestrator_mcp.cli serve
```

See [`examples/codex-config.toml`](examples/codex-config.toml), [`examples/claude-mcp.json`](examples/claude-mcp.json), and [`examples/kimi-stdio.json`](examples/kimi-stdio.json) for copy-paste starting points.

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

## Cheapest sensible default

For most developers, the best cost-to-capability starting point is:

1. Ollama or Ollama Pro for most coding and parallel delegation
2. Gemini for fast multimodal review and cloud fallback
3. NVIDIA-hosted Kimi or DeepSeek-class models for reasoning-heavy sidecars

If budget matters most, enable `poor_mans_mode` and route to local/Ollama models first.

## Configuration

Important settings in `orchestrator-mcp.yaml`:

- `budgets.daily_usd` and `budgets.weekly_usd` keep model usage under control
- `budgets.poor_mans_mode` aggressively prefers cheap or local routes
- `skills_dir` loads reusable skills
- `pricing` lets you override provider cost tables
- `models` and `workflows` define project-specific routing policy

## Safety model

`orchestrator-mcp` is intentionally narrower than a shell-capable coding agent.

It:

- does not execute shell commands
- does not crawl your filesystem for context
- redacts obvious secrets before outbound model calls
- blocks clear malware, phishing, and credential-exfiltration requests
- includes a release scanner for common leaks such as API keys and absolute local paths

Run the hygiene scan with:

```bash
orchestrator-mcp doctor
```

## Use it as a portable skill marketplace

If you only want the skills layer, you can use the repo as a standalone marketplace:

```bash
orchestrator-mcp skills list
orchestrator-mcp skills show liquid-glass-enforcer
orchestrator-mcp skills export liquid-glass-enforcer --to ./exported-skills
orchestrator-mcp skills export-category --category security --to ./exported-skills
```

The marketplace includes:

- a 120-pack on-disk library in `skills/`
- a 100-skill core marketplace across 10 domains
- 20 advanced first-party packs for orchestration, safety, routing, release hygiene, and AI optimization
- standalone packs with `README.md`, `SKILL.md`, `skill.yaml`, and `marketplace.yaml`
- real folders you can copy individually into Codex, Claude-oriented workflows, or other markdown-first agent setups

## CLI

```bash
orchestrator-mcp serve
orchestrator-mcp dashboard
orchestrator-mcp doctor
orchestrator-mcp benchmark
orchestrator-mcp cinematic-upgrade --path ./your-project
```

## Repository layout

- `src/orchestrator_mcp/`: core package
- `skills/`: 120-pack on-disk skill library and portable manifests
- `examples/`: copy-paste client config examples
- `docs/`: MkDocs site content
- `tests/`: regression and safety coverage
- `scripts/check_public_repo.py`: public release hygiene scan

## Development

```bash
python3 -m py_compile llm_delegator_mcp.py scripts/check_public_repo.py src/orchestrator_mcp/*.py tests/*.py
pytest
python3 scripts/check_public_repo.py
npm install
npm run docs:build
```

## Documentation

The full docs site lives on GitHub Pages:

https://jamiojala.github.io/orchestrator-mcp/

You can also serve docs locally:

```bash
npm install
npm run docs:dev
```

## Who this is for

This repo is for developers and teams who:

- use more than one coding model
- want safer local orchestration
- care about cost control
- want reusable skills that are not trapped inside one client
- want a cleaner bridge between MCP runtime and portable agent skills

## License

Apache-2.0
