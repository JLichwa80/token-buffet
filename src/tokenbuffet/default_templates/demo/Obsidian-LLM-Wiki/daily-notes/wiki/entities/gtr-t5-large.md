---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "gtr-t5-large embeddings model"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

generation_complete: true
---

# gtr-t5-large

## Description

gtr-t5-large is a sentence embeddings model distributed through Hugging Face. The author ran it locally in Python to compute embeddings. It is an embeddings model, not a full generative language model in the GPT-3 style, and is comparable to the OpenAI embeddings API the author described weeks earlier. The model is small enough to run on a MacBook M2, and possibly on weaker machines. The author reports that its embeddings give very good results for finding similar content. It was the first language model the author found that ran on his own hardware, which he had wanted for a long time. The model is covered in a TIL titled "Calculating embeddings with gtr-t5-large in Python."

## Related Entities

- [[entities/nanogpt|nanoGPT]]

## Related Concepts

## Mentions in Source

- "[gtr-t5-large](https://huggingface.co/sentence-transformers/gtr-t5-large) isn’t a full GPT-3 style generative text language model: it’s an embeddings model, similar to the OpenAI embeddings API I [described a few weeks ago](https://simonwillison.net/2023/Jan/13/semantic-search-answers/)." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]