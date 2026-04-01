# Docker Layer Optimizer

Category: `devops`
Version: `1.0.0`

Superpower: Shrink container builds and speed up rebuilds through smarter layer ordering and multi-stage decomposition.

## Trigger signals
- `docker layer`
- `multi stage`
- `image size`

## Best-fit files
- `**/Dockerfile*`
- `**/.dockerignore`

## Inputs to gather
- Relevant files, modules, docs, or data slices that define the current surface area.
- Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
- What success looks like in user, operator, or system terms.
- Environment topology, deployment path, secrets handling, and rollback expectations.

## Recommended workflow
1. Restate the goal, boundaries, and success metric in operational terms.
2. Map the files, surfaces, or decisions most likely to matter first.
3. Sequence rollout, rollback, and environment drift concerns before optimizing efficiency.
4. Produce a bounded plan with explicit validation hooks.
5. Return rollout, fallback, and open-question notes for handoff.

## Deliverables
- Capability summary and why this skill fits the request.
- Concrete implementation or decision slices with explicit targets.
- Validation, rollout, and rollback guidance sized to the risk.
- Operator-ready rollout sequence with promotion and rollback checkpoints.
- Environment-specific caveats, secrets, and drift risks.
- Validation plan covering `verify_image_size`.

## Failure modes to watch
- The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.
- Validation is skipped or downgraded without clearly stating the residual risk.
- The work lands as a broad rewrite instead of a bounded, reversible slice.
- Operator complexity rises because rollout, rollback, or secrets handling stays implicit.
- Environment-specific assumptions leak into reusable infrastructure defaults.

## Operational notes
- Call out the smallest safe rollout slice before proposing broader adoption.
- Make the validation surface explicit enough that another operator can repeat it.
- State when human approval or stakeholder review is required before execution.
- Tie rollouts to explicit health thresholds, rollback triggers, and environment boundaries.
- Document the operator path for secrets, permissions, and drift checks.

## Dependency and composition notes
- Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.
- If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.
- Often composes with architecture, security, and backend packs for rollout-safe implementation.

## Validation hooks
- `verify_image_size`

## Model preferences
- primary: `deepseek-ai/deepseek-v3.2`
- fallback: `qwen3-coder:480b-cloud`
- local: `llama3.1:8b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `marketplace.yaml` for catalog metadata and richer automation
