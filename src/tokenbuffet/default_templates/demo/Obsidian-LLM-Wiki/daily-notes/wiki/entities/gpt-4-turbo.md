---
type: entity
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-05-28-weeknotes_18b318]]"
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2023-11-22-weeknotes_49168f]]"
tags:
  - "other"
---

# GPT-4 Turbo

> Stub created by the ingest candidate gate (prose+named) — [[sources/2024-05-28-weeknotes_18b318]] names this without treating it. Will be filled by the next ingest of a source that does.

GPT-4 Turbo is an OpenAI model that serves as the comparison baseline for GPT-4o. The author reports that GPT-4o costs half as much as GPT-4 Turbo, runs around twice as fast, and appears to be slightly more capable. The comparison shows why GPT-4o is attractive for the author's structured data extraction work. GPT-4 Turbo is therefore mentioned only as a reference point against GPT-4o.

> "I’m also excited about GPT-4o—half the price of GPT-4 Turbo, around twice as fast and it appears to be slightly more capable too." — [[sources/2024-05-28-weeknotes_18b318]]

## New Information (2024-04-10-weeknotes-llm-releases)

- OpenAI finally released the non-preview version of GPT-4 Turbo (April 9, 2024), integrating GPT-4 Vision directly into the model (previously vision was a separate model). (This is a defining trait of the model's release and capabilities, which the existing Key Characteristics section does not yet describe.)
- Vision mode now supports both functions and JSON output, previously unavailable for image inputs. (This is a specific capability of the model's vision mode that fits the defining traits section.)
- The author's Datasette Extract plugin (structured data extraction from unstructured text) and the datasette-enrichments-gpt plugin (version 0.4) were both updated to use GPT-4 Turbo. (These are real-world usage scenarios of GPT-4 Turbo that belong in the Applications section.)

## New Information (2023-11-22-weeknotes)

- OpenAI finally released the non-preview version of GPT-4 Turbo (April 9, 2024), integrating GPT-4 Vision directly into the model (previously vision was a separate model). (This describes a defining trait of the model's release and architecture, which fits the Key Characteristics section.)
- Vision mode now supports both functions and JSON output, previously unavailable for image inputs. (This is a specific capability of the model's vision mode, a defining trait rather than a usage scenario.)
- GPT-4 Turbo was announced at OpenAI DevDay (November 2023) and is 2-3x cheaper than GPT-4, faster, and has a new increased 128,000 token limit. (These are defining launch-time properties of the model (pricing, speed, context size) that the existing page does not describe.)
- The author's Datasette Extract plugin (structured data extraction from unstructured text) and the datasette-enrichments-gpt plugin (version 0.4) were both updated to use GPT-4 Turbo. (These are real-world usage scenarios of GPT-4 Turbo.)
- Simon Willison shipped LLM 0.12 on the day of the DevDay announcement with support for the new GPT-4 Turbo model. (This is a real-world integration of the model into a tool, which fits the usage scenarios.)

## Mentions in Source

- "OpenAI finally released the non-preview version of **GPT-4 Turbo**, integrating GPT-4 Vision directly into the model (previously it was separate)." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "Vision mode now supports both functions and JSON output, previously unavailable for image inputs." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "I shipped [LLM 0.12](https://llm.datasette.io/en/stable/changelog.html#v0-12) that day with support for the brand new GPT-4 Turbo model (2-3x cheaper than GPT-4, faster and with a new increased 128,000 token limit), and built [ospeak](https://simonwillison.net/2023/Nov/7/ospeak/) that evening as a CLI tool for working with their excellent new text-to-speech API." — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]