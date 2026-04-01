# Skill Library

This repository includes a complete on-disk skill library for `orchestrator-mcp` and for other agent ecosystems that can consume portable skill packs.

## Library shape

- 20 advanced first-party packs
- 100 Superpower Tier global library packs
- 120 total skill packs on disk

## Every pack includes

- `README.md` for human-readable install and review context
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `marketplace.yaml` for richer metadata and catalog indexing

## Browse on the docs site

- `docs/skills.md` for the library landing page
- `docs/skills-categories/` for category pages grouped for web discovery and SEO

## Use packs directly

Pick any folder in `skills/` and use it as a standalone pack.

- Keep the whole folder if you want the full metadata surface
- Copy `SKILL.md` when a client only supports markdown-first skill instructions
- Use `skill.yaml` and `marketplace.yaml` when you want richer registry or catalog metadata
