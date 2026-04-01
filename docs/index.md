---
layout: home
title: SkillForge
titleTemplate: false
hero:
  name: SkillForge
  text: Run one local orchestration layer. Export the skills anywhere.
  tagline: Local-first MCP orchestration and portable skill marketplace for Codex, Claude Code, Kimi Code, Ollama, Gemini, and NVIDIA-backed models.
  image:
    src: /logo-mark.svg
    alt: SkillForge
  actions:
    - theme: brand
      text: Get started
      link: /quickstart
    - theme: alt
      text: One-paste installs
      link: /one-paste-installs
    - theme: alt
      text: View on GitHub
      link: https://github.com/jamiojala/skillforge
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

  <div class="omcp-kpi-strip" aria-label="Library metrics">
    <div class="omcp-kpi">
      <strong>130</strong>
      <span>pack folders on disk</span>
    </div>
    <div class="omcp-kpi">
      <strong>110</strong>
      <span>canonical marketplace skills</span>
    </div>
    <div class="omcp-kpi">
      <strong>20</strong>
      <span>advanced first-party packs</span>
    </div>
    <div class="omcp-kpi">
      <strong>11</strong>
      <span>core product domains</span>
    </div>
  </div>
</div>

<section class="omcp-home-shell omcp-section">
  <p class="omcp-label">Why this exists</p>
  <h2>Most multi-model workflows are still held together with prompt glue.</h2>
  <p class="omcp-lead">
    Without a shared layer, teams repeat architecture context, lose routing policy inside individual
    clients, and quietly pay for fragile fallbacks they can’t inspect. The problem is not model access.
    The problem is orchestration discipline.
  </p>
  <div class="omcp-grid omcp-grid--three">
    <article class="omcp-panel">
      <p class="omcp-label">Context drift</p>
      <h3>The same repo rules get re-explained again and again.</h3>
      <p>
        Architecture choices, cost policy, and safety expectations fade between tools and sessions.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Hidden tradeoffs</p>
      <h3>Fallbacks and model spend become invisible.</h3>
      <p>
        One client routes one way, another client routes another way, and nobody can see the system-level behavior.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Locked expertise</p>
      <h3>Good workflows get trapped inside one assistant.</h3>
      <p>
        Valuable skills stay glued to one vendor or editor instead of becoming reusable operational assets.
      </p>
    </article>
  </div>
</section>

<section class="omcp-home-shell omcp-section">
  <p class="omcp-label">What this is</p>
  <h2>One repo, two clean adoption paths.</h2>
  <p class="omcp-lead">
    SkillForge turns a messy multi-model setup into one local control surface for routing,
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
  <div class="omcp-grid omcp-grid--three">
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
        <li>130 on-disk packs checked into the repository</li>
        <li>110-skill global library plus 20 advanced first-party packs</li>
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
  <p class="omcp-label">Pack anatomy</p>
  <h2>Every pack says how it should activate, who should handle it, how it should think, and how it should be checked.</h2>
  <p class="omcp-lead">
    The strongest idea worth carrying over from the Kimi library is not the hype layer. It is the
    explicit pack contract. In SkillForge, the useful parts are visible: trigger signals,
    model chain, validation hooks, and portable files you can inspect directly.
  </p>
  <div class="omcp-grid omcp-grid--two">
    <article class="omcp-panel">
      <p class="omcp-label">Activation</p>
      <h3>Trigger signals are explicit</h3>
      <p>
        Packs expose keywords, file patterns, and task-type hints so you can see why a skill belongs
        in a workflow instead of treating it like hidden prompt magic.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Delegation</p>
      <h3>Preferred model chains are part of the pack</h3>
      <p>
        Skills declare preferred model lanes and fallbacks, which makes routing policy inspectable and easier to tune.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Validation</p>
      <h3>Checks live next to the workflow</h3>
      <p>
        Packs declare validation hooks so the quality bar is attached to the work itself rather than remembered later.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Persona</p>
      <h3>Specialist posture is explicit</h3>
      <p>
        Generated marketplace packs now expose role, voice, reasoning pattern, and response shape so
        they behave like specialist workflows instead of generic prompt wrappers.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Portability</p>
      <h3>Useful files ship with the pack</h3>
      <p>
        <code>README.md</code>, <code>SKILL.md</code>, <code>skill.yaml</code>, and <code>marketplace.yaml</code>
        give you human review context, portable instructions, structured registry loading, and richer metadata.
      </p>
    </article>
  </div>
</section>

<section class="omcp-home-shell omcp-section">
  <p class="omcp-label">Persona architecture</p>
  <h2>These packs are designed to think like specialists, not autocomplete like generalists.</h2>
  <p class="omcp-lead">
    The marketplace layer now carries explicit persona architecture on generated global-library packs:
    role, voice, reasoning steps, verification habits, and response shape. That makes the packs more
    legible, more portable, and much easier to audit when they leave the runtime.
  </p>
  <div class="omcp-grid omcp-grid--three">
    <article class="omcp-panel">
      <p class="omcp-label">Role</p>
      <h3>Expert posture is inspectable</h3>
      <p>
        A pack can behave like a systems architect, UI craftsperson, DPO, or grant strategist instead
        of flattening every request into the same generic assistant voice.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Method</p>
      <h3>Reasoning patterns are visible</h3>
      <p>
        Verification checklists, analysis approach, and decision criteria sit next to the skill
        instead of living in invisible system-prompt glue.
      </p>
    </article>
    <article class="omcp-panel">
      <p class="omcp-label">Output</p>
      <h3>Response shape is predictable</h3>
      <p>
        Packs can ask for threat models, design intent, proposal strategy, or eval baselines in a
        consistent format that another operator can review quickly.
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
        <li>130 total pack folders in <code>skills/</code></li>
        <li>110 canonical global-library skills across 11 domains</li>
        <li>20 advanced first-party packs for orchestration, routing, safety, and AI optimization</li>
      </ul>
    </div>
    <div>
      <p class="omcp-lead">
        Start with the <a href="/skillforge/marketplace.html">marketplace guide</a> for the catalog or jump into the
        <a href="/skillforge/skills.html">skills library</a> if you want the categorized on-site index.
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
      <a class="omcp-button omcp-button--brand" href="/skillforge/quickstart.html">Open Quickstart</a>
      <a class="omcp-button" href="/skillforge/one-paste-installs.html">See one-paste installs</a>
      <a class="omcp-button" href="/skillforge/marketplace.html">Browse the marketplace</a>
    </div>
  </section>
</div>
