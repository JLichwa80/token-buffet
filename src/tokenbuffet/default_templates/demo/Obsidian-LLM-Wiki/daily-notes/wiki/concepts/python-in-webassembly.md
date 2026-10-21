---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Python WASM build"
  - "Python WebAssembly build"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

generation_complete: true
---

# Python in WebAssembly

## Definition

Python in WebAssembly refers to builds of the Python interpreter compiled to run inside a WebAssembly runtime. Such builds let Python code execute within a sandboxed environment rather than directly on the host system.

## Key Characteristics

- The Python interpreter is compiled to WebAssembly, so it runs inside a WebAssembly runtime.
- Runs in a sandboxed environment, which makes it possible to isolate untrusted Python code.
- Can be driven from a regular Python script through the [[wasmtime]] library, according to the source.
- A Python WASM build released by VMware labs was used in the source's solution.
- Standard output and standard error must be redirected to temporary files, which the source describes as somewhat inelegant.

## Applications

- Running Python in the browser, as in [[Datasette Lite]], which uses one such build.
- Running Python inside a regular Python script via [[wasmtime]], a workflow the source attributes to [[Tim Bart]].
- Sandboxing untrusted Python code, which the source says this approach makes possible for the first time.

## Related Concepts

## Related Entities

- [[entities/wasmtime|wasmtime]]
- [[entities/datasette-lite|Datasette Lite]]
- [[entities/tim-bart|Tim Bart]]

## Mentions in Source

- "There are multiple builds of Python in WebAssembly now—I use one of them in my [Datasette Lite](https://simonwillison.net/2022/May/4/datasette-lite/) web application." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]