---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Plugin system"
  - "Plugin support"
sources:
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"

generation_complete: true
---

# Plugins

## Definition

A plugin is an extension that adds functionality to a host tool without changing the tool's core code.

## Key Characteristics

- Extends a host tool from the outside, leaving its core code unchanged.
- In [[sqlite-utils]], comes in two categories: plugins that add extra CLI commands, and plugins that add [[Custom SQL functions|custom SQL functions]].
- In [[LLM]], plugin support lets the tool work with models beyond OpenAI's. [[llm-llama-cpp]] and [[llm-replicate]] build on this support.
- Lets one author add new integrations to several projects with the same approach.

## Applications

- Adding model providers to [[LLM]], such as [[llm-llama-cpp]] and [[llm-replicate]].
- Adding CLI commands or SQL functions to [[sqlite-utils]].
- Extending [[Datasette]] with features such as [[datasette-auth-tokens]], which relies on [[API tokens]].

## Related Concepts

- [[concepts/custom-sql-functions|Custom SQL functions]]
- [[concepts/api-tokens|API tokens]]

## Related Entities

- [[entities/llm|LLM]]
- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/llm-llama-cpp|llm-llama-cpp]]
- [[entities/datasette-auth-tokens|datasette-auth-tokens]]

## Mentions in Source

- "The principle theme for the past few weeks has been plugins." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "There are two categories of plugins so far: plugins that add extra commands to the `sqlite-utils` CLI tool, and plugins that add extra custom SQL functions that can be executed against SQLite." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]