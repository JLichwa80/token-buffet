---
type: concept
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
tags:
generation_complete: true
---

# Configuration directory mode

## Definition

Configuration directory mode is a Datasette feature that loaded settings from a legacy `settings.json` file. Version 1.0a5 removed that file and moved its settings into the new [[datasette.yaml]] configuration file, under a `settings` section. The change is part of a wider effort to consolidate settings, plugin configuration, permissions, and canned queries into one file, a consolidation proposed by [[Alex Garcia]].

## Key Characteristics

- Was a Datasette feature that read configuration from a `settings.json` file.
- Was removed in version 1.0a5.
- Its settings now live in the `settings` section of `datasette.yaml`.
- Forms part of a broader consolidation of settings, plugin configuration, permissions, and canned queries into a single configuration file.
- Related to [[metadata.json]], another legacy configuration file in Datasette.

## Applications

- Migrating older Datasette deployments that rely on `settings.json` to the `datasette.yaml` format used from 1.0a5 onward.
- Understanding why `settings.json` no longer has any effect in current Datasette versions.
- Serving as a reference point when reviewing how Datasette configuration has been consolidated.

## Related Concepts

- [[concepts/datasette-metadata|metadata.json]]

## Related Entities

- [[entities/alex-garcia|Alex Garcia]]

## Mentions in Source

- "The legacy `settings.json` config file used for [Configuration directory mode](https://docs.datasette.io/en/1.0a5/settings.html#config-dir) has been removed, and `datasette.yaml` has a `"settings"` section where the same settings key/value pairs can be included." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]