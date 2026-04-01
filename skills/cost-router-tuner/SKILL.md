---
name: Cost Router Tuner
description: Tune provider routing policy for quality, cost ceilings, and fallback behavior across multiple model subscriptions.
public: true
category: routing
tags: [budget, routing, cost, providers]
preferred_models:
  - moonshotai/kimi-k2.5
  - gemini-2.5-flash
validation:
  - verify_text_unchanged
keywords: [budget, router, routing, cost, fallback, poor mans mode]
task_types: [architecture, reasoning]
prompt_template: |
  Optimize model routing for cost efficiency without sacrificing the highest-value specialist paths.
  Recommend policy changes, not just model swaps.
---
# Cost Router Tuner

Use this skill when you already have multiple subscriptions but want smarter default routing.

Expected output:

- recommended default routes
- escalation routes for high-stakes work
- budget thresholds
- cache and fallback suggestions
