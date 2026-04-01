# Cost Routing

`orchestrator-mcp` can bias routing using:

- daily budgets
- weekly budgets
- provider pricing weights
- poor-man's mode

## Poor-man's mode

Enable `budgets.poor_mans_mode: true` to strongly prefer cheap or local providers before cloud fallbacks.

## Why this matters

Most orchestration tools focus on capability. Public adoption usually depends just as much on predictable cost.
