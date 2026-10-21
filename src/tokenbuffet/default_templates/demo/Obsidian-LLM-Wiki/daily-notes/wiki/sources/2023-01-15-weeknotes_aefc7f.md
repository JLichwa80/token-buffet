---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Weeknotes: AI hacking and a SpatiaLite tutorial"
  - "2023-01-15-weeknotes"
contentHash: 147f-ee66b877
source_file: "[[_Inbox/2023-01-15-weeknotes.md]]"
generation_complete: true
---

# 2023-01-15-weeknotes - Summary

## Source

- Original file: [[_Inbox/2023-01-15-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

These weeknotes by Simon Willison, dated 15 January 2023, summarize a week of [[entities/datasette|Datasette]] work and act mainly as a link index to separate posts. The central project was an experiment that used [[concepts/custom-sql-functions|custom SQL functions]] in Datasette to build a question-and-answer interface over a document corpus, combining GPT-3 [[concepts/embeddings|embeddings]] with [[concepts/vector-search|vector similarity search]]. The experiment produced several releases, including [[entities/datasette-openai|datasette-openai]], [[entities/datasette-faiss|datasette-faiss]], [[entities/datasette-cookies-for-magic-parameters|datasette-cookies-for-magic-parameters]], which keeps API keys out of query strings using [[concepts/magic-parameters|magic parameters]], and [[entities/openai-to-sqlite|openai-to-sqlite]]. Datasette 0.64 added a `default_allow_sql` setting after some functions added by [[entities/spatialite|SpatiaLite]] were found to be able to crash an instance. A new official tutorial shows how SpatiaLite can safely support a [[concepts/geospatial-api|geospatial API]] that maps locations to time zones. The post lists ten releases and six TIL posts from the week.

## Key Entities

- [[entities/datasette|Datasette]]: the central platform for the week's work and the host for the AI experiment.
- [[entities/spatialite|SpatiaLite]]: a geospatial extension whose SQL functions prompted a security change and which powers the new tutorial.
- [[entities/sqlite|SQLite]]: the storage layer beneath Datasette, SpatiaLite, and the release tools.
- [[entities/faiss|FAISS]]: the vector similarity search library used for document retrieval.
- [[entities/datasette-openai|datasette-openai]]: a plugin that exposes OpenAI API calls as SQL functions.
- [[entities/datasette-faiss|datasette-faiss]]: a plugin that maintains a FAISS index for Datasette tables.
- [[entities/openai-to-sqlite|openai-to-sqlite]]: a command-line tool that stores OpenAI API responses in SQLite, useful for calculating embeddings.
- [[entities/datasette-cookies-for-magic-parameters|datasette-cookies-for-magic-parameters]]: a plugin that stores secrets such as API keys in cookies.

## Key Concepts

- [[concepts/embeddings|Embeddings]]: numerical vector representations of text that the Q&A experiment relies on.
- [[concepts/vector-search|Vector similarity search]]: the retrieval step that finds passages close to a query vector.
- [[concepts/custom-sql-functions|Custom SQL functions]]: plugin-defined functions in Datasette that enable the AI experiment and also introduced the SpatiaLite crash risk.
- [[concepts/magic-parameters|Magic parameters]]: Datasette query parameters populated from the environment, such as cookies.
- [[concepts/geospatial-api|Geospatial API]]: a web API that answers location-based queries, such as location-to-time-zone lookups.

## Main Points

- **An experiment used custom SQL functions in Datasette to build a Q&A interface over existing documents, using GPT-3, embeddings, and vector search.**
- **The experiment produced a burst of releases**, including datasette-openai, datasette-faiss, datasette-cookies-for-magic-parameters, and openai-to-sqlite.
- **Datasette 0.64 added a `default_allow_sql` setting** because some SpatiaLite SQL functions could crash a Datasette instance.
- **A new official tutorial shows how SpatiaLite can safely support a geospatial location-to-time-zone API.**
- The weeknotes list ten releases and six TIL posts, and point to separate posts for the main work.

## Mentions in Source

- "An open source multi-tool for exploring and publishing data" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "I released Datasette 0.64 with a new `--setting default_allow_sql off` setting, due to the discovery that some of the SQL functions added by the SpatiaLite module can be used to crash the Datasette instance." — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "described my experiment using custom SQL functions in Datasette to provide a Q&A interface against an existing corpus of documents." — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "It demonstrates how SpatiaLite can be used to safely build and deploy a geospatial API." — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "Load shapefiles into a SQLite (optionally SpatiaLite) database" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "a command-line tool for storing OpenAI API responses in a SQLite database—useful for calculating embeddings" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "a plugin that builds a FAISS index for fast vector similarity search" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "Maintain a FAISS index for specified Datasette tables" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "custom SQL functions for querying the OpenAI APIs from Datasette" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "[datasette-openai](https://datasette.io/plugins/datasette-openai)—custom SQL functions for querying the OpenAI APIs from Datasette" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "**[datasette-openai](https://github.com/simonw/datasette-openai)**: [0.2](https://github.com/simonw/datasette-openai/releases/tag/0.2)—([4 releases total](https://github.com/simonw/datasette-openai/releases))—2023-01-14" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]