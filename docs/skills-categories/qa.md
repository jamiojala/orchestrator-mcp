# Quality Assurance

This page collects the 10 quality assurance skills from the Superpower Tier global library. Each entry is stored as a portable pack in the repository and can be loaded locally or exported into other agent ecosystems.

Total skills on this page: 10

## Flaky Test Detective

Identify and stabilize non-deterministic tests through reproduction heuristics, isolation, and dependency analysis.

Source: `Superpower Tier global library`

### Trigger signals
- `flaky test`
- `retry`
- `nondeterministic`

### Best-fit files
- `**/tests/**`
- `**/*.spec.*`
- `**/*.test.*`

### Validation
- `verify_test_stability`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Visual Regression Architect

Set up screenshot-based UI regression pipelines that catch real layout and styling breakage without noise.

Source: `Superpower Tier global library`

### Trigger signals
- `visual regression`
- `playwright`
- `chromatic`

### Best-fit files
- `**/*.tsx`
- `**/playwright*.ts`
- `**/storybook/**`

### Validation
- `verify_screenshot_consistency`

### Preferred models
- `moonshotai/kimi-k2.5`
- `qwen3-coder:480b-cloud`
- `qwen2.5-coder:32b`

## Mutation Testing Agent

Challenge test suites with synthetic code mutations to measure whether tests actually protect behavior.

Source: `Superpower Tier global library`

### Trigger signals
- `mutation testing`
- `test effectiveness`
- `coverage`

### Best-fit files
- `**/tests/**`
- `**/*.ts`
- `**/*.py`

### Validation
- `verify_mutation_score`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## E2E Data Seeder

Generate realistic, relationally valid test data for end-to-end workflows without brittle manual setup.

Source: `Superpower Tier global library`

### Trigger signals
- `e2e seed`
- `test data`
- `fixtures`

### Best-fit files
- `**/tests/**`
- `**/seed*.ts`
- `**/fixtures/**`

### Validation
- `verify_data_consistency`

### Preferred models
- `meta/llama-3.3-70b-instruct`
- `deepseek-ai/deepseek-v3.2`
- `llama3.1:8b`

## Performance Regression Guard

Enforce performance budgets in CI so regressions are blocked before they become user-visible.

Source: `Superpower Tier global library`

### Trigger signals
- `lighthouse ci`
- `performance budget`
- `regression`

### Best-fit files
- `**/.github/workflows/**`
- `**/lighthouse*.js`
- `**/package.json`

### Validation
- `audit_lighthouse_score`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Accessibility Auditor Pro

Audit interface flows against WCAG 2.2 AA with both automated checks and human-readable remediation sequences.

Source: `Superpower Tier global library`

### Trigger signals
- `wcag`
- `axe`
- `accessibility audit`

### Best-fit files
- `**/*.tsx`
- `**/*.html`
- `**/pages/**`

### Validation
- `audit_wcag_compliance`

### Preferred models
- `moonshotai/kimi-k2.5`
- `deepseek-ai/deepseek-v3.2`
- `qwen2.5-coder:32b`

## Security Scan Automator

Wire security scanning into delivery workflows with exploitability-aware prioritization instead of raw alert floods.

Source: `Superpower Tier global library`

### Trigger signals
- `snyk`
- `dependabot`
- `security scan`

### Best-fit files
- `**/package.json`
- `**/.github/workflows/**`
- `**/requirements*.txt`

### Validation
- `verify_vulnerability_removal`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## API Fuzzing Strategist

Build property-based and boundary-oriented API tests that find input handling failures before attackers or customers do.

Source: `Superpower Tier global library`

### Trigger signals
- `api fuzzing`
- `property based`
- `boundary values`

### Best-fit files
- `**/api/**`
- `**/tests/**`
- `**/*.ts`

### Validation
- `verify_boundary_coverage`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Load Test Calibrator

Design realistic load scenarios with useful bottleneck signals rather than synthetic throughput vanity metrics.

Source: `Superpower Tier global library`

### Trigger signals
- `load test`
- `k6`
- `traffic simulation`

### Best-fit files
- `**/api/**`
- `**/k6/**`
- `**/artillery/**`

### Validation
- `verify_load_thresholds`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `deepseek-r1:32b`

## Dead Code Eliminator

Find and remove unused code paths, exports, and stale branches that still carry maintenance cost and risk.

Source: `Superpower Tier global library`

### Trigger signals
- `dead code`
- `unused exports`
- `bundle cleanup`

### Best-fit files
- `**/*.ts`
- `**/*.tsx`
- `**/*.py`

### Validation
- `verify_bundle_reduction`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `qwen3-coder:480b-cloud`
- `qwen2.5-coder:32b`
