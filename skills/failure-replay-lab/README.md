# Failure Replay Lab

Category: `debugging`
Source: `Advanced first-party pack`

Superpower: Investigate a failed delegation by replaying context, isolating likely root causes, and proposing the smallest reliable recovery path.

## Trigger signals
- `failed delegation`
- `replay`
- `retry`
- `incident`
- `recover`

## Best-fit files

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- The reproduction path stays too vague to catch the failure again later.
- A one-off fix lands without preserving the evidence trail for future regressions.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Preserve the minimal repro and failure fingerprint so future agents can restart quickly.
- Prefer instrumentation that narrows the next diagnostic step instead of broad logging dumps.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with testing and release packs when a repro should become a durable guardrail.

## Validation hooks
- `generate_diff`

## Preferred models
- `deepseek-ai/deepseek-v3.2`
- `gemini-2.5-pro`
