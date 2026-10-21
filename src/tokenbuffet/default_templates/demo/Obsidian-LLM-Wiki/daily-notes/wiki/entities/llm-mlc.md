---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "llm-mlc plugin"
sources:
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"

generation_complete: true
---

# llm-mlc

## Description

llm-mlc is an LLM plugin built by [[Simon Willison]] that runs models through the [[MLC]] Python library. Willison released it in August 2023 as part of his [[LLM]] tooling, after plugin support had been added to LLM a few weeks earlier. He presented it as possibly one of the easiest ways to run [[Llama 2]] on an Apple Silicon Mac with GPU acceleration. The setup requires installing LLM, installing the llm-mlc plugin, and installing the MLC nightly wheels, followed by `llm mlc setup`, which configures `git-lfs` for model downloads. Users then download Llama 2 with a single `llm mlc download-model` command and run prompts against it through an alias such as `llama2`. Willison acknowledged that the setup still involves more steps than he would like.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/llama-2|Llama 2]]
- [[entities/mlc|MLC]]

## Related Concepts

## Mentions in Source

- "I built a new plugin for LLM called [llm-mlc](https://github.com/simonw/llm-mlc)." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "I think this may now be one of the easiest ways to run Llama 2 on an Apple Silicon Mac with GPU acceleration." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]