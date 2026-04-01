---
name: Agent Handoff Designer
description: Shape approvals, status surfaces, and human handoff moments so advanced agent workflows stay legible and trustworthy.
public: true
category: design
tags:
  - handoff
  - approvals
  - agent ux
  - trust
preferred_models:
  - moonshotai/kimi-k2.5
  - meta/llama-3.3-70b-instruct
  - "qwen2.5-coder:32b"
validation:
  - verify_operator_clarity
  - audit_design_compliance
keywords:
  - agent handoff
  - approval ux
  - operator trust
  - status surface
file_globs:
  - **/*.tsx
  - **/agents/**
  - **/*.md
  - **/components/**
task_types:
  - visual
  - architecture
  - review
prompt_template: |
  Design the human-facing checkpoints around agent work so approvals, uncertainty, and next actions are legible under pressure.
  Prioritize trust-building surfaces such as progress, waiting states, diffs, risk summaries, and completion criteria.
  Return concrete UI states, copy, and interaction rules rather than vague UX commentary.
---
# Agent Handoff Designer

Shape approvals, status surfaces, and human handoff moments so advanced agent workflows stay legible and trustworthy.

Source: Advanced first-party pack

## Use this skill when
- The request signals `agent handoff` or a directly related problem.
- The request signals `approval ux` or a directly related problem.
- The request signals `operator trust` or a directly related problem.
- The request signals `status surface` or a directly related problem.
- The likely implementation surface includes `**/*.tsx`.
- The likely implementation surface includes `**/agents/**`.
- The likely implementation surface includes `**/*.md`.
- The likely implementation surface includes `**/components/**`.

## Gather this context first
- Relevant files, modules, or specs that define the current surface.
- Constraints, rollout limits, or non-goals that change the recommendation.
- What success looks like for the user, operator, or release owner.

## Recommended workflow
1. Confirm the trigger fit and boundaries before expanding scope.
2. Identify the highest-risk files, interfaces, or decision points first.
3. Produce a bounded plan or implementation slice with exact targets.
4. Run the listed validation hooks or explain what blocks them.
5. Return rollout, fallback, and open-question notes for the next agent or maintainer.

## Output contract
- Capability summary and why this skill fits the request.
- Concrete file, module, or artifact targets.
- Validation plan and residual risk notes.

## Failure modes to watch
- The pack matches the theme of the request but not the highest-leverage failure domain.
- Validation is mentioned without enough proof for another operator or agent to repeat it.
- The output becomes generic advice instead of a bounded next-step plan.
- Operator-facing surfaces become more polished but less legible under pressure.
- High-variance visual ideas land without an evaluation path for trust or clarity.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Verify operator-critical states such as loading, waiting, approval, and failure before polish.
- Keep accessibility and motion budgets explicit in the review surface.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration and docs packs when operator trust depends on the UI shell.

## Validation hooks
- `verify_operator_clarity`
- `audit_design_compliance`

## Model chain
- `moonshotai/kimi-k2.5`
- `meta/llama-3.3-70b-instruct`
- `qwen2.5-coder:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
