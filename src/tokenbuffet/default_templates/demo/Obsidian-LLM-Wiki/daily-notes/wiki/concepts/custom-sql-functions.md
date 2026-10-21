---
type: concept
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "terminology"
aliases:
  - "User-defined SQL functions"
  - "UDFs"
  - "Custom SQL function"
---

# Custom SQL functions

## Definition

Custom SQL functions are user-defined functions that can be executed against SQLite databases. In sqlite-utils they are added through plugins: third-party code registers a function, and that function can then be called from SQL.

## Key Characteristics

- Defined by users or third-party code rather than built into SQLite or sqlite-utils.
- Added to a database through the [[Plugins|plugin system]] of [[sqlite-utils]].
- Once registered, they can be called from SQL queries.
- Exposed to the user in the [[litecli]]-based shell, which makes all registered functions available.
- One of the two plugin categories that sqlite-utils supports.
- Some SQL functions added by the SpatiaLite module can crash a Datasette instance, which led to the `default_allow_sql` setting in Datasette 0.64. This makes exposing custom SQL functions a crash risk, not just a data risk.
## Applications

- Extending SQLite queries with custom logic, such as transforming or computing values inline in SQL.
- Packaging reusable SQL logic as a plugin that others can install.
- Querying data interactively from the litecli-based shell with custom functions available alongside built-in ones.
- A custom SQL function can call an external API, such as the `chatgpt()` function in openai-to-sqlite, so a single query can write model results back into existing SQLite tables. This enriches data in place from inside SQL, without exporting it to another tool.
- Datasette users can add custom SQL functions that call the OpenAI APIs through the datasette-openai plugin. The author used this approach to build a Q&A interface over an existing document corpus, so the same query-time function pattern works for document question answering.
## Related Concepts

- [[concepts/plugins|Plugins]]

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/litecli|litecli]]
- [[entities/openai-to-sqlite|openai-to-sqlite]]
- [[entities/datasette|Datasette]]
- [[entities/datasette-openai|datasette-openai]]
- [[entities/spatialite|SpatiaLite]]

## Mentions in Source

- "I ended up adding a new mechanism to my `openai-to-sqlite` CLI tool—it can now execute SQL queries that can update existing tables with the results of a `chatgpt()` API call using a custom SQL function." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "I wrote more about that in [Enriching data with GPT3.5 and SQLite SQL functions](https://simonwillison.net/2023/Apr/29/enriching-data/)." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "There are two categories of plugins so far: plugins that add extra commands to the `sqlite-utils` CLI tool, and plugins that add extra custom SQL functions that can be executed against SQLite." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "which lets you run the following command to get a full `litecli` shell with all of the custom SQL functions from other plugins:" — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "custom SQL functions for querying the OpenAI APIs from Datasette" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "described my experiment using custom SQL functions in Datasette to provide a Q&A interface against an existing corpus of documents." — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]