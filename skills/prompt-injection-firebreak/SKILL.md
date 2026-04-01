---
name: Prompt Injection Firebreak
description: Design hard prompt boundaries, tool gating, and context sanitization so indirect prompt injection has fewer places to land.
public: true
category: security
tags:
  - prompt-injection
  - tool-gating
  - sanitization
  - agents
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - moonshotai/kimi-k2.5
  - "deepseek-r1:32b"
validation:
  - verify_prompt_boundary
  - git_delegate_code_review
keywords:
  - prompt injection
  - context sanitization
  - tool gating
  - agent security
file_globs:
  - **/prompts/**
  - **/tools/**
  - **/*.md
  - **/*.yaml
task_types:
  - review
  - architecture
  - reasoning
prompt_template: |
  Audit the workflow for direct and indirect prompt-injection exposure, especially through retrieved content, tool responses, and long conversation state.
  Return concrete firebreaks for sanitization, permissioning, human approval, and tool result handling.
  Bias toward layered mitigations with clear residual-risk notes.
---
# Prompt Injection Firebreak

Design hard prompt boundaries, tool gating, and context sanitization so indirect prompt injection has fewer places to land.

Source: Advanced first-party pack

## Use this skill when
- The request signals `prompt injection` or a directly related problem.
- The request signals `context sanitization` or a directly related problem.
- The request signals `tool gating` or a directly related problem.
- The request signals `agent security` or a directly related problem.
- The likely implementation surface includes `**/prompts/**`.
- The likely implementation surface includes `**/tools/**`.
- The likely implementation surface includes `**/*.md`.
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
- The security story looks complete while indirect prompt, repo, or release paths remain exposed.
- Mitigations depend on operator memory instead of hard guardrails.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Record what was hardened, what remains exposed, and where human approval is still required.
- Prefer controls that fail closed when context quality or operator confidence is low.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with orchestration, release, and api packs when guardrails span multiple surfaces.

## Validation hooks
- `verify_prompt_boundary`
- `git_delegate_code_review`

## Model chain
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
