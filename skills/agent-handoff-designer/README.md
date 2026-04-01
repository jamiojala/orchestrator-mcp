# Agent Handoff Designer

Category: `design`
Source: `Advanced first-party pack`

Superpower: Shape approvals, status surfaces, and human handoff moments so advanced agent workflows stay legible and trustworthy.

## Trigger signals
- `agent handoff`
- `approval ux`
- `operator trust`
- `status surface`

## Best-fit files
- `**/*.tsx`
- `**/agents/**`
- `**/*.md`
- `**/components/**`

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Operator-facing surfaces become more polished but less legible under pressure.
- High-variance visual ideas land without an evaluation path for trust or clarity.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Verify operator-critical states such as loading, waiting, approval, and failure before polish.
- Keep accessibility and motion budgets explicit in the review surface.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration and docs packs when operator trust depends on the UI shell.

## Validation hooks
- `verify_operator_clarity`
- `audit_design_compliance`

## Preferred models
- `moonshotai/kimi-k2.5`
- `meta/llama-3.3-70b-instruct`
- `qwen2.5-coder:32b`
