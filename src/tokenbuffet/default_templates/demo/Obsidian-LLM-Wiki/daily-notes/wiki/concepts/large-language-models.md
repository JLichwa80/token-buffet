---
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
  - "[[sources/2023-04-23-weeknotes_572e37]]"
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"
tags:
  - "terminology"
aliases:
  - "Large Language Model"
---

## Description

Large language models (LLMs) are neural networks trained on large text corpora, a trait illustrated by the April 2023 analysis of the RedPajama-Data-1T LLM training set. Simon Willison's WordCamp US keynote in August 2023, published as the transcript "Making Large Language Models work for you," was built around the subject, and his North Bay Python closing talk, "Catching up on the weird world of LLMs," summarized the field's development in 40 minutes. In March 2023 his blog covered a wave of launches, including [[Claude]], [[GPT-4]], and [[Google Bard]], and he noted that [[ChatGPT]] cannot access the internet, that LLaMA was having its "Stable Diffusion moment," that Stanford Alpaca accelerated on-device model development, and that a ChatGPT-beating model might be trained for $85,000 and run in a browser. Bard's self-descriptions were also unreliable, since it was not trained on Gmail. LLMs can run in several places: [[Web LLM]] runs [[vicuna-7b]] entirely in the browser, [[Llama 2]] (the first commercially usable version of Meta's LLaMA) could be prompted through the LLM CLI on its July 18, 2023 launch day via the llm-replicate plugin, and llm-llama-cpp runs a GGML quantized Llama 2 on the user's own hardware. The [[LLM]] tool lets users run models locally or via APIs as both a CLI and a Python library, and the llm-openrouter and llm-anyscale-endpoints plugins add hosted models from OpenRouter and Anyscale Endpoints. Willison later described the LLM tool as a way to access large language models from the command line and argued that the Python community has a unique opportunity and responsibility to help nudge the technology in a positive direction.

## Related Concepts

- [[concepts/imitation-intelligence|Imitation intelligence]]
- [[concepts/structured-data-extraction|Structured data extraction]]
- [[concepts/weeknotes|Weeknotes]]
- [[concepts/my-blog-as-a-newsletter|My blog as a newsletter]]

## Related Entities

- [[entities/llm|llm]]
- [[entities/gpt-4o|GPT-4o]]
- [[entities/gemini-1-5-flash|Gemini 1.5 Flash]]

## New Information (2023-08-30-datasette-plus-weeknotes)

- Large Language Models are the subject of Simon Willison's WordCamp US keynote, delivered in August 2023 and later published as a detailed transcript, "Making Large Language Models work for you". (The source identifies LLMs as the central topic of the keynote, which is a public-facing account of the subject and belongs in the page description.)
- LLM lets you run large language models either locally or via APIs, as both a CLI tool and a Python library. (This describes a concrete tool for running LLMs, which is a real-world usage scenario for the concept.)
- The llm-openrouter and llm-anyscale-endpoints plugins add LLM support for models hosted by OpenRouter and Anyscale Endpoints. (These plugins are examples of accessing hosted LLMs through third-party providers, which fits under usage applications.)

## New Information (2023-08-05-weeknotes-plugins)

- Llama 2 (the first commercially usable version of Meta's LLaMA language model) could be prompted via the LLM command-line tool on its launch day, July 18, 2023, thanks to the llm-replicate plugin. (This is a concrete real-world use of running a large language model through the LLM CLI tool, which fits the Applications section.)
- The llm-llama-cpp plugin can run a GGML quantized version of Llama 2 directly on the user's own hardware. (This describes local, offline execution of an LLM, a distinct usage scenario from hosted APIs.)
- Simon Willison gave the closing talk at North Bay Python, titled "Catching up on the weird world of LLMs", which summarized the last few years of development in the field of LLMs in 40 minutes. (The talk is a public account centered on the subject of large language models, which belongs in the page description alongside the WordCamp keynote.)

## New Information (2023-04-23-weeknotes)

- Web LLM runs the vicuna-7b Large Language Model entirely in your browser, and it’s very impressive (This is a concrete real-world scenario of running an LLM locally in a web browser, which fits the Applications section.)
- LLMs are trained on large text corpora, as shown by the analysis of the RedPajama-Data-1T LLM training set in April 2023. (Training on large text corpora is a defining trait of LLMs, and the source ties it to a specific training dataset.)

## Mentions in Source

- "Since then I’ve been mostly decompressing and catching up with old friends, and having lots of interesting conversations about Python (and a few extras about LLMs)." — [[_Inbox/2023-04-23-weeknotes|2023-04-23-weeknotes]]
- "Web LLM runs the vicuna-7b Large Language Model entirely in your browser, and it’s very impressive" — [[_Inbox/2023-04-23-weeknotes|2023-04-23-weeknotes]]
- "I tried to summarize the last few years of development in the field of LLMs in just 40 minutes." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "Last Friday I gave a keynote at [WordCamp US](https://us.wordcamp.org/2023/) on the subject of Large Language Models." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "tying together much of what I’ve learned about Large Language Models over the past couple of years and making the case that the Python community has a unique opportunity and responsibility to help try to nudge this technology in a positive direction." — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "Access large language models from the command-line" — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "AI just keeps getting weirder and more interesting." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "Two Tuesdays ago we got a Google announcement, Anthropic’s Claude and GPT-4." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "I’m beginning to expect that every Tuesday may be a write-off for the next few years, since the AI community seems to have decided that Tuesday is the day to launch everything." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]