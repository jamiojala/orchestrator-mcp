# Data & Analytics

This page collects the 8 data & analytics skills from the Superpower Tier global library. Each entry is stored as a portable pack in the repository and can be loaded locally or exported into other agent ecosystems.

Total skills on this page: 8

## Data Warehouse Modeler

Shape analytics data into warehouse models that remain queryable, explainable, and maintainable as the product grows.

Source: `Superpower Tier global library`

### Trigger signals
- `star schema`
- `warehouse model`
- `dimensions`

### Best-fit files
- `**/*.sql`
- `**/dbt/**`
- `**/warehouse/**`

### Validation
- `verify_query_performance`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Real-Time Analytics Pipeline

Build sub-second analytics pipelines over streaming events without turning the system into an operational mystery.

Source: `Superpower Tier global library`

### Trigger signals
- `real time analytics`
- `clickhouse`
- `streaming`

### Best-fit files
- `**/*.sql`
- `**/stream/**`
- `**/analytics/**`

### Validation
- `verify_latency_metrics`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Data Quality Sentinel

Instrument data pipelines with freshness, completeness, and anomaly detection checks that fail usefully.

Source: `Superpower Tier global library`

### Trigger signals
- `great expectations`
- `data quality`
- `anomaly detection`

### Best-fit files
- `**/*.py`
- `**/etl/**`
- `**/dbt/**`

### Validation
- `verify_data_freshness`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Funnel Conversion Analyst

Design product event funnels that reveal meaningful drop-off and activation patterns instead of vanity charts.

Source: `Superpower Tier global library`

### Trigger signals
- `funnel analysis`
- `conversion`
- `event tracking`

### Best-fit files
- `**/*.sql`
- `**/analytics/**`
- `**/*.ts`

### Validation
- `verify_tracking_accuracy`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Cohort Retention Engineer

Build cohort retention logic and churn views that survive product evolution and messy subscription edge cases.

Source: `Superpower Tier global library`

### Trigger signals
- `cohort`
- `retention`
- `churn`

### Best-fit files
- `**/*.sql`
- `**/analytics/**`
- `**/*.py`

### Validation
- `verify_retention_calculation`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Privacy-Preserving Analytics

Design analytics flows that preserve useful product insight while reducing privacy and re-identification risk.

Source: `Superpower Tier global library`

### Trigger signals
- `differential privacy`
- `k anonymity`
- `privacy analytics`

### Best-fit files
- `**/*.sql`
- `**/analytics/**`
- `**/*.py`

### Validation
- `verify_privacy_guarantees`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Feature Store Architect

Organize machine-learning features so online and offline use stay aligned under evolving training pipelines.

Source: `Superpower Tier global library`

### Trigger signals
- `feature store`
- `online offline consistency`
- `ml features`

### Best-fit files
- `**/*.py`
- `**/features/**`
- `**/*.sql`

### Validation
- `verify_feature_consistency`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Experimentation Platform Builder

Design trustworthy experimentation infrastructure with sound randomization, sizing, and interpretation defaults.

Source: `Superpower Tier global library`

### Trigger signals
- `ab test`
- `experimentation`
- `sample size`

### Best-fit files
- `**/*.ts`
- `**/*.py`
- `**/experiments/**`

### Validation
- `verify_statistical_validity`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`
