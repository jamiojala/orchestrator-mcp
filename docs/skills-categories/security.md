# Security & Compliance

This page collects the 10 security & compliance skills from the Superpower Tier global library. Each entry is stored as a portable pack in the repository and can be loaded locally or exported into other agent ecosystems.

Total skills on this page: 10

## GDPR-by-Design Architect

Embed privacy-first product patterns with data minimization, retention controls, and defensible deletion workflows.

Source: `Superpower Tier global library`

### Trigger signals
- `gdpr`
- `pii`
- `data retention`

### Best-fit files
- `**/*.ts`
- `**/*.sql`
- `**/privacy/**`

### Validation
- `audit_gdpr_compliance`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## OWASP Top 10 Guardian

Systematically surface high-probability application security weaknesses across common OWASP failure modes.

Source: `Superpower Tier global library`

### Trigger signals
- `owasp`
- `xss`
- `csrf`

### Best-fit files
- `**/*.ts`
- `**/*.py`
- `**/api/**`

### Validation
- `verify_owasp_compliance`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Dependency Supply Chain Auditor

Audit dependencies for typosquatting, licensing risk, and supply-chain fragility before they hit production.

Source: `Superpower Tier global library`

### Trigger signals
- `sbom`
- `supply chain`
- `license compliance`

### Best-fit files
- `**/package.json`
- `**/pnpm-lock.yaml`
- `**/requirements*.txt`

### Validation
- `verify_supply_chain_safety`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `meta/llama-3.3-70b-instruct`
- `llama3.1:8b`

## Secrets Scanning Automator

Wire secret-detection into local and CI workflows so leaks are stopped before they become incidents.

Source: `Superpower Tier global library`

### Trigger signals
- `secret scan`
- `pre commit`
- `credential leak`

### Best-fit files
- `**/.git/hooks/**`
- `**/.github/workflows/**`
- `**/*.sh`

### Validation
- `verify_secret_detection`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## CORS Policy Hardening

Tighten cross-origin boundaries without silently breaking legitimate credentialed traffic.

Source: `Superpower Tier global library`

### Trigger signals
- `cors`
- `origin allowlist`
- `credentials`

### Best-fit files
- `**/api/**`
- `**/*.ts`
- `**/*.py`

### Validation
- `verify_cors_strictness`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Content Security Policy Architect

Design nonce- and policy-based browser defenses that meaningfully shrink XSS blast radius.

Source: `Superpower Tier global library`

### Trigger signals
- `content security policy`
- `nonce`
- `strict dynamic`

### Best-fit files
- `**/*.ts`
- `**/*.html`
- `**/headers/**`

### Validation
- `verify_csp_enforcement`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## SOC2 Control Documenter

Translate operating practices into audit-friendly SOC 2 evidence maps with technical verification hooks.

Source: `Superpower Tier global library`

### Trigger signals
- `soc2`
- `control evidence`
- `audit`

### Best-fit files
- `**/*.md`
- `**/policies/**`
- `**/controls/**`

### Validation
- `verify_control_effectiveness`

### Preferred models
- `meta/llama-3.3-70b-instruct`
- `deepseek-ai/deepseek-v3.2`
- `llama3.1:8b`

## Vulnerability Patch Prioritizer

Rank vulnerability work by exploitability and business impact instead of raw advisory volume.

Source: `Superpower Tier global library`

### Trigger signals
- `cvss`
- `patch prioritization`
- `security advisory`

### Best-fit files
- `**/package.json`
- `**/requirements*.txt`
- `**/*.md`

### Validation
- `verify_patch_urgency`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Zero-Trust Network Designer

Design service-to-service trust boundaries with strong identity, policy, and transport guarantees.

Source: `Superpower Tier global library`

### Trigger signals
- `zero trust`
- `mtls`
- `service mesh`

### Best-fit files
- `**/*.yaml`
- `**/network/**`
- `**/infra/**`

### Validation
- `verify_zero_trust_policies`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Audit Log Immutability Guardian

Protect critical audit trails against tampering with append-only integrity and verification strategies.

Source: `Superpower Tier global library`

### Trigger signals
- `audit log`
- `immutability`
- `worm`

### Best-fit files
- `**/*.ts`
- `**/*.py`
- `**/audit/**`

### Validation
- `verify_log_integrity`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`
