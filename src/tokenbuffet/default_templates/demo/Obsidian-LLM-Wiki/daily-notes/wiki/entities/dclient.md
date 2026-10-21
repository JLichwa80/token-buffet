---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
tags:
  - "project"
aliases:
  - "dclient CLI"
---

# dclient

## Description

dclient is a client CLI utility for interacting with remote [[Datasette]] instances. It can run queries against a Datasette instance, manage named aliases for instances, and insert data into tables through the JSON write API. Version 0.3, released 2024-02-25, added streaming support: the `--interval` and `--batch-size` options control when batched records are written to the API. It targets Datasette 1.0 alpha instances that expose the write API, such as those on [[Datasette Cloud]], and is one of the tools that extends the Datasette ecosystem. It is a command-line utility for interacting with Datasette instances through their API, and it is also referred to as "dclient CLI" and, in early development, "dcloud".

Version 0.2, released 2023-07-24, added a `dclient insert` command that reads CSV, TSV or JSON data and writes it to an external Datasette instance through the Datasette 1.0 write API. Before the public 0.2 release, the tool was developed quietly under the working name "dcloud".

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/sqlite-utils|sqlite-utils]]

## Related Concepts

- [[concepts/write-api|write API]]

## Mentions in Source

- "I’ve been quietly working on a new CLI utility for interacting with Datasette instances via the API, called `dcloud`." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "dclient provides a tool for interacting with a remote Datasette instance. You can use it to run queries:" — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "The 0.3 release adds improved support for streaming data into a table. You can run a command like this:" — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "I shipped [dcloud 0.2](https://github.com/simonw/dclient/releases/tag/0.2) with a new `dclient insert` command that can read CSV, TSV or JSON data and write it to an external Datasette instance using that new [1.0 write API](https://docs.datasette.io/en/1.0a2/json_api.html#the-json-write-api)." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]