---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "llm python command"
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"

generation_complete: true
---

# llm-python

## Description

llm-python is a plugin for the [[LLM]] command-line tool that adds an `llm python` command. The command runs a Python interpreter inside the same virtual environment that LLM uses. This helps when LLM was installed through pipx or Homebrew and the user does not know where that environment is. The author uses it for debugging, such as inspecting a user's Python path. It is also intended for tutorials about the LLM Python library. It was released as version 0.1 on 2023-10-27.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/pytorch|PyTorch]]

## Related Concepts

## Mentions in Source

- "Installing this plugin adds a new `llm python` command, which runs a Python interpreter in same virtual environment as LLM—useful for if you installed LLM via `pipx` or Homebrew and don’t know where that virtual environment is located." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]