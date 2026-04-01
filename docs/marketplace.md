# Marketplace

<p class="omcp-lead">
  The marketplace is not a side feature. It is one half of the product surface. You can run the full
  local orchestration layer, or you can take the packs as portable assets and leave the runtime out.
</p>

## By the numbers

<div class="omcp-kpi-strip">
  <div class="omcp-kpi">
    <strong>130</strong>
    <span>pack folders in the repo</span>
  </div>
  <div class="omcp-kpi">
    <strong>11</strong>
    <span>marketplace domains</span>
  </div>
  <div class="omcp-kpi">
    <strong>20</strong>
    <span>advanced first-party packs</span>
  </div>
  <div class="omcp-kpi">
    <strong>4</strong>
    <span>files per portable pack</span>
  </div>
</div>

## What ships in the library

<div class="omcp-grid omcp-grid--two">
  <article class="omcp-panel">
    <p class="omcp-label">On disk</p>
    <h3>130 real pack folders</h3>
    <p>
      The repo materializes the library directly in <code>skills/</code> instead of hiding it behind runtime-only
      export commands.
    </p>
  </article>
  <article class="omcp-panel">
    <p class="omcp-label">Catalog</p>
    <h3>110 global skills plus 20 advanced first-party packs</h3>
    <p>
      The core catalog now covers 11 product and engineering domains, and the first-party additions
      lean harder into orchestration, routing, safety, release hygiene, and AI optimization.
    </p>
  </article>
</div>

## Domain summary

| Domain | Count | Browse |
| --- | ---: | --- |
| Advanced first-party packs | 20 | [Open](./skills-categories/advanced-packs) |
| Architecture & System Design | 10 | [Open](./skills-categories/architecture) |
| Frontend Engineering | 15 | [Open](./skills-categories/frontend) |
| Backend & API Design | 12 | [Open](./skills-categories/backend) |
| Quality Assurance | 10 | [Open](./skills-categories/qa) |
| DevOps & Infrastructure | 10 | [Open](./skills-categories/devops) |
| Security & Compliance | 10 | [Open](./skills-categories/security) |
| Data & Analytics | 8 | [Open](./skills-categories/data) |
| Product & UX | 10 | [Open](./skills-categories/product) |
| Content & Communication | 8 | [Open](./skills-categories/content) |
| Business & Operations | 7 | [Open](./skills-categories/business) |
| AI/ML Engineering | 10 | [Open](./skills-categories/ai-ml) |

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
- [AI/ML Engineering](./skills-categories/ai-ml)

## Pack anatomy

Every pack includes:

- `SKILL.md` for portable markdown-first agent usage
- `skill.yaml` for structured registry loading inside the `orchestrator-mcp` runtime
- `marketplace.yaml` for richer metadata and catalog indexing
- `README.md` for human-readable installation and review context

## How to read a pack

| Surface | Why it matters |
| --- | --- |
| Persona | Shows the role, expertise, and specialist posture the pack is trying to activate |
| Voice and tone | Shows how the pack should communicate and what generic patterns it should avoid |
| Thinking pattern | Shows the reasoning steps and verification habits behind the workflow |
| Response shape | Shows the structure the pack expects the answer to follow |
| Trigger signals | Shows the keywords, file patterns, and task types that make a pack relevant |
| Preferred models | Shows the ideal model chain or fallback lane for the workflow |
| Validation hooks | Shows the minimum proof surface for calling the work complete |
| Output contract | Shows what the pack is supposed to return, not just what it is about |
| Operational notes | Shows rollout, residual risk, or handoff guidance when the work is not trivial |

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

## Persona architecture

Generated marketplace packs now carry persona metadata in addition to routing and validation.

- persona gives the expert role, experience level, and specialist posture
- voice keeps the pack from collapsing into generic assistant tone
- thinking makes the workflow inspectable through reasoning steps and verification checks
- response shape gives markdown-first installs a predictable high-quality output structure

## Why this is better than a prompt dump

- the catalog is organized by domain instead of being a flat bag of prompts
- pack metadata is explicit enough to audit and tune
- persona architecture makes specialist posture inspectable instead of hidden inside one vendor's system prompt
- model delegation and validation live next to the workflow instead of in tribal knowledge
- the web catalog and the on-disk folders are aligned, so browsing does not lie about what ships

Read [Persona Architecture](./persona-architecture) for the design model behind the persona-enhanced marketplace packs.
