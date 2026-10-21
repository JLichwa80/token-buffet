---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "wasmtime-py"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

generation_complete: true
---

# wasmtime

## Description

wasmtime is a WebAssembly runtime library. In the 2023-02-09 weeknotes, Simon Willison uses it through the wasmtime-py Python binding to run Python code inside a sandbox. Earlier attempts with wasmtime, wasmer-python, and pywasm3 failed because all three were poorly documented. [[Tim Bart]] found an example that combined wasmtime with the Python WebAssembly build released by VMware labs, and the author adapted it into his own working version. The approach is somewhat inelegant because standard output and standard error must be redirected to temporary files. It nonetheless gave the author his first way to run untrusted Python code in a sandbox. The sandboxing goal also connects to [[Datasette Lite]], which runs Python in the browser through WebAssembly.

## Related Entities

- [[entities/tim-bart|Tim Bart]]
- [[entities/datasette-lite|Datasette Lite]]

## Related Concepts

## Mentions in Source

- "After I complained about how hard this was noisily in a few different places, Tim Bart stepped in and figured out [this example](https://gist.github.com/pims/711549577759ad1341f1a90860f1f3a5) using `wasmtime` and the new Python WASM build [released by VMware labs](https://wasmlabs.dev/articles/python-wasm32-wasi/)." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]