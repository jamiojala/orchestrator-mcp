# Skill Library

This repository includes a first-party skill library designed to be useful both inside `orchestrator-mcp` and in other agent ecosystems.

This repo now has two layers:

- curated installable skills checked directly into `skills/`
- a larger marketplace catalog that can be browsed and exported on demand

## Why this matters

After reviewing adjacent ecosystems, a clear pattern emerges:

- OpenAI's public Codex skills catalog emphasizes portable task packages with instructions and resources
- Anthropic has pushed Agent Skills toward an open transferable format
- Cursor relies on reusable rules and scoped context
- Roo Code leans heavily on role-based modes and orchestrator patterns

The gap is a public skill library that is both:

- practical for day-to-day coding work
- opinionated about safety, release hygiene, and multi-model orchestration

This folder aims to fill that gap.

## Included skills

### Core engineering

- `multi-agent-prd-breakdown`
- `api-contract-diff`
- `test-matrix-generator`
- `docs-sync-guardian`

### Safety and release

- `public-repo-sanitizer`
- `mcp-server-hardening`
- `threat-model-synthesizer`
- `failure-replay-lab`

### Routing and quality

- `cost-router-tuner`
- `design-system-drift-audit`
- `cinematic-upgrade`

## Install patterns

### Use inside orchestrator-mcp

Point `skills_dir` at this folder or copy selected skill folders into your own project-level `skills/` directory.

### Use inside Codex

If your Codex environment supports GitHub-directory skill install, install a single folder from this repo and restart Codex.

### Use inside other agent systems

Portable skills include a `SKILL.md` with frontmatter so they can be copied into systems that understand agent-skill style markdown packages.

### Use the repo as a marketplace

```bash
orchestrator-mcp skills list
orchestrator-mcp skills show public-repo-sanitizer
orchestrator-mcp skills export public-repo-sanitizer --to ./exported-skills
orchestrator-mcp skills export-category --category frontend --to ./exported-skills
```

## Design principles

- Each skill should be installable on its own
- Each skill should state when to use it and what output shape to expect
- Skills should push safe defaults, not hidden automation
- Novel skills should solve gaps that general coding agents still handle poorly
