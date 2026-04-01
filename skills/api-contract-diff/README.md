# API Contract Diff

Category: `api`
Source: `Advanced first-party pack`

Superpower: Compare two API or schema revisions and surface behavioral breakage, migration steps, and compatibility risk.

## Trigger signals
- `api diff`
- `schema diff`
- `breaking change`
- `compatibility`

## Best-fit files

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Schema drift or naming ambiguity leaks into downstream tool or API consumers.
- Diffs look clean while backward compatibility quietly breaks at the edge.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Keep contract snapshots or diffs visible during rollout and review.
- Treat consumer migration notes as part of the deliverable, not an optional appendix.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with routing, security, and testing packs once the interface surface is clear.

## Validation hooks
- `generate_diff`

## Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
