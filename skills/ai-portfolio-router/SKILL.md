---
name: AI Portfolio Router
description: Allocate work across local, cloud, and premium models so teams maximize capability coverage per dollar and per latency budget.
public: true
category: routing
tags:
  - portfolio
  - routing
  - roi
  - models
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - meta/llama-3.3-70b-instruct
  - "deepseek-r1:32b"
validation:
  - verify_roi_assumptions
  - verify_text_unchanged
keywords:
  - model portfolio
  - ai roi
  - routing strategy
  - budget pressure
file_globs:
  - **/*.md
  - **/budgets/**
  - **/routing/**
  - **/config/**
task_types:
  - reasoning
  - architecture
  - content
prompt_template: |
  Map the current workload mix across local, cloud, and premium models, then recommend a portfolio that improves capability coverage without uncontrolled spend.
  Separate high-stakes, latency-sensitive, and bulk-work lanes clearly.
  Return tradeoffs, recommended defaults, and the signals that should trigger escalation to more expensive models.
---
# AI Portfolio Router

Allocate work across local, cloud, and premium models so teams maximize capability coverage per dollar and per latency budget.

Source: Advanced first-party pack

## Use this skill when
- The request signals `model portfolio` or a directly related problem.
- The request signals `ai roi` or a directly related problem.
- The request signals `routing strategy` or a directly related problem.
- The request signals `budget pressure` or a directly related problem.
- The likely implementation surface includes `**/*.md`.
- The likely implementation surface includes `**/budgets/**`.
- The likely implementation surface includes `**/routing/**`.
- The likely implementation surface includes `**/config/**`.

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
- `verify_roi_assumptions`
- `verify_text_unchanged`

## Model chain
- `deepseek-ai/deepseek-v3.2`
- `meta/llama-3.3-70b-instruct`
- `deepseek-r1:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
