---
name: Retrieval Grounding Optimizer
description: Improve chunking, metadata, and ranking design so agent answers stay grounded under larger repositories and longer tasks.
public: true
category: data
tags:
  - retrieval
  - chunking
  - grounding
  - ranking
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - "qwen3-coder:480b-cloud"
  - "deepseek-r1:32b"
validation:
  - verify_grounding_precision
  - verify_text_unchanged
keywords:
  - retrieval
  - chunking
  - grounding
  - ranking
file_globs:
  - **/docs/**
  - **/*.md
  - **/embeddings/**
  - **/retrieval/**
task_types:
  - architecture
  - review
  - reasoning
prompt_template: |
  Optimize retrieval quality by redesigning chunk size, metadata strategy, and ranking signals for the actual task mix.
  Explain how the retrieval stack should behave under broad repo scans, narrow code lookups, and long-horizon planning work.
  Return measurement hooks that show whether grounding improved rather than simply changing the index.
---
# Retrieval Grounding Optimizer

Improve chunking, metadata, and ranking design so agent answers stay grounded under larger repositories and longer tasks.

Source: Advanced first-party pack

## Use this skill when
- The request signals `retrieval` or a directly related problem.
- The request signals `chunking` or a directly related problem.
- The request signals `grounding` or a directly related problem.
- The request signals `ranking` or a directly related problem.
- The likely implementation surface includes `**/docs/**`.
- The likely implementation surface includes `**/*.md`.
- The likely implementation surface includes `**/embeddings/**`.
- The likely implementation surface includes `**/retrieval/**`.

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
- Grounding improves on one workflow while precision regresses on long-tail lookups.
- Metadata or chunking changes make debugging harder even if recall appears higher.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Measure both retrieval quality and debuggability after changes to chunking or ranking.
- Keep source-truth links close to any generated summary or recommendation.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration and testing packs when grounding quality needs measurable proof.

## Validation hooks
- `verify_grounding_precision`
- `verify_text_unchanged`

## Model chain
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
