---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [project]
aliases:
  - "llm-evals"
sources:
  - "[[sources/2024-04-23-weeknotes_a3933c]]"

generation_complete: true
---

# llm-evals-plugin

## Description

llm-evals-plugin is a very early prototype of a plugin for the [[LLM]] command-line tool, built to run evaluations of prompts against language models. Evals are defined as YAML files that specify a system prompt, a user prompt, and a set of checks, and the plugin runs them against multiple models with the command `llm evals`. Version 0.1a0 was released on 2024-04-21; the name `llmevals` was already taken on PyPI. The author intends to use it to answer questions about prompt quality, such as whether capitalizing OUTPUT IN JSON makes a difference, and to help [[datasette-query-assistant]] choose models and prompts. The major missing feature is [[Parameterization]], which would allow testing many prompt combinations and additional examples loaded from CSV, JSON or YAML files; the author also plans to record results in SQLite and export them for version tracking in GitHub.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/datasette-query-assistant|datasette-query-assistant]]
- [[entities/llama-3|Llama 3]]

## Related Concepts

- [[concepts/parameterization|Parameterization]]

## Mentions in Source

- "[llm-evals-plugin](https://github.com/simonw/llm-evals-plugin) (`llmevals` was taken on PyPI already) is a *very* early prototype of an [LLM](https://llm.datasette.io/) plugin that I hope to use to address this problem." — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]