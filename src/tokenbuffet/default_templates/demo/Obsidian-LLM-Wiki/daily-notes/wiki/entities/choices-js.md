---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [other]
aliases:
  - "Choices"
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"

generation_complete: true
---

# Choices.js

## Description

Choices.js is a JavaScript library that turns form inputs into enhanced select and tag widgets. In the 2024-09-06 weeknotes, Simon Willison wanted to use it in [[datasette-acl]] to make adding users or groups to a permission list easier. His first integration showed visual glitches, because [[Datasette]]'s core CSS styled the library's remove buttons as large blank boxes. The fix was to scope Datasette's rules to a core class so plugins like datasette-acl can style their own elements. Choices.js is therefore a third-party dependency whose integration exposed the CSS conflict.

## Related Entities

- [[entities/datasette-acl|datasette-acl]]
- [[entities/datasette|Datasette]]

## Related Concepts

## Mentions in Source

- "I wanted to integrate [Choices.js](https://github.com/Choices-js/Choices) with it, to provide a nicer interface for adding permissions to a user or group." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]
- "The weird visual glitches are caused by Datasette’s core CSS, which included [the following rule](https://github.com/datasette/datasette/blob/92c4d41ca605e0837a2711ee52fde9cf1eea74d0/datasette/static/app.css#L553-L564):" — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]