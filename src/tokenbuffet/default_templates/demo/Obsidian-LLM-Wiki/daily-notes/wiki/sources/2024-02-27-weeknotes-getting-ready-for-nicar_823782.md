---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Weeknotes: Getting ready for NICAR"
  - "Simon Willison weeknotes 2024-02-27"
contentHash: 26b3-cb61c906
source_file: "[[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar.md]]"
generation_complete: true
---

# 2024-02-27-weeknotes-getting-ready-for-nicar - Summary

## Source

- Original file: [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar.md]]
- Ingested: 2026-10-21

## Core Content

Simon Willison's weeknotes, dated 27 February 2024, preview his preparations for [[entities/nicar|NICAR 2024]], the data journalism conference run by [[entities/investigative-reporters-and-editors|Investigative Reporters and Editors]] in Baltimore. He is running a [[entities/datasette|Datasette]] workshop there, and he and [[entities/alex-garcia|Alex Garcia]] are finishing features for [[entities/datasette-cloud|Datasette Cloud]], including [[entities/datasette-enrichments|Datasette Enrichments]] and [[entities/datasette-comments|Datasette Comments]]. Most of the post is a release roundup. [[entities/llm-mistral|llm-mistral]] 0.3 added support for [[entities/mistral-large|Mistral Large]] by reading the Mistral API model list. [[entities/dclient|dclient]] 0.3 added streaming inserts. [[entities/datasette-events-forward|datasette-events-forward]] forwards analytics events, and [[entities/datasette-edit-schema|datasette-edit-schema]] 0.8a0 added fine-grained permissions. The post also covers [[entities/datasette-studio|datasette-studio]], a distribution defined only by a pyproject.toml file, and the [[entities/datasette-enrichments-opencage|datasette-enrichments-opencage]] 0.1.1 fix for "database locked" errors. That fix led to automatic transaction wrapping in Datasette 1.0a10. The closing TILs cover SQLite audit logs, [[entities/val-town|Val Town]] scheduled functions, and a lightweight [[concepts/rag|RAG]] workflow.

## Key Entities

- [[entities/nicar|nicar-2024]]
- [[entities/investigative-reporters-and-editors|investigative-reporters-and-editors]]
- [[entities/datasette|datasette]]
- [[entities/datasette-cloud|datasette-cloud]]
- [[entities/alex-garcia|alex-garcia]]
- [[entities/datasette-enrichments|datasette-enrichments]]
- [[entities/datasette-comments|datasette-comments]]
- [[entities/mistral|mistral]]
- [[entities/mistral-large|mistral-large]]
- [[entities/llm-mistral|llm-mistral]]
- [[entities/dclient|dclient]]
- [[entities/datasette-studio|datasette-studio]]
- [[entities/datasette-enrichments-opencage|datasette-enrichments-opencage]]
- [[entities/datasette-edit-schema|datasette-edit-schema]]
- [[entities/datasette-events-forward|datasette-events-forward]]
- [[entities/datasette-auth-tokens|datasette-auth-tokens]]
- [[entities/val-town|val-town]]

## Key Concepts

- [[concepts/datasette-events|datasette-events]]
- [[concepts/dogfooding|dogfooding]]
- [[concepts/rag|rag]]

## Main Points

- **Conference preparation:** Willison runs a Datasette workshop at [[entities/nicar|NICAR 2024]] and is readying [[entities/datasette-cloud|Datasette Cloud]] features with [[entities/alex-garcia|Alex Garcia]].
- **Mistral Large support:** [[entities/llm-mistral|llm-mistral]] 0.3 shipped the same day [[entities/mistral-large|Mistral Large]] launched (2024-02-26). It reads the Mistral API model list through a cache, so new models need no plugin release.
- **Streaming inserts:** [[entities/dclient|dclient]] 0.3 adds `--interval` and `--batch-size` options for streaming records into a table through the write API.
- **Analytics dogfooding:** [[entities/datasette-events-forward|datasette-events-forward]] was built for [[entities/datasette-cloud|Datasette Cloud]] to send events to a central analytics instance, an example of [[concepts/dogfooding|dogfooding]] built on [[concepts/datasette-events|Datasette Events]].
- **Permissions:** [[entities/datasette-edit-schema|datasette-edit-schema]] 0.8a0 respects core create-table, alter-table and drop-table permissions. Datasette 1.0a11 requires `update-row` permission to replace rows through the insert API.
- **Database locking fix:** [[entities/datasette-enrichments-opencage|datasette-enrichments-opencage]] 0.1.1 fixed "database locked" errors. That fix led [[entities/datasette|Datasette]] 1.0a10 to wrap write functions in transactions automatically.
- **Distribution experiment:** [[entities/datasette-studio|datasette-studio]] 0.1a0 is a full Datasette distribution defined only by a pyproject.toml file, described as very experimental.
- **TILs:** Topics include SQLite JSON audit logs, scheduled [[entities/val-town|Val Town]] functions that write to Datasette Cloud, FIPS-compliant MD5 issues, and piping ripgrep output into an LLM as a lightweight [[concepts/rag|RAG]] approach.

## Mentions in Source

- "Next week is NICAR 2024 in Baltimore—the annual data journalism conference hosted by Investigative Reporters and Editors." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "I’m running a workshop on Datasette, and I plan to spend most of my time in the hallway track talking to people about Datasette, Datasette Cloud and how the Datasette ecosystem can best help support their work." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "I plan to spend most of my time in the hallway track talking to people about Datasette, Datasette Cloud and how the Datasette ecosystem can best help support their work." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "I’m increasing the frequency of the Datasette 1.0 alphas. This one has a minor permissions fix (the ability to replace a row using the insert API now requires the update-row permission) and a small cosmetic fix which I’m really pleased with." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "I’ve been working with Alex Garcia to get Datasette Cloud ready for the conference." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "This new plugin was originally built for Datasette Cloud—it forwards analytical events from an instance to a central analytics instance." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "Mistral released Mistral Large this morning, so I rushed out a new release of my llm-mistral plugin to add support for it." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]