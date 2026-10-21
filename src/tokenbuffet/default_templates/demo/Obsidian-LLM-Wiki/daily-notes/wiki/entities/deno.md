---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-05-10-weeknotes_35d224]]"
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
tags:
  - "other"
aliases:
  - "Deno JavaScript runtime"
---

# Deno

## Description

Deno is a JavaScript and TypeScript runtime. In the 2023-05-10 weeknotes, the author uses it as the host for a [[Pyodide]] sandbox prototype. A Deno process is started from a Python `subprocess`, and Pyodide then runs inside it. The author notes that Deno can now load Pyodide, which made this approach possible, and calls the mechanism "somewhat convoluted." The prototype is a step toward safely running untrusted Python, as described in [[Running Python in a Deno/Pyodide sandbox]]. See also the [[sources/2023-05-10-weeknotes_35d224|2023-05-10 weeknotes]].

## Related Entities

- [[entities/pyodide|Pyodide]]

## Related Concepts

- [[concepts/running-python-in-a-denopyodide-sandbox|Running Python in a Deno/Pyodide sandbox]]

## Mentions in Source

- "I came up with a somewhat convoluted mechanism that starts a Deno process running in a Python `subprocess` and then runs Pyodide inside of Deno." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]