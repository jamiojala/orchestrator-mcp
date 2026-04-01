---
name: Public Repo Sanitizer
description: Audit a repo for secrets, personal paths, client-specific references, and OSS-readiness gaps before publishing.
public: true
category: release
tags: [security, release, open-source, hygiene]
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - gemini-2.5-pro
validation:
  - git_delegate_code_review
keywords: [open source, public repo, sanitize, release, publish, secret scan]
task_types: [review, architecture]
prompt_template: |
  Review the provided repo snapshot for anything that should not ship publicly.
  Flag secrets, private paths, client references, brittle docs, and configuration hazards.
---
# Public Repo Sanitizer

Use this skill before publishing a private internal tool as open source.

Focus on:

- inline secrets and credentials
- local absolute paths
- private client and project names
- docs that assume one user's environment
- examples that leak personal workflows

Expected output:

- findings ordered by severity
- exact files or surfaces to sanitize
- release-readiness checklist
