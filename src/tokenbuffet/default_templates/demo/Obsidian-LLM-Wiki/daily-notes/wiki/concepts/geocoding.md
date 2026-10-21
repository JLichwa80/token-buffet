---
type: concept
created: 2026-10-21
sources:
  - "[[sources/2023-12-08-weeknotes_cbd558]]"
tags: [terminology]
stub: true
generation_complete: true
---
# Geocoding

> Stub created by the ingest candidate gate (prose+named) — [[sources/2023-12-08-weeknotes_cbd558]] names this without treating it. Will be filled by the next ingest of a source that does.

Geocoding is the process of converting addresses into geographic coordinates. In this source it is the first example given of what a Datasette enrichment can do, alongside running GPT prompts and applying regular expressions. The author plans to use it as the motivating case for persistent enrichments, which would geocode new addresses as rows are added or updated. The release list also includes datasette-enrichments-opencage, which provides geocoding and reverse geocoding through OpenCage. Geocoding therefore serves as a concrete test case for the enrichment framework and the change-tracking mechanism.

> "The short version: you can now install plugins that can “enrich” data by running transformations (or data fetches) against selected rows—geocoding addresses, or executing a GPT prompt, or applying a regular expression." — [[sources/2023-12-08-weeknotes_cbd558]]
