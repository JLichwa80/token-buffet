---
type: entity
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-12-08-weeknotes_cbd558]]"
tags:
  - "project"
---

# datasette-enrichments

> Stub created by the ingest candidate gate (prose+named) — [[sources/2024-04-10-weeknotes-llm-releases_18e6bc]] names this without treating it. Will be filled by the next ingest of a source that does.

datasette-enrichments is a Datasette plugin that provides tools for running enrichments against data stored in Datasette. The source lists version 0.3.2, released on 2024-04-09, as part of the Datasette Cloud release work. Enrichments are the mechanism behind plugins such as datasette-enrichments-gpt, which runs prompts over table rows. The source notes that many of these releases add descriptions to action menu items in Datasette Cloud. It forms part of the infrastructure that the author is building for that platform.

> "**[datasette-enrichments 0.3.2](https://github.com/datasette/datasette-enrichments/releases/tag/0.3.2)**—2024-04-09  
  Tools for running enrichments against data stored in Datasette" — [[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]

## New Information (2024-02-27-weeknotes-getting-ready-for-nicar)

- Datasette Enrichments is a Datasette project that runs data-enrichment operations, such as geocoding, over the records stored in a Datasette instance. (The existing description says what enrichments are for but does not state the geocoding example or the operation over stored records from this source.)
- Its documentation is hosted at enrichments.datasette.io. (A documentation location is a basic factual detail the page does not currently record.)
- It is closely tied to the geocoding plugin datasette-enrichments-opencage. (This names a specific related plugin that the page does not yet link to.)
- Simon Willison and Alex Garcia were putting the final touches on Datasette Enrichments, alongside Datasette Comments, so both would be in good shape for NICAR 2024. (This records the pre-NICAR 2024 development context and the collaborator, which the page lacks.)

## New Information (2024-02-09-weeknotes)

- Datasette Enrichments runs data-enrichment operations, such as geocoding, over the records stored in a Datasette instance. (The existing description covers enrichments in general but lacks the geocoding example and the operation over stored records.)
- Its documentation is hosted at enrichments.datasette.io. (A documentation location is a basic factual detail that the page does not record.)
- datasette-enrichments-opencage is a geocoding plugin closely tied to Datasette Enrichments. (This names a specific related plugin that the page does not yet link to.)
- datasette-enrichments-quickjs is a plugin for Datasette Enrichments, released as version 0.1a0 on 2024-02-09, that runs a custom JavaScript function against every row of a table to populate a new column, using the quickjs Python package wrapping the QuickJS engine. (This adds a concrete enrichment plugin and shows Enrichments as the extension point for row-level transformations, which the page does not yet record.)
- Simon Willison and Alex Garcia were putting the final touches on Datasette Enrichments, alongside Datasette Comments, ahead of NICAR 2024. (This records the pre-NICAR 2024 development context and collaborator, which the page lacks.)

## New Information (2023-12-08-weeknotes)

- Datasette Enrichments is a plugin framework for augmenting data in Datasette, described by Simon Willison as the biggest new Datasette feature in quite a while and implemented entirely as a plugin. Enrichments run transformations or data fetches against selected rows, such as geocoding addresses, executing a GPT prompt, or applying a regular expression. (The 2023-12-08 source is primarily about this framework and gives the core mechanism, which the page's description lacks.)
- Its documentation is hosted at enrichments.datasette.io, including a developer guide at enrichments.datasette.io/en/stable/developing.html. (A documentation location is a basic factual detail the page does not record, and the source gives it directly.)
- The datasette-enrichments plugin provides the mechanism for running enrichments, and other plugins depend on it to define enrichment options. (This explains the dependency structure between Datasette Enrichments and its plugins, which the page only describes in general terms.)
- Willison had built four enrichment plugins by 2023-12-08 and wrote extensive documentation to help others build more. (This records the early ecosystem size and documentation effort, which the page does not include.)
- Willison proposed a form of "persistent" enrichment, configured to run repeatedly against new or updated rows (for example, geocoding new addresses), enabled by sqlite-chronicle. (This planned capability links enrichments to change tracking and is not yet recorded on the page.)
- datasette-enrichments-opencage is a geocoding and reverse-geocoding plugin for Datasette Enrichments that uses OpenCage. (This names a specific related plugin the page does not yet link to.)
- datasette-enrichments-quickjs is a plugin for Datasette Enrichments that runs a custom JavaScript function against every row of a table to populate a new column, using the quickjs Python package. (This names another concrete enrichment plugin that the page does not yet link to.)
- datasette-enrichments-gpt, datasette-enrichments-re2, datasette-enrichments-jinja, and datasette-enrichments-opencage are enrichment plugins built by Willison and released in late 2023. (The page mentions datasette-enrichments-gpt only in passing and does not list the other enrichment plugins from the source.)

## Mentions in Source

- "It’s a plugin for Datasette Enrichments that takes advantage of the quickjs Python package—a wrapper around the excellent QuickJS engine—to support running a custom JavaScript function against every row in a table to populate a new column." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "We have a few new features that we’re putting the final touches on, in addition to ensuring features like [Datasette Enrichments](https://enrichments.datasette.io/) and [Datasette Comments](https://github.com/datasette/datasette-comments) are in good shape for the event." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "This is the biggest new Datasette feature to arrive in quite a while, and it’s entirely implemented as a plugin." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "The [datasette-enrichments](https://datasette.io/plugins/datasette-enrichments) plugin provides the mechanism for running these enrichments." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]