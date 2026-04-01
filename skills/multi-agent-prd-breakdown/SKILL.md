---
name: Multi-Agent PRD Breakdown
description: Turn a product or engineering spec into bounded sub-tasks, ownership lanes, and integration checkpoints for multiple agents.
public: true
category: orchestration
tags:
  - planning
  - delegation
  - orchestration
  - handoff
preferred_models:
  - moonshotai/kimi-k2.5
  - "qwen3-coder:480b-cloud"
validation:
  - verify_text_unchanged
keywords:
  - prd
  - spec
  - breakdown
  - orchestrate
  - delegate
  - ownership
file_globs:
task_types:
  - architecture
  - reasoning
prompt_template: |
  Break the request into bounded implementation slices with clear ownership, dependencies, and integration checkpoints.
  Optimize for parallel work without overlapping write scopes.
---
# Multi-Agent PRD Breakdown

Turn a product or engineering spec into bounded sub-tasks, ownership lanes, and integration checkpoints for multiple agents.

Source: Advanced first-party pack

## Use this skill when
- The request signals `prd` or a directly related problem.
- The request signals `spec` or a directly related problem.
- The request signals `breakdown` or a directly related problem.
- The request signals `orchestrate` or a directly related problem.
- The request signals `delegate` or a directly related problem.

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
- Context or agent boundaries look elegant but break under long-running work or human interruption.
- Delegation lanes overlap, creating duplicated work or silent ownership gaps.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Name the checkpoint where a human can safely inspect, redirect, or pause the workflow.
- Keep context summaries and delegation boundaries stable enough for later handoffs.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Often acts as the lead pack, then hands off to routing, security, docs, or testing packs with clear boundaries.

## Validation hooks
- `verify_text_unchanged`

## Model chain
- `moonshotai/kimi-k2.5`
- `qwen3-coder:480b-cloud`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
