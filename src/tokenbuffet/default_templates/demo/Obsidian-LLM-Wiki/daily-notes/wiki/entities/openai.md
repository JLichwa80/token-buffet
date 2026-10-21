---
type: entity
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"
  - "[[sources/2024-05-28-weeknotes_18b318]]"
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2023-11-22-weeknotes_49168f]]"
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
  - "[[sources/2023-07-16-weeknotes_8e11f0]]"
  - "[[sources/2023-05-10-weeknotes_35d224]]"
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "organization"
---

# OpenAI

## Description

OpenAI is an AI company whose LLM APIs, like those of Anthropic and Google Gemini, can be called directly from browser JavaScript without the special header that Anthropic requires, according to [[Simon Willison]]'s weeknotes, where OpenAI is cited only in this comparison. In November 2023, OpenAI held its DevDay conference, where it announced GPTs (customizable, shareable GPT configurations) and the new GPT-4 Turbo model with a 128,000 token limit. Willison attended, shipped [[LLM]] 0.12 with GPT-4 Turbo support, and built [[ospeak]] as a CLI for OpenAI's text-to-speech API. That same week, the board of the non-profit that controls OpenAI fired CEO [[Sam Altman]] over a vague accusation that he was "not consistently candid in his communications with the board", a situation still unfolding when the post was written. On April 9, 2024, OpenAI released non-preview GPT-4 Turbo, which integrated GPT-4 Vision directly into the model and was described by OpenAI as "Majorly improved". In May 2024, OpenAI released [[GPT-4o]], which Willison described as half the price of GPT-4 Turbo, around twice as fast, and slightly more capable, and he released LLM 0.14, datasette-extract 0.1a7, and datasette-enrichments-gpt 0.5 with support for it.

Willison's [[LLM]] tool was originally built around OpenAI's hosted models, such as gpt-3.5-turbo. Its plugin system, introduced in July 2023, extended it beyond the OpenAI collection, and its Python API works the same way for OpenAI and self-hosted models.
## Related Entities

- [[entities/openai-devday|OpenAI DevDay]]
- [[entities/sam-altman|Sam Altman]]
- [[entities/gpt-4-turbo|GPT-4 Turbo]]
- [[entities/llm|LLM]]
- [[entities/ospeak|ospeak]]

## Related Concepts

- [[concepts/gpts|GPTs]]

## New Information (2024-05-28-weeknotes)

- OpenAI released GPT-4o in May 2024; the author released several tools with support for it, including LLM 0.14, datasette-extract 0.1a7 and datasette-enrichments-gpt 0.5. (The existing Description covers only the browser-accessible API comparison, so the May 2024 GPT-4o release and the author's GPT-4o-based tools are new facts about the company's models.)
- GPT-4o is half the price of GPT-4 Turbo, around twice as fast, and appears to be slightly more capable. (This is a comparative trait of OpenAI's GPT-4o model that the page does not yet record.)

## New Information (2024-04-10-weeknotes-llm-releases)

- OpenAI released GPT-4 Turbo non-preview on April 9, 2024, integrating GPT-4 Vision directly into the model (previously separate), with function and JSON output support for image inputs; OpenAI described it as "Majorly improved". (This is a concrete fact about OpenAI's model releases that the page does not yet record.)
- OpenAI released GPT-4o in May 2024, and the author released several tools supporting it (LLM 0.14, datasette-extract 0.1a7, datasette-enrichments-gpt 0.5). (The GPT-4o release is a main product event for the company and is absent from the page's current description.)
- GPT-4o is half the price of GPT-4 Turbo, around twice as fast, and appears to be slightly more capable. (This is a defining comparative trait of OpenAI's GPT-4o model.)

## Mentions in Source

- "And then last Friday everything went completely wild, when the board of directors of the non-profit that controls OpenAI fired Sam Altman over a vague accusation that he was “not consistently candid in his communications with the board”." — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]
- "The biggest announcement at OpenAI DevDay was GPTs—the ability to create and share customized GPT configurations." — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]
- "OpenAI finally released the non-preview version of **GPT-4 Turbo**, integrating GPT-4 Vision directly into the model (previously it was separate)." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "OpenAI also claim that the new model is [“Majorly improved”](https://twitter.com/OpenAI/status/1777772582680301665) but no-one knows what they mean by that." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "The big new language model releases from May were OpenAI GPT-4o and Google’s Gemini Flash." — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "I’m also excited about GPT-4o—half the price of GPT-4 Turbo, around twice as fast and it appears to be slightly more capable too." — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "I figured out quite a few of the details of this while offline on a camping trip up in the Northern California redwoods, which forced the issue on figuring out how to work with LLMs that I could host on my own computer because I didn’t have a connection to access the OpenAI APIs." — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]