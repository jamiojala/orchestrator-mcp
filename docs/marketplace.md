# Marketplace

<p class="omcp-lead">
  The marketplace is not a side feature. It is one half of the product surface. You can run the full
  local orchestration layer, or you can take the packs as portable assets and leave the runtime out.
</p>

## What ships in the library

<div class="omcp-grid omcp-grid--two">
  <article class="omcp-panel">
    <p class="omcp-label">On disk</p>
    <h3>120 real pack folders</h3>
    <p>
      The repo materializes the library directly in <code>skills/</code> instead of hiding it behind runtime-only
      export commands.
    </p>
  </article>
  <article class="omcp-panel">
    <p class="omcp-label">Catalog</p>
    <h3>100 global skills plus 20 advanced first-party packs</h3>
    <p>
      The core catalog covers 10 product and engineering domains, and the first-party additions lean
      harder into orchestration, routing, safety, release hygiene, and AI optimization.
    </p>
  </article>
</div>

## Browse the catalog on the site

- [Skills Library overview](./skills)
- [Advanced first-party packs](./skills-categories/advanced-packs)
- [Architecture & System Design](./skills-categories/architecture)
- [Frontend Engineering](./skills-categories/frontend)
- [Backend & API Design](./skills-categories/backend)
- [Quality Assurance](./skills-categories/qa)
- [DevOps & Infrastructure](./skills-categories/devops)
- [Security & Compliance](./skills-categories/security)
- [Data & Analytics](./skills-categories/data)
- [Product & UX](./skills-categories/product)
- [Content & Communication](./skills-categories/content)
- [Business & Operations](./skills-categories/business)

## Pack anatomy

Every pack includes:

- `SKILL.md` for portable markdown-first agent usage
- `skill.yaml` for structured registry loading inside `orchestrator-mcp`
- `marketplace.yaml` for richer metadata and catalog indexing
- `README.md` for human-readable installation and review context

## Browse and export with the CLI

```bash
orchestrator-mcp skills list
orchestrator-mcp skills show micro-frontend-orchestrator
orchestrator-mcp skills export micro-frontend-orchestrator --to ./exported-skills
orchestrator-mcp skills export-category --category frontend --to ./exported-skills
```

## Use packs separately

If you only want the skill layer:

- copy an individual folder from `skills/`
- keep the whole folder when you want the full metadata surface
- copy only `SKILL.md` when the target ecosystem is markdown-first and lightweight
- use the web catalog as a stable browsing layer before exporting packs into another setup
