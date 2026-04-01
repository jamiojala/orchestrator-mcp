# Marketplace

The repository is designed to work as both:

1. a local-first MCP server
2. a standalone skill marketplace

## Scope

The core marketplace covers 100 skills across:

- Architecture and system design
- Frontend engineering
- Backend and API design
- Quality assurance
- DevOps and infrastructure
- Security and compliance
- Data and analytics
- Product and UX
- Content and communication
- Business and operations

On top of that, the repo also includes curated first-party packs such as:

- `public-repo-sanitizer`
- `mcp-server-hardening`
- `cost-router-tuner`
- `failure-replay-lab`
- `threat-model-synthesizer`

## Browse and export

```bash
orchestrator-mcp skills list
orchestrator-mcp skills show micro-frontend-orchestrator
orchestrator-mcp skills export micro-frontend-orchestrator --to ./exported-skills
orchestrator-mcp skills export-category --category frontend --to ./exported-skills
```

Each exported skill pack contains:

- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for orchestrator-mcp registry usage
- `marketplace.yaml` for richer marketplace metadata
- `README.md` for human-readable install guidance
