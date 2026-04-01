---
name: MCP Server Hardening
description: Review an MCP server for prompt-exfiltration, shell abuse, overbroad tool scope, and unsafe logging.
public: true
category: security
tags: [mcp, security, hardening, privacy]
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - moonshotai/kimi-k2.5
validation:
  - git_delegate_code_review
keywords: [mcp hardening, prompt exfiltration, tool scope, unsafe logging, server safety]
task_types: [review, reasoning, architecture]
prompt_template: |
  Audit the MCP server design for overbroad capabilities, data exposure, and unsafe execution paths.
  Prefer specific mitigations over vague security advice.
---
# MCP Server Hardening

Use this skill when building or reviewing any MCP server that touches external APIs, credentials, or local state.

Review dimensions:

- tool capability scope
- authentication and secret handling
- prompt and environment leakage risks
- logging and persistence hygiene
- abuse resistance and rate limiting

Expected output:

- concrete risk list
- mitigation plan
- recommended guardrails by priority
