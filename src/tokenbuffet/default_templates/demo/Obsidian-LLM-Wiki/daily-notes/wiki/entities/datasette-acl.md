---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [other]
aliases:
  - "Datasette ACL plugin"
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"

generation_complete: true
---

# datasette-acl

## Description

datasette-acl is a [[Datasette]] plugin for advanced permission management, letting administrators grant access to users or groups. Simon Willison was building it in September 2024 when he found that [[Datasette]]'s core CSS styled every button inside a form, which broke plugins. He wanted the plugin to use [[Choices.js]] to offer a nicer interface for adding permissions, and that integration is what exposed the CSS conflict. He planned to write about the plugin separately. It is one of the main projects that drives the discussion of Datasette forms in the 2024-09-06 weeknotes.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/choices-js|Choices.js]]

## Related Concepts

## Mentions in Source

- "I’ve been working on a new Datasette plugin for permissions management, [datasette-acl](https://github.com/datasette/datasette-acl), which I’ll write about separately soon." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]
- "I wanted to integrate [Choices.js](https://github.com/Choices-js/Choices) with it, to provide a nicer interface for adding permissions to a user or group." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]