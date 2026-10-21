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
aliases: ["Prompt template plugins", "Template plugins"]
---

# Template plugins

## Definition

Template plugins are a planned category of [[LLM plugins]] that would distribute extra [[Prompt templates]] as installable packages, so users can share reusable prompt snippets instead of creating each one locally.

## Key Characteristics

- Planned as one of four initial [[LLM plugins]] categories, alongside command, model, and function plugins.
- Installed from a package with a command of the form `llm install name-of-package`.
- Extend the [[Prompt templates]] feature, which saves prompts and model settings as files and runs them with `-t`.
- Aim to make reusable prompt snippets shareable across users.
- Were still under active development at the time of the source post (June 2023).

## Applications

- Distributing a shared library of prompt templates (for example, summarizing text or explaining code) as a package.
- Installing ready-made templates with the [[LLM]] command-line tool rather than writing each one by hand.
- Sharing team or community prompt snippets through package installs.

## Related Concepts

- [[concepts/llm-plugins|LLM plugins]]
- [[concepts/prompt-templates|Prompt templates]]

## Related Entities

- [[entities/llm|LLM]]

## Mentions in Source

- "**Template plugins**. Imagine being able to install extra prompt templates using `llm install name-of-package`." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "The big new released feature is prompt templates." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]