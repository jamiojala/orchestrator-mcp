# DevOps & Infrastructure

This page collects the 10 devops & infrastructure skills from the Superpower Tier global library. Each entry is stored as a portable pack in the repository and can be loaded locally or exported into other agent ecosystems.

Total skills on this page: 10

## Terraform Module Architect

Refactor ad hoc infrastructure into reusable, environment-safe Terraform modules with clean variable boundaries.

Source: `Superpower Tier global library`

### Trigger signals
- `terraform module`
- `iac`
- `environment overlay`

### Best-fit files
- `**/*.tf`
- `**/*.tfvars`

### Validation
- `verify_terraform_plan`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`

## GitHub Actions Optimizer

Reduce CI waste through caching, parallelism, and smarter workflow conditions without losing signal quality.

Source: `Superpower Tier global library`

### Trigger signals
- `github actions`
- `ci cache`
- `workflow optimization`

### Best-fit files
- `**/.github/workflows/*.yml`
- `**/.github/workflows/*.yaml`

### Validation
- `verify_ci_duration`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`

## Docker Layer Optimizer

Shrink container builds and speed up rebuilds through smarter layer ordering and multi-stage decomposition.

Source: `Superpower Tier global library`

### Trigger signals
- `docker layer`
- `multi stage`
- `image size`

### Best-fit files
- `**/Dockerfile*`
- `**/.dockerignore`

### Validation
- `verify_image_size`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`

## Kubernetes Manifest Weaver

Compose Kubernetes manifests with overlays, health checks, and safer secret boundaries across environments.

Source: `Superpower Tier global library`

### Trigger signals
- `kubernetes`
- `kustomize`
- `health check`

### Best-fit files
- `**/*.yaml`
- `**/*.yml`
- `**/k8s/**`

### Validation
- `verify_manifest_validity`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`

## Env Secret Rotator

Plan and stage zero-downtime secret rotation across services that currently share brittle static credentials.

Source: `Superpower Tier global library`

### Trigger signals
- `secret rotation`
- `key rollover`
- `credential refresh`

### Best-fit files
- `**/.env*`
- `**/*.yaml`
- `**/*.ts`

### Validation
- `verify_rotation_safety`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Log Aggregation Architect

Turn ad hoc logs into structured, correlated observability streams with request and trace identity built in.

Source: `Superpower Tier global library`

### Trigger signals
- `structured logging`
- `correlation id`
- `log aggregation`

### Best-fit files
- `**/*.ts`
- `**/*.py`
- `**/middleware/**`

### Validation
- `verify_log_parsing`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`

## Blue-Green Deployer

Automate safer production rollouts with health-aware promotion and rollback triggers.

Source: `Superpower Tier global library`

### Trigger signals
- `blue green`
- `deployment rollback`
- `release health`

### Best-fit files
- `**/*.yaml`
- `**/deploy/**`
- `**/.github/workflows/**`

### Validation
- `verify_deployment_health`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`

## Cost Allocation Tagging

Standardize cloud tagging so spend can be attributed cleanly across teams, services, and environments.

Source: `Superpower Tier global library`

### Trigger signals
- `cost allocation`
- `tagging`
- `billing`

### Best-fit files
- `**/*.tf`
- `**/*.yaml`
- `**/cloud/**`

### Validation
- `verify_tag_coverage`

### Preferred models
- `meta/llama-3.3-70b-instruct`
- `deepseek-ai/deepseek-v3.2`
- `llama3.1:8b`

## Disaster Recovery Planner

Define realistic recovery objectives, backup validation, and operator runbooks for critical systems.

Source: `Superpower Tier global library`

### Trigger signals
- `disaster recovery`
- `rto`
- `rpo`

### Best-fit files
- `**/*.md`
- `**/infra/**`
- `**/backup/**`

### Validation
- `verify_recovery_procedures`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Observability Dashboard Synthesizer

Build SLO-aware dashboards and alerts that reveal burn rate, not just raw telemetry volume.

Source: `Superpower Tier global library`

### Trigger signals
- `slo`
- `burn rate`
- `dashboard`

### Best-fit files
- `**/*.json`
- `**/grafana/**`
- `**/datadog/**`

### Validation
- `verify_alert_thresholds`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `llama3.1:8b`
