---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "fast-fks"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# sqlite-utils-fast-fks

## Description

sqlite-utils-fast-fks is a plugin for [[sqlite-utils]] that restores the faster method of adding foreign keys to an existing table, which the core library dropped in version 3.35. That release replaced the `writable_schema` approach with the [[sqlite-utils transform() method|transform() method]], which rebuilds the table and is slower. The plugin adds a `fast-fks` command that uses the original approach. The source's example adds a `country_id` foreign key to a `places` table. Simon Willison presents the plugin as an example of keeping removed features available as opt-in plugins.

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]

## Related Concepts

- [[concepts/sqlite-utils-transform-method|sqlite-utils transform() method]]

## Mentions in Source

- "Since [sqlite-utils supports plugins now](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/), I realized I could set a healthy precedent by making the removed feature available in a new plugin: [sqlite-utils-fast-fks](https://github.com/simonw/sqlite-utils-fast-fks), which provides the following command for adding foreign keys the fast, old way (provided your installation supports it):" — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]