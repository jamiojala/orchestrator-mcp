# Model Latency Budgeter

Category: `routing`
Source: `Advanced first-party pack`

Superpower: Tune timeout, retry, and concurrency budgets across multi-model routes so orchestration stays fast without silent quality collapse.

## Trigger signals
- `latency budget`
- `timeout policy`
- `model concurrency`
- `routing policy`

## Best-fit files
- `**/*.yaml`
- `**/*.yml`
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
- `verify_latency_slo`
- `verify_text_unchanged`

## Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`
