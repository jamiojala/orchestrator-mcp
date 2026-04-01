# AI/ML Engineering

This page collects the 10 AI/ML engineering skills added to the Superpower Tier global library. Each entry is stored as a portable pack in the repository and can be loaded locally or exported into other agent ecosystems.

Total skills on this page: 10

## Prompt Engineering Architect

Design system prompts, prompt contracts, and eval-backed example sets that improve LLM reliability without hiding failure modes.

Source: `Superpower Tier global library`

### Trigger signals
- `system prompt`
- `few shot`
- `prompt contract`

### Best-fit files
- `**/*.py`
- `**/*.ts`
- `**/*.yaml`
- `**/*.json`
- `**/prompts/**`

### Validation
- `prompt-performance-checker`
- `output-consistency-validator`
- `token-usage-optimizer`

### Preferred models
- `moonshotai/kimi-k2.5`
- `deepseek-ai/deepseek-v3.2`
- `qwen2.5-coder:32b`

## LLM Integration Specialist

Integrate hosted and local LLM providers with fallback, rate limiting, and spend-aware routing that remains debuggable in production.

Source: `Superpower Tier global library`

### Trigger signals
- `llm integration`
- `provider fallback`
- `completion api`

### Best-fit files
- `**/*.py`
- `**/*.ts`
- `**/*.js`
- `**/providers/**`
- `**/models/**`

### Validation
- `api-reliability-checker`
- `fallback-strategy-validator`
- `cost-tracking-verifier`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `gemini-2.5-pro`
- `qwen2.5-coder:32b`

## Embedding Pipeline Designer

Build embedding pipelines with retrieval-aware chunking, vector index strategy, and similarity quality that can be measured.

Source: `Superpower Tier global library`

### Trigger signals
- `embedding`
- `vector db`
- `semantic search`

### Best-fit files
- `**/*.py`
- `**/*.ts`
- `**/embeddings/**`
- `**/vector/**`

### Validation
- `embedding-quality-checker`
- `vector-db-validator`
- `search-accuracy-test`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `gemini-2.5-pro`
- `qwen2.5-coder:32b`

## Fine-Tuning Workflow Creator

Create fine-tuning workflows with dataset preparation, evaluation baselines, and rollback-ready deployment checkpoints.

Source: `Superpower Tier global library`

### Trigger signals
- `fine tuning`
- `training loop`
- `evaluation set`

### Best-fit files
- `**/*.py`
- `**/*.ipynb`
- `**/*.yaml`
- `**/training/**`

### Validation
- `data-quality-checker`
- `training-convergence-validator`
- `evaluation-metrics-verifier`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## RAG System Architect

Design retrieval-augmented generation systems with chunking, ranking, citation, and context-budget discipline that hold up in production.

Source: `Superpower Tier global library`

### Trigger signals
- `rag`
- `retrieval`
- `context injection`

### Best-fit files
- `**/*.py`
- `**/*.ts`
- `**/rag/**`
- `**/retrieval/**`

### Validation
- `retrieval-accuracy-checker`
- `chunking-strategy-validator`
- `context-window-optimizer`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `qwen2.5-coder:32b`

## Model Governance Implementer

Put model versioning, experiment tracking, drift detection, and rollback policy around production AI systems.

Source: `Superpower Tier global library`

### Trigger signals
- `model governance`
- `drift detection`
- `model versioning`

### Best-fit files
- `**/*.py`
- `**/*.yaml`
- `**/*.json`
- `**/mlops/**`

### Validation
- `ab-test-validator`
- `drift-detection-checker`
- `version-control-verifier`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## AI Evaluation Framework Builder

Build evaluation loops for AI systems with benchmark sets, rubric design, judge calibration, and human-review anchors.

Source: `Superpower Tier global library`

### Trigger signals
- `ai evaluation`
- `benchmark suite`
- `llm judge`

### Best-fit files
- `**/*.py`
- `**/*.ts`
- `**/*.json`
- `**/evals/**`

### Validation
- `evaluation-coverage-checker`
- `judge-calibration-validator`
- `benchmark-completeness-test`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `moonshotai/kimi-k2.5`
- `deepseek-r1:32b`

## Multimodal AI Integrator

Integrate text, vision, audio, and document intelligence into one application surface with graceful modality-aware fallbacks.

Source: `Superpower Tier global library`

### Trigger signals
- `multimodal`
- `vision model`
- `audio model`

### Best-fit files
- `**/*.py`
- `**/*.ts`
- `**/vision/**`
- `**/audio/**`

### Validation
- `modality-fusion-checker`
- `latency-validator`
- `quality-assessment-test`

### Preferred models
- `gemini-2.5-pro`
- `deepseek-ai/deepseek-v3.2`
- `qwen2.5-coder:32b`

## Agent Memory Designer

Design short-term, long-term, and episodic memory layers for agents without turning retrieval into an unbounded context leak.

Source: `Superpower Tier global library`

### Trigger signals
- `agent memory`
- `episodic recall`
- `context retrieval`

### Best-fit files
- `**/*.py`
- `**/*.ts`
- `**/memory/**`
- `**/agents/**`

### Validation
- `memory-retrieval-checker`
- `context-relevance-validator`
- `forgetting-curve-test`

### Preferred models
- `moonshotai/kimi-k2.5`
- `deepseek-ai/deepseek-v3.2`
- `deepseek-r1:32b`

## Inference Optimization Engineer

Optimize model serving with batching, quantization, streaming, and deployment-aware latency budgets that preserve quality.

Source: `Superpower Tier global library`

### Trigger signals
- `quantization`
- `batching`
- `inference latency`

### Best-fit files
- `**/*.py`
- `**/*.cpp`
- `**/*.onnx`
- `**/*.gguf`
- `**/inference/**`

### Validation
- `inference-latency-checker`
- `throughput-validator`
- `accuracy-impact-test`

### Preferred models
- `deepseek-ai/deepseek-v3.2`
- `gemini-2.5-pro`
- `qwen2.5-coder:32b`
