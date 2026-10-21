---
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-07-16-weeknotes_8e11f0]]"
tags:
  - "project"
---

type: entity
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2023-10-30-weeknotes_d4a215]]"]
tags: [other]
aliases: ["GPT4All", "gpt4all"]
---

# GPT4All

## Description

GPT4All is a free-to-use, locally running chatbot project from [[Nomic AI]] that runs language models without a GPU or internet connection. It wraps [[llama.cpp]] and other libraries in a polished desktop experience with Windows, macOS, and Ubuntu installers. Its Python core is published as the installable `gpt4all` package, and compiled wheels on PyPI mean a plain `pip install gpt4all` works without a compiler toolchain. Simon Willison uses GPT4All as the backend for the [[llm-gpt4all]] plugin for his [[LLM]] tool, and in October 2023 he recommended that plugin as the way to start running local LLMs.

The `llm-gpt4all` plugin (version 0.1, released 2023-07-12) added the GPT4All model collection to the LLM tool, giving it 17 self-hosted models from the project at gpt4all.io. Because these models run locally, they also worked offline: Simon Willison used them on a camping trip where he had no access to the OpenAI APIs.
## Related Entities

- [[entities/nomic-ai|Nomic AI]]
- [[entities/llm-gpt4all|llm-gpt4all]]

## Related Concepts

## Mentions in Source

- "Under the hood it’s mostly Python, and Nomic have done a fantastic job releasing that Python core as an [installable Python package](https://docs.gpt4all.io/gpt4all_python.html)—meaning you can literally `pip install gpt4all` to get almost everything you need to run a local language model!" — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "[llm-gpt4all](https://github.com/simonw/llm-gpt4all) with 17 self-hosted models from the [GPT4All](https://gpt4all.io/) project." — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]
- "The self-hosted models provided by the [llm-gpt4all](https://github.com/simonw/llm-gpt4all) plugin work the same way:" — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]
- "Plugin for LLM adding support for the GPT4All collection of models" — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]