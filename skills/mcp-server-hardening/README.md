# MCP Server Hardening

Category: `security`
Source: `Advanced first-party pack`

Superpower: Review an MCP server for prompt-exfiltration, shell abuse, overbroad tool scope, and unsafe logging.

## Trigger signals
- `mcp hardening`
- `prompt exfiltration`
- `tool scope`
- `unsafe logging`
- `server safety`

## Best-fit files

## Output contract
- Capability summary and trigger fit
- Implementation slices or recommendations with clear targets
- Validation and rollout notes

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- The security story looks complete while indirect prompt, repo, or release paths remain exposed.
- Mitigations depend on operator memory instead of hard guardrails.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Record what was hardened, what remains exposed, and where human approval is still required.
- Prefer controls that fail closed when context quality or operator confidence is low.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration, release, and api packs when guardrails span multiple surfaces.

## Validation hooks
- `git_delegate_code_review`

## Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
