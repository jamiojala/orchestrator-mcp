---
name: Failure Replay Lab
description: Investigate a failed delegation by replaying context, isolating likely root causes, and proposing the smallest reliable recovery path.
public: true
category: debugging
tags:
  - debugging
  - replay
  - incident
  - recovery
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - gemini-2.5-pro
validation:
  - generate_diff
keywords:
  - failed delegation
  - replay
  - retry
  - incident
  - recover
file_globs:
task_types:
  - reasoning
  - review
prompt_template: Given a failed run payload, explain the likely failure cause, what to retry, and how to harden the workflow against repeat failures.
---
# Failure Replay Lab

Investigate a failed delegation by replaying context, isolating likely root causes, and proposing the smallest reliable recovery path.

Source: Advanced first-party pack

## Use this skill when
- The request signals `failed delegation` or a directly related problem.
- The request signals `replay` or a directly related problem.
- The request signals `retry` or a directly related problem.
- The request signals `incident` or a directly related problem.
- The request signals `recover` or a directly related problem.

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
- The reproduction path stays too vague to catch the failure again later.
- A one-off fix lands without preserving the evidence trail for future regressions.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Preserve the minimal repro and failure fingerprint so future agents can restart quickly.
- Prefer instrumentation that narrows the next diagnostic step instead of broad logging dumps.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with testing and release packs when a repro should become a durable guardrail.

## Validation hooks
- `generate_diff`

## Model chain
- `deepseek-ai/deepseek-v3.2`
- `gemini-2.5-pro`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
