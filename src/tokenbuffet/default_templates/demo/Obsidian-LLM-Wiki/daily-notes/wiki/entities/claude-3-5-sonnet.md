---
type: entity
created: 2026-10-20
updated: 2026-10-20
generation_complete: true
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"
  - "[[sources/2024-07-19-weeknotes_39632e]]"
  - "[[sources/2024-07-02-weeknotes_55c009]]"
tags:
  - "other"
aliases:
  - "Claude 3.5 Sonnet model"
  - "Claude Sonnet 3.5"
---

# Claude 3.5 Sonnet

## Description

Claude 3.5 Sonnet is an [[Anthropic]] model that the author used as the main code-writing assistant for two of the three LLM-powered tools in [[simonw/tools]]. The author states that it wrote almost every line of the Gemini bounding box tool and the [[Gemini Chat App]]. This makes it a concrete example of AI-assisted programming described in the source post. It is mentioned alongside [[Claude 3 Opus]] and [[Claude 3 Haiku]] as part of the development history of these tools.

Claude 3.5 Sonnet also proved useful outside tool-building. The author found it "great at helping refactor GitHub Actions YAML," which saved a lot of time. This is a second, non-tool use of the model: it refactored the GitHub Actions workflows behind the Datasette Cloud staging work.

Claude 3.5 Sonnet was released on 20 June 2024, and it was the model Simon Willison tried on launch day. He called it "quickly become my absolute favourite LLM." The [[simonw/llm-claude-3]] 0.4 plugin adds support for the model, so it can be accessed through the `llm` command-line tool.
## Related Entities

- [[entities/anthropic|Anthropic]]
- [[entities/claude-3-haiku|Claude 3 Haiku]]
- [[entities/simonwtools|simonw/tools]]
- [[entities/gemini-chat-app|Gemini Chat App]]

## Related Concepts

- [[concepts/claude-artifacts|Claude Artifacts]]

## New Information (2024-07-02-weeknotes)

- Claude 3.5 Sonnet was used to build a search-based RAG demonstration over the author's blog, to write code for several prototypes, and to create a tag cloud colour palette for the blog. (These are concrete real-world usage scenarios for the model that fit the Applications section.)
- The artifacts feature lets Claude 3.5 Sonnet write and display HTML, CSS and JavaScript, which the author used for several prototyping projects and an animated visualization in a keynote. (The artifacts capability is a defining feature of the model that the page does not describe.)

## Mentions in Source

- "Thankfully Claude 3.5 Sonnet is great at helping refactor GitHub Actions YAML, which has been saving me a lot of time." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]
- "All three of these tools made heavy use of AI-assisted development: Claude 3.5 Sonnet wrote almost every line of the last two, and the Haiku one was put together a few months ago using Claude 3 Opus." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]
- "We also got to try out the launched-that-day Claude 3.5 Sonnet, which has quickly become my absolute favourite LLM." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]
- "It is *so good* at writing code!" — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]