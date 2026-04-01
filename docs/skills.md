# Skills Library

SkillForge now ships a 130-pack on-disk skill library built for portable agent workflows, MCP runtime loading, and web-facing discoverability.

## Library summary

<div class="omcp-kpi-strip">
  <div class="omcp-kpi">
    <strong>130</strong>
    <span>pack folders on disk</span>
  </div>
  <div class="omcp-kpi">
    <strong>110</strong>
    <span>global library packs</span>
  </div>
  <div class="omcp-kpi">
    <strong>20</strong>
    <span>advanced first-party packs</span>
  </div>
  <div class="omcp-kpi">
    <strong>4</strong>
    <span>portable files per pack</span>
  </div>
</div>

## What is in the library

- 20 advanced first-party packs focused on orchestration, safety, release hygiene, and AI-optimization work.
- 110 Superpower Tier global library packs covering the cross-domain catalog defined for the project, including the new AI/ML engineering slice.
- Every pack ships with `README.md`, `SKILL.md`, `skill.yaml`, and `marketplace.yaml`.

## Browse by domain

- [Advanced First-Party Packs](skills-categories/advanced-packs.md): 20 skills
- [Architecture & System Design](skills-categories/architecture.md): 10 skills
- [Frontend Engineering](skills-categories/frontend.md): 15 skills
- [Backend & API Design](skills-categories/backend.md): 12 skills
- [Quality Assurance](skills-categories/qa.md): 10 skills
- [DevOps & Infrastructure](skills-categories/devops.md): 10 skills
- [Security & Compliance](skills-categories/security.md): 10 skills
- [Data & Analytics](skills-categories/data.md): 8 skills
- [Product & UX](skills-categories/product.md): 10 skills
- [Content & Communication](skills-categories/content.md): 8 skills
- [Business & Operations](skills-categories/business.md): 7 skills
- [AI/ML Engineering](skills-categories/ai-ml.md): 10 skills

## How to read one pack

The most useful idea from the external SkillForge-style reference is the explicit manifest contract.
In this repo, each pack is designed to be legible before you run it.

| Field or file | What it tells you |
| --- | --- |
| `README.md` | human-readable overview, intended use, and review context |
| `SKILL.md` | portable markdown-first instructions for agent use |
| `skill.yaml` | structured registry loading and trigger metadata |
| `marketplace.yaml` | richer marketplace metadata and catalog indexing |
| Persona | the expert role, experience level, and specialist posture the pack is trying to adopt |
| Voice and tone | how the pack should communicate and what it should avoid sounding like |
| Thinking pattern | the reasoning steps, verification checks, and decision criteria behind the output |
| Response shape | the sections and must-have elements the answer should include |
| Trigger signals | when the pack should activate |
| Preferred models | which model chain best fits the work |
| Validation hooks | what should be checked before the work is considered done |
| Failure modes and operational notes | where the pack can go wrong and how to hand it off safely |

## Persona architecture

The useful part of the Kimi persona material is not roleplay. It is explicit specialist posture.

- role and experience make the pack's quality bar easier to understand
- voice and tone keep outputs from collapsing into generic assistant prose
- thinking patterns make the workflow repeatable and auditable
- response shape helps markdown-first installs in Claude, Codex, and similar tools stay consistent

Read [Persona Architecture](./persona-architecture) for the design rationale behind the persona-enhanced marketplace packs.

## Domain table

| Area | Count | First stop |
| --- | ---: | --- |
| Advanced first-party packs | 20 | [Advanced Packs](skills-categories/advanced-packs.md) |
| Architecture & System Design | 10 | [Architecture](skills-categories/architecture.md) |
| Frontend Engineering | 15 | [Frontend](skills-categories/frontend.md) |
| Backend & API Design | 12 | [Backend](skills-categories/backend.md) |
| Quality Assurance | 10 | [QA](skills-categories/qa.md) |
| DevOps & Infrastructure | 10 | [DevOps](skills-categories/devops.md) |
| Security & Compliance | 10 | [Security](skills-categories/security.md) |
| Data & Analytics | 8 | [Data](skills-categories/data.md) |
| Product & UX | 10 | [Product](skills-categories/product.md) |
| Content & Communication | 8 | [Content](skills-categories/content.md) |
| Business & Operations | 7 | [Business](skills-categories/business.md) |
| AI/ML Engineering | 10 | [AI/ML](skills-categories/ai-ml.md) |

## Why these packs are useful in practice

- they are stored directly in the repo, so the public site and shipped files stay aligned
- they expose enough metadata to reason about delegation and validation instead of trusting invisible prompt logic
- they can be copied whole into another environment or reduced to `SKILL.md` when a target system is markdown-first
- they are grouped for search, browsing, and SEO instead of being buried in runtime-only export commands

## Why these pages exist

The repo now materializes the skill library as real files and real web pages instead of hiding most of the catalog behind runtime-only export commands. That makes the catalog easier to browse, index, audit, and reuse.

## SEO and portability surface

- Search-friendly category pages with stable skill headings
- Portable pack files stored directly in the repository
- Internal linking between the landing page and each domain page
- Consistent metadata across runtime, marketplace, and docs surfaces
