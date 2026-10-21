---
type: concept
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-10-22-weeknotes_1435b6]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
tags:
  - "terminology"
aliases:
  - "metadata.yaml"
  - "metadata.json"
---

# Datasette metadata

## Definition

Datasette metadata is the `metadata.yaml` file used by [[Datasette]] instances. It was first designed to describe data, such as license, source, and description. Over time it also came to hold plugin configuration, table-level settings, canned queries, and authentication controls. The project considers the name no longer accurate for this broader role.

## Key Characteristics

- Originally scoped to descriptive information about a Datasette instance: license, source, and description.
- Grew to also configure [[JavaScript plugin API|plugins]], table-level settings, canned queries, and the authentication system.
- Its name no longer matches its contents, which the project acknowledges.
- Being split: non-metadata settings (permissions, allow blocks, canned queries) are moving into a new configuration file, `datasette.yaml`.
- The split is a cleanup step in preparation for the Datasette 1.0 release.
- Over time, metadata.json also grew to hold plugin settings, default page sizes, default facets, and access permissions.
- The file was originally called metadata.json, which the author considers entirely inappropriate for what it actually does, and it began as a JSON file with that same name.
## Applications

- Documenting a Datasette instance or its tables with license, source, and description information.
- Configuring plugins and table-level settings for a Datasette instance.
- Defining canned queries and access permissions. Under the planned change, these move to `datasette.yaml`.
- Migrating existing projects from `metadata.yaml` to `datasette.yaml` as part of preparing for Datasette 1.0.
- The planned `datasette.yaml` (or `.json`) configuration file can be passed with `datasette -c path-to-file`, and its `settings` section can hold the same key/value pairs as the legacy `settings.json` used in configuration directory mode.
## Related Concepts

- [[concepts/javascript-plugin-api|JavaScript plugin API]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/alex-garcia|Alex Garcia]]

## Mentions in Source

- "[Metadata](https://docs.datasette.io/en/0.64.5/metadata.html) in Datasette was originally meant to support adding data about data—the license, source and description of data exposed through a Datasette instance." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]
- "Right from the very start of the project, Datasette has supported specifying metadata about databases—sources, licenses, etc, as a `metadata.json` file that can be passed to Datasette like this:" — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "The name `metadata.json` is entirely inappropriate for what the file actually does. It’s a mess." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]