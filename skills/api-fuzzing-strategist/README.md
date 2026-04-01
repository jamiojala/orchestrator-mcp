# API Fuzzing Strategist

Category: `qa`
Version: `1.0.0`

Superpower: Build property-based and boundary-oriented API tests that find input handling failures before attackers or customers do.

## Trigger signals
- `api fuzzing`
- `property based`
- `boundary values`

## Best-fit files
- `**/api/**`
- `**/tests/**`
- `**/*.ts`

## Inputs to gather
- Relevant files, modules, docs, or data slices that define the current surface area.
- Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
- What success looks like in user, operator, or system terms.
- Current regressions, flaky surfaces, and what confidence signals already exist or are missing.

## Recommended workflow
1. Restate the goal, boundaries, and success metric in operational terms.
2. Map the files, surfaces, or decisions most likely to matter first.
3. Start from failure reproduction and confidence gaps before expanding test surface area.
4. Produce a bounded plan with explicit validation hooks.
5. Return rollout, fallback, and open-question notes for handoff.

## Deliverables
- Capability summary and why this skill fits the request.
- Concrete implementation or decision slices with explicit targets.
- Validation, rollout, and rollback guidance sized to the risk.
- Regression matrix with must-test, edge, and deferred paths.
- A deterministic reproduction or instrumentation path where possible.
- Validation plan covering `verify_boundary_coverage`.

## Failure modes to watch
- The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.
- Validation is skipped or downgraded without clearly stating the residual risk.
- The work lands as a broad rewrite instead of a bounded, reversible slice.
- The suite grows while confidence stays flat because the real failure mode is still untested.
- Flaky signals are normalized instead of isolated and explained.

## Operational notes
- Call out the smallest safe rollout slice before proposing broader adoption.
- Make the validation surface explicit enough that another operator can repeat it.
- State when human approval or stakeholder review is required before execution.
- Keep the reproduction path close to the failing behavior so future regressions are diagnosable.
- Prefer test fixtures and seed data that are cheap to regenerate in CI.

## Dependency and composition notes
- Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.
- If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.
- Often composes with frontend, backend, and security packs to turn findings into durable regressions.

## Validation hooks
- `verify_boundary_coverage`

## Model preferences
- primary: `deepseek-ai/deepseek-v3.2`
- fallback: `qwen3-coder:480b-cloud`
- local: `deepseek-r1:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `marketplace.yaml` for catalog metadata and richer automation
