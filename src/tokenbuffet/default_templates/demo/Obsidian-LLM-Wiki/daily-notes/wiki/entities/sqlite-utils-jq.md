---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "jq plugin"
sources:
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"

generation_complete: true
---

# sqlite-utils-jq

## Description

sqlite-utils-jq is a small plugin for [[sqlite-utils]] that adds a `jq()` SQL function, so jq programs can run inside SQL queries. It was inspired by a Hacker News comment and was written partly to exercise the new plugins framework in sqlite-utils. The plugin is installed with the `sqlite-utils install` command. It can also be combined with sqlite-utils-litecli to call jq from an interactive shell.

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]

## Related Concepts

## Mentions in Source

- "[sqlite-utils-jq](https://github.com/simonw/sqlite-utils-jq) adds a new `jq()` function which can be used to execute [jq](https://jqlang.github.io/jq/) programs as part of a SQL query." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]