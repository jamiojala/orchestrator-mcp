# Skills

`orchestrator-mcp` now supports two skill formats:

- local `skill.yaml` manifests
- portable `SKILL.md` packs with frontmatter

That makes the repo useful both as a runtime registry and as a downloadable skill library.

## Included first-party library

- cinematic-upgrade
- public-repo-sanitizer
- mcp-server-hardening
- multi-agent-prd-breakdown
- failure-replay-lab
- cost-router-tuner
- design-system-drift-audit
- api-contract-diff
- docs-sync-guardian
- test-matrix-generator
- threat-model-synthesizer

See `skills/README.md` for install and portability guidance.

## Marketplace commands

```bash
orchestrator-mcp skills list
orchestrator-mcp skills show liquid-glass-enforcer
orchestrator-mcp skills export liquid-glass-enforcer --to ./exported-skills
orchestrator-mcp skills export-category --category security --to ./exported-skills
```

This makes the repo useful even for teams that do not want the MCP runtime and only want portable skill packs.
