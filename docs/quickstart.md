# Quickstart

<p class="omcp-lead">
  This is the fastest path to a working local runtime. Install the package, copy the config,
  validate the setup, and then wire the server into whichever MCP-capable client you already use.
</p>

## 1. Install the package

```bash
pip install "orchestrator-mcp[dashboard]"
```

::: tip
If your system exposes `python3` instead of `python`, keep that same executable choice in the install
examples and client commands.
:::

## 2. Copy the local config

```bash
cp .env.example .env
cp orchestrator-mcp.yaml.example orchestrator-mcp.yaml
```

Fill in only the provider credentials you actually plan to use. A lean config is easier to reason about.

## 3. Validate the environment

```bash
orchestrator-mcp doctor
```

This catches missing credentials, basic release-hygiene issues, and obvious local setup problems before
you wire the runtime into a client.

## 4. Start the MCP server

```bash
orchestrator-mcp serve
```

At that point, the runtime is ready for Codex, Claude Code, Kimi Code, or any other `stdio`-capable MCP client.

## 5. Open the optional dashboard

```bash
orchestrator-mcp dashboard
```

Use the dashboard when you want visibility into recent runs, cache behavior, failures, and estimated spend.

## Recommended next steps

- go to [One-Paste Installs](./one-paste-installs) if you want the exact client wiring
- go to [Marketplace](./marketplace) if you only want the portable skill layer
- go to [Safety](./safety) if you want the operating model and guardrails first
