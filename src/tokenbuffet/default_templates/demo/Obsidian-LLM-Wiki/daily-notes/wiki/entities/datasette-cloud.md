---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-08-weeknotes_cbd558]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
tags:
  - "project"
aliases:
  - "demos.datasette.cloud"
---

# Datasette Cloud

## Description

Datasette Cloud is the hosted Datasette service that the weeknotes refer to as the context for several projects. [[datasette-comments]] was built as part of a collaboration to develop it, with [[Alex Garcia]] involved in the work. [[Simon Willison]] runs [[datasette-chronicle]] against the documents table on demos.datasette.cloud, and that table is populated through GitHub scheduled actions and the Datasette API. The Datasette Cloud blog hosts the write-ups on datasette-comments and the Datasette Cloud API. Willison first spotted the INSERT OR REPLACE issue while working with this table.

Datasette Cloud runs on the latest Datasette 1.0 alpha series and uses the JSON write API. Its API uses database-backed access tokens that can be revoked and record when each was last used. Development on the service has driven major improvements across the wider Datasette ecosystem, including several plugin releases. Users can insert, edit and delete table rows through [[Alex Garcia]]'s datasette-write-ui plugin, introduced on the Datasette Cloud blog, and the service is gaining social features to help teams privately collaborate on data investigations.

Development on Datasette Cloud showed that plugins need a private place to store data, such as tokens and progress bars, that regular users should not see, which led to the expanded `_internal` database. Testing on the service also exposed a bug in restricted API tokens: a token limited to view-table access for one table failed because the access check first looked for view-instance and view-database permissions. Datasette Cloud keeps detailed access logs, which were used to confirm that no unauthenticated users accessed the vulnerable pages before the Datasette 1.0a4 security fix, and [[Alex Garcia]]'s work on the service and on Datasette generally was sponsored by Fly.

Datasette Cloud is now a significant step closer to general availability, and the weeknotes do not describe its progress toward GA as of August 2023. The service is also already being built on Fly, and as part of Alex's work the team will be extensively documenting what it learns about using Fly to build a multi-tenant SaaS platform. The existing section mentions Fly only as the sponsor of Alex Garcia's work, not as the hosting platform.

Users needed automatic data imports into their instances, which drove the API key mechanism built on the Datasette 1.0 write API. The author also extended the datasette-auth-tokens plugin so these API tokens can be created and revoked interactively.
## Related Entities

- [[entities/alex-garcia|Alex Garcia]]
- [[entities/datasette-comments|datasette-comments]]
- [[entities/datasette-chronicle|datasette-chronicle]]
- [[entities/simon-willison|Simon Willison]]
- [[entities/datasette|Datasette]]

## Related Concepts

## Mentions in Source

- "Datasette Cloud is now a significant step closer to general availability." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "Datasette Cloud is already being built on Fly, but as part of Alex’s work we’ll be extensively documenting what we learn along the way about using Fly to build a multi-tenant SaaS platform." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "In working on Datasette Cloud we realized that it’s actually quite common for plugins to need somewhere to store data that shouldn’t necessarily be visible to regular users of a Datasette instance" — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "Datasette Cloud itself has detailed access logs primarily to help evaluate this kind of threat." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "[Datasette Cloud](https://www.datasette.cloud/) continues to drive improvements to the wider Datasette ecosystem as a whole." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "It runs on the latest Datasette 1.0 alpha series, taking advantage of [the JSON write API](https://simonwillison.net/2022/Dec/2/datasette-write-api/)." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "I’m running the plugin against the [documents](https://demos.datasette.cloud/data/documents) table on `demos.datasette.cloud`—see [\_chronicle\_documents](https://demos.datasette.cloud/data/_chronicle_documents) there for the result." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "I wanted a mechanism for Datasette Cloud users to be able to setup automatic imports of data into their instances, taking advantage of that API." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "I’ll have more news to share about Datasette Cloud soon!" — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]