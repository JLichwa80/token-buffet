---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
sources:
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"

generation_complete: true
---

# Rye

## Description

Rye is an experimental Python packaging tool created by [[Armin Ronacher]]. It is delivered as a single binary written in Rust. Its most distinctive feature is that it bootstraps a Python environment by downloading a standalone Python build, stored in a `~/.rye` directory, instead of relying on the system Python. [[Simon Willison]] considers this the most interesting idea in Rye and says it makes getting Python running much easier. Willison wrote a TIL about how Rye works and where it puts files, and he released a [[datasette|Datasette]] fix so that Datasette installs cleanly with `rye install`.

## Related Entities

- [[entities/armin-ronacher|Armin Ronacher]]
- [[entities/datasette|datasette]]

## Related Concepts

## Mentions in Source

- "Rye has some *really* interesting ideas. By far my favourite is how it bundles Python itself: it doesn’t depend on a system Python, instead downloading a standalone Python build from the [python-build-standalone](https://github.com/indygreg/python-build-standalone) project and stashing it away in a `~/.rye` directory." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]