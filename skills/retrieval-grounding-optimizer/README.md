# Retrieval Grounding Optimizer

Category: `data`
Source: `Advanced first-party pack`

Superpower: Improve chunking, metadata, and ranking design so agent answers stay grounded under larger repositories and longer tasks.

## Trigger signals
- `retrieval`
- `chunking`
- `grounding`
- `ranking`

## Best-fit files
- `**/docs/**`
- `**/*.md`
- `**/embeddings/**`
- `**/retrieval/**`

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Grounding improves on one workflow while precision regresses on long-tail lookups.
- Metadata or chunking changes make debugging harder even if recall appears higher.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Measure both retrieval quality and debuggability after changes to chunking or ranking.
- Keep source-truth links close to any generated summary or recommendation.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration and testing packs when grounding quality needs measurable proof.

## Validation hooks
- `verify_grounding_precision`
- `verify_text_unchanged`

## Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`
