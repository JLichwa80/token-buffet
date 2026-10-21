---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
tags:
  - "project"
aliases:
  - "Datasette write UI"
---

# datasette-write-ui

## Description

[[entities/alex-garcia|Alex Garcia]] created [[entities/datasette-write-ui|datasette-write-ui]], a plugin for Datasette designed to let [[entities/datasette-cloud|Datasette Cloud]] users insert, edit, and delete rows directly within their tables. Introduced through an official post on the Datasette Cloud blog, the tool significantly expanded interactive data management capabilities. Its development inspired Simon Willison to release an updated version of [[entities/datasette-edit-schema|datasette-edit-schema]]. In combination with schema editing capabilities, [[entities/datasette-write-ui|datasette-write-ui]] equips [[entities/datasette-cloud|Datasette Cloud]] with a comprehensive suite of features for creating and populating tables backed by a [[concepts/json-write-api|JSON write API]].

Datasette previously had no built-in interface for editing rows, and [[entities/datasette-write-ui|datasette-write-ui]] adds one for editing, inserting, and deleting rows. The plugin was written by [[entities/alex-garcia|Alex Garcia]] while he worked with Simon Willison to get [[entities/datasette-cloud|Datasette Cloud]] ready for general availability.

The plugin was announced in a Datasette Cloud blog post titled "Introducing datasette-write-ui: a Datasette plugin for editing, inserting, and deleting rows," and is published on datasette.io. The announcement framed it as the first user interface in Datasette for editing, inserting, and deleting rows.

## Related Entities

- [[entities/alex-garcia|Alex Garcia]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/datasette-edit-schema|datasette-edit-schema]]
- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/json-write-api|JSON write API]]

## Mentions in Source

- "[Introducing datasette-write-ui: a Datasette plugin for editing, inserting, and deleting rows](https://www.datasette.cloud/blog/2023/datasette-write-ui/) introduces a brand new plugin, [datasette-write-ui](https://datasette.io/plugins/datasette-write-ui)—which finally adds a user interface for editing, inserting and deleting rows to Datasette." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "Combine that with datasette-write-ui and Datasette Cloud now has a full set of features for building, populating and editing tables—backed by a comprehensive JSON API." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "`datasette-write-ui` is particularly notable because it was written by Alex Garcia, who is now working with me to help get Datasette Cloud ready for general availability." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]