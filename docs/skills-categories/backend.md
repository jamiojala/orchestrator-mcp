# Backend & API Design

This page collects the 12 backend & api design skills from the Superpower Tier global library. Each entry is stored as a portable pack in the repository and can be loaded locally or exported into other agent ecosystems.

Total skills on this page: 12

## API Versioning Strategist

Introduce safe API versioning with compatibility lanes, deprecation notices, and migration guidance.

Source: `Superpower Tier global library`

### Trigger signals
- `api versioning`
- `backward compatibility`
- `deprecation`

### Best-fit files
- `**/api/**`
- `**/routes/**`
- `**/*.ts`

### Validation
- `verify_backward_compatibility`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Rate-Limiting Architect

Implement distributed rate limiting with token buckets, predictable headers, and production-safe behavior under load.

Source: `Superpower Tier global library`

### Trigger signals
- `rate limit`
- `token bucket`
- `redis`

### Best-fit files
- `**/api/**`
- `**/middleware/**`
- `**/*.ts`

### Validation
- `verify_rate_limit_headers`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Webhook Security Designer

Harden webhook handlers with signature verification, replay prevention, and idempotency discipline.

Source: `Superpower Tier global library`

### Trigger signals
- `webhook`
- `signature verification`
- `replay attack`

### Best-fit files
- `**/*webhook*.ts`
- `**/*webhook*.py`

### Validation
- `verify_webhook_security`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## JWT Rotation Engineer

Modernize session flows with rotating refresh tokens, revocation, and secure cookie handling.

Source: `Superpower Tier global library`

### Trigger signals
- `jwt`
- `refresh token`
- `httpOnly cookie`

### Best-fit files
- `**/auth/**`
- `**/*.ts`
- `**/*.py`

### Validation
- `verify_token_security`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Idempotency Guardian

Make mutation endpoints safely retryable with idempotency keys and conflict-aware persistence patterns.

Source: `Superpower Tier global library`

### Trigger signals
- `idempotency`
- `safe retries`
- `mutation api`

### Best-fit files
- `**/api/**`
- `**/payments/**`
- `**/*.ts`

### Validation
- `verify_idempotency_guarantees`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## API Pagination Architect

Replace offset-heavy APIs with cursor pagination that scales cleanly and remains client-friendly.

Source: `Superpower Tier global library`

### Trigger signals
- `cursor pagination`
- `list endpoint`
- `link headers`

### Best-fit files
- `**/api/**`
- `**/*.sql`
- `**/*.ts`

### Validation
- `verify_pagination_performance`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## GraphQL Query Complexity Guard

Protect GraphQL services from expensive queries with depth, complexity, and resource-aware limits.

Source: `Superpower Tier global library`

### Trigger signals
- `graphql complexity`
- `query depth`
- `dos protection`

### Best-fit files
- `**/*.graphql`
- `**/apollo*.ts`
- `**/graphql/**`

### Validation
- `verify_query_limits`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## OpenAPI Spec Generator

Generate OpenAPI documentation from typed routes and schemas without drifting from implementation.

Source: `Superpower Tier global library`

### Trigger signals
- `openapi`
- `zod schema`
- `api docs`

### Best-fit files
- `**/routes/**`
- `**/schema*.ts`
- `**/*.py`

### Validation
- `verify_spec_completeness`

### Preferred models
- `qwen3-coder:480b-cloud`
- `deepseek-ai/deepseek-v3.2`
- `qwen2.5-coder:32b`

## API Test Contract Enforcer

Set up contract testing so API consumers and providers fail safely before incompatible releases ship.

Source: `Superpower Tier global library`

### Trigger signals
- `contract test`
- `pact`
- `consumer provider`

### Best-fit files
- `**/tests/**`
- `**/api/**`
- `**/*.ts`

### Validation
- `verify_contract_compliance`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Event-Driven Sync Engine

Introduce outbox-driven cross-service communication with reliable publication and eventual consistency safeguards.

Source: `Superpower Tier global library`

### Trigger signals
- `outbox pattern`
- `event driven`
- `eventual consistency`

### Best-fit files
- `**/queue/**`
- `**/events/**`
- `**/*.ts`

### Validation
- `verify_eventual_consistency`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## API Deprecation Strategist

Sunset APIs with clear migration windows, explicit headers, and communication paths that reduce client breakage.

Source: `Superpower Tier global library`

### Trigger signals
- `api deprecation`
- `sunset header`
- `migration window`

### Best-fit files
- `**/api/**`
- `**/*.md`
- `**/*.ts`

### Validation
- `verify_deprecation_notices`

### Preferred models
- `meta/llama-3.3-70b-instruct`
- `deepseek-ai/deepseek-v3.2`
- `llama3.1:8b`

## Server Timing Analyzer

Expose backend bottlenecks through Server-Timing instrumentation that separates compute, database, and remote call cost.

Source: `Superpower Tier global library`

### Trigger signals
- `server timing`
- `performance header`
- `latency breakdown`

### Best-fit files
- `**/middleware/**`
- `**/api/**`
- `**/*.ts`

### Validation
- `verify_timing_accuracy`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`
