---
type: concept
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-09-30-weeknotes_8d48b1]]"
  - "[[sources/2023-12-31-weeknotes_456c53]]"
tags:
  - "terminology"
aliases:
  - "Plugin architecture"
---

# Plugin system

## Definition

A plugin system is a software design in which a host application can be extended by separately developed modules, or plugins, without changing its core code.

## Key Characteristics

- The host application exposes extension points that plugins hook into.
- Plugins are developed and released separately from the host's core code.
- Extending the host does not require modifying its core code.
- Individual plugins are packaged and distributed as independent units.

## Applications

- **Django plugins:** In September 2024, Simon Willison wrote and released [[DJP]], a plugin system for [[Django]], ahead of his [[DjangoCon US 2024]] talk on plugin systems. Several releases in the same month are Django plugins built on this model, including django-plugin-blog and llm-gemini.
- **Cross-project ecosystems:** The same model links the Django work to the [[llm]] command-line tool and [[Datasette]], where plugins extend the host tool's functionality.
- **Conference-driven development:** Preparing a talk on plugin systems led to building one, as described in [[Conference-driven development]].
- The LLM tool's plugin system has really started to pay off, with many model providers and local runtimes now supported as plugins, such as llm-mistral, llm-gemini, and llm-llama-cpp.
- The Datasette plugin pattern includes datasette-plot, which extends the base Datasette application.
## Related Concepts

- [[concepts/conference-driven-development|Conference-driven development]]
- [[concepts/using-llms-for-code|Using LLMs for code]]

## Related Entities

- [[entities/djp|DJP]]
- [[entities/django|Django]]
- [[entities/djangocon-us-2024|DjangoCon US 2024]]
- [[entities/llm|llm]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "My talk at DjangoCon was about plugin systems, and in a classic example of conference-driven development I ended up writing and releasing a new plugin system for Django in preparation for that talk." — [[_Inbox/2024-09-30-weeknotes|2024-09-30-weeknotes]]
- "A blog for Django as a DJP plugin." — [[_Inbox/2024-09-30-weeknotes|2024-09-30-weeknotes]]
- "LLM plugin to access Google’s Gemini family of models" — [[_Inbox/2024-09-30-weeknotes|2024-09-30-weeknotes]]
- "* [Many options for running Mistral models in your terminal using LLM](https://simonwillison.net/2023/Dec/18/mistral/), demonstrating how LLM’s plugins system has really started to pay off." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]