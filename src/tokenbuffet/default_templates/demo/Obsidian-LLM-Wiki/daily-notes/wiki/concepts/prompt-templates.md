---
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"

generation_complete: true
---

type: concept
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2023-06-27-weeknotes_f6a59b]]"]
tags: [terminology]
aliases: ["LLM prompt templates", "templates"]
---

# Prompt templates

## Definition

Prompt templates are a feature of the [[LLM]] command-line tool that packages a reusable prompt, such as a system instruction, together with a model setting, into a single file. A template is installed with the `llm templates edit` command, which opens the file in the user's `$EDITOR`, and is run with the `-t` option, optionally passing parameters through `-p`.

## Key Characteristics

- Bundles a reusable prompt (for example, a system instruction) and a model setting in one file
- Created and edited through `llm templates edit`, which opens the file in `$EDITOR`
- Run with the `-t` option; parameters can be supplied with `-p`
- Intended to make reusable snippets easy to create for many purposes
- Serves as the foundation for the [[LLM plugins]] of the template category planned for LLM

## Applications

- Generating git commit messages from a git diff
- Explaining code
- Sharing reusable prompt snippets for recurring tasks, with a base for template plugins that distribute installable templates

## Related Concepts

- [[concepts/llm-plugins|LLM plugins]]

## Related Entities

- [[entities/llm|LLM]]

## Mentions in Source

- "The big new released feature is [prompt templates](https://llm.datasette.io/en/stable/templates.html)." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "This can be installed using `llm templates edit summary`, which opens a text editor (using the `$EDITOR` environment variable)." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]