---
name: Test Matrix Generator
description: Derive a high-signal regression matrix from changed code, user risk, and likely failure surfaces.
public: true
category: testing
tags: [testing, regression, qa, coverage]
preferred_models:
  - qwen3-coder:480b-cloud
  - deepseek-ai/deepseek-v3.2
validation:
  - git_delegate_code_review
keywords: [test matrix, regression plan, qa matrix, coverage gaps]
task_types: [review, reasoning]
prompt_template: |
  Build a compact but high-signal regression matrix from the provided code or diff. Focus on real failure risk instead of exhaustive enumeration.
---
# Test Matrix Generator

Use this skill when a change is too broad for intuition but too small for a huge QA spreadsheet.

Expected output:

- must-test paths
- edge cases
- negative cases
- deferred or lower-risk cases
