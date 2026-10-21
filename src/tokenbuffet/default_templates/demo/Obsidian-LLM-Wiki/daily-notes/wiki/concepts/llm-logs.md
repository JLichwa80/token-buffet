---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "llm logs command"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# llm logs

## Definition

`llm logs` is the [[LLM]] command that displays the recorded history of prompts and responses stored in a SQLite database. From LLM 0.8 onward, its default output format is Markdown rather than JSON.

## Key Characteristics

- Reads and displays prompt and response history stored in SQLite.
- Since LLM 0.8, the default output is Markdown instead of JSON.
- Markdown output is easier to read and can be pasted directly into GitHub issue comments or Gists.
- The format change makes it simpler to share results with other people.
- Simon Willison describes this change as the most significant in the LLM 0.8 release.

## Applications

- Reviewing past prompts and model responses from the command line.
- Copying a session's history into GitHub issue comments to report or discuss model behaviour.
- Publishing results as Gists for others to read.

## Related Concepts

## Related Entities

- [[entities/llm|LLM]]

## Mentions in Source

- "The most significant of these was a change to the default `llm logs` output, which shows the logs (recorded in SQLite) of the previous prompts and responses you have sent through the tool." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]