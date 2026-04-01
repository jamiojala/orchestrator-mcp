# Accessibility-First Navigator

Category: `product`
Version: `1.0.0`

Superpower: Make site and app navigation work cleanly for keyboard and screen-reader users without feeling like a compliance add-on.

## Trigger signals
- `screen reader`
- `skip link`
- `navigation accessibility`

## Best-fit files
- `**/*.tsx`
- `**/navigation/**`
- `**/*.html`

## Inputs to gather
- Relevant files, modules, docs, or data slices that define the current surface area.
- Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
- What success looks like in user, operator, or system terms.
- Target user moment, behavioral metric, and friction that currently blocks value.

## Recommended workflow
1. Restate the goal, boundaries, and success metric in operational terms.
2. Map the files, surfaces, or decisions most likely to matter first.
3. Anchor recommendations in the target user moment and measurable outcome before feature expansion.
4. Produce a bounded plan with explicit validation hooks.
5. Return rollout, fallback, and open-question notes for handoff.

## Deliverables
- Capability summary and why this skill fits the request.
- Concrete implementation or decision slices with explicit targets.
- Validation, rollout, and rollback guidance sized to the risk.
- User-journey changes tied to a measurable product outcome.
- States, copy, or interaction guidance for critical moments.
- Validation plan covering `audit_screen_reader_compatibility`.

## Failure modes to watch
- The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.
- Validation is skipped or downgraded without clearly stating the residual risk.
- The work lands as a broad rewrite instead of a bounded, reversible slice.
- UX recommendations increase novelty without improving task completion or clarity.
- Instrumentation is missing, so the change cannot be evaluated after release.

## Operational notes
- Call out the smallest safe rollout slice before proposing broader adoption.
- Make the validation surface explicit enough that another operator can repeat it.
- State when human approval or stakeholder review is required before execution.
- Define the leading indicator that should move if the recommendation is correct.
- Keep copy, states, and instrumentation aligned during rollout.

## Dependency and composition notes
- Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.
- If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.
- Often composes with frontend, content, and data packs once the critical user moment is agreed.

## Validation hooks
- `audit_screen_reader_compatibility`

## Model preferences
- primary: `deepseek-ai/deepseek-v3.2`
- fallback: `moonshotai/kimi-k2.5`
- local: `qwen2.5-coder:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `marketplace.yaml` for catalog metadata and richer automation
