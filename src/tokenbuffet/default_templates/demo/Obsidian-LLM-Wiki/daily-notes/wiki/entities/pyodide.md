---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
sources:
  - "[[sources/2023-05-10-weeknotes_35d224]]"

generation_complete: true
---

# Pyodide

## Description

Pyodide is a port of Python that runs in WebAssembly. According to the source, it was previously available only in web browsers. The author's latest sandbox prototype uses Pyodide to run Python code, with [[Deno]] as the host runtime. The approach was inspired by a comment from Milan Raj showing that Deno can now load Pyodide. The Pyodide sandbox is the focus of the final section of the weeknotes and of a linked TIL entry. The author's goal with this work is to find a safe way to run untrusted Python code, as described in [[Running Python in a Deno/Pyodide sandbox]].

## Related Entities

- [[entities/deno|Deno]]

## Related Concepts

- [[concepts/running-python-in-a-denopyodide-sandbox|Running Python in a Deno/Pyodide sandbox]]

## Mentions in Source

- "My latest attempt takes advantage of Pyodide and Deno. It was inspired by [this comment](https://github.com/pyodide/pyodide/issues/3420#issuecomment-1542742906) by Milan Raj, showing how Deno can load Pyodide now. Pyodide was previously only available in web browsers." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]