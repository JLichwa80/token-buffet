---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Simon Willison weeknotes 2023-08-30"
  - "Datasette 1.0a4 and 1.0a5"
  - "plus weeknotes"
contentHash: 5466-348e56e7
source_file: "[[_Inbox/2023-08-30-datasette-plus-weeknotes.md]]"
generation_complete: true
---

# 2023-08-30-datasette-plus-weeknotes - Summary

## Source

- Original file: [[_Inbox/2023-08-30-datasette-plus-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

Simon Willison's weeknotes for 30 August 2023 report two new alpha releases of [[entities/datasette|Datasette]], 1.0a4 and 1.0a5, along with a WordCamp US keynote on large language models, a new [[entities/llm|LLM]] release, two new LLM plugins, and a set of TILs. Datasette 1.0a5 consolidates configuration into a `datasette.yaml` file, adds a `--setting` option, and adds an `--actor` option for `datasette --get`. It also fixes a usability flaw in restricted API tokens. Datasette 1.0a4 patched [[concepts/cve-2023-40570|CVE-2023-40570]], in which the API explorer leaked database and table names to unauthenticated users. The post covers [[entities/llm-openrouter|llm-openrouter]] and [[entities/llm-anyscale-endpoints|llm-anyscale-endpoints]], each with under 30 lines of core code, and the switch of `llm logs` output to Markdown in LLM 0.8. It also covers [[entities/sqlite-utils|sqlite-utils]] 3.35, which replaces a fragile `writable_schema` hack with `transform()`. The post closes with [[entities/paginate-json|paginate-json]] 1.0 and a list of releases.

## Key Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/alex-garcia|Alex Garcia]]
- [[entities/llm|LLM]]
- [[entities/llm-openrouter|llm-openrouter]]
- [[entities/llm-anyscale-endpoints|llm-anyscale-endpoints]]
- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/paginate-json|paginate-json]]
- [[entities/openrouter|OpenRouter]]
- [[entities/anyscale-endpoints|Anyscale Endpoints]]
- [[entities/claude|Claude]]
- [[entities/github|GitHub]]
- [[entities/sqlite|SQLite]]
- [[entities/python|Python]]
- [[entities/wordcamp-us|WordCamp US]]
- [[entities/datasette-json-api|Datasette JSON API]]

## Key Concepts

- [[concepts/finely-grained-permissions|Finely-grained permissions]]
- [[concepts/datasette-metadata|metadata.json]]
- [[concepts/configuration-directory-mode|Configuration directory mode]]
- [[concepts/datasette-get|datasette --get]]
- [[concepts/actor|Actor]]
- [[concepts/cve-2023-40570|CVE-2023-40570]]
- [[concepts/sqlite-utils-transform-method|sqlite-utils transform() method]]
- [[concepts/foreign-keys|Foreign keys]]
- [[concepts/link-pagination|Link pagination]]
- [[concepts/newline-delimited-json|Newline-delimited JSON]]
- [[concepts/llm-logs|llm logs]]
- [[concepts/large-language-models|Large Language Models]]
- [[concepts/github-security-advisory|GitHub security advisory]]

## Main Points

- **Datasette 1.0a5** consolidates configuration into `datasette.yaml`, adds a `--setting` option for command-line configuration, and adds an `--actor` option for `datasette --get`.
- **Datasette 1.0a5** fixes a usability flaw where a token restricted to `view-table` could not view that table. Applying `view-table` now implies `view-database` and `view-instance`.
- **Datasette 1.0a4** fixed **CVE-2023-40570**, which exposed database and table names (not content) to unauthenticated users through the API explorer. Datasette Cloud access logs showed no unauthenticated access before the fix.
- **llm-openrouter** and **llm-anyscale-endpoints** each have core code under 30 lines by reusing LLM's OpenAI-compatible code.
- **LLM 0.8** changed the default `llm logs` output from JSON to Markdown.
- **sqlite-utils 3.35** replaced the `writable_schema` foreign key hack with `transform()`, which works on Python installations that block schema writes. The old method lives on in the sqlite-utils-fast-fks plugin.
- **paginate-json 1.0** follows link-paginated JSON APIs and outputs a single array or newline-delimited JSON.

I returned the page here rather than writing it to a file, since no output path was given. The source's `sources:` frontmatter field from the schema isn't in your output template, so I left it out. The tags are `other` plus `project` and `topic` from the active vocabulary.

## Mentions in Source

- "Two new alpha releases of Datasette, plus a keynote at WordCamp, a new LLM release, two new LLM plugins and a flurry of TILs." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "The `datasette --get /...` option is a neat trick that can be used to simulate an HTTP request through the Datasette instance, without even starting a server running on a port." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "I run a lot of different Datasette instances, often on an ad-hoc basis." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "In working on Datasette Cloud we realized that it’s actually quite common for plugins to need somewhere to store data that shouldn’t necessarily be visible to regular users of a Datasette instance" — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "Datasette Cloud itself has detailed access logs primarily to help evaluate this kind of threat." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "This change took quite some time to develop, because any time I write code involving permissions I like to also include extremely comprehensive automated tests." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "Alex pointed out that the existing `_internal` database for Datasette could be expanded to cover these use-cases as well." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "Alex [expressed interest in fixing it](https://github.com/simonw/datasette/issues/2093), and has started to put a plan into motion for cleaning it up." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]