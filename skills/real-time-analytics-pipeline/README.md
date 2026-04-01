# Real-Time Analytics Pipeline

Category: `data`
Version: `1.0.0`

Superpower: Build sub-second analytics pipelines over streaming events without turning the system into an operational mystery.

## Trigger signals
- `real time analytics`
- `clickhouse`
- `streaming`

## Best-fit files
- `**/*.sql`
- `**/stream/**`
- `**/analytics/**`

## Inputs to gather
- Relevant files, modules, docs, or data slices that define the current surface area.
- Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
- What success looks like in user, operator, or system terms.
- Data lineage, freshness requirements, downstream consumers, and privacy boundaries.

## Recommended workflow
1. Restate the goal, boundaries, and success metric in operational terms.
2. Map the files, surfaces, or decisions most likely to matter first.
3. Verify lineage, freshness, and decision value before proposing new metrics or models.
4. Produce a bounded plan with explicit validation hooks.
5. Return rollout, fallback, and open-question notes for handoff.

## Deliverables
- Capability summary and why this skill fits the request.
- Concrete implementation or decision slices with explicit targets.
- Validation, rollout, and rollback guidance sized to the risk.
- Measurement or modeling plan that preserves correctness and explainability.
- Freshness, privacy, and downstream-consumer notes.
- Validation plan covering `verify_latency_metrics`.

## Failure modes to watch
- The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.
- Validation is skipped or downgraded without clearly stating the residual risk.
- The work lands as a broad rewrite instead of a bounded, reversible slice.
- Improved metrics or models become harder to trace back to source truth.
- Freshness, privacy, or downstream consumer assumptions remain implicit.

## Operational notes
- Call out the smallest safe rollout slice before proposing broader adoption.
- Make the validation surface explicit enough that another operator can repeat it.
- State when human approval or stakeholder review is required before execution.
- Record lineage, freshness expectations, and privacy constraints with the deliverable.
- Separate measurement changes from decision changes so regressions are easier to localize.

## Dependency and composition notes
- Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.
- If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.
- Often composes with product, backend, and security packs where measurement meets privacy and operations.

## Validation hooks
- `verify_latency_metrics`

## Model preferences
- primary: `deepseek-ai/deepseek-v3.2`
- fallback: `qwen3-coder:480b-cloud`
- local: `deepseek-r1:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `marketplace.yaml` for catalog metadata and richer automation
