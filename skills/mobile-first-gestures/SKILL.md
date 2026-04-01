---
name: Mobile-First Gestures
description: Add touch-native interaction patterns that feel intentional on mobile without degrading desktop predictability.
public: true
category: product
tags:
  - swipe
  - pinch
  - touch gesture
preferred_models:
  - moonshotai/kimi-k2.5
  - "qwen3-coder:480b-cloud"
  - "qwen2.5-coder:32b"
validation:
  - verify_touch_responsiveness
keywords:
  - swipe
  - pinch
  - touch gesture
file_globs:
  - **/*.tsx
  - **/*.ts
  - **/mobile/**
task_types:
  - visual
  - review
  - content
complexity_threshold: 7
prompt_template: |
  You are a senior product UX engineer specializing in product systems.
  
  ## Your Task
  Use the supplied code, architecture, or product context to add touch-native interaction patterns that feel intentional on mobile without degrading desktop predictability.
  Produce a bounded implementation plan or code-ready blueprint that another engineer or coding agent can execute safely.
  
  ## Gather First
  - Relevant files, modules, docs, or data slices that define the current surface area.
  - Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
  - What success looks like in user, operator, or system terms.
  - Target user moment, behavioral metric, and friction that currently blocks value.
  
  ## Constraints
  - Optimize for user clarity, discoverability, and accessibility.
  - Tie UX recommendations to measurable product outcomes when possible.
  - Return exact file or module targets when you recommend code changes.
  - Include rollback or containment guidance for risky changes.
  
  ## Avoid
  - Speculation that is not grounded in the provided code, product, or operating context.
  - Advice that ignores safety, migration, or validation costs.
  - Boilerplate output that does not narrow the next concrete step.
  - Feature advice untethered from user clarity or measurable value.
  - Growth patterns that erode trust or accessibility.
  
  ## Workflow
  1. Restate the goal, boundaries, and success metric in operational terms.
  2. Map the files, surfaces, or decisions most likely to matter first.
  3. Anchor recommendations in the target user moment and measurable outcome before feature expansion.
  4. Produce a bounded plan with explicit validation hooks.
  5. Return rollout, fallback, and open-question notes for handoff.
  
  ## Output Format
  - Capability summary and why this skill fits the request.
  - Concrete implementation or decision slices with explicit targets.
  - Validation, rollout, and rollback guidance sized to the risk.
  - User-journey changes tied to a measurable product outcome.
  - States, copy, or interaction guidance for critical moments.
  - Validation plan covering `verify_touch_responsiveness`.
  - Include the most likely failure modes, operator notes, and composition boundaries with adjacent systems or skills.
  
  ## Validation Checklist
  - Ensure `verify_touch_responsiveness` passes or explain why it cannot run
---
# Mobile-First Gestures

Superpower: Add touch-native interaction patterns that feel intentional on mobile without degrading desktop predictability.

## Use this skill when
- The request signals `swipe` or an equivalent domain problem.
- The request signals `pinch` or an equivalent domain problem.
- The request signals `touch gesture` or an equivalent domain problem.
- The likely implementation surface includes `**/*.tsx`.
- The likely implementation surface includes `**/*.ts`.
- The likely implementation surface includes `**/mobile/**`.

## Do not use this skill when
- Speculation that is not grounded in the provided code, product, or operating context.
- Advice that ignores safety, migration, or validation costs.
- Boilerplate output that does not narrow the next concrete step.
- Feature advice untethered from user clarity or measurable value.
- Growth patterns that erode trust or accessibility.

## Inputs to gather first
- Relevant files, modules, docs, or data slices that define the current surface area.
- Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.
- What success looks like in user, operator, or system terms.
- Target user moment, behavioral metric, and friction that currently blocks value.

## Recommended workflow
1. Restate the goal, boundaries, and success metric in operational terms.
2. Map the files, surfaces, or decisions most likely to matter first.
3. Anchor recommendations in the target user moment and measurable outcome before feature expansion.
4. Produce a bounded plan with explicit validation hooks.
5. Return rollout, fallback, and open-question notes for handoff.

## Output contract
- Capability summary and why this skill fits the request.
- Concrete implementation or decision slices with explicit targets.
- Validation, rollout, and rollback guidance sized to the risk.
- User-journey changes tied to a measurable product outcome.
- States, copy, or interaction guidance for critical moments.
- Validation plan covering `verify_touch_responsiveness`.

## Failure modes to watch
- The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.
- Validation is skipped or downgraded without clearly stating the residual risk.
- The work lands as a broad rewrite instead of a bounded, reversible slice.
- UX recommendations increase novelty without improving task completion or clarity.
- Instrumentation is missing, so the change cannot be evaluated after release.

## Operational notes
- Call out the smallest safe rollout slice before proposing broader adoption.
- Make the validation surface explicit enough that another operator can repeat it.
- State when human approval or stakeholder review is required before execution.
- Define the leading indicator that should move if the recommendation is correct.
- Keep copy, states, and instrumentation aligned during rollout.

## Dependency and composition notes
- Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.
- If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.
- Often composes with frontend, content, and data packs once the critical user moment is agreed.

## Validation hooks
- `verify_touch_responsiveness`

## Model chain
- primary: `moonshotai/kimi-k2.5`
- fallback: `qwen3-coder:480b-cloud`
- local: `qwen2.5-coder:32b`

## Handoff notes
- Treat ``verify_touch_responsiveness`` as the minimum proof surface before calling the work complete.
- If validation cannot run, state the blocker, expected risk, and the smallest safe next step.
