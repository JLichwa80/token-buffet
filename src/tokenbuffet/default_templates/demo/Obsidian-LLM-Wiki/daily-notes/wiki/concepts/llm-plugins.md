---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "Plugins for LLM"
  - "LLM plugin system"
sources:
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"

generation_complete: true
---

# LLM plugins

## Definition

LLM plugins are a planned extension system for the [[LLM]] command-line tool. They would let third parties add commands, prompt templates, language model backends, and model-callable functions. The system is inspired by the plugin design of Datasette, and the author describes it as the feature he is most excited about. The work is still under active development.

## Key Characteristics

- Planned as an extension mechanism for the [[LLM]] tool rather than a fixed feature set.
- Covers four planned plugin categories:
  - **Command plugins**, which add new commands such as `llm search` or `llm embed`.
  - **Template plugins**, which install extra [[Prompt templates]].
  - **Model plugins**, which add support for more language model families.
  - **Function plugins**, which make new functions executable by the model.
- A model plugin on a development branch calls Google's PaLM 2 model through Google Vertex.
- The author hopes to add plugins for local models, such as those run by llama.cpp.
- Still under active development at the time of the source.

## Applications

- Adding search or embedding commands to the [[LLM]] tool without changing its core code.
- Installing shared prompt templates through [[Prompt templates]] packages.
- Connecting the [[LLM]] tool to hosted model providers or local models through model plugins.
- Letting a model call user-defined functions during a conversation through function plugins.

## Related Concepts

- [[concepts/prompt-templates|Prompt templates]]

## Related Entities

- [[entities/llm|LLM]]

## Mentions in Source

- "These are still baking, but this is the feature I’m most excited about." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "I’m planning the following categories of plugins to start with:" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "**Function plugins**. Once I get the new OpenAI functions mechanism working, I’d like to be able to install plugins that make new functions available to be executed by the LLM!" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]