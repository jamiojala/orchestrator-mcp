---
name: Public Repo Sanitizer
description: Audit a repo for secrets, personal paths, client-specific references, and OSS-readiness gaps before publishing.
public: true
category: release
tags:
  - security
  - release
  - open-source
  - hygiene
preferred_models:
  - deepseek-ai/deepseek-v3.2
  - gemini-2.5-pro
validation:
  - git_delegate_code_review
keywords:
  - open source
  - public repo
  - sanitize
  - release
  - publish
  - secret scan
file_globs:
task_types:
  - review
  - architecture
prompt_template: |
  Review the provided repo snapshot for anything that should not ship publicly.
  Flag secrets, private paths, client references, brittle docs, and configuration hazards.
---
# Public Repo Sanitizer

Audit a repo for secrets, personal paths, client-specific references, and OSS-readiness gaps before publishing.

Source: Advanced first-party pack

## Use this skill when
- The request signals `open source` or a directly related problem.
- The request signals `public repo` or a directly related problem.
- The request signals `sanitize` or a directly related problem.
- The request signals `release` or a directly related problem.
- The request signals `publish` or a directly related problem.

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
- Release hygiene checks exist but are too narrow to catch high-cost leaks.
- The pack flags noise instead of the operator-visible failure modes that matter.

## Operational notes
- State the smallest safe slice that can be executed or reviewed next.
- Leave enough evidence behind that another maintainer can continue without re-deriving the workflow.
- Call out where human review or approval changes the recommended path.
- Tie hygiene checks to a concrete release gate or review step.
- Separate high-confidence blockers from advisory findings so the operator can act quickly.

## Dependency and composition notes
- Let this pack lead only when it owns the main bottleneck; otherwise treat it as a specialist sidecar.
- If another pack has a narrower, more concrete surface, hand off with explicit files, risks, and validation goals.
- Pairs well with security, debugging, and docs packs to turn checks into operator-ready release gates.

## Validation hooks
- `git_delegate_code_review`

## Model chain
- `deepseek-ai/deepseek-v3.2`
- `gemini-2.5-pro`

## Pack contents
- `SKILL.md` for portable agent-skill usage
- `skill.yaml` for runtime registry loading
- `README.md` for human install and review context
- `marketplace.yaml` for richer metadata and catalog indexing
