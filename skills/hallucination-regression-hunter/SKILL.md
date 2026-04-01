---
name: Hallucination Regression Hunter
description: Build eval cases that expose fabricated citations, brittle reasoning chains, and ungrounded tool usage before they hit real workflows.
public: true
category: testing
tags:
  - evals
  - grounding
  - regression
  - reliability
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - moonshotai/kimi-k2.5
  - "deepseek-r1:32b"
validation:
  - verify_eval_coverage
  - verify_text_unchanged
keywords:
  - hallucination
  - grounding
  - eval case
  - agent reliability
file_globs:
  - **/evals/**
  - **/tests/**
  - **/*.json
  - **/*.md
task_types:
  - review
  - reasoning
  - architecture
prompt_template: |
  Design high-signal regression cases that catch fabricated claims, ungrounded citations, and tool misuse in agent workflows.
  Bias toward realistic prompts, operator-visible failures, and the smallest repeatable eval loop that can guard future releases.
  Return the eval matrix, rubric, and likely false-positive traps.
---
# Hallucination Regression Hunter

Build eval cases that expose fabricated citations, brittle reasoning chains, and ungrounded tool usage before they hit real workflows.

Source: Advanced first-party pack

## Use this skill when
- The request signals `hallucination` or a directly related problem.
- The request signals `grounding` or a directly related problem.
- The request signals `eval case` or a directly related problem.
- The request signals `agent reliability` or a directly related problem.
- The likely implementation surface includes `**/evals/**`.
- The likely implementation surface includes `**/tests/**`.
- The likely implementation surface includes `**/*.json`.
- The likely implementation surface includes `**/*.md`.

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
- Eval or test coverage expands without improving confidence on real failure classes.
- Generated matrices overfit the happy path and miss cross-surface regressions.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Keep the eval loop cheap enough to run during active iteration, not only before release.
- Anchor the test surface in known failure classes before adding breadth.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with debugging, routing, and orchestration packs to convert fragile insight into regression coverage.

## Validation hooks
- `verify_eval_coverage`
- `verify_text_unchanged`

## Model chain
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
