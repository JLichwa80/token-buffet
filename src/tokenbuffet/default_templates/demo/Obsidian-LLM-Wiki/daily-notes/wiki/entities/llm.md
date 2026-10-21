---
type: entity
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-09-30-weeknotes_8d48b1]]"
  - "[[sources/2024-07-19-weeknotes_39632e]]"
  - "[[sources/2024-05-28-weeknotes_18b318]]"
  - "[[sources/2024-04-23-weeknotes_a3933c]]"
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-11-22-weeknotes_49168f]]"
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
  - "[[sources/2023-07-16-weeknotes_8e11f0]]"
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"
tags:
  - "project"
  - "other"
aliases:
  - "LLM CLI"
  - "llm command-line tool"
---

# llm

## Description

llm is a command-line tool for accessing large language models, released as version 0.16 on 2024-09-12. Simon Willison maintains it, and it is the central project in his LLM work during the month covered by the weeknotes. Its functionality is extended through plugins, including llm-gemini (access to Google's Gemini models), llm-jina-api (Jina AI embeddings), and llm-cmd (generating and running shell commands). The plugin-oriented design mirrors the approach Willison takes in his Django work. The post's discussion of using LLMs for code is closely related to the llm project, and the tool is part of the same toolset Willison develops alongside [[Datasette]].

LLM 0.15 (released 2024-07-18) added support for OpenAI's GPT-4o mini and made it the default model, replacing GPT-3.5 Turbo. Beyond the command-line tool, LLM is also a Python library for accessing large language models. A bug that appeared only under Homebrew installs, caused by a numpy issue, was fixed by Willison in the sqlite-utils dependency, which led to the sqlite-utils 3.37 release.

LLM 0.14 (released 2024-05-13) added support for OpenAI's GPT-4o. The llm-gemini 0.1a4 plugin (released 2024-05-14) added support for Google's Gemini 1.5 Flash model. The 2024-05-28 weeknotes also describe llm, which is known as the LLM CLI, as one of Willison's core tools for working with language models. Its plugin system is how llm-gemini adds access to Google's Gemini models, and the 0.14 release came alongside the GPT-4o support he reviews among the May model releases.

In April 2024 Willison released several more LLM plugins, including llm-llamafile, llm-anyscale-endpoints, llm-gpt4all, llm-fireworks, llm-replicate, llm-mistral, llm-reka and llm-gemini. The post also shows LLM in use: running Llama 3 from the terminal and running evaluations with `llm evals`.

The llm-gemini 0.1a2 release (April 2024) added support for system prompts to Google's Gemini models, so LLM users can pass a system prompt through the llm-gemini plugin.

The llm-claude-3 plugin provides access to Anthropic's Claude 3 models from the LLM tool, extending the plugin-based model support described above.

LLM 0.13 was released in January 2024, and version 0.13.1 followed on 27 January 2024. The llm-embed-onnx plugin is a thin wrapper around onnx_embedding_models, which wraps the ONNX Runtime, and it makes several new embedding models available to LLM. The llm-gpt4all 0.3 release added access to model options such as `-o max_tokens 3`, allowed models to work without an internet connection, and documented the location of the model files. llm-sentence-transformers gained an `llm sentence-transformers register --trust-remote-code` option, which was needed to support the nomic-embed-text-v1 embedding model.

The earliest plugin releases date from December 2023: llm-llama-cpp 0.3 (2023-12-09) runs models through llama.cpp, llm-gemini 0.1a0 (2023-12-13) was the first release of the Gemini plugin, llm-anyscale-endpoints 0.4 (2023-12-14) provides access to models hosted on Anyscale Endpoints, and llm-mistral 0.2 (2023-12-15) provides access to Mistral models through the Mistral API. A later llm-llama-cpp release added `llm -m gguf -o path` support for trying new GGUF model files. The 2023-12-31 weeknotes highlight "Many options for running Mistral models in your terminal using LLM", which shows the plugin system already being used this way.

LLM 0.12 was released on 2023-11-06, the day of OpenAI DevDay, and added support for OpenAI's GPT-4 Turbo model. GPT-4 Turbo is 2-3x cheaper than GPT-4, faster, and has a 128,000-token limit. The earlier llm-anyscale-endpoints 0.3 plugin, which provides access to models hosted by Anyscale Endpoints, was released on 2023-11-03.

In 2023 Willison recommended the llm-gpt4all plugin as the way to get started running local LLMs, installed with `pipx install llm` followed by `llm install llm-gpt4all`. The llm-python plugin adds an `llm python` command that runs a Python interpreter in the same virtual environment as LLM, which helps when debugging installs made with pipx or Homebrew. In October 2023 the LLM Homebrew package moved to Python 3.12, but PyTorch did not yet support that version, so plugins that depend on it, such as llm-embed-jina, failed to install. Willison replaced the Homebrew installation recommendation with pipx in several places.

LLM gained embedding support in version 0.9, and version 0.10 added binary embedding support for CLIP. Embedding models can now be built as LLM plugins: llm-clip 0.1 (2023-09-12) provides image and text embeddings using CLIP, llm-sentence-transformers 0.1.2 (2023-09-13) was released alongside it, and llm-cluster 0.2 (2023-09-04) adds clustering of embeddings. Willison uses the sqlite-migrate library to manage the schema that stores LLM's embeddings, and that schema is beginning to appear in some [[Datasette]] plugins.

LLM 0.8 (released 2023-08-30) changed the default `llm logs` output from JSON to Markdown. The logs are stored in SQLite and record the prompts and responses previously sent through the tool.

LLM 0.7 added custom model aliases, so you can register a shorthand for an existing model, for example with `llm aliases set turbo gpt-3.5-turbo-16k`. Plugin support arrived a few weeks before 2023-08-16, letting LLM use additional models, including ones that run directly on the user's own device. The llm-mlc plugin (2023-08-16) extends LLM to run Llama 2 locally, and Willison describes it as one of the easiest ways to run Llama 2 on an Apple Silicon Mac with GPU acceleration.

In July 2023 Willison released the llm-replicate plugin the day before Llama 2 launched, so LLM could prompt Llama 2 on launch day. In August 2023 LLM became available in Homebrew core, which made installing LLM and its Llama 2 plugins a short sequence of commands (`brew install llm`, then `llm install llm-llama-cpp llama-cpp-python`). The llm-llama-cpp plugin could also run GGML-quantized Llama 2 models directly on the user's own hardware, as described in the August 2023 weeknotes. Willison describes LLM as similar in design to sqlite-utils, another combined CLI tool and Python library, and added plugin support to sqlite-utils in response to community requests.

LLM 0.5 (July 2023) added a plugin system for alternative language models, so the tool was no longer limited to OpenAI's models. It also added a Python API that works the same way for OpenAI models and for self-hosted models installed via plugins. Early model plugins from this period include llm-palm, which gives access to Google's PaLM 2 model through Google's API, and llm-mpt30b, which provides the 19GB MPT-30B model using the TheBloke/mpt-30B-GGML build. At the July 2023 release, llm-gpt4all provided 17 self-hosted models from the GPT4All project.

Prompt templates arrived in June 2023 as LLM's newest major feature. They let you save reusable prompts and model settings as files, which you create with `llm templates edit summary` and run with the `-t` option.
## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/llm-gemini|llm-gemini]]
- [[entities/gpt-4o|GPT-4o]]
- [[entities/llm-evals-plugin|llm-evals-plugin]]
- [[entities/llm-command-r|llm-command-r]]
- [[entities/llm-rag|llm-rag]]

## Related Concepts

- [[concepts/using-llms-for-code|Using LLMs for code]]
- [[concepts/plugins|Plugin system]]
- [[concepts/large-language-models|Large Language Models]]
- Willison plans to add Retrieval Augmented Generation support to LLM, either in LLM itself or in Datasette, built on the LLM embedding mechanism.
- llm-openrouter and llm-anyscale-endpoints were released as [[concepts/plugins|plugin]] extensions built on LLM's existing OpenAI-compatible code, each under 30 lines, extending LLM to OpenRouter and Anyscale Endpoints.
- Willison's stated goal for LLM is to grow a community of enthusiasts who write [[concepts/plugins|plugins]] to support new models as they are released, supported by a tutorial on writing a model plugin.
- In June 2023 Willison planned four LLM plugin categories, inspired by Datasette's plugin system: command plugins, template plugins, model plugins and function plugins. The model plugin category had the only working example, a PaLM 2 plugin that calls Google Vertex.
## New Information (2023-08-30-datasette-plus-weeknotes)

- LLM runs both locally and via APIs, available as a CLI tool and a Python library. (Restates the core scope of the tool; the Description page section already covers this, so it is supplementary.)

## New Information (2023-07-16-weeknotes)

- Willison's symbex tool supports a --rexec option that passes a function's body through a shell command such as `llm --system 'add type hints and a docstring'`, then writes the output back to the file in place. (This is a concrete scenario in which LLM is used as a component inside another tool, which fits the page's usage examples.)

## Mentions in Source

- "[LLM](https://llm.datasette.io/) is my command-line tool and Python library for interacting with Large Language Models." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I released updates for two LLM plugins as well:" — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "llm-claude-3 provides access to the new Claude 3 models from my LLM tool." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "Since I have a lot of software that builds on these models, I spent a bunch of time today publishing new releases of things." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "[llm cmd undo last git commit—a new plugin for LLM](https://simonwillison.net/2024/Mar/26/llm-cmd/)" — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "[llm-evals-plugin](https://github.com/simonw/llm-evals-plugin) (`llmevals` was taken on PyPI already) is a *very* early prototype of an [LLM](https://llm.datasette.io/) plugin that I hope to use to address this problem." — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]
- "Then, to run the eval against multiple models:" — [[_Inbox/2024-04-23-weeknotes|2024-04-23-weeknotes]]
- "adding support for the new inexpensive Gemini 1.5 Flash." — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "LLM had a frustrating bug involving a weird numpy issue that only manifested on LLM when installed via Homebrew." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]
- "I shipped a new LLM release to support the new model." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]
- "Access large language models from the command-line" — [[_Inbox/2024-09-30-weeknotes|2024-09-30-weeknotes]]
- "LLM plugin to access Google’s Gemini family of models" — [[_Inbox/2024-09-30-weeknotes|2024-09-30-weeknotes]]
- "Use LLM to generate and execute commands in your shell" — [[_Inbox/2024-09-30-weeknotes|2024-09-30-weeknotes]]
- "* [Many options for running Mistral models in your terminal using LLM](https://simonwillison.net/2023/Dec/18/mistral/), demonstrating how LLM’s plugins system has really started to pay off." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "* **[llm-llama-cpp 0.3](https://github.com/simonw/llm-llama-cpp/releases/tag/0.3)**—2023-12-09  
  LLM plugin for running models using llama.cpp" — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]