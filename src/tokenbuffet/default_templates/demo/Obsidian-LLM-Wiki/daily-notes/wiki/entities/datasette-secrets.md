---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [organization]
aliases:
  - "Datasette Secrets"
sources:
  - "[[sources/2024-04-23-weeknotes_a3933c]]"

generation_complete: true
---

# datasette-secrets

## Description

datasette-secrets is a draft [[Datasette]] plugin for managing secrets such as API keys so that other Datasette plugins can use them. It provides a UI for entering registered secrets, available only to administrator-level users who hold the `manage-secrets` permission. Secrets are stored encrypted in the SQLite database using symmetric encryption from the Python cryptography library, with the encryption key kept separately. The plugin is needed because plugins such as [[datasette-extract]], [[datasette-enrichments-gpt]], datasette-enrichments-opencage and [[datasette-query-assistant]] each require API keys, and [[Datasette Cloud]] and Datasette Desktop users should be able to supply their own keys. Version 0.1a1 was released on 2024-04-23; the next step is to ship plugins that depend on it.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/datasette-query-assistant|datasette-query-assistant]]

## Related Concepts

## Mentions in Source

- "[datasette-secrets](https://github.com/datasette/datasette-secrets) is another draft project, this time a Datasette plugin." — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]
- "`datasette-secrets` adds a UI for entering registered secrets, available to administrator level users with the `manage-secrets` permission." — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]