---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
sources:
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"

generation_complete: true
---

# python-build-standalone

## Description

python-build-standalone is a project by indygreg that produces standalone Python builds. Rye downloads these builds and stores them in a ~/.rye directory, so Rye does not need a system Python installed. The project supplies the Python runtime that makes Rye's bootstrapping approach work. In the source, it appears only as a dependency of [[Rye]].

## Related Entities

- [[entities/rye|Rye]]

## Related Concepts

## Mentions in Source

- "By far my favourite is how it bundles Python itself: it doesn’t depend on a system Python, instead downloading a standalone Python build from the [python-build-standalone](https://github.com/indygreg/python-build-standalone) project and stashing it away in a `~/.rye` directory." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]