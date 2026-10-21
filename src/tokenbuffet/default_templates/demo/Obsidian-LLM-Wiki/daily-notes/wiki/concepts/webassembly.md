---
type: concept
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-05-10-weeknotes_35d224]]"
tags:
generation_complete: true
---

# WebAssembly

## Definition

WebAssembly is a binary instruction format that lets code run in a sandboxed environment. In the source, it is the basis for the sandbox that Simon Willison is trying to build, to run untrusted Python code safely. His latest prototype runs [[Pyodide]], a Python runtime compiled to WebAssembly, inside [[Deno]]. Pyodide had previously been available only in web browsers, and Deno's ability to load it made the prototype possible. The sandbox idea is the motivation for the broader [[Running Python in a Deno/Pyodide sandbox]] experiment.

## Key Characteristics

- Binary instruction format, distinct from text-based source languages.
- Runs in a sandboxed environment, which makes it suitable for executing untrusted code.
- Allows language runtimes such as Python (via Pyodide) to be compiled and executed outside their native environment.
- Runtime support depends on the host: Pyodide originally targeted browsers, and Deno's support for loading it enabled the source's prototype.

## Applications

- Running untrusted Python code in a sandbox, as in the Pyodide-in-Deno prototype described in the source.
- Hosting compiled language runtimes (such as Pyodide) inside JavaScript runtimes like [[Deno]], which can load them through [[ECMAScript modules]].

## Related Concepts

- [[concepts/running-python-in-a-denopyodide-sandbox|Running Python in a Deno/Pyodide sandbox]]
- [[concepts/ecmascript-modules|ECMAScript modules]]

## Related Entities

- [[entities/pyodide|Pyodide]]
- [[entities/deno|Deno]]

## Mentions in Source

- "I'm still trying to find the best way to run untrusted Python code in a safe WebAssembly sandbox." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]
- "My latest attempt takes advantage of Pyodide and Deno." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]