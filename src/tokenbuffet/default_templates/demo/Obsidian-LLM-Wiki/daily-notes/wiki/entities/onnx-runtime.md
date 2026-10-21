---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "ONNX"
  - "ORT"
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
generation_complete: true
---

# ONNX Runtime

## Description

ONNX Runtime is an inference engine that the onnx_embedding_models library wraps, according to the 2024-02-09 weeknotes. The [[llm-embed-onnx]] plugin builds on that library, so ONNX Runtime sits beneath the embedding models that the plugin makes available to the LLM tool. The source describes it as a powerful runtime. It appears only as a dependency in the context of LLM embedding support, so the source gives no details on its features, versions, or other uses. It is relevant to [[Embeddings]] because it executes the embedding models.

## Related Entities

- [[entities/llm-embed-onnx|llm-embed-onnx]]

## Related Concepts

- [[concepts/embedding-vector|Embeddings]]

## Mentions in Source

- "is a thin wrapper on top of onnx\_embedding\_models by Benjamin Anderson which itself wraps the powerful ONNX Runtime." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]