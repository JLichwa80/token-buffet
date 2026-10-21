---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "LLM function plugins"
sources:
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"

generation_complete: true
---

# Function plugins

## Definition

Function plugins are a planned category of [[LLM plugins]] that would make new functions available for the [[LLM]] to execute. Installing a function plugin would add a callable function, extending what the model can do during a session. The author plans to build them after the [[OpenAI functions mechanism]] is working.

## Key Characteristics

- Planned as the last of the four plugin categories in the author's starting scope
- Extends the model's abilities by adding callable functions, rather than changing its text output
- Installed by the user as a plugin
- Depends on the [[OpenAI functions mechanism]], making it the most technically dependent of the planned plugin categories
- Scheduled to be built after that mechanism is working

## Applications

- Letting the model call a user-installed function during a session to perform an action or fetch information it cannot otherwise access
- Extending a [[LLM plugins]] system with new callable capabilities once the underlying function-calling mechanism is in place

## Related Concepts

- [[concepts/llm-plugins|LLM plugins]]
- [[concepts/openai-functions|OpenAI functions mechanism]]

## Related Entities

- [[entities/llm|LLM]]

## Mentions in Source

- "**Function plugins**. Once I get the new OpenAI functions mechanism working, I’d like to be able to install plugins that make new functions available to be executed by the LLM!" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "All of this is under active development at the moment." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]