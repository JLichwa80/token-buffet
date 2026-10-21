---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
tags: [other]
aliases:
  - "sqlite-utils litecli command"
sources:
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"

---

# sqlite-utils-litecli

## Description

sqlite-utils-litecli is a plugin for [[sqlite-utils]] that exposes the [[litecli]] interactive shell through the `sqlite-utils litecli` command. The author, [[Simon Willison]], built it as a better alternative to the earlier [[sqlite-utils-shell]] plugin, after Alex Garcia suggested looking at litecli. The shell includes all of the [[Custom SQL functions]] installed by other sqlite-utils [[Plugins]], and litecli adds table and column auto-completion. The source lists version 0.1.1, released 2023-07-26, described as "Interactive shell for sqlite-utils using litecli". The source's weeknotes of 5 August 2023 note that it replaced sqlite-utils-shell as a full-featured shell.

## Related Entities

- [[entities/litecli|litecli]]
- [[entities/sqlite-utils-shell|sqlite-utils-shell]]
- [[entities/sqlite-utils|sqlite-utils]]

## Related Concepts

- [[concepts/custom-sql-functions|Custom SQL functions]]
- [[concepts/plugins|Plugins]]

## Mentions in Source

- "I used that to build a better alternative to my `sqlite-utils-shell` plugin: [sqlite-utils-litecli](https://github.com/simonw/sqlite-utils-litecli), which lets you run the following command to get a full `litecli` shell with all of the custom SQL functions from other plugins:" — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]