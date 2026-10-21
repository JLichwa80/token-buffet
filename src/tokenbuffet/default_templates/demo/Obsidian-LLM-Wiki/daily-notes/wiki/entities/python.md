---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Python installations"
  - "system Python"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# Python

## Description

Python is the programming language in which [[Datasette]], [[sqlite-utils]], and [[LLM]] are written. In the 2023-08-30 weeknotes, it is the runtime environment where a compatibility problem occurred: some Python installations block writes to the `sqlite_master` table regardless of the pragmas set. This behavior caused bug reports from LLM users and motivated the switch to the sqlite-utils `transform()` method, which works on installations that block schema writes. The LLM plugins [[llm-openrouter]] and [[llm-anyscale-endpoints]] rely on the Python `openai` library, which is part of why they were quick to build.

## Related Entities

- [[entities/sqlite|SQLite]]
- [[entities/llm|LLM]]
- [[entities/llm-openrouter|llm-openrouter]]
- [[entities/llm-anyscale-endpoints|llm-anyscale-endpoints]]

## Related Concepts

## Mentions in Source

- "It turns out there are Python installations out there—most notably the system Python on macOS—which completely disable the ability to write to that table, no matter what the status of the various pragmas." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]