---
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"

generation_complete: true
---

type: entity
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2023-10-30-weeknotes_d4a215]]"]
tags: [other]
aliases: ["pipx tool", "pipx install"]
---

# pipx

## Description

pipx is a tool for installing and running Python command-line applications in isolated environments. In the source post, the author replaced [[Homebrew]] with pipx as the recommended way to install [[LLM]] after a PyTorch incompatibility appeared through Homebrew. The post suggests running `pipx install llm` followed by `llm python`, which gives an interpreter that already includes the library. The source uses pipx as a practical installation workaround rather than as a central subject.

## Related Entities

- [[entities/homebrew|Homebrew]]
- [[entities/llm|LLM]]
- [[entities/llm-python|llm-python]]

## Related Concepts

## Mentions in Source

- "For the moment I’ve removed the recommendation to install using Homebrew and replaced it with [pipx](https://pypa.github.io/pipx/) in a few places." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "I can tell people to `pipx install llm` and then run `llm python` to get a Python interpreter with the library already installed, without them having to mess around with virtual environments directly." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]