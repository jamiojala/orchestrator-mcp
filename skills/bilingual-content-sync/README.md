# Bilingual Content Sync

Category: `frontend`
Version: `1.0.0`

Superpower: Maintain product and UI parity across languages while adapting tone and cultural context beyond literal translation.

## Trigger signals
- `i18n`
- `translation parity`
- `localized copy`

## Best-fit files
- `**/locales/**/*.json`
- `**/i18n/**`
- `**/*.tsx`

## Inputs to gather
- Relevant files, modules, docs, or data slices that define the current surface area.
- Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
- What success looks like in user, operator, or system terms.
- Interaction states, accessibility expectations, and device or viewport constraints.

## Recommended workflow
1. Restate the goal, boundaries, and success metric in operational terms.
2. Map the files, surfaces, or decisions most likely to matter first.
3. Audit user-visible states, responsive behavior, and accessibility before styling or motion changes.
4. Produce a bounded plan with explicit validation hooks.
5. Return rollout, fallback, and open-question notes for handoff.

## Deliverables
- Capability summary and why this skill fits the request.
- Concrete implementation or decision slices with explicit targets.
- Validation, rollout, and rollback guidance sized to the risk.
- UI or interaction recommendations tied to concrete components, states, and accessibility outcomes.
- Performance notes for motion, rendering, and asset cost.
- Validation plan covering `verify_translation_coverage`.

## Failure modes to watch
- The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.
- Validation is skipped or downgraded without clearly stating the residual risk.
- The work lands as a broad rewrite instead of a bounded, reversible slice.
- Visual or motion upgrades reduce accessibility, responsiveness, or input clarity.
- Hydration, bundle, or rendering cost increases without an explicit budget check.

## Operational notes
- Call out the smallest safe rollout slice before proposing broader adoption.
- Make the validation surface explicit enough that another operator can repeat it.
- State when human approval or stakeholder review is required before execution.
- Verify critical flows on the devices and motion preferences that matter most.
- Track bundle, hydration, and interaction regressions alongside visual polish.

## Dependency and composition notes
- Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.
- If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.
- Often composes with product, qa, and accessibility-heavy UX work after the UI target is fixed.

## Validation hooks
- `verify_translation_coverage`

## Model preferences
- primary: `meta/llama-3.3-70b-instruct`
- fallback: `qwen3-coder:480b-cloud`
- local: `llama3.1:8b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `marketplace.yaml` for catalog metadata and richer automation
