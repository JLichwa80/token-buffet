---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Simon Willison weeknotes"
  - "27 June 2023"
  - "2023-06-27-weeknotes"
contentHash: 1ebd-5757cef0
source_file: "[[_Inbox/2023-06-27-weeknotes.md]]"
generation_complete: true
---

# 2023-06-27-weeknotes - Summary

## Source

- Original file: [[_Inbox/2023-06-27-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

Simon Willison's weeknotes of 27 June 2023 cover a short break that included a UK holiday, along with the projects he kept building. The main one is [[entities/symbex|symbex]], a command-line tool for finding Python functions and classes, which had grown across 12 releases. Its `-s/--signatures` option returns only signatures, keeping output short when piped to a model, which reflects the importance of [[concepts/token-count|token count]]. Planned filters such as `--undocumented` and `--untyped` would show how well a codebase is typed and documented.

The second topic is [[entities/llm|LLM]], his command-line tool for working with language models. Its big new feature is [[concepts/prompt-templates|prompt templates]], which are saved as files and run with `-t`. The post also outlines [[concepts/llm-plugins|LLM plugins]] inspired by [[entities/datasette|Datasette]]: [[concepts/command-plugins|command plugins]], [[concepts/template-plugins|template plugins]], [[concepts/model-plugins|model plugins]] and [[concepts/function-plugins|function plugins]]. The function plugins depend on the [[concepts/openai-functions|OpenAI functions mechanism]]. All of this work was still under active development.

## Key Entities

- [[entities/symbex|symbex]]: Python code search tool that outputs function and class bodies, signatures, docstrings and imports.
- [[entities/llm|llm]]: Command-line tool for language models, extended with prompt templates and planned plugins.
- [[entities/datasette|datasette]]: Data exploration project whose plugin system inspired LLM's plugins.

## Key Concepts

- [[concepts/prompt-templates|prompt-templates]]: Reusable prompts and model settings saved as files and run with `-t`.
- [[concepts/llm-plugins|llm-plugins]]: Planned extension system for LLM with four plugin categories.
- [[concepts/token-count|token-count]]: The key constraint when piping text into a model, motivating symbex's signature output.
- [[concepts/openai-functions|openai-functions-mechanism]]: OpenAI API feature for model-callable functions, which function plugins depend on.
- [[concepts/command-plugins|command-plugins]]: Plugins that add subcommands such as `llm search` or `llm embed`.
- [[concepts/template-plugins|template-plugins]]: Plugins that distribute installable prompt templates.
- [[concepts/model-plugins|model-plugins]]: Plugins that let LLM use models beyond GPT-3.5 and GPT-4, such as PaLM 2 and local models.
- [[concepts/function-plugins|function-plugins]]: Plugins that make new functions available for the model to execute.

## Main Points

- **symbex** has reached 12 releases. Its signature output reduces the text sent to a language model.
- Planned symbex filters such as `--undocumented` and `--untyped` would report how well a codebase is documented and typed.
- **Prompt templates** are the major new LLM feature, saving reusable prompts and model settings as files.
- LLM plugins are planned in four categories: command, template, model and function plugins.
- An example model plugin can call Google's PaLM 2 model through Google Vertex. The author hopes to support local models such as those run by llama.cpp.
- The plugin work was still under active development at the time of the post.

## Mentions in Source

- "`symbex` is a tool for searching Python code." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "It’s since grown a bunch more features across [12 total releases](https://github.com/simonw/symbex/releases)." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "So... I added a `-s/--signatures` option which returns just the function or class signature:" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "I’ve also been working on some major improvements to my [LLM](https://llm.datasette.io/) tool for working with language models from the command-line." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "My [LLM](https://llm.datasette.io/) tool is shaping up in some interesting directions as well." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "I want LLM to be able to use more than just GPT-3.5 and GPT-4." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "The initial goal was to make it quick to find and output the body of a specific Python function or class, such that you could then pipe it to [LLM](https://llm.datasette.io/) to process it with GPT-3.5 or GPT-4:" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "I’m adding plugins to LLM, inspired by [plugins in Datasette](https://docs.datasette.io/en/stable/plugins.html)." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "Datasette plugin that renders binary blob images using data-uris" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "The big new released feature is [prompt templates](https://llm.datasette.io/en/stable/templates.html)." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "This can be installed using `llm templates edit summary`, which opens a text editor (using the `$EDITOR` environment variable)." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "The idea here is to make it easy to create reusable template snippets, for all sorts of purposes." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]