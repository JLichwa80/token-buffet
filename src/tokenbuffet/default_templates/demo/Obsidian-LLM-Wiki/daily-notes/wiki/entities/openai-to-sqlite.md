---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "project"
  - "other"
---

# openai-to-sqlite

## Description

openai-to-sqlite is a command-line tool written by Simon Willison for loading data from various [[openai|OpenAI]] APIs into a SQLite database. Version 0.4 was released during the period covered by the source, followed by a smaller release that same week. The release was motivated by the author's wish to add related content recommendations to his TIL website. Each TIL post now shows related posts generated from OpenAI embeddings, which the author uses to plot semantically similar posts. The tool builds on [[sqlite-utils|sqlite-utils]] for its SQLite storage.

Version 0.3 (released 2023-04-29) added a way for SQL queries to update existing tables with the results of a `chatgpt()` API call, exposed as a custom SQL function. The feature grew out of a Datasette Office Hours conversation about running sentiment analysis on SQLite data, and Willison explained it in the companion post "Enriching data with GPT3.5 and SQLite SQL functions."

The tool is one of the three main subjects of the 2023-05-01 weeknotes source, which describes the 0.3 `chatgpt()` mechanism as a way to enrich data in place. In that source, the tool is a command-line CLI that saves OpenAI API results to a SQLite database, and the `chatgpt()` SQL function lets queries write GPT-3.5 output back into existing tables. The feature was built for [[datasette|Datasette]] users who want to run tasks such as sentiment analysis on their data without leaving SQL.

openai-to-sqlite version 0.2 was released on 13 January 2023, one of four software releases that came out of the Q&A documentation experiment, alongside datasette-openai, datasette-faiss, and datasette-cookies-for-magic-parameters. Early on, the tool was used to calculate the embeddings that experiment required, and storing OpenAI API responses in SQLite let the author query and reuse those results from Datasette. The 2023-01-15 weeknotes describe the tool as a command-line tool for storing OpenAI API responses in a SQLite database, useful for calculating [[concepts/embeddings|embeddings]]. At that point the project had two releases in total, with 0.2 as the latest.

## Related Entities

- [[entities/openai|openai]]
- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/datasette|datasette]]
- [[entities/chatgpt-code-interpreter|ChatGPT Code Interpreter]]
- [[entities/sqlite|SQLite]]
- [[entities/datasette-openai|datasette-openai]]

## Related Concepts

- [[concepts/custom-sql-functions|Custom SQL function]]
- [[concepts/sentiment-analysis|Sentiment analysis]]
- [[concepts/embeddings|Embeddings]]

## Mentions in Source

- "[openai-to-sqlite](https://datasette.io/tools/openai-to-sqlite)—a command-line tool for storing OpenAI API responses in a SQLite database—useful for calculating embeddings" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "**[openai-to-sqlite](https://github.com/simonw/openai-to-sqlite)**: [0.2](https://github.com/simonw/openai-to-sqlite/releases/tag/0.2)—([2 releases total](https://github.com/simonw/openai-to-sqlite/releases))—2023-01-13" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "I ended up adding a new mechanism to my `openai-to-sqlite` CLI tool—it can now execute SQL queries that can update existing tables with the results of a `chatgpt()` API call using a custom SQL function." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "I wrote more about that in [Enriching data with GPT3.5 and SQLite SQL functions](https://simonwillison.net/2023/Apr/29/enriching-data/)." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "A smaller release this week: [openai-to-sqlite 0.4](https://github.com/simonw/openai-to-sqlite/releases/tag/0.4), an update to my CLI tool for loading data from various OpenAI APIs into a SQLite database." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]