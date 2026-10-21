---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
tags:
  - "other"
aliases:
  - "Homebrew package manager"
  - "brew"
---

# Homebrew

## Description

Homebrew is a package manager through which the [[LLM]] command-line tool was distributed. In the week before the post, the LLM package for Homebrew was upgraded to Python 3.12, but [[PyTorch]] did not yet support that Python version. As a result, the base LLM installed through Homebrew worked, while plugins that depend on PyTorch, such as [[llm-embed-jina]], failed with errors. The author removed the Homebrew installation recommendation in several places and recommended [[pipx]] instead, and opened an issue to find a better long-term installation solution.

LLM is available in Homebrew core, so installing the tool takes a single command: `brew install llm`.
## Related Entities

- [[entities/pytorch|PyTorch]]
- [[entities/llm|LLM]]
- [[entities/llm-embed-jina|llm-embed-jina]]
- [[entities/pipx|pipx]]

## Related Concepts

## Mentions in Source

- "This means that while base LLM installed from Homebrew works fine, attempts to install things like my new [llm-embed-jina](https://github.com/simonw/llm-embed-jina) plugin fail with [weird errors](https://github.com/simonw/llm-embed-jina/issues/5)." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "LLM is [available in Homebrew core now](https://formulae.brew.sh/formula/llm), so getting Llama 2 working is as simple as:" — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]