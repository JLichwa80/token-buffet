---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [other]
aliases:
  - "Datasette desktop app"
sources:
  - "[[sources/2024-04-23-weeknotes_a3933c]]"

generation_complete: true
---

# Datasette Desktop

## Description

Datasette Desktop is a version of [[Datasette]] that the author names alongside [[Datasette Cloud]] as a deployment target. In both cases, end users run the software without managing their own environment. The author wants these users to be able to bring their own API keys, which motivated the [[datasette-secrets]] plugin. Today, plugin keys are set through environment variables, which is awkward for non-technical users. Datasette Desktop is therefore one of the reasons for building secret management into Datasette.

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/datasette|Datasette]]
- [[entities/datasette-secrets|datasette-secrets]]

## Related Concepts

## Mentions in Source

- "Currently those keys are set using environment variables, but for both [Datasette Cloud](https://www.datasette.cloud) and [Datasette Desktop](https://datasette.io/desktop) I’d like users to be able to bring their own keys, without messing around with their environment." — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]
- "I’m increasingly finding a need for Datasette plugins to access secrets—things like API keys." — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]