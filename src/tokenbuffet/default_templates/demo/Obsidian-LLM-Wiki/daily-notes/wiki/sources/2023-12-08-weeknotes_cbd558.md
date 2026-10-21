---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Weeknotes 8 December 2023"
  - "2023-12-08-weeknotes"
contentHash: 2651-2da86b86
source_file: "[[_Inbox/2023-12-08-weeknotes.md]]"
generation_complete: true
---

# 2023-12-08-weeknotes - Summary

## Source

- Original file: [[_Inbox/2023-12-08-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

This is Simon Willison's weeknotes post from 8 December 2023, which covers his recent work on [[entities/datasette|Datasette]] and related tools. The main highlight is [[entities/datasette-enrichments|Datasette Enrichments]], a plugin framework for running transformations or data fetches, such as geocoding, GPT prompts, or regular expressions, against selected rows. [[entities/alex-garcia|Alex Garcia]] released the first version of [[entities/datasette-comments|datasette-comments]], which lets users annotate individual rows. Willison also explored [[entities/sqlite-chronicle|sqlite-chronicle]], which uses triggers to track row inserts and updates with a table-wide version number. He released [[entities/datasette-chronicle|datasette-chronicle]] to expose this tracking in Datasette through a `?_since=VERSION` filter, and he plans to use it for persistent enrichments. The post also mentions a [[entities/newsroom-robots|Newsroom Robots]] podcast appearance and the [[entities/sqlite-utils|sqlite-utils]] 3.36 release, which adds STRICT table support.

## Key Entities

- [[entities/simon-willison|Simon Willison]]: author of the weeknotes and lead developer of the Datasette ecosystem
- [[entities/alex-garcia|Alex Garcia]]: developer who released the first version of datasette-comments
- [[entities/datasette-enrichments|Datasette Enrichments]]: plugin framework for running transformations against selected rows
- [[entities/datasette-comments|datasette-comments]]: plugin for leaving comments on individual rows
- [[entities/sqlite-chronicle|sqlite-chronicle]]: Python library for tracking table changes with a companion chronicle table
- [[entities/datasette-chronicle|datasette-chronicle]]: Datasette plugin that exposes sqlite-chronicle tracking
- [[entities/sqlite-utils|sqlite-utils]]: Python CLI and library for manipulating SQLite databases
- [[entities/datasette-cloud|Datasette Cloud]]: hosted Datasette service that provides context for several projects
- [[entities/newsroom-robots|Newsroom Robots]]: AI-in-journalism podcast on which Willison appeared
- [[entities/datasette|Datasette]]: open-source tool for exploring and publishing SQLite data

## Key Concepts

- [[concepts/chronicle-table|Chronicle table]]: the companion table that sqlite-chronicle maintains for each tracked table
- [[concepts/geocoding|Geocoding]]: an example of an enrichment that can run against new or updated rows

## Main Points

- **Datasette Enrichments** is the biggest new Datasette feature in a while and is implemented entirely as a plugin.
- **datasette-comments**, first released by Alex Garcia, lets users collaborate on finding stories in data by commenting on rows.
- **sqlite-chronicle** records insert and update timestamps with a table-wide version number and is the planned mechanism for persistent enrichments.
- **datasette-chronicle** adds table actions to enable change tracking and a `?_since=VERSION` filter for changed rows.
- Willison reported that `INSERT OR REPLACE INTO` queries in sqlite-chronicle do not behave as he expected (issue #7).
- **sqlite-utils 3.36** adds STRICT table support, contributed by Taj Khattra, which Willison cites as an example of an ideal pull request.

## Mentions in Source

- "I’ve built four of these so far, and I wrote some [extensive documentation](https://enrichments.datasette.io/en/stable/developing.html) to help people build more." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "I’m excited to see how people use and build further on this initial foundation." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "I first wrote about [sqlite-chronicle](https://github.com/simonw/sqlite-chronicle) in [weeknotes back in September](https://simonwillison.net/2023/Sep/17/weeknotes-embeddings/#sqlite-chronicle)." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "Alex Garcia released the first version of [datasette-comments](https://datasette.io/plugins/datasette-comments) as part of our continuing collaboration to build out Datasette Cloud." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "He wrote about that on the Datasette Cloud blog: **[Annotate and explore your data with datasette-comments](https://www.datasette.cloud/blog/2023/datasette-comments/)**." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "This is the biggest new Datasette feature to arrive in quite a while, and it’s entirely implemented as a plugin." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "The [datasette-enrichments](https://datasette.io/plugins/datasette-enrichments) plugin provides the mechanism for running these enrichments." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "Other plugins can then depend on it and define all manner of interesting options for enriching and transforming data." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "This is another capability I’ve been looking forward to for years: the plugin lets you leave comments on individual rows within a Datasette instance, in order to collaborate with others on finding stories in data." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]