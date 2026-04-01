---
name: Design System Drift Audit
description: Detect when implemented UI patterns drift away from the intended design language, tokens, or motion rules.
public: true
category: design
tags: [design-system, audit, frontend, consistency]
preferred_models:
  - gemini-2.5-pro
  - qwen3-coder:480b-cloud
validation:
  - audit_design_compliance
keywords: [design drift, token drift, visual audit, consistency, ui system]
task_types: [visual, review]
prompt_template: |
  Compare the provided UI implementation against the stated design system and identify drift, inconsistency, or quality regressions.
---
# Design System Drift Audit

Use this skill when a codebase slowly starts looking less coherent even though components still technically work.

Expected output:

- drift findings
- missing token usage
- repeated anti-patterns
- a focused cleanup sequence
