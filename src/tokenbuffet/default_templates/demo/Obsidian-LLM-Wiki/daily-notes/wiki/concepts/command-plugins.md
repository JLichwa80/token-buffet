---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "command plugin"
  - "Command plugins"
sources:
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"

generation_complete: true
---

# Command plugins

## Definition

Command plugins are the first of four planned categories of plugins for the [[LLM]] command-line tool. Each one adds a new subcommand to the `llm` tool, with `llm search` and `llm embed` given as examples. They extend what the tool can do from the terminal beyond prompting, such as retrieval and embeddings.

## Key Characteristics

- Adds new subcommands to the `llm` command-line tool.
- Extends terminal functionality beyond prompting, for example into retrieval and embeddings.
- Examples given by the author: `llm search` and `llm embed`.
- First of four planned plugin categories within the [[LLM plugins]] effort.
- At the time of the June 2023 weeknotes, the overall plugin system was still under active development.
- Inspired by the plugin system of [[Datasette]].

## Applications

- Adding a search subcommand that retrieves content from the terminal.
- Adding an embedding subcommand that generates vector embeddings from the command line.

## Related Concepts

- [[concepts/llm-plugins|LLM plugins]]

## Related Entities

- [[entities/llm|LLM]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "**Command plugins**. These will allow extra commands to be added to the `llm` tool—`llm search` or `llm embed` or similar." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "I’m planning the following categories of plugins to start with:" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]