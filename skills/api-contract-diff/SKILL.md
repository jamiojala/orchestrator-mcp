---
name: API Contract Diff
description: Compare two API or schema revisions and surface behavioral breakage, migration steps, and compatibility risk.
public: true
category: api
tags: [api, schema, diff, compatibility]
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - qwen3-coder:480b-cloud
validation:
  - generate_diff
keywords: [api diff, schema diff, breaking change, compatibility]
task_types: [review, reasoning]
prompt_template: |
  Compare the old and new contracts, identify behavior changes, and classify migration risk for clients and tests.
---
# API Contract Diff

Use this skill when changing API payloads, JSON schemas, SDK types, or tool input contracts.

Expected output:

- breaking changes
- non-breaking additions
- migration notes
- test updates required
