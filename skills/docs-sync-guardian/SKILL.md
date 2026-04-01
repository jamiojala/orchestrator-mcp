---
name: Docs Sync Guardian
description: Keep README, docs, examples, and CLI behavior aligned so public repos do not drift out of date.
public: true
category: docs
tags:
  - docs
  - readme
  - examples
  - drift
preferred_models:
  - gemini-2.5-flash
  - "qwen3-coder:480b-cloud"
validation:
  - verify_text_unchanged
keywords:
  - docs sync
  - readme drift
  - docs rot
  - example drift
file_globs:
task_types:
  - review
  - content
prompt_template: Review implementation, examples, and documentation together. Find drift, missing steps, and misleading instructions.
---
# Docs Sync Guardian

Keep README, docs, examples, and CLI behavior aligned so public repos do not drift out of date.

Source: Advanced first-party pack

## Use this skill when
- The request signals `docs sync` or a directly related problem.
- The request signals `readme drift` or a directly related problem.
- The request signals `docs rot` or a directly related problem.
- The request signals `example drift` or a directly related problem.

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
- Portable pack docs drift from the real runtime surface after the next product change.
- The pack becomes reusable in theory but underspecified in actual agent handoffs.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Cross-link the pack to the runtime or code surface it documents so drift is easier to spot.
- Version the examples or assumptions that are likely to change quickly.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration, api, and release packs when a workflow needs to travel cleanly.

## Validation hooks
- `verify_text_unchanged`

## Model chain
- `gemini-2.5-flash`
- `qwen3-coder:480b-cloud`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
