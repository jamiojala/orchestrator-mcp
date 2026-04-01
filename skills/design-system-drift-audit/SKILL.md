---
name: Design System Drift Audit
description: Detect when implemented UI patterns drift away from the intended design language, tokens, or motion rules.
public: true
category: design
tags:
  - design-system
  - audit
  - frontend
  - consistency
preferred_models:
  - gemini-2.5-pro
  - "qwen3-coder:480b-cloud"
validation:
  - audit_design_compliance
keywords:
  - design drift
  - token drift
  - visual audit
  - consistency
  - ui system
file_globs:
task_types:
  - visual
  - review
prompt_template: Compare the provided UI implementation against the stated design system and identify drift, inconsistency, or quality regressions.
---
# Design System Drift Audit

Detect when implemented UI patterns drift away from the intended design language, tokens, or motion rules.

Source: Advanced first-party pack

## Use this skill when
- The request signals `design drift` or a directly related problem.
- The request signals `token drift` or a directly related problem.
- The request signals `visual audit` or a directly related problem.
- The request signals `consistency` or a directly related problem.
- The request signals `ui system` or a directly related problem.

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
- `audit_design_compliance`

## Model chain
- `gemini-2.5-pro`
- `qwen3-coder:480b-cloud`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
