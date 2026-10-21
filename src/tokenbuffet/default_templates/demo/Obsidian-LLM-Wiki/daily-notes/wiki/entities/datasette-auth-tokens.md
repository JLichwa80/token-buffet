---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
tags:
  - "project"
  - "other"
---

# datasette-auth-tokens

> Stub created by the ingest candidate gate (prose+named) — 2024-02-27-weeknotes-getting-ready-for-nicar names this without treating it. Will be filled by the next ingest of a source that does.

datasette-auth-tokens is a Datasette plugin for authenticating access with API tokens. Version 0.4a9, released 2024-02-20, is a small cosmetic bug fix. The source describes the release only briefly. The plugin is part of the wider Datasette authentication and permissions ecosystem.

> "> * **[datasette-auth-tokens 0.4a9](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a9)**—2024-02-20  
>   Datasette plugin for authenticating access using API tokens" — 2024-02-27-weeknotes-getting-ready-for-nicar
## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/database-backed-access-tokens|database-backed access tokens]]
- [[concepts/write-api|write API]]
- [[concepts/api-tokens|API tokens]]
- [[concepts/plugins|Plugins]]

## New Information (2023-09-17-weeknotes-embeddings)

- Willison extended datasette-auth-tokens to support the database-backed access tokens used by Datasette Cloud, in version 0.4a3 released 2023-08-31. (The source adds the plugin's Datasette Cloud token-support history, which the page does not yet describe.)
- Database-backed tokens can be revoked and record when they were last used, which signed tokens cannot easily do. (This explains the design rationale for the plugin's database-backed tokens, a fact not on the page.)
- Datasette Cloud (The source links this plugin's database-backed token work to Datasette Cloud, which is not yet linked from the page.)
- database-backed access tokens (The source names database-backed access tokens as the concept this plugin work implements.)

## New Information (2023-08-30-datasette-plus-weeknotes)

- Release 0.4a2 of datasette-auth-tokens shipped on 2023-08-29, as listed in the week's releases. (This is a dated release fact the page lacks, and the existing page already tracks version history under New Information.)
- The source cites datasette-auth-tokens as a concrete example of a plugin needing private storage for data not meant to be visible to regular Datasette users, such as the tokens it creates. This is a concrete case behind the decision to expand the _internal database for plugin-private storage. (This explains the plugin's role in the design rationale for plugin-private storage, which the page does not yet describe.)

## New Information (2023-08-05-weeknotes-plugins)

- Version 0.4a0 was released in preview on 2023-07-17, extending the plugin so that API tokens can be both created and revoked interactively, which Datasette Cloud needed for automatic data imports. (This dated release and its interactive create/revoke feature are not yet recorded on the page, which only tracks versions 0.4a2, 0.4a3, and 0.4a9.)
- The plugin is the authentication mechanism underpinning the write API workflow for Datasette Cloud's automatic data imports. (This states the plugin's role in the write API workflow, which the Description section does not yet cover.)

## Mentions in Source

- "I ended up building that into the existing `datasette-auth-tokens` plugin, released in preview in the [datasette-auth-tokens 0.4a0](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a0) alpha." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "In working on Datasette Cloud we realized that it’s actually quite common for plugins to need somewhere to store data that shouldn’t necessarily be visible to regular users of a Datasette instance—things like tokens created by [datasette-auth-tokens](https://datasette.io/plugins/datasette-auth-tokens), or the progress bar mechanism used by [datasette-upload-csvs](https://datasette.io/plugins/datasette-upload-csvs)." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "Datasette Cloud’s API works using database-backed access tokens, to ensure users can revoke tokens if they need to (something that’s not easily done with purely signed tokens) and that each token can record when it was most recently used." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]