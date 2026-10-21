---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-07-16-weeknotes_8e11f0]]"
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"
tags:
  - "project"
---

# symbex

## Description

Symbex is a command-line tool by Simon Willison for extracting symbols, meaning functions, methods, and classes, from Python code. Version 1.4 added JSON, CSV, and TSV output, so the symbol lists can be piped into [[LLM|llm]] `embed-multi`. This makes it possible to create an embedding for every function in a codebase. The resulting embeddings support related-function lookup and [[Semantic search|semantic function search]]. The source connects Symbex to the wider embedding work described in the weeknotes.

Symbex is also a Python CLI for finding functions and classes and printing either their full source or only their signature. Its own description in the 27 June 2023 weeknotes is a tool for searching Python code that outputs the body of a matching function or class. Version 1.1 added a `--check` mode, modeled on `black . --check`, that enforces code-quality rules such as docstrings and type annotations, for example `symbex --function --undocumented --check`. It also added `--rexec`, which replaces a symbol's body with the output of a shell command, such as `symbex my_function --rexec "llm --system 'add type hints and a docstring'"`; Willison cautions that this should only be run on code already committed to Git.

Symbex began as a way to quickly find and print the body of a specific Python function or class, so the output could be piped to an LLM such as GPT-3.5 or GPT-4 for processing. The `-s`/`--signatures` option prints only a matching symbol's signature, which keeps the token count low when the output goes to a language model. Further options add docstrings and import lines to the output and suppress the file comment, for example `symbex find_symbol_nodes -s --docstrings -in`. A planned set of filters would select symbols by type or documentation status, such as `--undocumented` and `--untyped`. By the 27 June 2023 weeknotes, Symbex had received 12 total releases.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/gpt-4|gpt-4]]

## Related Concepts

- [[concepts/embeddings|Embeddings]]
- [[concepts/semantic-search|Semantic search]]
- [[concepts/token-count|Token count]]

## Mentions in Source

- "`symbex` is a tool for searching Python code." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "It’s since grown a bunch more features across [12 total releases](https://github.com/simonw/symbex/releases)." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "So... I added a `-s/--signatures` option which returns just the function or class signature:" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "Symbex is my Python CLI tool for quickly finding Python functions and classes and outputting either the full code or just the signature of the matching symbol." — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]
- "It’s an imitation of black . --check—the idea is that Symbex can now be used to enforce code quality issues like docstrings and the presence of type annotations." — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]
- "Symbex 1.4 adds a tiny but impactful feature: it can now output a list of symbols as JSON, CSV or TSV." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]