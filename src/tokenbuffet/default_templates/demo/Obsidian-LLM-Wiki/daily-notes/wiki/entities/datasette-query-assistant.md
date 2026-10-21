---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [project]
aliases:
  - "Query Assistant"
sources:
  - "[[sources/2024-04-23-weeknotes_a3933c]]"

generation_complete: true
---

# datasette-query-assistant

## Description

datasette-query-assistant is a [[Datasette]] plugin built on top of Claude 3 that converts a question written in English into a SQL query. The author describes it as the most notable of the twelve live demos in his Stanford talk. It had been released only recently, as version 0.1a2, after being cleaned up for release. The plugin is central to the post's discussion of evaluation: the author wants to know which models generate SQLite SQL best, and which prompts yield queries that execute successfully against a schema. It is therefore the motivating use case for [[llm-evals-plugin]].

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/llm-evals-plugin|llm-evals-plugin]]
- [[entities/llama-3|Llama 3]]

## Related Concepts

## Mentions in Source

- "The most notable of those is [datasette-query-assistant](https://datasette.io/plugins/datasette-query-assistant), a plugin built on top of Claude 3 that takes a question in English and converts that into a SQL query." — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]