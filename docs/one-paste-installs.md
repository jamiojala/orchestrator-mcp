# One-Paste Installs

## Codex

```bash
codex mcp add orchestrator -- python -m orchestrator_mcp.cli serve
```

Config alternative:

```toml
[mcp_servers.orchestrator]
command = "python"
args = ["-m", "orchestrator_mcp.cli", "serve"]
```

## Claude Code

```bash
claude mcp add orchestrator -- python -m orchestrator_mcp.cli serve
```

Project config example:

```json
{
  "mcpServers": {
    "orchestrator": {
      "command": "python",
      "args": ["-m", "orchestrator_mcp.cli", "serve"]
    }
  }
}
```

## Kimi Code

Kimi Code documents local MCP setup through its MCP Servers UI.

Use:

- Transport: `stdio`
- Command: `python`
- Args: `-m orchestrator_mcp.cli serve`

The repo also includes a generic stdio example in `examples/kimi-stdio.json`.
