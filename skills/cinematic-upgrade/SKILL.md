---
name: Cinematic Upgrade
description: Plan premium motion and UI polish upgrades without mutating code prematurely.
public: true
category: design
tags: [motion, polish, ui, review]
preferred_models:
  - moonshotai/kimi-k2.5
  - gemini-2.5-pro
  - qwen3-coder:480b-cloud
validation:
  - audit_design_compliance
  - verify_text_unchanged
keywords: [cinematic, motion, premium, polish, upgrade]
task_types: [architecture, review, visual]
prompt_template: |
  Produce a non-mutating cinematic upgrade plan grounded in the provided repo context.
  Keep suggestions modular, accessible, GPU-friendly, and realistic to implement.
---
# Cinematic Upgrade

Use this skill when a project needs premium motion, stronger hierarchy, or a more intentional interaction layer.

Workflow:

1. Audit the existing UI and interaction surface
2. Separate structural changes from motion-only upgrades
3. Prefer transform and opacity over layout-driven animation
4. Preserve meaning, accessibility, and performance budgets

Expected output:

- a prioritized upgrade plan
- component-level recommendations
- motion constraints
- verification steps
