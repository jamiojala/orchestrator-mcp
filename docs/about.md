# About

<p class="omcp-lead">
  <code>orchestrator-mcp</code> exists because serious coding workflows are already multi-model, multi-client,
  and operationally messy by default. The project is an attempt to give that mess a clean local control surface.
</p>

## Why this repo exists

Most real developer setups already split work across tools and models:

- Codex for repo-native implementation
- Claude Code for planning and review
- Kimi Code for IDE-first iteration
- Ollama for cheap local or subscription-backed open-model capacity
- Gemini and NVIDIA-backed models for multimodal review and reasoning-heavy sidecars

The problem is not access. The problem is coordination. Without a shared layer, teams end up with
duplicated prompts, inconsistent routing, weak cost discipline, and skills that get trapped inside
whichever client happened to be used first.

## What the project optimizes for

<div class="omcp-grid omcp-grid--two">
  <article class="omcp-panel">
    <p class="omcp-label">Local-first</p>
    <h3>Keep orchestration close to the repo</h3>
    <p>
      Routing, fallback logic, caching, and safety checks should be inspectable and controllable by
      the team using them.
    </p>
  </article>
  <article class="omcp-panel">
    <p class="omcp-label">Portable</p>
    <h3>Keep the skills reusable</h3>
    <p>
      The pack format is designed to travel between ecosystems instead of locking valuable workflow
      knowledge inside one client.
    </p>
  </article>
  <article class="omcp-panel">
    <p class="omcp-label">Visible</p>
    <h3>Keep tradeoffs explicit</h3>
    <p>
      Budget pressure, fallback behavior, and release hygiene should be visible operating choices,
      not hidden side effects.
    </p>
  </article>
  <article class="omcp-panel">
    <p class="omcp-label">Practical</p>
    <h3>Keep adoption friction low</h3>
    <p>
      Standard <code>stdio</code> installs, straightforward config, and exportable packs matter more than demo
      theatrics.
    </p>
  </article>
</div>

## Two products in one repo

### 1. Local-first MCP server

Run one shared orchestration layer across supported clients with routing, safety, semantic caching,
budget-aware fallback, and observability.

### 2. Portable skill marketplace

Browse, inspect, and export standalone skill packs with `SKILL.md`, `skill.yaml`, `marketplace.yaml`,
and `README.md`, even if you do not want to run the runtime itself.

## What it is not

- not a shell-capable agent that blindly executes local commands
- not a single-model ideology project
- not a private prompt library disguised as product
- not a marketplace that only exists as runtime export output

## Who this is for

This repo is a strong fit if you:

- use more than one coding model or agent client
- want a local layer you can inspect and control
- care about budget pressure and fallback behavior
- want reusable skill packs that can travel between ecosystems
- want the public docs to feel like a product surface, not internal notes
