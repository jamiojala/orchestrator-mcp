---
name: Cost Router Tuner
description: Tune provider routing policy for quality, cost ceilings, and fallback behavior across multiple model subscriptions.
public: true
category: routing
tags:
  - budget
  - routing
  - cost
  - providers
preferred_models:
  - moonshotai/kimi-k2.5
  - gemini-2.5-flash
validation:
  - verify_text_unchanged
keywords:
  - budget
  - router
  - routing
  - cost
  - fallback
  - poor mans mode
file_globs:
task_types:
  - architecture
  - reasoning
prompt_template: |
  Optimize model routing for cost efficiency without sacrificing the highest-value specialist paths.
  Recommend policy changes, not just model swaps.
---
# Cost Router Tuner

Tune provider routing policy for quality, cost ceilings, and fallback behavior across multiple model subscriptions.

Source: Advanced first-party pack

## Use this skill when
- The request signals `budget` or a directly related problem.
- The request signals `router` or a directly related problem.
- The request signals `routing` or a directly related problem.
- The request signals `cost` or a directly related problem.
- The request signals `fallback` or a directly related problem.

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
- Faster or cheaper routes silently degrade answer quality without an escalation rule.
- Routing logic optimizes averages while breaking the tail latencies users actually feel.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Track both latency and answer quality before changing default lanes permanently.
- Make escalation to slower or more expensive models rule-based instead of ad hoc.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration, data, and testing packs when route quality must be measured, not guessed.

## Validation hooks
- `verify_text_unchanged`

## Model chain
- `moonshotai/kimi-k2.5`
- `gemini-2.5-flash`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
