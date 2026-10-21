---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "MLC LLM"
  - "MLC Python library"
sources:
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"

generation_complete: true
---

# MLC

## Description

MLC is a Python library documented in the MLC LLM project docs, which the author used to get [[Llama 2]] running with GPU acceleration on an Apple Silicon Mac. The author describes it as "excellent" and credits it with making the setup work. The [[llm-mlc]] plugin for [[LLM]] depends on MLC's nightly wheels (`mlc-ai-nightly` and `mlc-chat-nightly`), which the setup process installs. In this role, MLC provides the runtime that llm-mlc uses to run local models.

## Related Entities

- [[entities/llm-mlc|llm-mlc]]
- [[entities/llama-2|Llama 2]]
- [[entities/llm|LLM]]

## Related Concepts

## Mentions in Source

- "I finally figured that out the other week, using the excellent [MLC Python library](https://mlc.ai/mlc-llm/docs/deploy/python.html)." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "There’s an additional installation step which I’ve not yet been able to automate fully—on an M1/M2 Mac run the following:" — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]