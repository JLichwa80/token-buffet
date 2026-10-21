---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
tags:
  - "project"
aliases:
  - "datasette-upload-csvs 0.9"
---

# datasette-upload-csvs

## Description

datasette-upload-csvs is a Datasette plugin for uploading CSV files and converting them into database tables. Version 0.9 was released on 2024-01-30. This release added the ability to upload CSVs into a specified database, instead of always using the first available one. Simon Willison also re-engineered the plugin's threading strategy, as described in GitHub issue 38 of the project. The plugin was tested against the Datasette 1.0 alpha series as well as 0.x stable releases. The weeknotes list it under "significant updates to existing plugins."

The plugin's progress bar needs somewhere to store data that regular Datasette users should not see. The Datasette Cloud team cited this as one of the examples that motivated expanding the `_internal` database.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/datasette-auth-tokens|datasette-auth-tokens]]
- [[entities/alex-garcia|Alex Garcia]]

## Related Concepts

## Mentions in Source

- "In working on Datasette Cloud we realized that it’s actually quite common for plugins to need somewhere to store data that shouldn’t necessarily be visible to regular users of a Datasette instance—things like tokens created by [datasette-auth-tokens](https://datasette.io/plugins/datasette-auth-tokens), or the progress bar mechanism used by [datasette-upload-csvs](https://datasette.io/plugins/datasette-upload-csvs)." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "datasette-upload-csvs got a long-overdue improvement allowing it to upload CSVs to a specified database, rather than just using the first available one." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "As part of this I completely re-engineered how it works in terms of threading strategies, as described in issue 38." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]