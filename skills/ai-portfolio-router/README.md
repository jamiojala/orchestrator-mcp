# AI Portfolio Router

Category: `routing`
Source: `Advanced first-party pack`

Superpower: Allocate work across local, cloud, and premium models so teams maximize capability coverage per dollar and per latency budget.

## Trigger signals
- `model portfolio`
- `ai roi`
- `routing strategy`
- `budget pressure`

## Best-fit files
- `**/*.md`
- `**/budgets/**`
- `**/routing/**`
- `**/config/**`

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Faster or cheaper routes silently degrade answer quality without an escalation rule.
- Routing logic optimizes averages while breaking the tail latencies users actually feel.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Track both latency and answer quality before changing default lanes permanently.
- Make escalation to slower or more expensive models rule-based instead of ad hoc.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration, data, and testing packs when route quality must be measured, not guessed.

## Validation hooks
- `verify_roi_assumptions`
- `verify_text_unchanged`

## Preferred models
- `deepseek-ai/deepseek-v3.2`
- `meta/llama-3.3-70b-instruct`
- `deepseek-r1:32b`
