# Prompt Pack Documenter

Category: `docs`
Source: `Advanced first-party pack`

Superpower: Turn advanced agent workflows into reusable skill and prompt packs with trigger rules, output contracts, and maintainable docs.

## Trigger signals
- `prompt pack`
- `skill docs`
- `workflow documentation`
- `portable skills`

## Best-fit files
- `**/*.md`
- `**/skills/**`
- `**/prompts/**`
- `**/docs/**`

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Portable pack docs drift from the real runtime surface after the next product change.
- The pack becomes reusable in theory but underspecified in actual agent handoffs.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Cross-link the pack to the runtime or code surface it documents so drift is easier to spot.
- Version the examples or assumptions that are likely to change quickly.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration, api, and release packs when a workflow needs to travel cleanly.

## Validation hooks
- `verify_prompt_usability`
- `verify_text_unchanged`

## Preferred models
- `meta/llama-3.3-70b-instruct`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`
