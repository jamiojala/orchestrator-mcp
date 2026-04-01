# Multi-Agent PRD Breakdown

Category: `orchestration`
Source: `Advanced first-party pack`

Superpower: Turn a product or engineering spec into bounded sub-tasks, ownership lanes, and integration checkpoints for multiple agents.

## Trigger signals
- `prd`
- `spec`
- `breakdown`
- `orchestrate`
- `delegate`
- `ownership`

## Best-fit files

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Context or agent boundaries look elegant but break under long-running work or human interruption.
- Delegation lanes overlap, creating duplicated work or silent ownership gaps.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Name the checkpoint where a human can safely inspect, redirect, or pause the workflow.
- Keep context summaries and delegation boundaries stable enough for later handoffs.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Often acts as the lead pack, then hands off to routing, security, docs, or testing packs with clear boundaries.

## Validation hooks
- `verify_text_unchanged`

## Preferred models
- `moonshotai/kimi-k2.5`
- `qwen3-coder:480b-cloud`
