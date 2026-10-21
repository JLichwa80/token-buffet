---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "fine-grained permissions"
  - "finely-grained permissions"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# finely-grained permissions

## Definition

Finely-grained permissions are a [[Datasette]] mechanism for creating API tokens that can perform only a subset of the actions a user is allowed to perform. A token can be restricted to specific operations, so it does not carry the full authority of the user who created it.

## Key Characteristics

- Tokens are scoped to a subset of actions rather than granting everything the user can do.
- First described by the author in the 1.0a2 release notes.
- In 1.0a5, a table-level `view-table` restriction implies `view-database` and `view-instance` access. Before this change, a table-only token was denied access, which was a usability flaw.
- The change to the permission logic was verified with extensive automated tests. The author considers such tests essential for permission code.

## Applications

- Issuing API tokens that can read a single table without access to other tables in the same database.
- Giving scripts or third-party integrations narrow, revocable access to a Datasette instance.
- Hosted deployments, such as [[Datasette Cloud]], where tokens must limit what an external client can reach.

## Related Concepts

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "They provide a mechanism for creating an API token that’s only allowed to perform a subset of actions on behalf of the user." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "I [described finely-grained permissions](https://simonwillison.net/2022/Dec/15/datasette-1a2/#finely-grained-permissions) for access tokens in my annotated release notes for 1.0a2." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]