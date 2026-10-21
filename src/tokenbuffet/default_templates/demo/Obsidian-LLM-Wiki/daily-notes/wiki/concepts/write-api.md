---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Datasette 1.0 write API"
  - "JSON write API"
sources:
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"

generation_complete: true
---

# write API

## Definition

The write API is a Datasette 1.0 alpha feature that lets clients write data into a Datasette instance over HTTP. It is the mechanism that enables automated data imports into [[Datasette Cloud]] instances.

## Key Characteristics

- Allows clients to write data into a Datasette instance over HTTP.
- Accepts CSV, TSV, or JSON data, as used by the [[dclient]] `insert` command.
- Access is controlled by the [[API tokens]] mechanism added to datasette-auth-tokens.
- Part of [[Datasette]] 1.0 alpha.

## Applications

- Automated data imports into [[Datasette Cloud]] instances.
- Writing CSV, TSV, or JSON data to external Datasette instances with the [[dclient]] `insert` command.
- Scripted or programmatic data ingestion from external systems over HTTP, gated by API tokens.

## Related Concepts

- [[concepts/api-tokens|API tokens]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/dclient|dclient]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "The Datasette 1.0 alphas introduced a write API." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "I shipped [dcloud 0.2](https://github.com/simonw/dclient/releases/tag/0.2) with a new `dclient insert` command that can read CSV, TSV or JSON data and write it to an external Datasette instance using that new [1.0 write API](https://docs.datasette.io/en/1.0a2/json_api.html#the-json-write-api)." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]