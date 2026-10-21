---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [idea]
aliases:
  - "Parametrization"
  - "Parameterized Evaluation"
sources:
  - "[[sources/2024-04-23-weeknotes_a3933c]]"

generation_complete: true
---

# Parameterization

## Definition

Parameterization is a planned feature that lets an evaluation run be repeated across many combinations of prompts, system prompts, and additional examples. Instead of running a single eval, a user can run the same evaluation over a larger dataset and compare results across variants. Examples are loaded from external CSV, JSON, or YAML files rather than written inline.

## Key Characteristics

- Runs one evaluation across multiple prompt and system prompt combinations.
- Supports additional examples as a dataset, not only inline test cases.
- Loads examples from CSV, JSON, or YAML files.
- Enables side-by-side comparison of prompts over a larger set of inputs.
- Was identified by the author as the major missing feature of [[llm-evals-plugin]] at the time of writing, and is tracked in a GitHub issue.

## Applications

- Turning a single eval into a practical tool for comparing prompt variants over a full dataset.
- Systematic prompt testing, where many prompt and system prompt variants are evaluated against the same examples.
- Preparing an evaluation workflow for repeatable, dataset-driven testing, which the author describes as one of the main steps before the tool can be used for systematic prompt testing.

## Related Concepts

## Related Entities

- [[entities/llm-evals-plugin|llm-evals-plugin]]

## Mentions in Source

- "The big missing feature at the moment is [parameterization](https://github.com/simonw/llm-evals-plugin/issues/4): I want to be able to try out different prompt/system prompt combinations and run a whole bunch of additional examples that are defined in a CSV or JSON or YAML file." — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]