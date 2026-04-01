# Contributing

Thanks for helping improve `orchestrator-mcp`.

## Local setup

```bash
git clone https://github.com/jamiojala/orchestrator-mcp.git
cd orchestrator-mcp
pip install -e ".[dashboard,docs,dev]"
cp .env.example .env
cp orchestrator-mcp.yaml.example orchestrator-mcp.yaml
```

## Before opening a pull request

```bash
pytest
python -m py_compile llm_delegator_mcp.py src/orchestrator_mcp/*.py
python scripts/check_public_repo.py
```

## Contribution guidelines

- Keep changes small and reviewable
- Prefer environment variables over inline secrets
- Do not commit local paths, logs, caches, or private editor config
- Add tests for behavior changes where practical
- Keep docs and example install snippets aligned with the actual code
- Avoid adding shell execution or arbitrary filesystem exfiltration to the MCP server

## Skills and examples

Reusable routing packs belong in `skills/<slug>/skill.yaml`.

Client install snippets belong in `examples/`.
