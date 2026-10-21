---
type: source
created: 2026-10-20
updated: 2026-10-20
tags: [other]
aliases:
  - "Three major LLM releases in 24 hours (plus weeknotes)"
  - "2024-04-10-weeknotes-llm-releases"
contentHash: 2c05-6d807b9d
source_file: "[[_Inbox/2024-04-10-weeknotes-llm-releases.md]]"
generation_complete: true
---

# 2024-04-10-weeknotes-llm-releases - Summary

## Source

- Original file: [[_Inbox/2024-04-10-weeknotes-llm-releases.md]]
- Ingested: 2026-10-20

## Core Content

Simon Willison's weeknotes post of April 10, 2024 opens with a review of three major LLM releases from April 9, 2024 (US Pacific time). [[entities/google-gemini-pro-1-5|Google Gemini Pro 1.5]] reached general availability with a free API tier of 50 requests per day, and it gained audio input and system prompt support. [[entities/openai|OpenAI]] released the non-preview [[entities/gpt-4-turbo|GPT-4 Turbo]], which integrates [[entities/gpt-4-vision|GPT-4 Vision]] directly into the model. [[entities/mistral|Mistral]] released [[entities/mixtral-8x22b|Mixtral 8x22B]] as a BitTorrent magnet link. [[entities/cohere|Cohere]]'s [[entities/command-r+|Command R+]] reached position 6 on the [[entities/lmsys-chatbot-arena-leaderboard|LMSYS Chatbot Arena Leaderboard]], the highest ranking yet for an [[concepts/open-weights-model|open weights model]]. The rest of the post covers the author's own releases, including [[entities/datasette-extract|Datasette Extract]], [[entities/datasette-enrichments-gpt|datasette-enrichments-gpt]], and [[entities/llm-gemini|llm-gemini]] 0.1a2, which added [[concepts/system-prompt|system prompt]] support. The author notes that system prompts are not a guaranteed defense against [[concepts/prompt-injection|prompt injection]].

## Key Entities

- [[entities/google-gemini-pro-1-5|Google Gemini Pro 1.5]]: 1 million token context model, generally available April 9, 2024
- [[entities/gpt-4-turbo|GPT-4 Turbo]]: non-preview release with integrated vision
- [[entities/gpt-4-vision|GPT-4 Vision]]: image input capability, now part of GPT-4 Turbo
- [[entities/openai|OpenAI]]: released the non-preview GPT-4 Turbo
- [[entities/mistral|Mistral]]: released Mixtral 8x22B via a magnet link
- [[entities/mixtral-8x22b|Mixtral 8x22B]]: openly licensed model, about 281GB
- [[entities/command-r+|Command R+]]: Cohere's open model, position 6 on the LMSYS leaderboard
- [[entities/cohere|Cohere]]: developer of Command R+
- [[entities/lmsys-chatbot-arena-leaderboard|LMSYS Chatbot Arena Leaderboard]]: public model ranking used as the benchmark
- [[entities/llm-gemini|llm-gemini]]: the author's plugin for Gemini models, version 0.1a2 added system prompts
- [[entities/datasette-extract|Datasette Extract]]: structured data extraction plugin, updated to GPT-4 Turbo
- [[entities/datasette-enrichments-gpt|datasette-enrichments-gpt]]: runs prompts over table data, version 0.4 switched to GPT-4 Turbo
- [[entities/datasette-cloud|Datasette Cloud]]: hosted service that much of the author's recent work supports
- [[entities/llm|LLM]]: the author's command-line tool and Python library for working with LLMs
- [[entities/datasette-enrichments|datasette-enrichments]], [[entities/datasette-embeddings|datasette-embeddings]], [[entities/files-to-prompt|files-to-prompt]], [[entities/llm-command-r|llm-command-r]], [[entities/llm-cmd|llm-cmd]]: other releases listed in the post

## Key Concepts

- [[concepts/free-tier|Free tier]]: no-cost API usage allowance, here 50 requests per day for Gemini Pro 1.5
- [[concepts/system-prompt|System prompt]]: extra instructions passed to an LLM alongside the main input
- [[concepts/prompt-injection|Prompt injection]]: malicious input overriding an LLM's instructions
- [[concepts/open-weights-model|Open weights model]]: a model whose trained weights are publicly available
- [[concepts/structured-data-extraction|Structured data extraction]]: turning unstructured text into structured tables with an LLM
- [[concepts/embedding-vector|Embedding vector]]: numeric representation used by the author's datasette-embeddings release
- [[concepts/weeknotes|Weeknotes]]: short, regular posts summarizing recent work

## Main Points

- **Three major releases in 24 hours (April 9, 2024):** Gemini Pro 1.5 general availability, GPT-4 Turbo non-preview with vision, and the Mixtral 8x22B torrent release.
- **Command R+ leaderboard milestone:** position 6 on the LMSYS Chatbot Arena Leaderboard, the highest ranking for an open weights model at that time.
- **Gemini Pro 1.5 access:** no waitlist, 180 countries, a free tier of 50 requests per day rate-limited to 2 per minute, and paid pricing of $7 per million input tokens and $21 per million output tokens beyond that.
- **Ecosystem updates:** the author's Datasette plugins were ported to GPT-4 Turbo, and llm-gemini 0.1a2 added system prompt support.
- **Caveat on system prompts:** they are useful for non-adversarial situations but do not reliably prevent prompt injection.

## Mentions in Source

- "11:01am: Google Gemini Pro 1.5 hits general availability, here’s [the blog post](https://developers.googleblog.com/2024/04/gemini-15-pro-in-public-preview-with-new-features.html)—their 1 million token context GPT-4 class model now has no waitlist, is available to anyone in 180 countries (not including Europe or the UK as far as I can tell) and most impressively all the API has a **free tier** that allows up to 50 requests a day, though rate limited to 2 per minute." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "Gemini Pro also now support audio inputs and system prompts." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "OpenAI finally released the non-preview version of **GPT-4 Turbo**, integrating GPT-4 Vision directly into the model (previously it was separate)." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "Vision mode now supports both functions and JSON output, previously unavailable for image inputs." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "6:20pm (3:20am in their home country of France): Mistral [tweet a link](https://twitter.com/MistralAI/status/1777869263778291896) to a 281GB magnet BitTorrent of **Mixtral 8x22B**—their latest openly licensed model release, significantly larger than their previous best open model Mixtral 8x7B." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "I’ve not seen anyone get this running yet but it’s likely to perform extremely well, given how good the original Mixtral was." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]