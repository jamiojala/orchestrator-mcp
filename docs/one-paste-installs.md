# One-Paste Installs

<p class="omcp-lead">
  These are the cleanest client wiring patterns for <code>orchestrator-mcp</code>. Use the same Python
  executable that installed the package. If your machine exposes <code>python3</code> instead of <code>python</code>,
  swap that value in every snippet below.
</p>

## Codex

```bash
codex mcp add orchestrator -- python -m orchestrator_mcp.cli serve
```

Config file alternative:

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

Kimi Code documents local MCP setup through its MCP Servers UI. Use:

- Transport: `stdio`
- Command: `python`
- Args: `-m orchestrator_mcp.cli serve`

The repo also includes a generic stdio example in `examples/kimi-stdio.json`.

## Generic MCP client

Any client that can launch an `stdio` MCP server can use the same pattern:

```bash
python -m orchestrator_mcp.cli serve
```

## After wiring it in

Once the client can start the runtime, validate the broader setup with:

```bash
orchestrator-mcp doctor
```

Then browse [Marketplace](./marketplace) if you want the portable packs, or head back to [Quickstart](./quickstart)
if you still need the runtime path.
