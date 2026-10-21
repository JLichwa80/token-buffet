---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"
tags:
  - "other"
---

# llama.cpp

> Stub created by the ingest candidate gate (prose+named) — [[sources/2023-12-31-weeknotes_456c53]] names this without treating it. Will be filled by the next ingest of a source that does.

llama.cpp is an open-source runtime for running large language models locally. In this source it appears only as the backend behind the llm-llama-cpp plugin, which lets the LLM command-line tool run models through it. The December 2023 release of llm-llama-cpp 0.3 is described as an LLM plugin for running models using llama.cpp. The source treats llama.cpp as infrastructure for that plugin rather than as its own subject. It connects to the GGUF model format, since llm-llama-cpp's new option loads GGUF files.

> "**[llm-llama-cpp 0.3](https://github.com/simonw/llm-llama-cpp/releases/tag/0.3)**—2023-12-09  
  LLM plugin for running models using llama.cpp" — [[sources/2023-12-31-weeknotes_456c53]]

## New Information (2023-10-30-weeknotes)

- llama.cpp is an open-source library for running language models locally, and it forms the core of the GPT4All chatbot project. (The source identifies llama.cpp as the core of GPT4All, a fact that extends the page's description beyond the llm-llama-cpp context.)
- Nomic AI took llama.cpp and other libraries and wrapped them in a more polished user experience, with installers for Windows, macOS and Ubuntu. (This describes how llama.cpp is packaged for end users by a third party, which adds to the page's account of its role as a dependency.)
- A debugging-output problem that affected llm-gpt4all, which wraps GPT4All and llama.cpp, still affects llm-llama-cpp. (The source notes a shared debugging-output issue that links llama.cpp-based tooling to the llm-gpt4all plugin.)

## New Information (2023-08-05-weeknotes-plugins)

- llama.cpp is the inference engine that the llm-llama-cpp plugin uses to run models, and the plugin can run a GGML quantized version of Llama 2 directly on local hardware. (The 2023-08-05 source states the engine role and the GGML Llama 2 use case, which extend the page's description of llama.cpp's role in the plugin.)
- The setup installs the llama-cpp-python package (llm install llm-llama-cpp llama-cpp-python), which connects llama.cpp to the LLM command-line tool's Python environment. (This is a new setup detail from the 2023-08-05 source that clarifies how llama.cpp is integrated as a dependency.)

## Mentions in Source

- "they’ve taken [llama.cpp](https://github.com/ggerganov/llama.cpp) (and other libraries) and wrapped them in a much nicer experience, complete with Windows, macOS and Ubuntu installers." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "Unfortunately, it spat out weird debugging information that I had been unable to hide (a problem that [still affects llm-llama-cpp](https://github.com/simonw/llm-llama-cpp/issues/22))." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "A few days ago I took that a step further: the new [llm-llama-cpp](https://github.com/simonw/llm-llama-cpp) plugin can now be used to run a GGML quantized version of the Llama 2 model directly on your own hardware." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "LLM plugin for running models using llama.cpp" — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]