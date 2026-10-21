---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "Pyodide sandbox"
  - "Deno/Pyodide sandbox"
sources:
  - "[[sources/2023-05-10-weeknotes_35d224]]"

generation_complete: true
---

# Running Python in a Deno/Pyodide sandbox

## Definition

Running Python in a Deno/Pyodide sandbox is an experimental approach to executing untrusted Python code safely inside a [[WebAssembly]] sandbox. A Deno process is started from a Python subprocess, and [[Pyodide]] (a Python runtime compiled to WebAssembly) runs inside that Deno process. The author describes the mechanism as "somewhat convoluted" but considers it a promising route. It became possible once [[Deno]] could load Pyodide, which previously ran only in web browsers.

## Key Characteristics

- Runs untrusted Python code inside a WebAssembly sandbox rather than directly on the host Python interpreter.
- Layers three components: a Python subprocess, a Deno process started by that subprocess, and Pyodide running inside Deno.
- Depends on Deno's ability to load Pyodide, which was not available outside browsers before.
- Described by its author as a prototype with a convoluted design, but a promising one.
- Code and next steps are documented in a linked TIL entry dated 2023-05-10.

## Applications

- Executing untrusted or user-supplied Python code in a sandboxed environment.
- Providing a safer execution layer for code generated or influenced by language models, where [[Prompt injection]] could cause untrusted code to run.
- Running Python inside server-side JavaScript runtimes such as Deno, without a native Python runtime.

## Related Concepts

- [[concepts/prompt-injection|Prompt injection]]

## Related Entities

- [[entities/pyodide|Pyodide]]
- [[entities/deno|Deno]]

## Mentions in Source

- "I'm still trying to find the best way to run untrusted Python code in a safe WebAssembly sandbox." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]