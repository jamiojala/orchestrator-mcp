---
name: Server Timing Analyzer
description: Expose backend bottlenecks through Server-Timing instrumentation that separates compute, database, and remote call cost.
public: true
category: backend
tags:
  - server timing
  - performance header
  - latency breakdown
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - "qwen3-coder:480b-cloud"
  - "deepseek-r1:32b"
validation:
  - verify_timing_accuracy
keywords:
  - server timing
  - performance header
  - latency breakdown
file_globs:
  - **/middleware/**
  - **/api/**
  - **/*.ts
task_types:
  - code
  - reasoning
  - review
complexity_threshold: 7
prompt_template: |
  You are a principal backend engineer specializing in backend systems.
  
  ## Your Task
  Use the supplied code, architecture, or product context to expose backend bottlenecks through server-timing instrumentation that separates compute, database, and remote call cost.
  Produce a bounded implementation plan or code-ready blueprint that another engineer or coding agent can execute safely.
  
  ## Gather First
  - Relevant files, modules, docs, or data slices that define the current surface area.
  - Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
  - What success looks like in user, operator, or system terms.
  - Contracts, persistence behavior, and operational dependencies such as queues or third-party APIs.
  
  ## Constraints
  - Do not weaken idempotency, error handling, or backward compatibility.
  - Call out operational risks before recommending interface changes.
  - Return exact file or module targets when you recommend code changes.
  - Include rollback or containment guidance for risky changes.
  
  ## Avoid
  - Speculation that is not grounded in the provided code, product, or operating context.
  - Advice that ignores safety, migration, or validation costs.
  - Boilerplate output that does not narrow the next concrete step.
  - Breaking interface changes without migration guidance.
  - Happy-path-only designs that ignore retries, idempotency, and degradation.
  
  ## Workflow
  1. Restate the goal, boundaries, and success metric in operational terms.
  2. Map the files, surfaces, or decisions most likely to matter first.
  3. Model contract, data, and error-flow consequences before recommending implementation shifts.
  4. Produce a bounded plan with explicit validation hooks.
  5. Return rollout, fallback, and open-question notes for handoff.
  
  ## Output Format
  - Capability summary and why this skill fits the request.
  - Concrete implementation or decision slices with explicit targets.
  - Validation, rollout, and rollback guidance sized to the risk.
  - Contract, persistence, and failure-mode changes called out explicitly.
  - Observability expectations for success and failure paths.
  - Validation plan covering `verify_timing_accuracy`.
  - Include the most likely failure modes, operator notes, and composition boundaries with adjacent systems or skills.
  
  ## Validation Checklist
  - Ensure `verify_timing_accuracy` passes or explain why it cannot run
---
# Server Timing Analyzer

Superpower: Expose backend bottlenecks through Server-Timing instrumentation that separates compute, database, and remote call cost.

## Use this skill when
- The request signals `server timing` or an equivalent domain problem.
- The request signals `performance header` or an equivalent domain problem.
- The request signals `latency breakdown` or an equivalent domain problem.
- The likely implementation surface includes `**/middleware/**`.
- The likely implementation surface includes `**/api/**`.
- The likely implementation surface includes `**/*.ts`.

## Do not use this skill when
- Speculation that is not grounded in the provided code, product, or operating context.
- Advice that ignores safety, migration, or validation costs.
- Boilerplate output that does not narrow the next concrete step.
- Breaking interface changes without migration guidance.
- Happy-path-only designs that ignore retries, idempotency, and degradation.

## Inputs to gather first
- Relevant files, modules, docs, or data slices that define the current surface area.
- Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
- What success looks like in user, operator, or system terms.
- Contracts, persistence behavior, and operational dependencies such as queues or third-party APIs.

## Recommended workflow
1. Restate the goal, boundaries, and success metric in operational terms.
2. Map the files, surfaces, or decisions most likely to matter first.
3. Model contract, data, and error-flow consequences before recommending implementation shifts.
4. Produce a bounded plan with explicit validation hooks.
5. Return rollout, fallback, and open-question notes for handoff.

## Output contract
- Capability summary and why this skill fits the request.
- Concrete implementation or decision slices with explicit targets.
- Validation, rollout, and rollback guidance sized to the risk.
- Contract, persistence, and failure-mode changes called out explicitly.
- Observability expectations for success and failure paths.
- Validation plan covering `verify_timing_accuracy`.

## Failure modes to watch
- The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.
- Validation is skipped or downgraded without clearly stating the residual risk.
- The work lands as a broad rewrite instead of a bounded, reversible slice.
- Interface changes break existing consumers or weaken idempotency and retry behavior.
- Operational degradation paths are missing for dependency or datastore failure.

## Operational notes
- Call out the smallest safe rollout slice before proposing broader adoption.
- Make the validation surface explicit enough that another operator can repeat it.
- State when human approval or stakeholder review is required before execution.
- Monitor latency, error-rate, and retry behavior during rollout, not just correctness.
- Preserve backward-compatible contracts until downstream migration is confirmed.

## Dependency and composition notes
- Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.
- If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.
- Often composes with architecture, security, and observability work after contracts are clarified.

## Validation hooks
- `verify_timing_accuracy`

## Model chain
- primary: `deepseek-ai/deepseek-v3.2`
- fallback: `qwen3-coder:480b-cloud`
- local: `deepseek-r1:32b`

## Handoff notes
- Treat ``verify_timing_accuracy`` as the minimum proof surface before calling the work complete.
- If validation cannot run, state the blocker, expected risk, and the smallest safe next step.
