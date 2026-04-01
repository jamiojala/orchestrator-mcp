---
name: Threat Model Synthesizer
description: Build a practical threat model for agent workflows, MCP tools, provider routing, and persisted run data.
public: true
category: security
tags: [threat-model, security, agents, privacy]
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - moonshotai/kimi-k2.5
validation:
  - git_delegate_code_review
keywords: [threat model, attack surface, privacy model, agent workflow security]
task_types: [reasoning, architecture, review]
prompt_template: |
  Build a concrete threat model for the provided workflow. Cover assets, trust boundaries, likely abuse paths, and priority mitigations.
---
# Threat Model Synthesizer

Use this skill when generic "secure it" advice is not enough and you need a structured view of what can go wrong.

Expected output:

- assets and trust boundaries
- likely attack paths
- mitigation priorities
- residual risk notes
