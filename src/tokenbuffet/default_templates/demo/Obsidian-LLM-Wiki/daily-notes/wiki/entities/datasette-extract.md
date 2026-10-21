---
type: entity
created: 2026-10-20
updated: 2026-10-20
generation_complete: true
sources:
  - "[[sources/2024-05-28-weeknotes_18b318]]"
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"
tags:
  - "project"
  - "other"
---

# datasette-extract

## Description

datasette-extract is a plugin for [[Datasette]] released at version 0.1a7 on 15 May 2024. It imports unstructured data, such as text and images, into structured tables. The author reports good results using it with [[GPT-4o]] for structured data extraction. He observes that GPT-4o reliably produces longer sequences of extracted rows from a given input. The plugin is a concrete example of how new model releases feed into the broader Datasette tooling ecosystem.

Datasette Extract is a plugin for Datasette that adds structured data extraction from unstructured text, powered by GPT-4 Turbo. The author had been developing it for some time before the April 2024 update. The 0.1a4 release (2024-04-09) updated the plugin for the new model releases, and the author published a demo video showing its capabilities.

datasette-extract was first released as version 0.1a3, which lets Datasette tables be populated from unstructured data such as pasted text or images. The author demonstrated the plugin in a lightning talk at NICAR 2024, having got it working just in time for the conference, and describes it as really effective. The plugin's data extraction is based on a variant of the OpenAI function-calling technique, which the author had documented in a [TIL note on OpenAI Python functions for data extraction](https://til.simonwillison.net/gpt3/openai-python-functions-data-extraction). The plugin's listing is on the [datasette.io plugin directory](https://datasette.io/plugins/datasette-extract).

The author first highlighted the plugin in the weeknotes post "The aftermath of NICAR" dated 16 March 2024, where it appeared among the release highlights. The post said the author would write more about the plugin in a future post.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/gpt-4o|GPT-4o]]
- [[entities/nicar|NICAR]]

## Related Concepts

- [[concepts/structured-data-extraction|Structured data extraction]]
- [[concepts/large-language-models|Large Language Models]]

## Mentions in Source

- "I need to write more about the latter one: it enables populating tables from unstructured content (using a variant of [this technique](https://til.simonwillison.net/gpt3/openai-python-functions-data-extraction)) and it’s really effective." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "I’ve been working on [Datasette Extract](https://datasette.io/plugins/datasette-extract) for a while now: it’s a plugin for Datasette that adds structured data extraction from unstructured text, powered by GPT-4 Turbo." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "Import unstructured data (text and images) into structured tables" — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "it seems to be able to more reliably produce a longer sequence of extracted rows from a given input." — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "[datasette-extract](https://datasette.io/plugins/datasette-extract), hinted at above, is a new plugin that enables tables in Datasette to be populated from unstructured data in pasted text or images." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "I got it working just in time for the conference." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]