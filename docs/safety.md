# Safety

<p class="omcp-lead">
  SkillForge is intentionally narrower than a shell-capable coding agent. The current
  <code>orchestrator-mcp</code> runtime is designed to orchestrate model work locally, not to act like
  an unrestricted automation surface.
</p>

## Built-in protections

- obvious secret redaction before outbound model calls
- malicious prompt blocking for clear abuse patterns
- model name validation so routes do not silently drift
- rate limiting and budget-aware routing pressure
- public release scanning for common leaks and hygiene failures

## What safety looks like in practice

| Surface | What the project tries to make explicit |
| --- | --- |
| Prompt flow | suspicious requests can be blocked instead of blindly routed |
| Provider calls | obvious secrets are redacted before leaving the local layer |
| Release hygiene | public-facing repo scans catch common leaks before publication |
| Skill usage | validation hooks can be attached to higher-risk workflows |
| Routing | model policy stays visible and configurable instead of buried in one client |

## Important limitation

This is not a complete security boundary. If you send sensitive text to a model provider, you still control that disclosure.

## What this does not promise

- it does not make sensitive data magically safe once you choose to send it to a provider
- it does not replace normal application security, infrastructure security, or legal review
- it does not turn a weak workflow into a safe one just by putting MCP in front of it

## Safer operating posture

- keep provider credentials narrow and intentional
- route cheaper or local models first when that matches the task
- use `orchestrator-mcp doctor` before release or public sharing
- treat the local orchestration layer as an inspectable control plane, not as a reason to skip normal review
