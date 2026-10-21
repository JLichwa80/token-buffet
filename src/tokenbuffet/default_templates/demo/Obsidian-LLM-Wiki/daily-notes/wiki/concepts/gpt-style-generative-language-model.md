---
type: concept
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
tags: [terminology]
aliases:
  - "GPT-style language model"
  - "generative language model"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

---

# GPT-style generative language model

## Definition

A GPT-style generative language model is a language model that generates text one token at a time. It differs from an embeddings model, which maps text to vectors rather than producing new text.

## Key Characteristics

- Generates output sequentially, one token at a time
- Contrasted with embeddings models, which produce vector representations instead of text
- Output quality depends heavily on training data volume: small models trained on small corpora produce poor, low-quality text
- Small-scale training is feasible on consumer hardware: [[nanoGPT]] trained a small model on a MacBook M2
- Meaningful output would require training on terabytes of text over many years

## Applications

- Small-scale experiments to verify that the approach works at a limited scale, without expecting useful output
- Training a model from scratch on a personal corpus, such as a blog, to test whether it captures the author's writing style
- Learning and demonstration of how generative language models are trained, using tools such as [[nanoGPT]]

## Related Concepts

## Related Entities

- [[entities/nanogpt|nanoGPT]]
- [[entities/gtr-t5-large|gtr-t5-large]]

## Mentions in Source

- "... even more exciting, I *did* manage to train and run a GPT-style generative language model! I used [nanoGPT](https://github.com/karpathy/nanoGPT) by Andrej Karpathy, which trains really nicely on an M2." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]