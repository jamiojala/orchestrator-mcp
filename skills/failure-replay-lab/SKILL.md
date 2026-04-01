---
name: Failure Replay Lab
description: Investigate a failed delegation by replaying context, isolating likely root causes, and proposing the smallest reliable recovery path.
public: true
category: debugging
tags: [debugging, replay, incident, recovery]
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - gemini-2.5-pro
validation:
  - generate_diff
keywords: [failed delegation, replay, retry, incident, recover]
task_types: [reasoning, review]
prompt_template: |
  Given a failed run payload, explain the likely failure cause, what to retry, and how to harden the workflow against repeat failures.
---
# Failure Replay Lab

Use this skill when an agent run failed and you want a disciplined retry plan instead of a blind re-run.

Expected output:

- probable root cause
- minimum retry payload
- hardening recommendations
- what not to retry unchanged
