# Public Repo Sanitizer

Category: `release`
Source: `Advanced first-party pack`

Superpower: Audit a repo for secrets, personal paths, client-specific references, and OSS-readiness gaps before publishing.

## Trigger signals
- `open source`
- `public repo`
- `sanitize`
- `release`
- `publish`
- `secret scan`

## Best-fit files

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Release hygiene checks exist but are too narrow to catch high-cost leaks.
- The pack flags noise instead of the operator-visible failure modes that matter.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Tie hygiene checks to a concrete release gate or review step.
- Separate high-confidence blockers from advisory findings so the operator can act quickly.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with security, debugging, and docs packs to turn checks into operator-ready release gates.

## Validation hooks
- `git_delegate_code_review`

## Preferred models
- `deepseek-ai/deepseek-v3.2`
- `gemini-2.5-pro`
