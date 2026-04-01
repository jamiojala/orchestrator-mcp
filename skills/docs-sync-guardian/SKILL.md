---
name: Docs Sync Guardian
description: Keep README, docs, examples, and CLI behavior aligned so public repos do not drift out of date.
public: true
category: docs
tags: [docs, readme, examples, drift]
preferred_models:
  - gemini-2.5-flash
  - qwen3-coder:480b-cloud
validation:
  - verify_text_unchanged
keywords: [docs sync, readme drift, docs rot, example drift]
task_types: [review, content]
prompt_template: |
  Review implementation, examples, and documentation together. Find drift, missing steps, and misleading instructions.
---
# Docs Sync Guardian

Use this skill before releases, after CLI changes, or whenever examples start feeling suspiciously old.

Expected output:

- docs drift findings
- stale commands
- missing setup notes
- exact update targets
