# Hallucination Regression Hunter

Category: `testing`
Source: `Advanced first-party pack`

Superpower: Build eval cases that expose fabricated citations, brittle reasoning chains, and ungrounded tool usage before they hit real workflows.

## Trigger signals
- `hallucination`
- `grounding`
- `eval case`
- `agent reliability`

## Best-fit files
- `**/evals/**`
- `**/tests/**`
- `**/*.json`
- `**/*.md`

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Eval or test coverage expands without improving confidence on real failure classes.
- Generated matrices overfit the happy path and miss cross-surface regressions.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Keep the eval loop cheap enough to run during active iteration, not only before release.
- Anchor the test surface in known failure classes before adding breadth.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with debugging, routing, and orchestration packs to convert fragile insight into regression coverage.

## Validation hooks
- `verify_eval_coverage`
- `verify_text_unchanged`

## Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`
