---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Steampipe plugins"
  - "Steampipe extension"
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"

generation_complete: true
---

# Steampipe extensions

## Description

Steampipe extensions are plugins for the [[entities/steampipe|Steampipe]] tool that the author wanted to run inside SQLite. The [[entities/sqlite-utils-shell|sqlite-utils-shell]] 0.3 release added the `--load-extension` option, which allows Steampipe extensions to be loaded into SQLite. A TIL in the 2023-12-31 weeknotes documents how to run them in [[entities/sqlite-utils|sqlite-utils]] and [[entities/datasette|Datasette]]. They are a concrete integration point in the post's tooling work.

## Related Entities

- [[entities/sqlite-utils-shell|sqlite-utils-shell]]
- [[entities/datasette|Datasette]]

## Related Concepts

## Mentions in Source

- "The [sqlite-utils-shell](https://github.com/simonw/sqlite-utils-shell) plugin now supports the `--load-extension` option—I added this to let it be used with [Steampipe extensions](https://til.simonwillison.net/sqlite/steampipe)." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "* [Running Steampipe extensions in sqlite-utils and Datasette](https://til.simonwillison.net/sqlite/steampipe)—2023-12-21" — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]