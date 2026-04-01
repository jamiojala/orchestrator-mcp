# Architecture & System Design

This page collects the 10 architecture & system design skills from the Superpower Tier global library. Each entry is stored as a portable pack in the repository and can be loaded locally or exported into other agent ecosystems.

Total skills on this page: 10

## Micro-Frontend Orchestrator

Decompose monolithic frontend systems into deployable micro-frontends without breaking route contracts or shared state.

Source: `Superpower Tier global library`

### Trigger signals
- `micro frontend`
- `module federation`
- `route integrity`

### Best-fit files
- `**/*.tsx`
- `**/vite.config.*`
- `**/webpack*.js`

### Validation
- `audit_bundle_size`
- `verify_route_integrity`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `qwen2.5-coder:32b`

## Event-Sourcing Architect

Transform CRUD-heavy state flows into event-sourced patterns with replayability and time-travel debugging.

Source: `Superpower Tier global library`

### Trigger signals
- `event sourcing`
- `redux`
- `zustand`

### Best-fit files
- `**/*store*.ts`
- `**/*redux*.ts`
- `**/*zustand*.ts`

### Validation
- `verify_state_consistency`

### Preferred models
- `moonshotai/kimi-k2.5`
- `deepseek-ai/deepseek-v3.2`
- `deepseek-r1:32b`

## Database-Per-Tenant Designer

Blueprint multi-tenant database isolation, row-level security, and connection pooling without breaking tenant routing.

Source: `Superpower Tier global library`

### Trigger signals
- `multi tenant`
- `tenant_id`
- `row level security`

### Best-fit files
- `**/schema.prisma`
- `**/*.sql`
- `**/supabase/**`

### Validation
- `audit_rls_policies`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Circuit-Breaker Weaver

Wrap external API calls with circuit breakers, retries, fallbacks, and backoff while preserving business logic shape.

Source: `Superpower Tier global library`

### Trigger signals
- `circuit breaker`
- `retry`
- `backoff`

### Best-fit files
- `**/*.ts`
- `**/*.py`
- `**/api/**`

### Validation
- `verify_error_handling`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `qwen2.5-coder:32b`

## CQRS Pattern Synthesizer

Separate read and write models into typed CQRS flows with query optimization and command safety.

Source: `Superpower Tier global library`

### Trigger signals
- `cqrs`
- `command handler`
- `query model`

### Best-fit files
- `**/*.ts`
- `**/*.tsx`
- `**/schema*.ts`

### Validation
- `verify_type_consistency`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Real-Time Sync Engineer

Add optimistic UI, sync reconciliation, and offline-safe conflict handling to collaborative product flows.

Source: `Superpower Tier global library`

### Trigger signals
- `realtime`
- `optimistic ui`
- `conflict resolution`

### Best-fit files
- `**/*.tsx`
- `**/*realtime*.ts`
- `**/*socket*.ts`

### Validation
- `verify_offline_behavior`

### Preferred models
- `moonshotai/kimi-k2.5`
- `deepseek-ai/deepseek-v3.2`
- `qwen2.5-coder:32b`

## Serverless Cost Optimizer

Split long-running serverless logic into edge-safe, cold-start-aware execution paths with lower runtime cost.

Source: `Superpower Tier global library`

### Trigger signals
- `serverless cost`
- `cold start`
- `lambda`

### Best-fit files
- `**/api/**/*.ts`
- `**/*.lambda.*`
- `**/functions/**`

### Validation
- `audit_cold_start_metrics`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `meta/llama-3.3-70b-instruct`
- `qwen2.5-coder:32b`

## GraphQL Federation Gateway

Merge multiple GraphQL schemas into a stitched or federated gateway with conflict detection and safe ownership boundaries.

Source: `Superpower Tier global library`

### Trigger signals
- `graphql federation`
- `schema stitching`
- `apollo`

### Best-fit files
- `**/*.graphql`
- `**/schema*.ts`
- `**/apollo*.ts`

### Validation
- `verify_schema_conflicts`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `qwen2.5-coder:32b`

## Feature-Flag Architect

Introduce feature-flag systems with kill switches, experiment hooks, and isolated rollout boundaries.

Source: `Superpower Tier global library`

### Trigger signals
- `feature flag`
- `kill switch`
- `ab test`

### Best-fit files
- `**/*.ts`
- `**/*.tsx`
- `**/.env*`

### Validation
- `verify_flag_isolation`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `qwen2.5-coder:32b`

## Data Migration Blueprinter

Design zero-downtime data migrations with rollback choreography, phased reads, and production-safe cutovers.

Source: `Superpower Tier global library`

### Trigger signals
- `data migration`
- `rollback`
- `zero downtime`

### Best-fit files
- `**/migrations/**`
- `**/schema.prisma`
- `**/*.sql`

### Validation
- `verify_migration_safety`

### Preferred models
- `moonshotai/kimi-k2.5`
- `deepseek-ai/deepseek-v3.2`
- `deepseek-r1:32b`
