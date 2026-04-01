---
layout: home
title: orchestrator-mcp
titleTemplate: false
hero:
  name: orchestrator-mcp
  text: Run one local orchestration layer. Export the skills anywhere.
  tagline: Local-first MCP server and portable skill marketplace for Codex, Claude Code, Kimi Code, Ollama, Gemini, and NVIDIA-backed models.
  image:
    src: /logo-mark.svg
    alt: orchestrator-mcp
  actions:
    - theme: brand
      text: Get started
      link: /quickstart
    - theme: alt
      text: One-paste installs
      link: /one-paste-installs
    - theme: alt
      text: View on GitHub
      link: https://github.com/jamiojala/orchestrator-mcp
---

<div class="omcp-home-shell">
  <div class="omcp-client-band" aria-label="Supported clients and providers">
    <span>Codex</span>
    <span>Claude Code</span>
    <span>Kimi Code</span>
    <span>Ollama</span>
    <span>Gemini</span>
    <span>NVIDIA-backed models</span>
  </div>
</div>

<section class="omcp-home-shell omcp-section">
  <p class="omcp-label">What this is</p>
  <h2>One repo, two clean adoption paths.</h2>
  <p class="omcp-lead">
    <code>orchestrator-mcp</code> turns a messy multi-model setup into one local control surface for routing,
    safety, caching, fallback behavior, and portable skill reuse. It is built for developers who
    already move between clients and models instead of pretending one silo wins every task.
  </p>
  <div class="omcp-grid omcp-grid--three">
    <article class="omcp-panel">
      <p class="omcp-label">Shared runtime</p>
      <h3>One local orchestration layer</h3>
      <p>
        Run one MCP server for serious coding workflows instead of rebuilding prompt glue,
        routing policy, and fallback behavior inside every client.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Portable packs</p>
      <h3>One skill library that travels</h3>
      <p>
        Use the repo as a standalone skill marketplace when you only want the packs. Export them,
        copy them, or keep the runtime out of the picture entirely.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Operational sanity</p>
      <h3>One place to keep the rules</h3>
      <p>
        Budget pressure, secret redaction, release hygiene, semantic caching, and validation stay
        visible and reusable instead of getting lost inside one editor or provider.
      </p>
    </article>
  </div>
</section>

<section class="omcp-home-shell omcp-section">
  <p class="omcp-label">Use it two ways</p>
  <h2>Adopt the layer you actually need.</h2>
  <p class="omcp-lead">
    Run the full local runtime when you want shared orchestration. Export only the library when you
    want portable skills with no client lock-in.
  </p>
  <div class="omcp-grid omcp-grid--two">
    <article class="omcp-panel">
      <p class="omcp-label">Path 01</p>
      <h3>Run the MCP server</h3>
      <p>Use one shared local layer for clients that can talk MCP.</p>
      <ul class="omcp-list">
        <li>Shared routing, fallback logic, and provider policy</li>
        <li>Budget-aware execution and semantic caching</li>
        <li>Safety checks and observability in one place</li>
      </ul>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Path 02</p>
      <h3>Use only the skill marketplace</h3>
      <p>Take the packs without taking the runtime.</p>
      <ul class="omcp-list">
        <li>120 on-disk packs checked into the repository</li>
        <li>100-skill global library plus 20 advanced first-party packs</li>
        <li>
          Portable <code>SKILL.md</code>, <code>skill.yaml</code>, <code>marketplace.yaml</code>,
          and <code>README.md</code> surfaces
        </li>
      </ul>
    </article>
  </div>
</section>

### Runtime path

```bash
pip install "orchestrator-mcp[dashboard]"
cp .env.example .env
cp orchestrator-mcp.yaml.example orchestrator-mcp.yaml
orchestrator-mcp doctor
orchestrator-mcp serve
```

### Marketplace path

```bash
orchestrator-mcp skills list
orchestrator-mcp skills show liquid-glass-enforcer
orchestrator-mcp skills export-category --category frontend --to ./exported-skills
```

<section class="omcp-home-shell omcp-section">
  <p class="omcp-label">Install in minutes</p>
  <h2>Wire it into the clients you already use.</h2>
  <p class="omcp-lead">
    Plug the local runtime into Codex, Claude Code, or Kimi Code with a standard <code>stdio</code>
    MCP setup. If your machine exposes <code>python3</code> instead of <code>python</code>, swap the executable accordingly.
  </p>
</section>

::: code-group
```bash [Codex]
codex mcp add orchestrator -- python -m orchestrator_mcp.cli serve
```

```bash [Claude Code]
claude mcp add orchestrator -- python -m orchestrator_mcp.cli serve
```

```bash [Kimi Code]
# transport: stdio
# command: python
# args: -m orchestrator_mcp.cli serve
```
:::

```bash
pip install "orchestrator-mcp[dashboard]"
orchestrator-mcp doctor
orchestrator-mcp serve
```

<section class="omcp-home-shell omcp-section">
  <p class="omcp-label">Why teams keep it in the loop</p>
  <h2>Trust comes from explicit tradeoffs.</h2>
  <p class="omcp-lead">
    This project earns trust by making the hard parts of multi-model work explicit instead of hiding
    them behind a shiny client wrapper.
  </p>
  <div class="omcp-grid omcp-grid--two">
    <article class="omcp-panel">
      <p class="omcp-label">Routing</p>
      <h3>Cost-aware by default</h3>
      <p>
        Shape fallback lanes, poor-man's mode, and local-first defaults instead of paying premium
        rates for every request by accident.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Safety</p>
      <h3>Guardrails live in the orchestration layer</h3>
      <p>
        Secret redaction, prompt blocking, model validation, and release hygiene stay attached to
        the workflow instead of depending on editor memory.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Reuse</p>
      <h3>Skills are first-class assets</h3>
      <p>
        The library is materialized on disk, categorized for the web, and portable enough to move
        between agent ecosystems without rebuilding everything from scratch.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Visibility</p>
      <h3>Fallbacks and failures stay visible</h3>
      <p>
        Recent runs, cache hits, spend, and failure paths become inspectable instead of disappearing
        into ad hoc model calls.
      </p>
    </article>
  </div>
</section>

<section class="omcp-home-shell omcp-section">
  <p class="omcp-label">Portable marketplace</p>
  <div class="omcp-slab">
    <div>
      <h3>The runtime is optional. The packs are not trapped.</h3>
      <p>
        The marketplace ships as real repository folders, not a hidden export format. Browse the web
        catalog, inspect individual packs, or copy the ones you want into your own setup.
      </p>
      <ul class="omcp-metrics">
        <li>120 total pack folders in <code>skills/</code></li>
        <li>100 canonical global-library skills across 10 domains</li>
        <li>20 advanced first-party packs for orchestration, routing, safety, and AI optimization</li>
      </ul>
    </div>
    <div>
      <p class="omcp-lead">
        Start with the <a href="/orchestrator-mcp/marketplace">marketplace guide</a> for the catalog or jump into the
        <a href="/orchestrator-mcp/skills">skills library</a> if you want the categorized on-site index.
      </p>
    </div>
  </div>
</section>

```bash
orchestrator-mcp skills list
orchestrator-mcp skills show micro-frontend-orchestrator
orchestrator-mcp skills export micro-frontend-orchestrator --to ./exported-skills
```

<div class="omcp-home-shell">
  <section class="omcp-final-cta">
    <p class="omcp-label">Start here</p>
    <h2>Bring order to the model sprawl.</h2>
    <p>
      Run the local orchestration layer when you want shared routing and safety. Take the packs when
      you only want portable skills. Either way, the surface is built for real adoption, not demo-only docs.
    </p>
    <div class="omcp-action-row">
      <a class="omcp-button omcp-button--brand" href="/orchestrator-mcp/quickstart">Open Quickstart</a>
      <a class="omcp-button" href="/orchestrator-mcp/one-paste-installs">See one-paste installs</a>
      <a class="omcp-button" href="/orchestrator-mcp/marketplace">Browse the marketplace</a>
    </div>
  </section>
</div>
