---
type: entity
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-07-19-weeknotes_39632e]]"
  - "[[sources/2023-12-08-weeknotes_cbd558]]"
  - "[[sources/2023-11-22-weeknotes_49168f]]"
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
  - "[[sources/2023-05-10-weeknotes_35d224]]"
tags:
  - "other"
  - "project"
---

# sqlite-utils

## Description

sqlite-utils is a Python CLI utility and library for manipulating SQLite databases. It is part of the Datasette ecosystem and is maintained by [[entities/simon-willison|Simon Willison]], the same author as [[entities/datasette|Datasette]]. It is a dependency of [[entities/llm|LLM]]. Version 3.37, released on 2024-07-18, lets the create-table and insert-files commands accept multiple `--pk` options to define [[concepts/compound-primary-keys|Compound primary keys]]. This release is tested against the Python 3.13 pre-release. It also fixes a crash that occurred in environments with a broken numpy installation, a bug Simon Willison tracked down after it surfaced in LLM.

Version 3.36 added support for creating tables in SQLite STRICT mode, exposed as a `--strict` option on the `create-table`, `insert` and `upsert` CLI commands and as a `strict=True` parameter on `table.create()` and the insert and upsert methods. The `create-table` command also accepts `str`, `int` and `bytes` as aliases for `text`, `integer` and `blob`. The STRICT mode support was contributed by Taj Khattra (issue #344, pull request #604). Simon Willison highlighted the contribution in his 2023-12-08 weeknotes as a model pull request, combining a clean implementation, comprehensive tests and thoughtful documentation, and called the release one of the highlights of that post.

Version 3.35.2 (released 2023-11-04) fixed the `--load-extension=spatialite` option and the `find_spatialite()` utility so both work correctly on `arm64` Linux, and it fixed a bug where `sqlite-utils insert` could make the terminal cursor disappear. The same release changed `datetime.timedelta` values to be stored as `TEXT` columns, a change contributed by Harald Nezbeda (issue #522), and extended the test suite to run against Python 3.12. Simon Willison's 2023-11-22 weeknotes featured sqlite-utils 3.35.2 and highlighted its external contributions, describing it as one of the two releases in that post that recognized community work.

[[entities/sqlite-migrate|sqlite-migrate]] is a plugin by Simon Willison that adds a simple migration system to sqlite-utils, so schema changes can be applied to a database in a controlled, repeatable way. Simon Willison's 2023-10-30 weeknotes describe sqlite-migrate as built on sqlite-utils and note that, combined with the `table.transform()` method, it offers a robust solution to the difficulty of running schema migrations in SQLite. Related schema-change work is covered under [[concepts/alter-table|ALTER TABLE]].

Version 3.35.1 fixed a bug in which calls to `table.transform()` rewrote the rowid column of a table, breaking full-text search because FTS records are related to their underlying rows by rowid. The bug broke full-text search on [[entities/datasette|Datasette]] Cloud ([[entities/datasette-cloud|Datasette Cloud]]), and Simon Willison described it in his 2023-09-17 weeknotes, where he noted that the rowid column was being rewritten by `table.transform()`. The fix was tracked as issue #592 and shipped in 3.35.1. Simon Willison released sqlite-utils-move-tables 0.1, a plugin that adds a `move-tables` command for moving a table from one database to another (for example, `sqlite-utils move-tables origin.db destination.db tablename`). Willison also noted that rowid values in SQLite have always been unstable, because they are rewritten whenever a table is VACUUMed. The rowid problem led him to realize this instability, which makes the tool central to the SQLite data-integrity discussion in those weeknotes. The related [[entities/sqlite-chronicle|sqlite-chronicle]] project also comes up in that discussion.

Version 3.35 was released on 2023-08-18 and was driven by bug reports from [[entities/llm|LLM]] users trying to add foreign keys to existing tables. SQLite does not support adding foreign keys to an existing table out of the box, so sqlite-utils provides its own mechanism for doing so. The release replaced the fragile `writable_schema` approach with the `table.transform()` method, which creates a new table, copies the data across and renames it, because the old approach failed on some Python installations, including the system Python on macOS. The removed fast foreign-key feature was kept available as the opt-in sqlite-utils-fast-fks plugin, following the jQuery-style pattern of preserving old features as plugins after a major release. The project's plugin support is what made this approach possible.

Simon Willison released [[entities/sqlite-utils-jq|sqlite-utils-jq]], a tiny plugin written partly to exercise the new plugins framework, which is one of the main ways sqlite-utils is extended. The plugin was inspired by a Hacker News comment, and Willison's 2023-08-16 Datasette Cloud weeknotes describe it as an excuse to exercise the [plugins framework](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/) a little more. sqlite-utils also works with the sqlite-utils-litecli plugin, which lets the `jq()` function run inside the interactive litecli shell. The source material also lists [[entities/openai-to-sqlite|openai-to-sqlite]] as a related project in the same ecosystem.

Based on community requests, Simon Willison added plugin support to sqlite-utils in July 2023, and the plugin system became the main subject of the 2023-08-05 weeknotes; version 3.34 was released on 2023-07-22. sqlite-utils is a combined CLI tool and Python library, similar to LLM in that respect. sqlite-utils plugins fall into two categories: those that add commands to the sqlite-utils CLI, and those that add custom SQL functions that can be executed against SQLite. By the time of the 2023-08-05 weeknotes, the plugin directory already listed many plugins. Willison built sqlite-utils-shell to demonstrate the new plugin system, adding a `sqlite-utils shell` command for an interactive shell with access to SQL functions from other plugins, then built sqlite-utils-litecli as a better alternative that runs `sqlite-utils litecli mydatabase.db` to open a full litecli shell with all custom SQL functions from other plugins. The same weeknotes also tie the plugin work to the litecli and dclient projects.

Sqlite-utils 3.31 was released on 2023-05-08, after small fixes and pull requests had accumulated since the 3.30 release in October 2022. The release notes credit Chris Amico, Kenny Song, Martin Carpenter and Scott Perry as contributors. It automatically locates the SpatiaLite extension on Apple Silicon (thanks, Chris Amico), adds a `--raw-lines` option to the `sqlite-utils query` and `sqlite-utils memory` commands that outputs the raw value of the first column of every row, and adds a `skip_false` option to `table.convert()` and `sqlite-utils convert --no-skip-false` to avoid skipping rows with falsey values. It also fixed a bug where `table.upsert_all()` failed when `not_null=` was passed, allowed tables to be created with self-referential foreign keys (thanks, Scott Perry), stopped `sqlite-utils transform` from breaking on tables with default column values (thanks, Kenny Song), and fixed repeated calls to `table.transform()` (thanks, Martin Carpenter). Simon Willison's 2023-05-10 weeknotes center on this release and describe it as the result of a day spent tidying up the fixes and pull requests that had built up since 3.30.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/simon-willison|Simon Willison]]
- [[entities/datasette|Datasette]]
- [[entities/shot-scraper|shot-scraper]]
- [[entities/sqlite-migrate|sqlite-migrate]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/sqlite-chronicle|sqlite-chronicle]]
- [[entities/sqlite-utils-jq|sqlite-utils-jq]]
- [[entities/openai-to-sqlite|openai-to-sqlite]]
- [[entities/litecli|litecli]]
- [[entities/dclient|dclient]]
- [[entities/pyodide|Pyodide]]
- [[entities/deno|Deno]]

## Related Concepts

- [[concepts/compound-primary-keys|Compound primary keys]]
- [[concepts/alter-table|ALTER TABLE]]
- [[concepts/rowid|rowid]]
- [[concepts/sqlite-utils-transform-method|sqlite-utils transform() method]]
- [[concepts/plugins|Plugins]]
- [[concepts/custom-sql-functions|Custom SQL functions]]

## Mentions in Source

- "I realized that [sqlite-utils](https://sqlite-utils.datasette.io/) had been quietly accumulating small fixes and pull requests since the 3.30 release last October, and spent a day tidying those up and turning them into a release." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]
- "My [sqlite-utils](https://sqlite-utils.datasette.io/) project, similar to LLM, is a combined CLI tool and Python library." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "Based on requests from the community I [adding plugin support to it](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/) too." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "A tiny new plugin for [sqlite-utils](https://sqlite-utils.datasette.io/), inspired by [this Hacker News comment](https://news.ycombinator.com/item?id=37083501) and written mainly as an excuse for me to exercise that [new plugins framework](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/) a little more." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "You can also use it in combination with [sqlite-utils-litecli](https://github.com/simonw/sqlite-utils-litecli) to run that new function as part of an interactive shell:" — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "`sqlite-utils` has a mechanism for adding foreign keys to an existing table—something that’s not supported by SQLite out of the box." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "I was getting bug reports from LLM users who were running into this." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "It turned out the `rowid` column in SQLite was being rewritten by calls to the `sqlite-utils` [table.transform()](https://sqlite-utils.datasette.io/en/stable/python-api.html#transforming-a-table) method." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "I pushed out [a fix for this](https://github.com/simonw/sqlite-utils/issues/592) in 3.35.1." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "so I built a little plugin for `sqlite-utils` that adds a `sqlite-utils move-tables origin.db destination.db tablename` command." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "[sqlite-migrate](https://github.com/simonw/sqlite-migrate) is my plugin that adds a simple migration system to [sqlite-utils](https://sqlite-utils.datasette.io/), for applying changes to a database schema in a controlled, repeatable way." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "The combination `sqlite-migrate` and the [table.transform() method](https://sqlite-utils.datasette.io/en/stable/python-api.html#python-api-transform) in `sqlite-utils` offers a pretty robust solution to this problem." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "**[sqlite-utils 3.35.2](https://sqlite-utils.datasette.io/en/stable/changelog.html#v3-35-2)**" — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]
- "> * `datetime.timedelta` values are now stored as `TEXT` columns. Thanks, [Harald Nezbeda](https://github.com/nezhar). ([#522](https://github.com/simonw/sqlite-utils/issues/522))" — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]
- "Python CLI utility and library for manipulating SQLite databases" — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]
- "Taj Khattra’s contribution of the `--strict` and `strict=True` options is a beautiful example of my ideal pull request: a clean implementation, comprehensive tests and thoughtful updates to the documentation [all bundled together in one go](https://github.com/simonw/sqlite-utils/pull/604)." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "Support for creating tables in [SQLite STRICT mode](https://www.sqlite.org/stricttables.html). Thanks, [Taj Khattra](https://github.com/tkhattra). ([#344](https://github.com/simonw/sqlite-utils/issues/344))" — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "I ended up fixing that in its sqlite-utils dependency—here are the full release notes for sqlite-utils 3.37:" — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]
- "Fixed a crash that can occur in environments with a broken numpy installation, producing a module 'numpy' has no attribute 'int8'." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]
- "Notably, four contributors get credited in [the release notes](https://sqlite-utils.datasette.io/en/stable/changelog.html#v3-31): Chris Amico, Kenny Song, Martin Carpenter and Scott Perry." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]