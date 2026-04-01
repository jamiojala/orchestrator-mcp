---
name: Multi-Agent PRD Breakdown
description: Turn a product or engineering spec into bounded sub-tasks, ownership lanes, and integration checkpoints for multiple agents.
public: true
category: orchestration
tags: [planning, delegation, orchestration, handoff]
preferred_models:
  - moonshotai/kimi-k2.5
  - qwen3-coder:480b-cloud
validation:
  - verify_text_unchanged
keywords: [prd, spec, breakdown, orchestrate, delegate, ownership]
task_types: [architecture, reasoning]
prompt_template: |
  Break the request into bounded implementation slices with clear ownership, dependencies, and integration checkpoints.
  Optimize for parallel work without overlapping write scopes.
---
# Multi-Agent PRD Breakdown

Use this skill when a task is too large or ambiguous for one uninterrupted coding pass.

Expected output:

- atomic sub-tasks
- ownership by file or module
- dependency edges
- validation gates
- integration order
