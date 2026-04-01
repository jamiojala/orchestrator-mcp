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

    def system_prompt(self) -> str:
        role = CATEGORY_ROLES[self.category]
        constraint_lines = CATEGORY_CONSTRAINTS[self.category] + list(self.custom_constraints)
        rendered_constraints = "\n".join(f"- {item}" for item in constraint_lines)
        rendered_validation = "\n".join(f"- Ensure `{tool}` passes or explain why it cannot run" for tool in self.validation_tools)
        return "\n".join(
            [
                f"You are a {role} specializing in {self.category} systems.",
                "",
                "## Your Task",
                f"Use the supplied code, architecture, or product context to {self.superpower.lower()}",
                "Produce a bounded implementation plan or code-ready blueprint that another engineer or coding agent can execute safely.",
                "",
                "## Constraints",
                rendered_constraints,
                "- Return exact file or module targets when you recommend code changes.",
                "- Include rollback or containment guidance for risky changes.",
                "",
                "## Output Format",
                "- Capability summary",
                "- Trigger fit and assumptions",
                "- Implementation slices with file targets",
                "- Validation and rollout plan",
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
                "author": "orchestrator-mcp contributors",
                "license": "MIT",
                "pricing_tier": "free",
                "language_support": CATEGORY_LANGUAGES[self.category],
                "featured": self.featured,
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
        frontmatter = [
            "---",
            f"name: {self.name}",
            f"description: {self.superpower}",
            "public: true",
            f"category: {self.category}",
            f"tags: [{', '.join(self.keywords[:4])}]",
            "preferred_models:",
            f"  - {self.primary_model}",
            f"  - {self.fallback_model}",
            f"  - {self.local_only_model}",
            "validation:",
        ]
        frontmatter.extend(f"  - {tool}" for tool in self.validation_tools)
        frontmatter.extend(
            [
                "keywords:",
                *[f"  - {item}" for item in self.keywords],
                "task_types:",
                *[f"  - {item}" for item in _task_types_for_category(self.category)],
                "prompt_template: |",
            ]
        )
        frontmatter.extend(f"  {line}" for line in self.system_prompt().splitlines())
        frontmatter.append("---")
        body = [
            f"# {self.name}",
            "",
            f"Superpower: {self.superpower}",
            "",
            "Best used when:",
            *[f"- keyword or signal: {item}" for item in self.keywords[:4]],
            "",
            "Recommended validation:",
            *[f"- `{tool}`" for tool in self.validation_tools],
            "",
            "Model chain:",
            f"- primary: `{self.primary_model}`",
            f"- fallback: `{self.fallback_model}`",
            f"- local: `{self.local_only_model}`",
        ]
        if self.notes:
            body.extend(["", "Notes:", *[f"- {note}" for note in self.notes]])
        return "\n".join(frontmatter + body) + "\n"

    def readme_text(self) -> str:
        lines = [
            f"# {self.name}",
            "",
            f"Category: `{self.category}`",
            "",
            f"Superpower: {self.superpower}",
            "",
            "Trigger signals:",
            *[f"- `{item}`" for item in self.keywords],
            "",
            "Suggested file patterns:",
            *[f"- `{item}`" for item in self.file_patterns],
            "",
            "Validation hooks:",
            *[f"- `{item}`" for item in self.validation_tools],
            "",
            "Model preferences:",
            f"- primary: `{self.primary_model}`",
            f"- fallback: `{self.fallback_model}`",
            f"- local: `{self.local_only_model}`",
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
]
