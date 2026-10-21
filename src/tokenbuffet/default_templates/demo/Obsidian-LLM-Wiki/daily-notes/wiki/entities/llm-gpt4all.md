---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-07-16-weeknotes_8e11f0]]"
tags:
  - "project"
  - "other"
---

# llm-gpt4all

## Description

llm-gpt4all is a plugin for the [[LLM]] tool that adds support for the GPT4All collection of models. Version 0.3 was released on 24 January 2024 with improvements from three contributors. The release added access to model options such as `max_tokens`, allowed models to run without an internet connection, and documented where model files are stored. The release notes are quoted in full in the source post, which makes this plugin one of the most detailed examples of LLM ecosystem work in that update.

llm-gpt4all has been a plugin for the LLM tool since July 2023, when the author first added alternative model backends via plugins, and the author now recommends it as the easiest way to get started running local LLMs. In the author's weeknotes of 30 October 2023, the recommendation was stated directly: llm-gpt4all is the recommended plugin for getting started running local LLMs. Early versions printed debugging information that could not be hidden, a product-quality issue that Nomic AI fixed. Version 0.2, released on 24 October 2023, added GPU support on macOS.

llm-gpt4all version 0.1 was released on 12 July 2023, adding support for the GPT4All collection of models. It was one of three model plugins the author released alongside the new LLM version. The plugin provides 17 self-hosted models from the GPT4All project, installed with `pip install llm-gpt4all`. These self-hosted models are used through the same Python API as hosted OpenAI models.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/gpt4all|GPT4All]]
- [[entities/nomic-ai|Nomic AI]]
- [[entities/self-hosted-language-models|Self-hosted language models]]

## Related Concepts

- [[concepts/embedding-vector|Embeddings]]

## Mentions in Source

- "llm-gpt4all with 17 self-hosted models from the GPT4All project." — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]
- "The self-hosted models provided by the llm-gpt4all plugin work the same way:" — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]
- "As a result, `llm-gpt4all` is now my recommended plugin for getting started running local LLMs:" — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "My [LLM](https://llm.datasette.io/) tool has had a [llm-gpt4all](https://github.com/simonw/llm-gpt4all) plugin since I first added alternative model backends via plugins [in July](https://simonwillison.net/2023/Jul/12/llm/)." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "**[llm-gpt4all](https://github.com/simonw/llm-gpt4all)** got a release with improvements from three contributors." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I’ll quote [the release notes](https://github.com/simonw/llm-gpt4all/releases/tag/0.3) in full:" — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]