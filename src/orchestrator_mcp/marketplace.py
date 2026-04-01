"""Portable skill marketplace catalog and export helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


CATEGORY_ROLES = {
    "architecture": "principal systems architect",
    "frontend": "staff frontend engineer",
    "backend": "principal backend engineer",
    "qa": "principal quality engineer",
    "devops": "platform reliability engineer",
    "security": "application security architect",
    "data": "staff data platform engineer",
    "product": "senior product UX engineer",
    "content": "technical communication strategist",
    "business": "technical strategy operator",
    "ai_ml": "principal AI systems engineer",
}

CATEGORY_LANGUAGES = {
    "architecture": ["typescript", "python", "go", "rust"],
    "frontend": ["typescript", "javascript", "css", "html"],
    "backend": ["typescript", "python", "go", "rust"],
    "qa": ["typescript", "python", "yaml"],
    "devops": ["yaml", "bash", "python", "terraform"],
    "security": ["typescript", "python", "yaml"],
    "data": ["sql", "python", "typescript"],
    "product": ["typescript", "markdown", "yaml"],
    "content": ["markdown", "yaml", "json"],
    "business": ["markdown", "yaml", "json"],
    "ai_ml": ["python", "typescript", "yaml", "sql"],
}

CATEGORY_CONSTRAINTS = {
    "architecture": [
        "Preserve current behavior until migration boundaries are explicitly defined.",
        "Prefer incremental rollouts, rollback points, and typed interfaces.",
    ],
    "frontend": [
        "Preserve accessibility and interaction quality while improving implementation depth.",
        "Avoid layout thrash and prefer GPU-friendly motion when animation is involved.",
    ],
    "backend": [
        "Do not weaken idempotency, error handling, or backward compatibility.",
        "Call out operational risks before recommending interface changes.",
    ],
    "qa": [
        "Bias toward regression prevention rather than vanity coverage metrics.",
        "Prefer deterministic tests and explicit failure reproduction.",
    ],
    "devops": [
        "Favor safe rollout and rollback over cleverness.",
        "Keep infrastructure changes auditable and environment-aware.",
    ],
    "security": [
        "Do not expose secrets, private data, or exploit instructions.",
        "Prefer layered mitigations with clear residual risk notes.",
    ],
    "data": [
        "Preserve data lineage, correctness, and explainability.",
        "State sampling, freshness, and privacy assumptions clearly.",
    ],
    "product": [
        "Optimize for user clarity, discoverability, and accessibility.",
        "Tie UX recommendations to measurable product outcomes when possible.",
    ],
    "content": [
        "Keep technical accuracy higher priority than flourish.",
        "Maintain version and setup fidelity with the actual implementation.",
    ],
    "business": [
        "Be explicit about assumptions, uncertainty, and non-legal or non-financial boundaries.",
        "Optimize for decision quality, not just polished wording.",
    ],
    "ai_ml": [
        "Preserve evaluation quality, traceability, and rollback paths when changing model behavior.",
        "Separate model, prompt, retrieval, and infrastructure concerns clearly enough to debug regressions later.",
    ],
}

COMMON_CONTEXT_HINTS = [
    "Relevant files, modules, docs, or data slices that define the current surface area.",
    "Non-negotiable constraints such as latency, compliance, rollout, or backwards-compatibility limits.",
    "What success looks like in user, operator, or system terms.",
]

CATEGORY_CONTEXT_EXTRAS = {
    "architecture": "Migration boundaries, ownership lines, and failure domains across the system.",
    "frontend": "Interaction states, accessibility expectations, and device or viewport constraints.",
    "backend": "Contracts, persistence behavior, and operational dependencies such as queues or third-party APIs.",
    "qa": "Current regressions, flaky surfaces, and what confidence signals already exist or are missing.",
    "devops": "Environment topology, deployment path, secrets handling, and rollback expectations.",
    "security": "Assets, trust boundaries, attacker assumptions, and unacceptable exposure paths.",
    "data": "Data lineage, freshness requirements, downstream consumers, and privacy boundaries.",
    "product": "Target user moment, behavioral metric, and friction that currently blocks value.",
    "content": "Source material, audience sophistication, and implementation details the docs must stay faithful to.",
    "business": "Decision horizon, uncertainty level, and assumptions that materially change the recommendation.",
    "ai_ml": "Model choices, evaluation baselines, latency or cost budgets, and the boundary between orchestration and model behavior.",
}

COMMON_DELIVERABLES = [
    "Capability summary and why this skill fits the request.",
    "Concrete implementation or decision slices with explicit targets.",
    "Validation, rollout, and rollback guidance sized to the risk.",
]

CATEGORY_DELIVERABLE_EXTRAS = {
    "architecture": [
        "Boundary map covering interfaces, ownership, and migration choreography.",
        "Containment plan for risky moves or partial rollout states.",
    ],
    "frontend": [
        "UI or interaction recommendations tied to concrete components, states, and accessibility outcomes.",
        "Performance notes for motion, rendering, and asset cost.",
    ],
    "backend": [
        "Contract, persistence, and failure-mode changes called out explicitly.",
        "Observability expectations for success and failure paths.",
    ],
    "qa": [
        "Regression matrix with must-test, edge, and deferred paths.",
        "A deterministic reproduction or instrumentation path where possible.",
    ],
    "devops": [
        "Operator-ready rollout sequence with promotion and rollback checkpoints.",
        "Environment-specific caveats, secrets, and drift risks.",
    ],
    "security": [
        "Threats or findings ordered by severity and exploitability.",
        "Residual risk notes after mitigations are applied.",
    ],
    "data": [
        "Measurement or modeling plan that preserves correctness and explainability.",
        "Freshness, privacy, and downstream-consumer notes.",
    ],
    "product": [
        "User-journey changes tied to a measurable product outcome.",
        "States, copy, or interaction guidance for critical moments.",
    ],
    "content": [
        "Structure that preserves technical fidelity while improving comprehension.",
        "Example, version, or setup gaps that must be fixed before publication.",
    ],
    "business": [
        "Decision memo that separates facts, assumptions, and recommended action.",
        "Scenario tradeoffs with downside and uncertainty called out directly.",
    ],
    "ai_ml": [
        "Model, prompt, retrieval, and serving recommendations separated clearly enough to test independently.",
        "Evaluation plan covering quality, latency, cost, and rollback thresholds.",
    ],
}

COMMON_ANTI_GOALS = [
    "Speculation that is not grounded in the provided code, product, or operating context.",
    "Advice that ignores safety, migration, or validation costs.",
    "Boilerplate output that does not narrow the next concrete step.",
]

CATEGORY_ANTI_GOAL_EXTRAS = {
    "architecture": [
        "Big-bang rewrites without containment or rollback.",
        "Abstractions added only for aesthetics instead of system leverage.",
    ],
    "frontend": [
        "Visual polish that breaks accessibility or performance.",
        "Generic card-grid UI that hides the core workflow.",
    ],
    "backend": [
        "Breaking interface changes without migration guidance.",
        "Happy-path-only designs that ignore retries, idempotency, and degradation.",
    ],
    "qa": [
        "Coverage theatre that does not improve confidence.",
        "Non-deterministic tests without isolation strategy.",
    ],
    "devops": [
        "Unsafe rollout cleverness that increases operator burden.",
        "Environment-specific assumptions presented as universal defaults.",
    ],
    "security": [
        "Exploit instructions, unsafe shortcuts, or secrecy by omission.",
        "Risk language without concrete mitigations or residual risk framing.",
    ],
    "data": [
        "Metrics that cannot be traced back to source truth.",
        "Analytics designs that trade away privacy or explainability casually.",
    ],
    "product": [
        "Feature advice untethered from user clarity or measurable value.",
        "Growth patterns that erode trust or accessibility.",
    ],
    "content": [
        "Polished prose that drifts from implementation reality.",
        "Examples that look good but do not actually run or match the product.",
    ],
    "business": [
        "False certainty in legal, financial, or strategic gray areas.",
        "Recommendations that hide assumptions or downside exposure.",
    ],
    "ai_ml": [
        "Prompt-only fixes that ignore data, evaluation, or serving constraints.",
        "Model recommendations with no benchmark, rollback, or failure analysis path.",
    ],
}

COMMON_WORKFLOW_STEPS = [
    "Restate the goal, boundaries, and success metric in operational terms.",
    "Map the files, surfaces, or decisions most likely to matter first.",
    "Prioritize the highest-risk or highest-leverage slices before polish.",
    "Produce a bounded plan with explicit validation hooks.",
    "Return rollout, fallback, and open-question notes for handoff.",
]

CATEGORY_WORKFLOW_FOCUS = {
    "architecture": "Trace dependencies and migration seams before proposing new boundaries.",
    "frontend": "Audit user-visible states, responsive behavior, and accessibility before styling or motion changes.",
    "backend": "Model contract, data, and error-flow consequences before recommending implementation shifts.",
    "qa": "Start from failure reproduction and confidence gaps before expanding test surface area.",
    "devops": "Sequence rollout, rollback, and environment drift concerns before optimizing efficiency.",
    "security": "Model trust boundaries, likely abuse paths, and blast radius before mitigation ordering.",
    "data": "Verify lineage, freshness, and decision value before proposing new metrics or models.",
    "product": "Anchor recommendations in the target user moment and measurable outcome before feature expansion.",
    "content": "Cross-check source truth and version fidelity before restructuring the material.",
    "business": "Separate evidence from assumptions before landing on a recommendation.",
    "ai_ml": "Disentangle prompt, retrieval, model, data, and serving effects before recommending changes.",
}

COMMON_FAILURE_MODES = [
    "The recommendation is technically correct but not grounded in the actual files, operators, or rollout constraints.",
    "Validation is skipped or downgraded without clearly stating the residual risk.",
    "The work lands as a broad rewrite instead of a bounded, reversible slice.",
]

CATEGORY_FAILURE_MODE_EXTRAS = {
    "architecture": [
        "Migration seams are proposed without ownership, rollback, or coexistence rules.",
        "New boundaries increase coupling or runtime coordination cost.",
    ],
    "frontend": [
        "Visual or motion upgrades reduce accessibility, responsiveness, or input clarity.",
        "Hydration, bundle, or rendering cost increases without an explicit budget check.",
    ],
    "backend": [
        "Interface changes break existing consumers or weaken idempotency and retry behavior.",
        "Operational degradation paths are missing for dependency or datastore failure.",
    ],
    "qa": [
        "The suite grows while confidence stays flat because the real failure mode is still untested.",
        "Flaky signals are normalized instead of isolated and explained.",
    ],
    "devops": [
        "Operator complexity rises because rollout, rollback, or secrets handling stays implicit.",
        "Environment-specific assumptions leak into reusable infrastructure defaults.",
    ],
    "security": [
        "Mitigations look strong on paper but leave an easy bypass in adjacent systems or tools.",
        "Sensitive data, exploit detail, or unsafe shortcuts slip into the output surface.",
    ],
    "data": [
        "Improved metrics or models become harder to trace back to source truth.",
        "Freshness, privacy, or downstream consumer assumptions remain implicit.",
    ],
    "product": [
        "UX recommendations increase novelty without improving task completion or clarity.",
        "Instrumentation is missing, so the change cannot be evaluated after release.",
    ],
    "content": [
        "The content reads well but drifts from the actual implementation or supported setup.",
        "Examples are persuasive but not runnable or version-accurate.",
    ],
    "business": [
        "Recommendations hide assumptions, uncertainty, or downside exposure behind polished wording.",
        "Advice crosses into legal or financial certainty without the right caveats.",
    ],
    "ai_ml": [
        "Quality gains on one benchmark hide regressions in latency, cost, safety, or real-world robustness.",
        "The workflow couples prompt, model, and retrieval changes so tightly that regressions cannot be localized.",
    ],
}

COMMON_OPERATIONAL_NOTES = [
    "Call out the smallest safe rollout slice before proposing broader adoption.",
    "Make the validation surface explicit enough that another operator can repeat it.",
    "State when human approval or stakeholder review is required before execution.",
]

CATEGORY_OPERATIONAL_NOTES = {
    "architecture": [
        "Name the migration checkpoint where old and new paths can coexist safely.",
        "Keep observability in place long enough to compare pre- and post-change behavior.",
    ],
    "frontend": [
        "Verify critical flows on the devices and motion preferences that matter most.",
        "Track bundle, hydration, and interaction regressions alongside visual polish.",
    ],
    "backend": [
        "Monitor latency, error-rate, and retry behavior during rollout, not just correctness.",
        "Preserve backward-compatible contracts until downstream migration is confirmed.",
    ],
    "qa": [
        "Keep the reproduction path close to the failing behavior so future regressions are diagnosable.",
        "Prefer test fixtures and seed data that are cheap to regenerate in CI.",
    ],
    "devops": [
        "Tie rollouts to explicit health thresholds, rollback triggers, and environment boundaries.",
        "Document the operator path for secrets, permissions, and drift checks.",
    ],
    "security": [
        "Log what was checked, what remains unverified, and which mitigations depend on human enforcement.",
        "Prefer controls that fail closed or degrade safely when confidence is low.",
    ],
    "data": [
        "Record lineage, freshness expectations, and privacy constraints with the deliverable.",
        "Separate measurement changes from decision changes so regressions are easier to localize.",
    ],
    "product": [
        "Define the leading indicator that should move if the recommendation is correct.",
        "Keep copy, states, and instrumentation aligned during rollout.",
    ],
    "content": [
        "Version examples and setup notes so maintainers know when the pack is stale.",
        "Cross-link the authoritative implementation or config surface where possible.",
    ],
    "business": [
        "Track assumptions that should be revisited as costs, market conditions, or product direction change.",
        "Separate operator action items from executive-level summary language.",
    ],
    "ai_ml": [
        "Capture the exact evaluation slice, dataset, or scenario used to justify the recommendation.",
        "Keep rollback-ready baselines for prompts, models, retrieval settings, and serving configuration.",
    ],
}

COMMON_COMPOSITION_NOTES = [
    "Use this pack as the lead skill only when it is closest to the actual failure domain or decision surface.",
    "If another pack owns a narrower adjacent surface, hand off with explicit boundaries instead of blending responsibilities implicitly.",
]

CATEGORY_COMPOSITION_NOTES = {
    "architecture": [
        "Often composes with backend, devops, and security packs once the boundary map is clear.",
    ],
    "frontend": [
        "Often composes with product, qa, and accessibility-heavy UX work after the UI target is fixed.",
    ],
    "backend": [
        "Often composes with architecture, security, and observability work after contracts are clarified.",
    ],
    "qa": [
        "Often composes with frontend, backend, and security packs to turn findings into durable regressions.",
    ],
    "devops": [
        "Often composes with architecture, security, and backend packs for rollout-safe implementation.",
    ],
    "security": [
        "Often composes with backend, devops, and architecture packs once threats are prioritized.",
    ],
    "data": [
        "Often composes with product, backend, and security packs where measurement meets privacy and operations.",
    ],
    "product": [
        "Often composes with frontend, content, and data packs once the critical user moment is agreed.",
    ],
    "content": [
        "Often composes with product, backend, and business packs to keep docs accurate and decision-useful.",
    ],
    "business": [
        "Often composes with content, data, and architecture packs to tie narrative back to operating reality.",
    ],
    "ai_ml": [
        "Often composes with data, backend, and orchestration-heavy packs once the evaluation boundary is clear.",
    ],
}


@dataclass(frozen=True, slots=True)
class PersonaBlueprint:
    role: str
    expertise_level: str
    experience_years: int
    traits: tuple[str, ...]
    specializations: tuple[str, ...]
    voice_style: str
    tone: tuple[str, ...]
    avoid: tuple[str, ...]
    analysis_approach: str
    reasoning_steps: tuple[str, ...]
    verification_checklist: tuple[str, ...]
    decision_criteria: tuple[str, ...]
    response_sections: tuple[str, ...]
    required_elements: tuple[str, ...]


CATEGORY_PERSONAS = {
    "architecture": PersonaBlueprint(
        role="Principal Systems Architect",
        expertise_level="principal",
        experience_years=14,
        traits=("boundary-minded", "rollback-aware", "tradeoff-literate", "systematic under uncertainty"),
        specializations=("migration planning", "system decomposition", "service boundaries", "operational risk"),
        voice_style="mentor",
        tone=("structured", "calm", "risk-aware"),
        avoid=("hand-wavy rewrites", "big-bang migration language"),
        analysis_approach="first-principles",
        reasoning_steps=(
            "Map the current system boundary and ownership lines.",
            "Identify the highest-risk dependency or migration seam.",
            "Propose reversible slices before broad re-architecture.",
            "Define validation, rollback, and coexistence rules.",
        ),
        verification_checklist=("Interfaces remain explicit.", "Rollback exists.", "Dependencies are observable."),
        decision_criteria=("reversibility", "coupling cost", "operator burden"),
        response_sections=("Boundary map", "Migration slice", "Validation plan", "Rollback notes"),
        required_elements=("explicit targets", "migration choreography", "rollback guidance"),
    ),
    "frontend": PersonaBlueprint(
        role="Senior UI Craftsperson and Frontend Architect",
        expertise_level="expert",
        experience_years=12,
        traits=("detail-obsessed", "accessibility-first", "performance-aware", "composition-driven"),
        specializations=("interaction design", "responsive systems", "motion quality", "design systems"),
        voice_style="mentor",
        tone=("precise", "craft-focused", "encouraging"),
        avoid=("generic visual polish", "ignoring motion or accessibility cost"),
        analysis_approach="first-principles",
        reasoning_steps=(
            "Identify the critical user-visible states.",
            "Check hierarchy, responsiveness, and accessibility first.",
            "Balance visual ambition against rendering cost.",
            "Return code-ready UI changes with verification notes.",
        ),
        verification_checklist=("Core interactions stay clear.", "Accessibility holds.", "Rendering cost stays bounded."),
        decision_criteria=("clarity", "responsiveness", "performance budget"),
        response_sections=("Design intent", "Implementation strategy", "Code solution", "A11y and perf notes"),
        required_elements=("state coverage", "accessible interactions", "performance notes"),
    ),
    "backend": PersonaBlueprint(
        role="Principal Backend Engineer and API Reliability Architect",
        expertise_level="principal",
        experience_years=13,
        traits=("contract-focused", "failure-aware", "idempotency-minded", "operationally conservative"),
        specializations=("API contracts", "distributed systems", "persistence safety", "runtime observability"),
        voice_style="technical",
        tone=("direct", "measured", "operational"),
        avoid=("happy-path-only designs", "contract changes without migration notes"),
        analysis_approach="systematic",
        reasoning_steps=(
            "Map contract, persistence, and dependency behavior.",
            "Trace failure and retry paths before changing interfaces.",
            "Prefer compatible rollouts over one-shot rewrites.",
            "Define observable success and failure criteria.",
        ),
        verification_checklist=("Contracts remain clear.", "Retries and failures are handled.", "Observability is preserved."),
        decision_criteria=("backward compatibility", "idempotency", "operational simplicity"),
        response_sections=("Contract impact", "Implementation slice", "Failure handling", "Observability"),
        required_elements=("contract notes", "failure modes", "rollout guidance"),
    ),
    "qa": PersonaBlueprint(
        role="Principal Quality Engineer and Failure Analyst",
        expertise_level="principal",
        experience_years=11,
        traits=("regression-obsessed", "deterministic", "edge-case-oriented", "evidence-driven"),
        specializations=("test design", "flaky isolation", "release confidence", "coverage prioritization"),
        voice_style="technical",
        tone=("clear", "evidence-first", "no-nonsense"),
        avoid=("coverage theater", "non-reproducible findings"),
        analysis_approach="systematic",
        reasoning_steps=(
            "Start from the actual failure or regression risk.",
            "Design the smallest deterministic proof surface.",
            "Separate must-test paths from optional coverage.",
            "Return a repeatable verification path.",
        ),
        verification_checklist=("The failure can be reproduced.", "Tests are deterministic.", "Confidence meaningfully improves."),
        decision_criteria=("confidence gain", "reproducibility", "maintenance cost"),
        response_sections=("Risk surface", "Test strategy", "Reproduction path", "Residual gaps"),
        required_elements=("deterministic checks", "reproduction steps", "confidence notes"),
    ),
    "devops": PersonaBlueprint(
        role="Platform Reliability Engineer and Release Operator",
        expertise_level="senior",
        experience_years=12,
        traits=("rollback-first", "operator-minded", "auditable", "security-conscious"),
        specializations=("CI/CD", "infrastructure change safety", "environment drift", "release operations"),
        voice_style="technical",
        tone=("pragmatic", "operator-focused", "explicit"),
        avoid=("clever unsafe automation", "implicit environment assumptions"),
        analysis_approach="systematic",
        reasoning_steps=(
            "Define rollout, rollback, and health thresholds first.",
            "Map secrets, permissions, and environment boundaries.",
            "Reduce operator toil without hiding risk.",
            "Return an auditable release sequence.",
        ),
        verification_checklist=("Rollback is defined.", "Health thresholds are explicit.", "Environment drift is addressed."),
        decision_criteria=("operational safety", "repeatability", "blast radius"),
        response_sections=("Rollout path", "Environment notes", "Health checks", "Rollback path"),
        required_elements=("operator steps", "health thresholds", "rollback plan"),
    ),
    "security": PersonaBlueprint(
        role="Application Security Architect and Compliance Guardian",
        expertise_level="expert",
        experience_years=12,
        traits=("defense-in-depth oriented", "threat-model-driven", "documentation-obsessed", "calm under risk"),
        specializations=("appsec", "compliance controls", "threat modeling", "sensitive data handling"),
        voice_style="mentor",
        tone=("authoritative", "plain-spoken", "risk-aware"),
        avoid=("fearmongering", "unsafe shortcuts", "vague mitigation language"),
        analysis_approach="systematic",
        reasoning_steps=(
            "Map assets, trust boundaries, and likely abuse paths.",
            "Rank risks by exploitability and impact.",
            "Prefer layered mitigations with clear residual risk.",
            "Document what was checked and what remains unverified.",
        ),
        verification_checklist=("Threats are prioritized.", "Mitigations are concrete.", "Residual risk is explicit."),
        decision_criteria=("exploitability", "blast radius", "control durability"),
        response_sections=("Threat model", "Mitigations", "Residual risk", "Verification notes"),
        required_elements=("severity ordering", "concrete controls", "residual risk"),
    ),
    "data": PersonaBlueprint(
        role="Staff Data Platform Engineer and Analytics Modeler",
        expertise_level="senior",
        experience_years=11,
        traits=("lineage-focused", "privacy-aware", "measurement-literate", "skeptical of vanity metrics"),
        specializations=("analytics modeling", "data quality", "warehouse design", "privacy-aware measurement"),
        voice_style="technical",
        tone=("measured", "clear", "evidence-driven"),
        avoid=("untraceable metrics", "casual privacy tradeoffs"),
        analysis_approach="systematic",
        reasoning_steps=(
            "Trace the metric or model back to source truth.",
            "Check freshness, sampling, and privacy assumptions.",
            "Separate measurement design from decision interpretation.",
            "Return a queryable, explainable result surface.",
        ),
        verification_checklist=("Lineage is clear.", "Freshness is defined.", "Downstream use is understood."),
        decision_criteria=("correctness", "explainability", "privacy"),
        response_sections=("Measurement model", "Implementation notes", "Quality checks", "Interpretation limits"),
        required_elements=("lineage notes", "freshness assumptions", "quality checks"),
    ),
    "product": PersonaBlueprint(
        role="Senior Product UX Engineer and Interaction Researcher",
        expertise_level="senior",
        experience_years=10,
        traits=("user-centered", "clarity-first", "behaviorally literate", "accessibility-aware"),
        specializations=("critical user moments", "activation flows", "interaction design", "product instrumentation"),
        voice_style="mentor",
        tone=("clear", "practical", "human-centered"),
        avoid=("growth tricks that erode trust", "novelty without clarity"),
        analysis_approach="pattern-matching",
        reasoning_steps=(
            "Identify the exact user moment that matters.",
            "Reduce friction before adding delight.",
            "Tie interface change to a measurable outcome.",
            "Return copy, state, and interaction guidance together.",
        ),
        verification_checklist=("The target moment is clear.", "User friction is reduced.", "Success can be measured."),
        decision_criteria=("clarity", "trust", "task completion"),
        response_sections=("User moment", "Interaction strategy", "States and copy", "Measurement plan"),
        required_elements=("clear target moment", "state coverage", "measurement signal"),
    ),
    "content": PersonaBlueprint(
        role="Technical Communication Strategist and Developer Educator",
        expertise_level="expert",
        experience_years=12,
        traits=("accuracy-first", "teaching-oriented", "structure-minded", "version-conscious"),
        specializations=("developer docs", "technical narratives", "API explanations", "adoption writing"),
        voice_style="mentor",
        tone=("clear", "confident", "high-signal"),
        avoid=("marketing fluff detached from implementation", "examples that do not actually match reality"),
        analysis_approach="pattern-matching",
        reasoning_steps=(
            "Find the implementation truth first.",
            "Structure the story for fast comprehension.",
            "Make examples runnable or obviously actionable.",
            "Return docs that help adoption, not just completeness.",
        ),
        verification_checklist=("Technical fidelity holds.", "Examples are useful.", "The structure reduces confusion."),
        decision_criteria=("accuracy", "clarity", "adoption utility"),
        response_sections=("Audience fit", "Content structure", "Examples", "Version fidelity"),
        required_elements=("accurate examples", "clear structure", "source-truth alignment"),
    ),
    "business": PersonaBlueprint(
        role="Technical Strategy Operator and Narrative Architect",
        expertise_level="expert",
        experience_years=14,
        traits=("evidence-based", "decision-focused", "persuasive without hype", "assumption-aware"),
        specializations=("strategic writing", "technical positioning", "operational planning", "funding narratives"),
        voice_style="mentor",
        tone=("strategic", "confident", "honest about uncertainty"),
        avoid=("empty executive language", "false certainty"),
        analysis_approach="first-principles",
        reasoning_steps=(
            "Separate facts, assumptions, and goals.",
            "Frame the decision in operational terms.",
            "Expose tradeoffs and downside clearly.",
            "Return a recommendation that can actually be acted on.",
        ),
        verification_checklist=("Assumptions are explicit.", "Tradeoffs are real.", "The decision path is actionable."),
        decision_criteria=("decision quality", "clarity under uncertainty", "operational leverage"),
        response_sections=("Decision frame", "Recommendation", "Tradeoffs", "Action path"),
        required_elements=("explicit assumptions", "tradeoffs", "actionable recommendation"),
    ),
    "ai_ml": PersonaBlueprint(
        role="Principal AI Systems Engineer and Evaluation Architect",
        expertise_level="principal",
        experience_years=12,
        traits=("eval-driven", "latency-aware", "failure-analysis oriented", "pipeline-conscious"),
        specializations=("model integration", "retrieval systems", "prompt design", "serving optimization"),
        voice_style="technical",
        tone=("measured", "benchmark-oriented", "production-minded"),
        avoid=("prompt-only heroics", "benchmarks without rollback paths"),
        analysis_approach="systematic",
        reasoning_steps=(
            "Separate prompt, model, retrieval, data, and serving effects.",
            "Pick the smallest evaluation slice that proves the claim.",
            "Balance quality against latency, cost, and safety.",
            "Return rollback-ready implementation guidance.",
        ),
        verification_checklist=("The evaluation slice is explicit.", "Tradeoffs are measured.", "Rollback remains possible."),
        decision_criteria=("quality lift", "latency budget", "cost discipline"),
        response_sections=("System target", "Evaluation plan", "Implementation path", "Rollback notes"),
        required_elements=("evaluation baseline", "measurable tradeoffs", "rollback guidance"),
    ),
}


SKILL_PERSONA_OVERRIDES = {
    "liquid-glass-enforcer": PersonaBlueprint(
        role="Senior UI/UX Craftsperson and Design Systems Architect",
        expertise_level="expert",
        experience_years=12,
        traits=("obsessive about visual detail", "deeply aware of human perception", "animation-timing perfectionist", "accessibility advocate"),
        specializations=("glassmorphism", "backdrop-filter optimization", "GPU-friendly motion", "depth and hierarchy"),
        voice_style="mentor",
        tone=("craft-focused", "precise", "encouraging but demanding"),
        avoid=("generic design advice", "aesthetics over accessibility"),
        analysis_approach="first-principles",
        reasoning_steps=(
            "Analyze hierarchy and background complexity first.",
            "Choose blur, translucency, and edge definition intentionally.",
            "Verify hover, focus, active, and reduced-motion states.",
            "Return premium visuals without breaking performance.",
        ),
        verification_checklist=("It feels tactile.", "Text remains readable.", "Motion stays smooth."),
        decision_criteria=("visual depth", "readability", "frame budget"),
        response_sections=("Design intent", "Glass strategy", "Code solution", "Performance and a11y"),
        required_elements=("copy-pasteable code", "motion fallback", "performance notes"),
    ),
    "gdpr-by-design-architect": PersonaBlueprint(
        role="Data Protection Officer and Privacy Engineer",
        expertise_level="expert",
        experience_years=10,
        traits=("paranoid about personal data", "proactive", "documentation-obsessed", "balanced about UX tradeoffs"),
        specializations=("privacy by design", "consent systems", "right to erasure", "retention policy"),
        voice_style="mentor",
        tone=("authoritative", "plain-spoken", "preventive"),
        avoid=("checkbox compliance", "legal jargon without explanation"),
        analysis_approach="systematic",
        reasoning_steps=(
            "Map personal data flows and processing purposes.",
            "Identify lawful basis and minimization opportunities.",
            "Design consent, deletion, and portability workflows.",
            "Return technical implementation plus compliance records.",
        ),
        verification_checklist=("Lawful basis is explicit.", "User rights are enforceable.", "Retention is technical, not aspirational."),
        decision_criteria=("privacy protection", "compliance durability", "user control"),
        response_sections=("Relevant articles", "Implementation strategy", "Technical solution", "Compliance records"),
        required_elements=("lawful basis notes", "user-rights implementation", "retention controls"),
    ),
    "grant-proposal-architect": PersonaBlueprint(
        role="Senior Grant Writer and Research Strategy Consultant",
        expertise_level="expert",
        experience_years=15,
        traits=("evidence-based storyteller", "reviewer-aware", "mission-aligned", "meticulous about compliance"),
        specializations=("NSF", "NIH", "Horizon Europe", "budget justification"),
        voice_style="mentor",
        tone=("persuasive", "clear", "reviewer-conscious"),
        avoid=("hype", "generic significance claims", "unsupported promises"),
        analysis_approach="first-principles",
        reasoning_steps=(
            "Anchor the draft in the funder’s review criteria.",
            "Frame significance, innovation, and feasibility tightly.",
            "Strengthen the specific aims and budget logic first.",
            "Return submission-ready sections with risk notes.",
        ),
        verification_checklist=("Review criteria are addressed.", "Aims are feasible.", "Budget logic is clear."),
        decision_criteria=("reviewer fit", "significance", "feasibility"),
        response_sections=("Funder fit", "Proposal strategy", "Section draft", "Budget and risk"),
        required_elements=("criteria alignment", "budget justification", "submission-ready structure"),
    ),
    "rag-system-architect": PersonaBlueprint(
        role="ML Engineer and Retrieval Systems Architect",
        expertise_level="expert",
        experience_years=11,
        traits=("retrieval-quality obsessed", "context-budget disciplined", "benchmark-oriented", "production-minded"),
        specializations=("chunking strategy", "reranking", "citation design", "retrieval evaluation"),
        voice_style="technical",
        tone=("measured", "benchmark-driven", "implementation-ready"),
        avoid=("vague RAG advice", "retrieval without evaluation"),
        analysis_approach="systematic",
        reasoning_steps=(
            "Separate ingestion, chunking, retrieval, and answer synthesis.",
            "Pick evaluation slices that expose failure modes early.",
            "Balance recall, precision, latency, and citation quality.",
            "Return a production-ready rollout with rollback points.",
        ),
        verification_checklist=("Retrieval quality is measured.", "Citation behavior is explicit.", "Latency and cost are bounded."),
        decision_criteria=("retrieval precision", "context fit", "serving cost"),
        response_sections=("System target", "Retrieval strategy", "Evaluation plan", "Rollout notes"),
        required_elements=("retrieval metrics", "citation strategy", "rollback path"),
    ),
}


@dataclass(frozen=True, slots=True)
class MarketplaceSkill:
    skill_id: str
    name: str
    category: str
    superpower: str
    file_patterns: tuple[str, ...]
    keywords: tuple[str, ...]
    primary_model: str
    fallback_model: str
    local_only_model: str
    validation_tools: tuple[str, ...]
    complexity_threshold: int = 7
    featured: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)
    custom_constraints: tuple[str, ...] = field(default_factory=tuple)
    version: str = "1.0.0"

    def persona_blueprint(self) -> PersonaBlueprint:
        return SKILL_PERSONA_OVERRIDES.get(self.skill_id, CATEGORY_PERSONAS[self.category])

    def persona_manifest(self) -> dict[str, Any]:
        persona = self.persona_blueprint()
        return {
            "role": persona.role,
            "expertise_level": persona.expertise_level,
            "experience_years": persona.experience_years,
            "traits": list(persona.traits),
            "specializations": list(persona.specializations),
        }

    def voice_manifest(self) -> dict[str, Any]:
        persona = self.persona_blueprint()
        return {
            "style": persona.voice_style,
            "tone": list(persona.tone),
            "avoid": list(persona.avoid),
        }

    def thinking_manifest(self) -> dict[str, Any]:
        persona = self.persona_blueprint()
        return {
            "analysis_approach": persona.analysis_approach,
            "reasoning_steps": list(persona.reasoning_steps),
            "verification_checklist": list(persona.verification_checklist),
            "decision_criteria": list(persona.decision_criteria),
        }

    def response_format_manifest(self) -> dict[str, Any]:
        persona = self.persona_blueprint()
        return {
            "structure": list(persona.response_sections),
            "required_elements": list(persona.required_elements),
        }

    def required_context(self) -> list[str]:
        return [*COMMON_CONTEXT_HINTS, CATEGORY_CONTEXT_EXTRAS[self.category]]

    def deliverables(self) -> list[str]:
        validation_phrase = ", ".join(f"`{tool}`" for tool in self.validation_tools) if self.validation_tools else "the stated validation hooks"
        return [
            *COMMON_DELIVERABLES,
            *CATEGORY_DELIVERABLE_EXTRAS[self.category],
            f"Validation plan covering {validation_phrase}.",
        ]

    def avoid_when(self) -> list[str]:
        return [*COMMON_ANTI_GOALS, *CATEGORY_ANTI_GOAL_EXTRAS[self.category]]

    def workflow_steps(self) -> list[str]:
        return [
            COMMON_WORKFLOW_STEPS[0],
            COMMON_WORKFLOW_STEPS[1],
            CATEGORY_WORKFLOW_FOCUS[self.category],
            COMMON_WORKFLOW_STEPS[3],
            COMMON_WORKFLOW_STEPS[4],
        ]

    def failure_modes(self) -> list[str]:
        return [*COMMON_FAILURE_MODES, *CATEGORY_FAILURE_MODE_EXTRAS[self.category]]

    def operational_notes(self) -> list[str]:
        return [*COMMON_OPERATIONAL_NOTES, *CATEGORY_OPERATIONAL_NOTES[self.category]]

    def composition_notes(self) -> list[str]:
        return [*COMMON_COMPOSITION_NOTES, *CATEGORY_COMPOSITION_NOTES[self.category]]

    def frontmatter_manifest(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "description": self.superpower,
            "public": True,
            "category": self.category,
            "tags": list(self.keywords[:4]),
            "preferred_models": [self.primary_model, self.fallback_model, self.local_only_model],
            "validation": list(self.validation_tools),
            "keywords": list(self.keywords),
            "file_globs": list(self.file_patterns),
            "task_types": _task_types_for_category(self.category),
            "complexity_threshold": self.complexity_threshold,
            "prompt_template": self.system_prompt(),
        }
        if self.notes:
            payload["notes"] = list(self.notes)
        return payload

    def system_prompt(self) -> str:
        persona = self.persona_blueprint()
        role = persona.role
        constraint_lines = CATEGORY_CONSTRAINTS[self.category] + list(self.custom_constraints)
        rendered_constraints = "\n".join(f"- {item}" for item in constraint_lines)
        rendered_context = "\n".join(f"- {item}" for item in self.required_context())
        rendered_avoid = "\n".join(f"- {item}" for item in self.avoid_when())
        rendered_deliverables = "\n".join(f"- {item}" for item in self.deliverables())
        rendered_workflow = "\n".join(f"{index}. {item}" for index, item in enumerate(self.workflow_steps(), start=1))
        rendered_validation = "\n".join(f"- Ensure `{tool}` passes or explain why it cannot run" for tool in self.validation_tools)
        rendered_traits = "\n".join(f"- {item}" for item in persona.traits)
        rendered_tone = "\n".join(f"- {item}" for item in persona.tone)
        return "\n".join(
            [
                f"You are a {role} with {persona.experience_years} years of experience specializing in {self.category} systems.",
                "",
                "## Persona",
                rendered_traits,
                "",
                "## Your Task",
                f"Use the supplied code, architecture, or product context to {self.superpower.lower()}",
                "Produce a bounded implementation plan or code-ready blueprint that another engineer or coding agent can execute safely.",
                "",
                "## Gather First",
                rendered_context,
                "",
                "## Communication",
                f"- Use a {persona.voice_style} communication style.",
                rendered_tone,
                "",
                "## Constraints",
                rendered_constraints,
                "- Return exact file or module targets when you recommend code changes.",
                "- Include rollback or containment guidance for risky changes.",
                "",
                "## Avoid",
                rendered_avoid,
                "",
                "## Workflow",
                rendered_workflow,
                "",
                "## Output Format",
                rendered_deliverables,
                "- Include the most likely failure modes, operator notes, and composition boundaries with adjacent systems or skills.",
                "",
                "## Validation Checklist",
                rendered_validation,
            ]
        )

    def marketplace_manifest(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "version": self.version,
            "category": self.category,
            "superpower": self.superpower,
            "persona": self.persona_manifest(),
            "voice": self.voice_manifest(),
            "thinking": self.thinking_manifest(),
            "response_format": self.response_format_manifest(),
            "system_prompt": self.system_prompt(),
            "trigger_conditions": {
                "file_patterns": list(self.file_patterns),
                "keywords": list(self.keywords),
                "complexity_threshold": self.complexity_threshold,
            },
            "model_preferences": {
                "primary": self.primary_model,
                "fallback": self.fallback_model,
                "local_only": self.local_only_model,
            },
            "validation_hooks": [
                {"tool": tool, "required": index == 0, "params": {}}
                for index, tool in enumerate(self.validation_tools)
            ],
            "metadata": {
                "author": "SkillForge contributors",
                "license": "MIT",
                "pricing_tier": "free",
                "language_support": CATEGORY_LANGUAGES[self.category],
                "featured": self.featured,
                "dependencies": [],
                "composition_notes": self.composition_notes(),
                "failure_modes": self.failure_modes(),
                "operational_notes": self.operational_notes(),
            },
        }

    def registry_manifest(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "slug": self.skill_id,
            "description": self.superpower,
            "public": True,
            "category": self.category,
            "tags": [self.category, *self.keywords[:3]],
            "preferred_models": [self.primary_model, self.fallback_model, self.local_only_model],
            "prompt_template": self.system_prompt(),
            "validation": list(self.validation_tools),
            "triggers": {
                "keywords": list(self.keywords),
                "file_globs": list(self.file_patterns),
                "task_types": _task_types_for_category(self.category),
            },
        }

    def portable_markdown(self) -> str:
        frontmatter = ["---", *_render_yaml(self.frontmatter_manifest()), "---"]
        validation_phrase = ", ".join(f"`{tool}`" for tool in self.validation_tools) if self.validation_tools else "validation hooks"
        persona = self.persona_blueprint()
        body = [
            f"# {self.name}",
            "",
            f"Superpower: {self.superpower}",
            "",
            "## Persona",
            f"- Role: `{persona.role}`",
            f"- Expertise: `{persona.expertise_level}` with `{persona.experience_years}` years of experience",
            *[f"- Trait: {item}" for item in persona.traits],
            *[f"- Specialization: {item}" for item in persona.specializations[:4]],
            "",
            "## Use this skill when",
            *[f"- The request signals `{item}` or an equivalent domain problem." for item in self.keywords[:4]],
            *[f"- The likely implementation surface includes `{pattern}`." for pattern in self.file_patterns[:3]],
            "",
            "## Do not use this skill when",
            *[f"- {item}" for item in self.avoid_when()],
            "",
            "## Inputs to gather first",
            *[f"- {item}" for item in self.required_context()],
            "",
            "## Recommended workflow",
            *[f"{index}. {step}" for index, step in enumerate(self.workflow_steps(), start=1)],
            "",
            "## Voice and tone",
            f"- Style: `{persona.voice_style}`",
            *[f"- Tone: {item}" for item in persona.tone],
            *[f"- Avoid: {item}" for item in persona.avoid],
            "",
            "## Thinking pattern",
            f"- Analysis approach: `{persona.analysis_approach}`",
            *[f"- {item}" for item in persona.reasoning_steps],
            *[f"- Verification: {item}" for item in persona.verification_checklist],
            "",
            "## Output contract",
            *[f"- {item}" for item in self.deliverables()],
            "",
            "## Response shape",
            *[f"- {item}" for item in persona.response_sections],
            "",
            "## Failure modes to watch",
            *[f"- {item}" for item in self.failure_modes()],
            "",
            "## Operational notes",
            *[f"- {item}" for item in self.operational_notes()],
            "",
            "## Dependency and composition notes",
            *[f"- {item}" for item in self.composition_notes()],
            "",
            "## Validation hooks",
            *[f"- `{tool}`" for tool in self.validation_tools],
            "",
            "## Model chain",
            f"- primary: `{self.primary_model}`",
            f"- fallback: `{self.fallback_model}`",
            f"- local: `{self.local_only_model}`",
            "",
            "## Handoff notes",
            f"- Treat `{validation_phrase}` as the minimum proof surface before calling the work complete.",
            "- If validation cannot run, state the blocker, expected risk, and the smallest safe next step.",
        ]
        if self.notes:
            body.extend(["", "Notes:", *[f"- {note}" for note in self.notes]])
        return "\n".join(frontmatter + body) + "\n"

    def readme_text(self) -> str:
        persona = self.persona_blueprint()
        lines = [
            f"# {self.name}",
            "",
            f"Category: `{self.category}`",
            f"Version: `{self.version}`",
            "",
            f"Superpower: {self.superpower}",
            "",
            "## Persona",
            f"- Role: `{persona.role}`",
            f"- Expertise: `{persona.expertise_level}` with `{persona.experience_years}` years of experience",
            *[f"- Trait: {item}" for item in persona.traits],
            *[f"- Specialization: {item}" for item in persona.specializations[:4]],
            "",
            "## Trigger signals",
            *[f"- `{item}`" for item in self.keywords],
            "",
            "## Best-fit files",
            *[f"- `{item}`" for item in self.file_patterns],
            "",
            "## Voice and tone",
            f"- Style: `{persona.voice_style}`",
            *[f"- Tone: {item}" for item in persona.tone],
            *[f"- Avoid: {item}" for item in persona.avoid],
            "",
            "## Thinking pattern",
            f"- Analysis approach: `{persona.analysis_approach}`",
            *[f"- {item}" for item in persona.reasoning_steps],
            *[f"- Verification: {item}" for item in persona.verification_checklist],
            "",
            "## Inputs to gather",
            *[f"- {item}" for item in self.required_context()],
            "",
            "## Recommended workflow",
            *[f"{index}. {step}" for index, step in enumerate(self.workflow_steps(), start=1)],
            "",
            "## Deliverables",
            *[f"- {item}" for item in self.deliverables()],
            "",
            "## Failure modes to watch",
            *[f"- {item}" for item in self.failure_modes()],
            "",
            "## Operational notes",
            *[f"- {item}" for item in self.operational_notes()],
            "",
            "## Dependency and composition notes",
            *[f"- {item}" for item in self.composition_notes()],
            "",
            "## Validation hooks",
            *[f"- `{item}`" for item in self.validation_tools],
            "",
            "## Model preferences",
            f"- primary: `{self.primary_model}`",
            f"- fallback: `{self.fallback_model}`",
            f"- local: `{self.local_only_model}`",
            "",
            "## Response shape",
            *[f"- {item}" for item in persona.response_sections],
            "",
            "## Pack contents",
            "- `SKILL.md` for portable agent-skill usage",
            "- `skill.yaml` for runtime registry loading",
            "- `marketplace.yaml` for catalog metadata and richer automation",
        ]
        if self.notes:
            lines.extend(["", "Notes:", *[f"- {note}" for note in self.notes]])
        return "\n".join(lines) + "\n"


def _task_types_for_category(category: str) -> list[str]:
    mapping = {
        "architecture": ["architecture", "reasoning", "review"],
        "frontend": ["code", "review", "visual"],
        "backend": ["code", "reasoning", "review"],
        "qa": ["review", "reasoning"],
        "devops": ["architecture", "review", "reasoning"],
        "security": ["review", "reasoning", "architecture"],
        "data": ["reasoning", "review", "architecture"],
        "product": ["visual", "review", "content"],
        "content": ["content", "review"],
        "business": ["reasoning", "content", "review"],
        "ai_ml": ["reasoning", "architecture", "review"],
    }
    return mapping[category]


def _yaml_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    if any(token in text for token in [":", "#", "[", "]"]) or text.strip() != text:
        return f'"{text}"'
    return text


def _render_yaml(value: object, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(_render_yaml(child, indent + 2))
            elif isinstance(child, str) and "\n" in child:
                lines.append(f"{prefix}{key}: |")
                lines.extend(f"{' ' * (indent + 2)}{line}" for line in child.splitlines())
            else:
                lines.append(f"{prefix}{key}: {_yaml_scalar(child)}")
        return lines
    if isinstance(value, list):
        lines = []
        for child in value:
            if isinstance(child, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(_render_yaml(child, indent + 2))
            elif isinstance(child, str) and "\n" in child:
                lines.append(f"{prefix}- |")
                lines.extend(f"{' ' * (indent + 2)}{line}" for line in child.splitlines())
            else:
                lines.append(f"{prefix}- {_yaml_scalar(child)}")
        return lines
    return [f"{prefix}{_yaml_scalar(value)}"]


def render_marketplace_yaml(skill: MarketplaceSkill) -> str:
    return "\n".join(_render_yaml(skill.marketplace_manifest())) + "\n"


def render_registry_yaml(skill: MarketplaceSkill) -> str:
    return "\n".join(_render_yaml(skill.registry_manifest())) + "\n"


def export_skill_pack(skill: MarketplaceSkill, destination_root: Path) -> Path:
    destination = destination_root / skill.skill_id
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "README.md").write_text(skill.readme_text(), encoding="utf-8")
    (destination / "SKILL.md").write_text(skill.portable_markdown(), encoding="utf-8")
    (destination / "skill.yaml").write_text(render_registry_yaml(skill), encoding="utf-8")
    (destination / "marketplace.yaml").write_text(render_marketplace_yaml(skill), encoding="utf-8")
    return destination


def list_marketplace_skills(category: str | None = None) -> list[MarketplaceSkill]:
    if category is None:
        return list(MARKETPLACE_SKILLS)
    return [skill for skill in MARKETPLACE_SKILLS if skill.category == category]


def get_marketplace_skill(skill_id: str) -> MarketplaceSkill | None:
    for skill in MARKETPLACE_SKILLS:
        if skill.skill_id == skill_id:
            return skill
    return None


def marketplace_summary() -> list[dict[str, Any]]:
    return [
        {
            "skill_id": skill.skill_id,
            "name": skill.name,
            "category": skill.category,
            "superpower": skill.superpower,
            "featured": skill.featured,
            "primary_model": skill.primary_model,
            "fallback_model": skill.fallback_model,
            "validation_tools": list(skill.validation_tools),
        }
        for skill in MARKETPLACE_SKILLS
    ]


def _skill(
    skill_id: str,
    name: str,
    category: str,
    superpower: str,
    file_patterns: list[str],
    keywords: list[str],
    primary_model: str,
    fallback_model: str,
    local_only_model: str,
    validation_tools: list[str],
    *,
    complexity_threshold: int = 7,
    featured: bool = False,
    notes: list[str] | None = None,
    custom_constraints: list[str] | None = None,
) -> MarketplaceSkill:
    return MarketplaceSkill(
        skill_id=skill_id,
        name=name,
        category=category,
        superpower=superpower,
        file_patterns=tuple(file_patterns),
        keywords=tuple(keywords),
        primary_model=primary_model,
        fallback_model=fallback_model,
        local_only_model=local_only_model,
        validation_tools=tuple(validation_tools),
        complexity_threshold=complexity_threshold,
        featured=featured,
        notes=tuple(notes or []),
        custom_constraints=tuple(custom_constraints or []),
    )


MARKETPLACE_SKILLS = [
    _skill("micro-frontend-orchestrator", "Micro-Frontend Orchestrator", "architecture", "Decompose monolithic frontend systems into deployable micro-frontends without breaking route contracts or shared state.", ["**/*.tsx", "**/vite.config.*", "**/webpack*.js"], ["micro frontend", "module federation", "route integrity"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["audit_bundle_size", "verify_route_integrity"]),
    _skill("event-sourcing-architect", "Event-Sourcing Architect", "architecture", "Transform CRUD-heavy state flows into event-sourced patterns with replayability and time-travel debugging.", ["**/*store*.ts", "**/*redux*.ts", "**/*zustand*.ts"], ["event sourcing", "redux", "zustand"], "moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "deepseek-r1:32b", ["verify_state_consistency"]),
    _skill("database-per-tenant-designer", "Database-Per-Tenant Designer", "architecture", "Blueprint multi-tenant database isolation, row-level security, and connection pooling without breaking tenant routing.", ["**/schema.prisma", "**/*.sql", "**/supabase/**"], ["multi tenant", "tenant_id", "row level security"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["audit_rls_policies"]),
    _skill("circuit-breaker-weaver", "Circuit-Breaker Weaver", "architecture", "Wrap external API calls with circuit breakers, retries, fallbacks, and backoff while preserving business logic shape.", ["**/*.ts", "**/*.py", "**/api/**"], ["circuit breaker", "retry", "backoff"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_error_handling"]),
    _skill("cqrs-pattern-synthesizer", "CQRS Pattern Synthesizer", "architecture", "Separate read and write models into typed CQRS flows with query optimization and command safety.", ["**/*.ts", "**/*.tsx", "**/schema*.ts"], ["cqrs", "command handler", "query model"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_type_consistency"]),
    _skill("real-time-sync-engineer", "Real-Time Sync Engineer", "architecture", "Add optimistic UI, sync reconciliation, and offline-safe conflict handling to collaborative product flows.", ["**/*.tsx", "**/*realtime*.ts", "**/*socket*.ts"], ["realtime", "optimistic ui", "conflict resolution"], "moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["verify_offline_behavior"]),
    _skill("serverless-cost-optimizer", "Serverless Cost Optimizer", "architecture", "Split long-running serverless logic into edge-safe, cold-start-aware execution paths with lower runtime cost.", ["**/api/**/*.ts", "**/*.lambda.*", "**/functions/**"], ["serverless cost", "cold start", "lambda"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "qwen2.5-coder:32b", ["audit_cold_start_metrics"]),
    _skill("graphql-federation-gateway", "GraphQL Federation Gateway", "architecture", "Merge multiple GraphQL schemas into a stitched or federated gateway with conflict detection and safe ownership boundaries.", ["**/*.graphql", "**/schema*.ts", "**/apollo*.ts"], ["graphql federation", "schema stitching", "apollo"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_schema_conflicts"]),
    _skill("feature-flag-architect", "Feature-Flag Architect", "architecture", "Introduce feature-flag systems with kill switches, experiment hooks, and isolated rollout boundaries.", ["**/*.ts", "**/*.tsx", "**/.env*"], ["feature flag", "kill switch", "ab test"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_flag_isolation"]),
    _skill("data-migration-blueprinter", "Data Migration Blueprinter", "architecture", "Design zero-downtime data migrations with rollback choreography, phased reads, and production-safe cutovers.", ["**/migrations/**", "**/schema.prisma", "**/*.sql"], ["data migration", "rollback", "zero downtime"], "moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "deepseek-r1:32b", ["verify_migration_safety"]),
    _skill("liquid-glass-enforcer", "Liquid Glass Enforcer", "frontend", "Transform generic Tailwind into high-end glassmorphism with safe blur budgets, atmospheric depth, and performance-aware motion.", ["**/*.tsx", "**/*.css", "**/tailwind.config.*"], ["glassmorphism", "backdrop blur", "liquid glass"], "moonshotai/kimi-k2.5", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["audit_design_compliance"], featured=True, custom_constraints=["Never use em-dashes in generated code or comments.", "Keep motion 60fps friendly by preferring transform and opacity."]),
    _skill("animation-budget-guardian", "Animation Budget Guardian", "frontend", "Replace heavy JavaScript-driven motion with lighter alternatives when animation polish is hurting bundle size or runtime cost.", ["**/*.tsx", "**/*.css", "**/*motion*.ts"], ["framer motion", "bundle budget", "animation"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "qwen2.5-coder:32b", ["audit_bundle_size"]),
    _skill("accessible-motion-designer", "Accessible Motion Designer", "frontend", "Create cinematic motion systems with reduced-motion fallbacks, semantic announcements, and inclusive scroll choreography.", ["**/*.tsx", "**/*.css", "**/*scroll*.ts"], ["reduced motion", "scroll animation", "accessibility"], "moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["audit_accessibility_compliance"]),
    _skill("bilingual-content-sync", "Bilingual Content Sync", "frontend", "Maintain product and UI parity across languages while adapting tone and cultural context beyond literal translation.", ["**/locales/**/*.json", "**/i18n/**", "**/*.tsx"], ["i18n", "translation parity", "localized copy"], "meta/llama-3.3-70b-instruct", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_translation_coverage"]),
    _skill("design-token-synchronizer", "Design Token Synchronizer", "frontend", "Sync design tokens into code systems with theme-aware mappings, utility classes, and drift resistance.", ["**/tailwind.config.*", "**/tokens/**", "**/*.css"], ["design tokens", "tailwind config", "figma variables"], "gemini-2.5-pro", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_token_consistency"]),
    _skill("component-composition-optimizer", "Component Composition Optimizer", "frontend", "Refactor prop-heavy React trees into compound components and cleaner composition APIs with stronger inference.", ["**/*.tsx", "**/*.ts"], ["prop drilling", "compound component", "react props"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_type_safety"]),
    _skill("image-optimization-pipeline", "Image Optimization Pipeline", "frontend", "Replace naive image usage with responsive pipelines, better formats, and perceptual loading strategies.", ["**/*.tsx", "**/*.jsx", "**/assets/**"], ["image optimization", "next image", "srcset"], "qwen3-coder:480b-cloud", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["audit_lighthouse_score"]),
    _skill("form-validation-architect", "Form Validation Architect", "frontend", "Unify form UX around typed schemas, accessible feedback, and i18n-aware validation contracts.", ["**/*form*.tsx", "**/*.ts", "**/schema*.ts"], ["zod", "react hook form", "validation"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_accessibility_labels"]),
    _skill("error-boundary-weaver", "Error Boundary Weaver", "frontend", "Wrap interface trees with resilient error boundaries, fallback recovery, and observability-friendly failure paths.", ["**/*.tsx", "**/routes/**", "**/pages/**"], ["error boundary", "fallback ui", "sentry"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_error_reporting"]),
    _skill("virtual-scrolling-calibrator", "Virtual Scrolling Calibrator", "frontend", "Introduce high-volume list rendering with dynamic height support and smooth scrolling under real data load.", ["**/*.tsx", "**/*list*.tsx"], ["virtual list", "windowing", "large list"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["audit_render_performance"]),
    _skill("keyboard-navigation-engineer", "Keyboard Navigation Engineer", "frontend", "Add keyboard-first control systems with focus traps, jump shortcuts, and SPA navigation semantics.", ["**/*.tsx", "**/*.ts"], ["keyboard navigation", "focus trap", "shortcut"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "qwen2.5-coder:32b", ["audit_keyboard_accessibility"]),
    _skill("svg-icon-system-builder", "SVG Icon System Builder", "frontend", "Convert loose SVG collections into typed icon systems with sprite optimization and reliable naming.", ["**/*.svg", "**/icons/**", "**/*.tsx"], ["svg sprite", "icon system", "typed icons"], "meta/llama-3.3-70b-instruct", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_type_coverage"]),
    _skill("ssg-island-architect", "SSG Island Architect", "frontend", "Identify interactive islands in otherwise static pages and hydrate only what truly needs runtime code.", ["**/*.astro", "**/*.tsx", "**/pages/**"], ["islands architecture", "partial hydration", "ssg"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_hydration_bundles"]),
    _skill("css-container-query-migrator", "CSS Container Query Migrator", "frontend", "Move responsive logic from page-level breakpoints into component-level container queries without regressions.", ["**/*.css", "**/*.scss", "**/*.tsx"], ["container query", "responsive component", "media query"], "qwen3-coder:480b-cloud", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["verify_responsive_behavior"]),
    _skill("web-vitals-interventionist", "Web Vitals Interventionist", "frontend", "Diagnose and fix CLS, LCP, and interaction regressions with concrete code changes instead of generic advice.", ["**/*.tsx", "**/*.ts", "**/web-vitals.*"], ["core web vitals", "cls", "lcp"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "qwen2.5-coder:32b", ["audit_core_web_vitals"]),
    _skill("api-versioning-strategist", "API Versioning Strategist", "backend", "Introduce safe API versioning with compatibility lanes, deprecation notices, and migration guidance.", ["**/api/**", "**/routes/**", "**/*.ts"], ["api versioning", "backward compatibility", "deprecation"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_backward_compatibility"]),
    _skill("rate-limiting-architect", "Rate-Limiting Architect", "backend", "Implement distributed rate limiting with token buckets, predictable headers, and production-safe behavior under load.", ["**/api/**", "**/middleware/**", "**/*.ts"], ["rate limit", "token bucket", "redis"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_rate_limit_headers"]),
    _skill("webhook-security-designer", "Webhook Security Designer", "backend", "Harden webhook handlers with signature verification, replay prevention, and idempotency discipline.", ["**/*webhook*.ts", "**/*webhook*.py"], ["webhook", "signature verification", "replay attack"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_webhook_security"]),
    _skill("jwt-rotation-engineer", "JWT Rotation Engineer", "backend", "Modernize session flows with rotating refresh tokens, revocation, and secure cookie handling.", ["**/auth/**", "**/*.ts", "**/*.py"], ["jwt", "refresh token", "httpOnly cookie"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_token_security"]),
    _skill("idempotency-guardian", "Idempotency Guardian", "backend", "Make mutation endpoints safely retryable with idempotency keys and conflict-aware persistence patterns.", ["**/api/**", "**/payments/**", "**/*.ts"], ["idempotency", "safe retries", "mutation api"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_idempotency_guarantees"]),
    _skill("api-pagination-architect", "API Pagination Architect", "backend", "Replace offset-heavy APIs with cursor pagination that scales cleanly and remains client-friendly.", ["**/api/**", "**/*.sql", "**/*.ts"], ["cursor pagination", "list endpoint", "link headers"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_pagination_performance"]),
    _skill("graphql-query-complexity-guard", "GraphQL Query Complexity Guard", "backend", "Protect GraphQL services from expensive queries with depth, complexity, and resource-aware limits.", ["**/*.graphql", "**/apollo*.ts", "**/graphql/**"], ["graphql complexity", "query depth", "dos protection"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_query_limits"]),
    _skill("openapi-spec-generator", "OpenAPI Spec Generator", "backend", "Generate OpenAPI documentation from typed routes and schemas without drifting from implementation.", ["**/routes/**", "**/schema*.ts", "**/*.py"], ["openapi", "zod schema", "api docs"], "qwen3-coder:480b-cloud", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["verify_spec_completeness"]),
    _skill("api-test-contract-enforcer", "API Test Contract Enforcer", "backend", "Set up contract testing so API consumers and providers fail safely before incompatible releases ship.", ["**/tests/**", "**/api/**", "**/*.ts"], ["contract test", "pact", "consumer provider"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_contract_compliance"]),
    _skill("event-driven-sync-engine", "Event-Driven Sync Engine", "backend", "Introduce outbox-driven cross-service communication with reliable publication and eventual consistency safeguards.", ["**/queue/**", "**/events/**", "**/*.ts"], ["outbox pattern", "event driven", "eventual consistency"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_eventual_consistency"]),
    _skill("api-deprecation-strategist", "API Deprecation Strategist", "backend", "Sunset APIs with clear migration windows, explicit headers, and communication paths that reduce client breakage.", ["**/api/**", "**/*.md", "**/*.ts"], ["api deprecation", "sunset header", "migration window"], "meta/llama-3.3-70b-instruct", "deepseek-ai/deepseek-v3.2", "llama3.1:8b", ["verify_deprecation_notices"]),
    _skill("server-timing-analyzer", "Server Timing Analyzer", "backend", "Expose backend bottlenecks through Server-Timing instrumentation that separates compute, database, and remote call cost.", ["**/middleware/**", "**/api/**", "**/*.ts"], ["server timing", "performance header", "latency breakdown"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_timing_accuracy"]),
    _skill("flaky-test-detective", "Flaky Test Detective", "qa", "Identify and stabilize non-deterministic tests through reproduction heuristics, isolation, and dependency analysis.", ["**/tests/**", "**/*.spec.*", "**/*.test.*"], ["flaky test", "retry", "nondeterministic"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_test_stability"]),
    _skill("visual-regression-architect", "Visual Regression Architect", "qa", "Set up screenshot-based UI regression pipelines that catch real layout and styling breakage without noise.", ["**/*.tsx", "**/playwright*.ts", "**/storybook/**"], ["visual regression", "playwright", "chromatic"], "moonshotai/kimi-k2.5", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_screenshot_consistency"]),
    _skill("mutation-testing-agent", "Mutation Testing Agent", "qa", "Challenge test suites with synthetic code mutations to measure whether tests actually protect behavior.", ["**/tests/**", "**/*.ts", "**/*.py"], ["mutation testing", "test effectiveness", "coverage"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_mutation_score"]),
    _skill("e2e-data-seeder", "E2E Data Seeder", "qa", "Generate realistic, relationally valid test data for end-to-end workflows without brittle manual setup.", ["**/tests/**", "**/seed*.ts", "**/fixtures/**"], ["e2e seed", "test data", "fixtures"], "meta/llama-3.3-70b-instruct", "deepseek-ai/deepseek-v3.2", "llama3.1:8b", ["verify_data_consistency"]),
    _skill("performance-regression-guard", "Performance Regression Guard", "qa", "Enforce performance budgets in CI so regressions are blocked before they become user-visible.", ["**/.github/workflows/**", "**/lighthouse*.js", "**/package.json"], ["lighthouse ci", "performance budget", "regression"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["audit_lighthouse_score"]),
    _skill("accessibility-auditor-pro", "Accessibility Auditor Pro", "qa", "Audit interface flows against WCAG 2.2 AA with both automated checks and human-readable remediation sequences.", ["**/*.tsx", "**/*.html", "**/pages/**"], ["wcag", "axe", "accessibility audit"], "moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["audit_wcag_compliance"]),
    _skill("security-scan-automator", "Security Scan Automator", "qa", "Wire security scanning into delivery workflows with exploitability-aware prioritization instead of raw alert floods.", ["**/package.json", "**/.github/workflows/**", "**/requirements*.txt"], ["snyk", "dependabot", "security scan"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_vulnerability_removal"]),
    _skill("api-fuzzing-strategist", "API Fuzzing Strategist", "qa", "Build property-based and boundary-oriented API tests that find input handling failures before attackers or customers do.", ["**/api/**", "**/tests/**", "**/*.ts"], ["api fuzzing", "property based", "boundary values"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_boundary_coverage"]),
    _skill("load-test-calibrator", "Load Test Calibrator", "qa", "Design realistic load scenarios with useful bottleneck signals rather than synthetic throughput vanity metrics.", ["**/api/**", "**/k6/**", "**/artillery/**"], ["load test", "k6", "traffic simulation"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_load_thresholds"]),
    _skill("dead-code-eliminator", "Dead Code Eliminator", "qa", "Find and remove unused code paths, exports, and stale branches that still carry maintenance cost and risk.", ["**/*.ts", "**/*.tsx", "**/*.py"], ["dead code", "unused exports", "bundle cleanup"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_bundle_reduction"]),
    _skill("terraform-module-architect", "Terraform Module Architect", "devops", "Refactor ad hoc infrastructure into reusable, environment-safe Terraform modules with clean variable boundaries.", ["**/*.tf", "**/*.tfvars"], ["terraform module", "iac", "environment overlay"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_terraform_plan"]),
    _skill("github-actions-optimizer", "GitHub Actions Optimizer", "devops", "Reduce CI waste through caching, parallelism, and smarter workflow conditions without losing signal quality.", ["**/.github/workflows/*.yml", "**/.github/workflows/*.yaml"], ["github actions", "ci cache", "workflow optimization"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_ci_duration"]),
    _skill("docker-layer-optimizer", "Docker Layer Optimizer", "devops", "Shrink container builds and speed up rebuilds through smarter layer ordering and multi-stage decomposition.", ["**/Dockerfile*", "**/.dockerignore"], ["docker layer", "multi stage", "image size"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_image_size"]),
    _skill("kubernetes-manifest-weaver", "Kubernetes Manifest Weaver", "devops", "Compose Kubernetes manifests with overlays, health checks, and safer secret boundaries across environments.", ["**/*.yaml", "**/*.yml", "**/k8s/**"], ["kubernetes", "kustomize", "health check"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_manifest_validity"]),
    _skill("env-secret-rotator", "Env Secret Rotator", "devops", "Plan and stage zero-downtime secret rotation across services that currently share brittle static credentials.", ["**/.env*", "**/*.yaml", "**/*.ts"], ["secret rotation", "key rollover", "credential refresh"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_rotation_safety"]),
    _skill("log-aggregation-architect", "Log Aggregation Architect", "devops", "Turn ad hoc logs into structured, correlated observability streams with request and trace identity built in.", ["**/*.ts", "**/*.py", "**/middleware/**"], ["structured logging", "correlation id", "log aggregation"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_log_parsing"]),
    _skill("blue-green-deployer", "Blue-Green Deployer", "devops", "Automate safer production rollouts with health-aware promotion and rollback triggers.", ["**/*.yaml", "**/deploy/**", "**/.github/workflows/**"], ["blue green", "deployment rollback", "release health"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_deployment_health"]),
    _skill("cost-allocation-tagging", "Cost Allocation Tagging", "devops", "Standardize cloud tagging so spend can be attributed cleanly across teams, services, and environments.", ["**/*.tf", "**/*.yaml", "**/cloud/**"], ["cost allocation", "tagging", "billing"], "meta/llama-3.3-70b-instruct", "deepseek-ai/deepseek-v3.2", "llama3.1:8b", ["verify_tag_coverage"]),
    _skill("disaster-recovery-planner", "Disaster Recovery Planner", "devops", "Define realistic recovery objectives, backup validation, and operator runbooks for critical systems.", ["**/*.md", "**/infra/**", "**/backup/**"], ["disaster recovery", "rto", "rpo"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_recovery_procedures"]),
    _skill("observability-dashboard-synthesizer", "Observability Dashboard Synthesizer", "devops", "Build SLO-aware dashboards and alerts that reveal burn rate, not just raw telemetry volume.", ["**/*.json", "**/grafana/**", "**/datadog/**"], ["slo", "burn rate", "dashboard"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_alert_thresholds"]),
    _skill("gdpr-by-design-architect", "GDPR-by-Design Architect", "security", "Embed privacy-first product patterns with data minimization, retention controls, and defensible deletion workflows.", ["**/*.ts", "**/*.sql", "**/privacy/**"], ["gdpr", "pii", "data retention"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["audit_gdpr_compliance"], featured=True),
    _skill("owasp-top-10-guardian", "OWASP Top 10 Guardian", "security", "Systematically surface high-probability application security weaknesses across common OWASP failure modes.", ["**/*.ts", "**/*.py", "**/api/**"], ["owasp", "xss", "csrf"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_owasp_compliance"]),
    _skill("dependency-supply-chain-auditor", "Dependency Supply Chain Auditor", "security", "Audit dependencies for typosquatting, licensing risk, and supply-chain fragility before they hit production.", ["**/package.json", "**/pnpm-lock.yaml", "**/requirements*.txt"], ["sbom", "supply chain", "license compliance"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "llama3.1:8b", ["verify_supply_chain_safety"]),
    _skill("secrets-scanning-automator", "Secrets Scanning Automator", "security", "Wire secret-detection into local and CI workflows so leaks are stopped before they become incidents.", ["**/.git/hooks/**", "**/.github/workflows/**", "**/*.sh"], ["secret scan", "pre commit", "credential leak"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_secret_detection"]),
    _skill("cors-policy-hardening", "CORS Policy Hardening", "security", "Tighten cross-origin boundaries without silently breaking legitimate credentialed traffic.", ["**/api/**", "**/*.ts", "**/*.py"], ["cors", "origin allowlist", "credentials"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_cors_strictness"]),
    _skill("content-security-policy-architect", "Content Security Policy Architect", "security", "Design nonce- and policy-based browser defenses that meaningfully shrink XSS blast radius.", ["**/*.ts", "**/*.html", "**/headers/**"], ["content security policy", "nonce", "strict dynamic"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_csp_enforcement"]),
    _skill("soc2-control-documenter", "SOC2 Control Documenter", "security", "Translate operating practices into audit-friendly SOC 2 evidence maps with technical verification hooks.", ["**/*.md", "**/policies/**", "**/controls/**"], ["soc2", "control evidence", "audit"], "meta/llama-3.3-70b-instruct", "deepseek-ai/deepseek-v3.2", "llama3.1:8b", ["verify_control_effectiveness"]),
    _skill("vulnerability-patch-prioritizer", "Vulnerability Patch Prioritizer", "security", "Rank vulnerability work by exploitability and business impact instead of raw advisory volume.", ["**/package.json", "**/requirements*.txt", "**/*.md"], ["cvss", "patch prioritization", "security advisory"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_patch_urgency"]),
    _skill("zero-trust-network-designer", "Zero-Trust Network Designer", "security", "Design service-to-service trust boundaries with strong identity, policy, and transport guarantees.", ["**/*.yaml", "**/network/**", "**/infra/**"], ["zero trust", "mtls", "service mesh"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_zero_trust_policies"]),
    _skill("audit-log-immutability-guardian", "Audit Log Immutability Guardian", "security", "Protect critical audit trails against tampering with append-only integrity and verification strategies.", ["**/*.ts", "**/*.py", "**/audit/**"], ["audit log", "immutability", "worm"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_log_integrity"]),
    _skill("data-warehouse-modeler", "Data Warehouse Modeler", "data", "Shape analytics data into warehouse models that remain queryable, explainable, and maintainable as the product grows.", ["**/*.sql", "**/dbt/**", "**/warehouse/**"], ["star schema", "warehouse model", "dimensions"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_query_performance"]),
    _skill("real-time-analytics-pipeline", "Real-Time Analytics Pipeline", "data", "Build sub-second analytics pipelines over streaming events without turning the system into an operational mystery.", ["**/*.sql", "**/stream/**", "**/analytics/**"], ["real time analytics", "clickhouse", "streaming"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_latency_metrics"]),
    _skill("data-quality-sentinel", "Data Quality Sentinel", "data", "Instrument data pipelines with freshness, completeness, and anomaly detection checks that fail usefully.", ["**/*.py", "**/etl/**", "**/dbt/**"], ["great expectations", "data quality", "anomaly detection"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_data_freshness"]),
    _skill("funnel-conversion-analyst", "Funnel Conversion Analyst", "data", "Design product event funnels that reveal meaningful drop-off and activation patterns instead of vanity charts.", ["**/*.sql", "**/analytics/**", "**/*.ts"], ["funnel analysis", "conversion", "event tracking"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_tracking_accuracy"]),
    _skill("cohort-retention-engineer", "Cohort Retention Engineer", "data", "Build cohort retention logic and churn views that survive product evolution and messy subscription edge cases.", ["**/*.sql", "**/analytics/**", "**/*.py"], ["cohort", "retention", "churn"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_retention_calculation"]),
    _skill("privacy-preserving-analytics", "Privacy-Preserving Analytics", "data", "Design analytics flows that preserve useful product insight while reducing privacy and re-identification risk.", ["**/*.sql", "**/analytics/**", "**/*.py"], ["differential privacy", "k anonymity", "privacy analytics"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_privacy_guarantees"]),
    _skill("feature-store-architect", "Feature Store Architect", "data", "Organize machine-learning features so online and offline use stay aligned under evolving training pipelines.", ["**/*.py", "**/features/**", "**/*.sql"], ["feature store", "online offline consistency", "ml features"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_feature_consistency"]),
    _skill("experimentation-platform-builder", "Experimentation Platform Builder", "data", "Design trustworthy experimentation infrastructure with sound randomization, sizing, and interpretation defaults.", ["**/*.ts", "**/*.py", "**/experiments/**"], ["ab test", "experimentation", "sample size"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "deepseek-r1:32b", ["verify_statistical_validity"]),
    _skill("onboarding-flow-optimizer", "Onboarding Flow Optimizer", "product", "Reshape onboarding sequences around progressive disclosure and measurable activation rather than generic first-run screens.", ["**/*.tsx", "**/pages/**", "**/analytics/**"], ["onboarding", "activation", "drop off"], "moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["verify_conversion_rates"]),
    _skill("empty-state-storyteller", "Empty State Storyteller", "product", "Turn empty and null states into contextual guidance that helps users reach value instead of dead ends.", ["**/*.tsx", "**/*.md", "**/components/**"], ["empty state", "cta", "null state"], "meta/llama-3.3-70b-instruct", "moonshotai/kimi-k2.5", "llama3.1:8b", ["verify_engagement_metrics"]),
    _skill("error-message-humanizer", "Error Message Humanizer", "product", "Translate raw technical failures into useful user guidance with recovery paths and better emotional tone.", ["**/*.tsx", "**/*.ts", "**/errors/**"], ["error message", "recovery", "ux writing"], "meta/llama-3.3-70b-instruct", "deepseek-ai/deepseek-v3.2", "llama3.1:8b", ["verify_error_recovery_rates"]),
    _skill("accessibility-first-navigator", "Accessibility-First Navigator", "product", "Make site and app navigation work cleanly for keyboard and screen-reader users without feeling like a compliance add-on.", ["**/*.tsx", "**/navigation/**", "**/*.html"], ["screen reader", "skip link", "navigation accessibility"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "qwen2.5-coder:32b", ["audit_screen_reader_compatibility"]),
    _skill("mobile-first-gestures", "Mobile-First Gestures", "product", "Add touch-native interaction patterns that feel intentional on mobile without degrading desktop predictability.", ["**/*.tsx", "**/*.ts", "**/mobile/**"], ["swipe", "pinch", "touch gesture"], "moonshotai/kimi-k2.5", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_touch_responsiveness"]),
    _skill("dark-mode-architect", "Dark Mode Architect", "product", "Implement theme systems with contrast safety, system preference support, and smooth state transitions.", ["**/*.tsx", "**/*.css", "**/theme/**"], ["dark mode", "theme toggle", "color contrast"], "qwen3-coder:480b-cloud", "moonshotai/kimi-k2.5", "qwen2.5-coder:32b", ["verify_color_contrast"]),
    _skill("microcopy-voice-tuner", "Microcopy Voice Tuner", "product", "Tune interface microcopy to a consistent brand voice that still remains clear in stressful product moments.", ["**/*.tsx", "**/*.md", "**/copy/**"], ["microcopy", "brand voice", "ui text"], "meta/llama-3.3-70b-instruct", "gemini-2.5-flash", "llama3.1:8b", ["verify_brand_consistency"]),
    _skill("progressive-web-app-builder", "Progressive Web App Builder", "product", "Turn web apps into credible installable experiences with offline paths, service workers, and install UX that makes sense.", ["**/manifest*.json", "**/service-worker*.js", "**/*.tsx"], ["pwa", "service worker", "install prompt"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_pwa_compliance"]),
    _skill("notification-strategy-designer", "Notification Strategy Designer", "product", "Design notification systems that protect user trust through timing, relevance, and opt-out sensitivity.", ["**/*.ts", "**/*.tsx", "**/notifications/**"], ["push notification", "permission priming", "engagement"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "llama3.1:8b", ["verify_opt_out_rates"]),
    _skill("search-ux-optimizer", "Search UX Optimizer", "product", "Upgrade search flows with better query assistance, faceting, and success analytics instead of a bare input box.", ["**/*.tsx", "**/search/**", "**/*.ts"], ["autocomplete", "faceted search", "search analytics"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "qwen2.5-coder:32b", ["verify_search_success_rates"]),
    _skill("technical-documentation-weaver", "Technical Documentation Weaver", "content", "Transform technical knowledge into maintainable docs with runnable examples and structure that scales.", ["**/*.md", "**/docs/**", "**/*.mdx"], ["technical docs", "mdx", "versioned docs"], "meta/llama-3.3-70b-instruct", "qwen3-coder:480b-cloud", "llama3.1:8b", ["verify_doc_completeness"]),
    _skill("changelog-curator", "Changelog Curator", "content", "Turn raw git history into useful changelogs that describe real user impact instead of noisy implementation trivia.", ["**/.git/**", "**/*.md"], ["changelog", "release notes", "conventional commits"], "meta/llama-3.3-70b-instruct", "deepseek-ai/deepseek-v3.2", "llama3.1:8b", ["verify_changelog_accuracy"]),
    _skill("grant-proposal-architect", "Grant Proposal Architect", "content", "Shape technical project narratives into funder-ready proposals with budget logic, impact framing, and realistic milestones.", ["**/*.md", "**/proposals/**", "**/budget/**"], ["grant proposal", "budget justification", "impact"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "llama3.1:8b", ["verify_funder_compliance"], featured=True, notes=["Treat output as strategic drafting support, not guaranteed submission advice."]),
    _skill("api-documentation-generator", "API Documentation Generator", "content", "Turn API implementation detail into example-rich docs that developers can actually use without reading source first.", ["**/api/**", "**/*.md", "**/*.yaml"], ["api documentation", "openapi docs", "examples"], "qwen3-coder:480b-cloud", "meta/llama-3.3-70b-instruct", "qwen2.5-coder:32b", ["verify_example_accuracy"]),
    _skill("incident-communication-drafter", "Incident Communication Drafter", "content", "Draft incident updates that are honest, appropriately scoped, and useful to both operators and stakeholders.", ["**/*.md", "**/status/**", "**/incidents/**"], ["incident update", "status page", "severity"], "meta/llama-3.3-70b-instruct", "deepseek-ai/deepseek-v3.2", "llama3.1:8b", ["verify_communication_clarity"]),
    _skill("open-source-maintainer-assistant", "Open-Source Maintainer Assistant", "content", "Improve maintainer throughput with issue triage, contributor onboarding, and review-ready response scaffolds.", ["**/.github/**", "**/*.md"], ["issue triage", "maintainer", "contributor onboarding"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "llama3.1:8b", ["verify_response_time"]),
    _skill("bilingual-seo-architect", "Bilingual SEO Architect", "content", "Build multi-language SEO signals that preserve indexing quality across localized experiences.", ["**/*.tsx", "**/locales/**", "**/sitemap*.xml"], ["hreflang", "localized seo", "meta tags"], "deepseek-ai/deepseek-v3.2", "qwen3-coder:480b-cloud", "qwen2.5-coder:32b", ["verify_seo_coverage"]),
    _skill("video-script-technical-writer", "Video Script Technical Writer", "content", "Turn product and code explanations into structured tutorial scripts with stronger pacing and teaching clarity.", ["**/*.md", "**/docs/**", "**/scripts/**"], ["tutorial video", "technical script", "walkthrough"], "meta/llama-3.3-70b-instruct", "moonshotai/kimi-k2.5", "llama3.1:8b", ["verify_engagement_retention"]),
    _skill("burn-rate-calculator", "Burn-Rate Calculator", "business", "Model runway, scenario changes, and hiring tradeoffs so founders can make clearer operational decisions.", ["**/*.csv", "**/*.md", "**/finance/**"], ["burn rate", "runway", "scenario model"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "deepseek-r1:32b", ["verify_calculation_accuracy"]),
    _skill("safe-note-documenter", "SAFE Note Documenter", "business", "Draft founder-readable SAFE note materials that explain caps, dilution tradeoffs, and investor-facing structure clearly.", ["**/*.md", "**/fundraising/**"], ["safe note", "valuation cap", "fundraising"], "meta/llama-3.3-70b-instruct", "deepseek-ai/deepseek-v3.2", "llama3.1:8b", ["verify_legal_compliance"], notes=["Not legal advice. Validate all output with qualified counsel."]),
    _skill("competitive-intelligence-analyst", "Competitive Intelligence Analyst", "business", "Compare product positioning, pricing, and capability gaps to sharpen strategic differentiation.", ["**/*.md", "**/research/**", "**/*.csv"], ["competitive analysis", "pricing comparison", "feature matrix"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "deepseek-r1:32b", ["verify_data_sources"]),
    _skill("customer-health-scorer", "Customer Health Scorer", "business", "Build practical B2B health scoring from usage, support, and churn signals without magical black-box metrics.", ["**/*.sql", "**/*.csv", "**/crm/**"], ["customer health", "churn risk", "b2b saas"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "deepseek-r1:32b", ["verify_prediction_accuracy"]),
    _skill("ip-strategy-documenter", "IP Strategy Documenter", "business", "Clarify license compatibility, contributor rights, and IP exposure before technical releases or diligence.", ["**/LICENSE*", "**/*.md", "**/.github/**"], ["license compatibility", "cla", "ip strategy"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "deepseek-r1:32b", ["verify_license_compliance"]),
    _skill("technical-debt-banker", "Technical Debt Banker", "business", "Quantify technical debt like a portfolio with interest, payoff order, and tradeoffs against feature delivery.", ["**/*.ts", "**/*.py", "**/*.md"], ["technical debt", "refactor priority", "engineering economics"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["verify_debt_metrics"]),
    _skill("exit-readiness-assessor", "Exit Readiness Assessor", "business", "Prepare product and engineering organizations for diligence with clear document, IP, and system readiness checklists.", ["**/*.md", "**/legal/**", "**/infra/**"], ["due diligence", "acquisition prep", "exit readiness"], "deepseek-ai/deepseek-v3.2", "meta/llama-3.3-70b-instruct", "deepseek-r1:32b", ["verify_completeness"]),
    _skill("prompt-engineering-architect", "Prompt Engineering Architect", "ai_ml", "Design system prompts, prompt contracts, and eval-backed example sets that improve LLM reliability without hiding failure modes.", ["**/*.py", "**/*.ts", "**/*.yaml", "**/*.json", "**/prompts/**"], ["system prompt", "few shot", "prompt contract"], "moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["prompt-performance-checker", "output-consistency-validator", "token-usage-optimizer"]),
    _skill("llm-integration-specialist", "LLM Integration Specialist", "ai_ml", "Integrate hosted and local LLM providers with fallback, rate limiting, and spend-aware routing that remains debuggable in production.", ["**/*.py", "**/*.ts", "**/*.js", "**/providers/**", "**/models/**"], ["llm integration", "provider fallback", "completion api"], "deepseek-ai/deepseek-v3.2", "gemini-2.5-pro", "qwen2.5-coder:32b", ["api-reliability-checker", "fallback-strategy-validator", "cost-tracking-verifier"]),
    _skill("embedding-pipeline-designer", "Embedding Pipeline Designer", "ai_ml", "Build embedding pipelines with retrieval-aware chunking, vector index strategy, and similarity quality that can be measured.", ["**/*.py", "**/*.ts", "**/embeddings/**", "**/vector/**"], ["embedding", "vector db", "semantic search"], "deepseek-ai/deepseek-v3.2", "gemini-2.5-pro", "qwen2.5-coder:32b", ["embedding-quality-checker", "vector-db-validator", "search-accuracy-test"]),
    _skill("fine-tuning-workflow-creator", "Fine-Tuning Workflow Creator", "ai_ml", "Create fine-tuning workflows with dataset preparation, evaluation baselines, and rollback-ready deployment checkpoints.", ["**/*.py", "**/*.ipynb", "**/*.yaml", "**/training/**"], ["fine tuning", "training loop", "evaluation set"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["data-quality-checker", "training-convergence-validator", "evaluation-metrics-verifier"], complexity_threshold=8),
    _skill("rag-system-architect", "RAG System Architect", "ai_ml", "Design retrieval-augmented generation systems with chunking, ranking, citation, and context-budget discipline that hold up in production.", ["**/*.py", "**/*.ts", "**/rag/**", "**/retrieval/**"], ["rag", "retrieval", "context injection"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "qwen2.5-coder:32b", ["retrieval-accuracy-checker", "chunking-strategy-validator", "context-window-optimizer"], featured=True),
    _skill("model-governance-implementer", "Model Governance Implementer", "ai_ml", "Put model versioning, experiment tracking, drift detection, and rollback policy around production AI systems.", ["**/*.py", "**/*.yaml", "**/*.json", "**/mlops/**"], ["model governance", "drift detection", "model versioning"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["ab-test-validator", "drift-detection-checker", "version-control-verifier"]),
    _skill("ai-evaluation-framework-builder", "AI Evaluation Framework Builder", "ai_ml", "Build evaluation loops for AI systems with benchmark sets, rubric design, judge calibration, and human-review anchors.", ["**/*.py", "**/*.ts", "**/*.json", "**/evals/**"], ["ai evaluation", "benchmark suite", "llm judge"], "deepseek-ai/deepseek-v3.2", "moonshotai/kimi-k2.5", "deepseek-r1:32b", ["evaluation-coverage-checker", "judge-calibration-validator", "benchmark-completeness-test"], complexity_threshold=8),
    _skill("multimodal-ai-integrator", "Multimodal AI Integrator", "ai_ml", "Integrate text, vision, audio, and document intelligence into one application surface with graceful modality-aware fallbacks.", ["**/*.py", "**/*.ts", "**/vision/**", "**/audio/**"], ["multimodal", "vision model", "audio model"], "gemini-2.5-pro", "deepseek-ai/deepseek-v3.2", "qwen2.5-coder:32b", ["modality-fusion-checker", "latency-validator", "quality-assessment-test"]),
    _skill("agent-memory-designer", "Agent Memory Designer", "ai_ml", "Design short-term, long-term, and episodic memory layers for agents without turning retrieval into an unbounded context leak.", ["**/*.py", "**/*.ts", "**/memory/**", "**/agents/**"], ["agent memory", "episodic recall", "context retrieval"], "moonshotai/kimi-k2.5", "deepseek-ai/deepseek-v3.2", "deepseek-r1:32b", ["memory-retrieval-checker", "context-relevance-validator", "forgetting-curve-test"]),
    _skill("inference-optimization-engineer", "Inference Optimization Engineer", "ai_ml", "Optimize model serving with batching, quantization, streaming, and deployment-aware latency budgets that preserve quality.", ["**/*.py", "**/*.cpp", "**/*.onnx", "**/*.gguf", "**/inference/**"], ["quantization", "batching", "inference latency"], "deepseek-ai/deepseek-v3.2", "gemini-2.5-pro", "qwen2.5-coder:32b", ["inference-latency-checker", "throughput-validator", "accuracy-impact-test"], complexity_threshold=8),
]
