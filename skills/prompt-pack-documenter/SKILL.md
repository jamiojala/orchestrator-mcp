---
name: Prompt Pack Documenter
description: Turn advanced agent workflows into reusable skill and prompt packs with trigger rules, output contracts, and maintainable docs.
public: true
category: docs
tags:
  - prompt-pack
  - skills
  - docs
  - workflow
preferred_models:
  - meta/llama-3.3-70b-instruct
  - "qwen3-coder:480b-cloud"
  - "llama3.1:8b"
validation:
  - verify_prompt_usability
  - verify_text_unchanged
keywords:
  - prompt pack
  - skill docs
  - workflow documentation
  - portable skills
file_globs:
  - **/*.md
  - **/skills/**
  - **/prompts/**
  - **/docs/**
task_types:
  - content
  - review
  - architecture
prompt_template: |
  Take a complex agent workflow and package it into reusable, portable documentation with trigger rules, required context, and clear deliverables.
  Bias toward maintainable structure so another maintainer can update the pack when the workflow or product changes.
  Return the documentation shape, missing context, and examples required for reliable reuse.
---
# Prompt Pack Documenter

Turn advanced agent workflows into reusable skill and prompt packs with trigger rules, output contracts, and maintainable docs.

Source: Advanced first-party pack

## Use this skill when
- The request signals `prompt pack` or a directly related problem.
- The request signals `skill docs` or a directly related problem.
- The request signals `workflow documentation` or a directly related problem.
- The request signals `portable skills` or a directly related problem.
- The likely implementation surface includes `**/*.md`.
- The likely implementation surface includes `**/skills/**`.
- The likely implementation surface includes `**/prompts/**`.
- The likely implementation surface includes `**/docs/**`.

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
- `verify_prompt_usability`
- `verify_text_unchanged`

## Model chain
- `meta/llama-3.3-70b-instruct`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
