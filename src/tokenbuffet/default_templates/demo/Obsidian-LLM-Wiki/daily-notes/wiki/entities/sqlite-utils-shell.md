---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
tags:
  - "other"
aliases:
  - "sqlite-utils shell"
---

# sqlite-utils-shell

## Description

sqlite-utils-shell is an interactive shell plugin for sqlite-utils, a SQLite tool written by the same author. In the period covered by the source, it gained support for the `--load-extension` option, which the author added so it could work with [[entities/steampipe|Steampipe]] extensions. The release 0.3 is listed on 2023-12-21. A TIL (today-I-learned note) on running Steampipe extensions in sqlite-utils and Datasette accompanies the change. The source highlights it as one of the author's SQLite tools.

sqlite-utils-shell was built in time for the initial launch of the sqlite-utils plugin system, where it demonstrated the new system by adding a `sqlite-utils shell` command. That command opens an interactive shell with access to any SQL functions installed by other plugins. The author later superseded it with sqlite-utils-litecli, a litecli-based shell that exposes all installed SQL functions.
## Related Entities

- [[entities/steampipe|Steampipe]]
- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/litecli|litecli]]
- [[entities/sqlite-utils-litecli|sqlite-utils-litecli]]

## Related Concepts

- [[concepts/plugins|Plugins]]
- [[concepts/custom-sql-functions|Custom SQL functions]]

## Mentions in Source

- "The [sqlite-utils-shell](https://github.com/simonw/sqlite-utils-shell) plugin now supports the `--load-extension` option—I added this to let it be used with [Steampipe extensions](https://til.simonwillison.net/sqlite/steampipe)." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "* **[sqlite-utils-shell 0.3](https://github.com/simonw/sqlite-utils-shell/releases/tag/0.3)**—2023-12-21  
  Interactive shell for sqlite-utils" — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]