---
name: Tool Contract Normalizer
description: Normalize tool input and output schemas so multi-agent tool calling becomes more reliable, typed, and retry-safe.
public: true
category: api
tags:
  - tooling
  - schema
  - contracts
  - agents
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - "qwen3-coder:480b-cloud"
  - "deepseek-r1:32b"
validation:
  - verify_schema_consistency
  - generate_diff
keywords:
  - tool schema
  - function calling
  - tool contract
  - typed payload
file_globs:
  - **/tools/**
  - **/api/**
  - **/*.json
  - **/*.yaml
task_types:
  - architecture
  - review
  - reasoning
prompt_template: |
  Audit the current tool surface for inconsistent schemas, weak typing, ambiguous field names, and brittle error contracts.
  Return a normalized contract strategy that reduces agent tool-call failures and makes retries or fallbacks predictable.
  Include migration notes for existing tools and consumers.
---
# Tool Contract Normalizer

Normalize tool input and output schemas so multi-agent tool calling becomes more reliable, typed, and retry-safe.

Source: Advanced first-party pack

## Use this skill when
- The request signals `tool schema` or a directly related problem.
- The request signals `function calling` or a directly related problem.
- The request signals `tool contract` or a directly related problem.
- The request signals `typed payload` or a directly related problem.
- The likely implementation surface includes `**/tools/**`.
- The likely implementation surface includes `**/api/**`.
- The likely implementation surface includes `**/*.json`.
- The likely implementation surface includes `**/*.yaml`.

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
- Schema drift or naming ambiguity leaks into downstream tool or API consumers.
- Diffs look clean while backward compatibility quietly breaks at the edge.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Keep contract snapshots or diffs visible during rollout and review.
- Treat consumer migration notes as part of the deliverable, not an optional appendix.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with routing, security, and testing packs once the interface surface is clear.

## Validation hooks
- `verify_schema_consistency`
- `generate_diff`

## Model chain
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
