# API Documentation Generator

Category: `content`
Version: `1.0.0`

Superpower: Turn API implementation detail into example-rich docs that developers can actually use without reading source first.

## Trigger signals
- `api documentation`
- `openapi docs`
- `examples`

## Best-fit files
- `**/api/**`
- `**/*.md`
- `**/*.yaml`

## Inputs to gather
- Relevant files, modules, docs, or data slices that define the current surface area.
- Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
- What success looks like in user, operator, or system terms.
- Source material, audience sophistication, and implementation details the docs must stay faithful to.

## Recommended workflow
1. Restate the goal, boundaries, and success metric in operational terms.
2. Map the files, surfaces, or decisions most likely to matter first.
3. Cross-check source truth and version fidelity before restructuring the material.
4. Produce a bounded plan with explicit validation hooks.
5. Return rollout, fallback, and open-question notes for handoff.

## Deliverables
- Capability summary and why this skill fits the request.
- Concrete implementation or decision slices with explicit targets.
- Validation, rollout, and rollback guidance sized to the risk.
- Structure that preserves technical fidelity while improving comprehension.
- Example, version, or setup gaps that must be fixed before publication.
- Validation plan covering `verify_example_accuracy`.

## Failure modes to watch
- The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.
- Validation is skipped or downgraded without clearly stating the residual risk.
- The work lands as a broad rewrite instead of a bounded, reversible slice.
- The content reads well but drifts from the actual implementation or supported setup.
- Examples are persuasive but not runnable or version-accurate.

## Operational notes
- Call out the smallest safe rollout slice before proposing broader adoption.
- Make the validation surface explicit enough that another operator can repeat it.
- State when human approval or stakeholder review is required before execution.
- Version examples and setup notes so maintainers know when the pack is stale.
- Cross-link the authoritative implementation or config surface where possible.

## Dependency and composition notes
- Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.
- If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.
- Often composes with product, backend, and business packs to keep docs accurate and decision-useful.

## Validation hooks
- `verify_example_accuracy`

## Model preferences
- primary: `qwen3-coder:480b-cloud`
- fallback: `meta/llama-3.3-70b-instruct`
- local: `qwen2.5-coder:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `marketplace.yaml` for catalog metadata and richer automation
