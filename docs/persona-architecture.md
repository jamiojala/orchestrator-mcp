# Persona Architecture

<p class="omcp-lead">
  The strongest packs in SkillForge are not just trigger words plus a prompt blob. They carry a
  usable expert posture: role, voice, reasoning pattern, verification habits, and a predictable
  response shape. That is the difference between "tips" and work that feels production-minded.
</p>

## Why this matters

Without persona architecture, a pack often degrades into generic advice. It may know the topic, but
it does not consistently approach the problem like a real specialist.

With persona architecture, a pack can be much more explicit about:

- who it is trying to sound and think like
- what quality bar it is holding
- how it reasons through the task
- what it should avoid
- how it should present the answer

## The SkillForge persona stack

Every persona-enhanced marketplace pack now carries four layers in its pack metadata and markdown surface.

| Layer | What it gives you |
| --- | --- |
| Persona | Role, experience level, traits, and specializations |
| Voice | Communication style, tone, and patterns to avoid |
| Thinking | Analysis approach, reasoning steps, and verification checklist |
| Response shape | Expected sections and must-have output elements |

## What this looks like in practice

<div class="omcp-grid omcp-grid--two">
  <article class="omcp-panel">
    <p class="omcp-label">Craft persona</p>
    <h3>Liquid Glass Enforcer</h3>
    <p>
      The pack now behaves like a senior UI craftsperson: detail-obsessed, performance-aware,
      accessibility-conscious, and explicit about why a visual choice is worth making.
    </p>
  </article>
  <article class="omcp-panel">
    <p class="omcp-label">Guardian persona</p>
    <h3>GDPR-by-Design Architect</h3>
    <p>
      The pack approaches privacy work like a DPO and privacy engineer, not like a generic compliance
      assistant. Lawful basis, user rights, retention, and documentation all stay in frame.
    </p>
  </article>
  <article class="omcp-panel">
    <p class="omcp-label">Strategist persona</p>
    <h3>Grant Proposal Architect</h3>
    <p>
      The pack now carries reviewer-aware strategic writing posture: evidence, significance,
      feasibility, and criteria fit instead of inflated funding-speak.
    </p>
  </article>
  <article class="omcp-panel">
    <p class="omcp-label">AI systems persona</p>
    <h3>RAG System Architect</h3>
    <p>
      The pack works like a retrieval systems engineer: benchmark-oriented, citation-aware, and
      disciplined about chunking, latency, cost, and rollback.
    </p>
  </article>
</div>

## Design principle

Persona architecture should make a pack sharper, not bloated.

- It should constrain the skill toward better judgment.
- It should not turn the skill into roleplay fluff.
- It should make failure modes easier to spot.
- It should help portable markdown-first usage, not depend on hidden runtime machinery.

## What ships today

- All generated marketplace packs now include persona, voice, thinking, and response-shape metadata in `marketplace.yaml`.
- Their `README.md` and `SKILL.md` surfaces now expose the same persona architecture for markdown-first installs.
- Signature packs such as `liquid-glass-enforcer`, `gdpr-by-design-architect`, `grant-proposal-architect`, and `rag-system-architect` use richer overrides instead of only category defaults.

## Boundaries

Persona architecture is an accelerator, not a magic trick.

- It does not replace real validation.
- It does not justify copying low-quality work with more confident wording.
- It should stay grounded in the actual repo, task, and operator constraints.
- It should remain inspectable and editable as plain repo files.
