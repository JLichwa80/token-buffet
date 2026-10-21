# Weeknotes: Plugins for LLM, sqlite-utils and Datasette

Source: https://simonwillison.net/2023/Aug/5/weeknotes-plugins/

## Weeknotes: Plugins for LLM, sqlite-utils and Datasette

5th August 2023

The principle theme for the past few weeks has been plugins.

#### Llama 2 in LLM via plugins

I added the ability to support models other than the OpenAI ones to my [LLM](https://llm.datasette.io/) command-line tool [last month](https://simonwillison.net/2023/Jul/12/llm/). The timing on this could not have been better: [Llama 2](https://ai.meta.com/llama/) (the first commercially usable version of Meta’s LLaMA language model) was released on July 18th, and I was able to add support to prompting it via LLM that very morning thanks to [the llm-replicate plugin](https://simonwillison.net/2023/Jul/18/accessing-llama-2/) I had released the day before that launch.

(I had heard a tip that a new exciting LLM was about to be released on [Replicate](https://replicate.com/), though I didn’t realize it was Llama 2 until after the announcement.)

A few days ago I took that a step further: the new [llm-llama-cpp](https://github.com/simonw/llm-llama-cpp) plugin can now be used to run a GGML quantized version of the Llama 2 model directly on your own hardware.

LLM is [available in Homebrew core now](https://formulae.brew.sh/formula/llm), so getting Llama 2 working is as simple as:

```
brew install llm
llm install llm-llama-cpp llama-cpp-python
llm llama-cpp download-model \
  https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q8_0.bin \
  --alias llama2-chat --alias l2c --llama2-chat
```

Then:

```
llm -m l2c 'Tell me a joke about a llama'
```

I wrote more about this in [Run Llama 2 on your own Mac using LLM and Homebrew](https://simonwillison.net/2023/Aug/1/llama-2-mac/)—including instructions for calling Llama 2 using the LLM Python API as well.

#### Plugins for sqlite-utils

My [sqlite-utils](https://sqlite-utils.datasette.io/) project, similar to LLM, is a combined CLI tool and Python library. Based on requests from the community I [adding plugin support to it](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/) too.

There are two categories of plugins so far: plugins that add extra commands to the `sqlite-utils` CLI tool, and plugins that add extra custom SQL functions that can be executed against SQLite.

There are quite a few plugins [listed in the sqlite-utils plugins directory](https://github.com/simonw/sqlite-utils-plugins) already.

I built [sqlite-utils-shell](https://github.com/simonw/sqlite-utils-shell) in time for the initial launch, to help demonstrate the new system by adding a `sqlite-utils shell` command that opens an interactive shell enabling any SQL functions that have been installed by other plugins.

Alex Garcia suggested I look at [litecli](https://github.com/dbcli/litecli) by Amjith Ramanujam, which is a much more sophisticated terminal shell for SQLite, incorporating auto-completion against tables and columns.

I used that to build a better alternative to my `sqlite-utils-shell` plugin: [sqlite-utils-litecli](https://github.com/simonw/sqlite-utils-litecli), which lets you run the following command to get a full `litecli` shell with all of the custom SQL functions from other plugins:

```
sqlite-utils litecli mydatabase.db
```

![Screenshot showing the plugin in action - it includes autocomplete of SQLite table names](https://static.simonwillison.net/static/2023/sqlite-utils-litecli.jpg)

#### datasette-auth-tokens and dclient

Meanwhile, in Datasette land... I’ve been investing more time building [Datasette Cloud](https://www.datasette.cloud/), the SaaS cloud hosted version of Datasette.

The Datasette 1.0 alphas introduced a write API. I wanted a mechanism for Datasette Cloud users to be able to setup automatic imports of data into their instances, taking advantage of that API.

This meant I needed an API key mechanism that allowed tokens to be both created and revoked interactively.

I ended up building that into the existing `datasette-auth-tokens` plugin, released in preview in the [datasette-auth-tokens 0.4a0](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a0) alpha.

I’ve been quietly working on a new CLI utility for interacting with Datasette instances via the API, called `dcloud`. I shipped [dcloud 0.2](https://github.com/simonw/dclient/releases/tag/0.2) with a new `dclient insert` command that can read CSV, TSV or JSON data and write it to an external Datasette instance using that new [1.0 write API](https://docs.datasette.io/en/1.0a2/json_api.html#the-json-write-api).

I’ll have more news to share about Datasette Cloud soon!

#### Large Language Model talk at North Bay Python

On Sunday I gave the closing talk at [North Bay Python](https://2023.northbaypython.org/), titled [Catching up on the weird world of LLMs](https://simonwillison.net/2023/Aug/3/weird-world-of-llms/).

I tried to summarize the last few years of development in the field of LLMs in just 40 minutes. I’m pretty happy with how it turned out! I’ve since published a full annotated transcript of the talk, with slides, additional links and notes—so even if you don’t want to watch the full talk you can still read through a thorough summary of what I covered.

I’ve given a few of my talks this treatment now and I really like it—it’s a great way to unlock as much value as possible from the time I spend putting one of these things together.

Examples of this format:

* [Catching up on the weird world of LLMs](https://simonwillison.net/2023/Aug/3/weird-world-of-llms/)—from this Sunday.
* [Prompt injection explained, with video, slides, and a transcript](https://simonwillison.net/2023/May/2/prompt-injection-explained/) for a LangChain webinar in May 2023.
* [Coping strategies for the serial project hoarder](https://simonwillison.net/2022/Nov/26/productivity/) for DjangoCon US 2022.
* [How to build, test and publish an open source Python library](https://simonwillison.net/2021/Nov/4/publish-open-source-python-library/) for PyGotham in November 2021
* [Datasette—an ecosystem of tools for working with small data](https://simonwillison.net/2021/Jul/22/small-data/) for PyGotham 2020.
* [Personal Data Warehouses: Reclaiming Your Data](https://simonwillison.net/2020/Nov/14/personal-data-warehouses/) for the GitHub OCTO speaker series in November 2020.
* [Redis tutorial at NoSQL Europe](https://static.simonwillison.net/static/2010/redis-tutorial/)—this was the first time I put together annotated slides like this, for a three hour tutorial on Redis presented at NoSQL Europe back in 2010.

This time round I [built a small tool](https://til.simonwillison.net/tools/annotated-presentations) to help me assemble the notes and alt attributes for the video—I hope to write more about that soon.

#### Blog entries these weeks

* [Catching up on the weird world of LLMs](https://simonwillison.net/2023/Aug/3/weird-world-of-llms/)
* [Run Llama 2 on your own Mac using LLM and Homebrew](https://simonwillison.net/2023/Aug/1/llama-2-mac/)
* [sqlite-utils now supports plugins](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/)
* [Accessing Llama 2 from the command-line with the llm-replicate plugin](https://simonwillison.net/2023/Jul/18/accessing-llama-2/)

#### Releases these weeks

* **[llm-llama-cpp 0.1a0](https://github.com/simonw/llm-llama-cpp/releases/tag/0.1a0)**—2023-08-01  
  LLM plugin for running models using llama.cpp
* **[datasette-upload-dbs 0.2](https://github.com/simonw/datasette-upload-dbs/releases/tag/0.2)**—2023-08-01  
  Upload SQLite database files to Datasette
* **[sqlite-utils-litecli 0.1.1](https://github.com/simonw/sqlite-utils-litecli/releases/tag/0.1.1)**—2023-07-26  
  Interactive shell for sqlite-utils using litecli
* **[llm-gpt4all 0.1.1](https://github.com/simonw/llm-gpt4all/releases/tag/0.1.1)**—2023-07-25  
  Plugin for LLM adding support for the GPT4All collection of models
* **[dclient 0.2](https://github.com/simonw/dclient/releases/tag/0.2)**—2023-07-24  
  A client CLI utility for Datasette instances
* **[llm 0.6.1](https://github.com/simonw/llm/releases/tag/0.6.1)**—2023-07-24  
  Access large language models from the command-line
* **[asgi-replay 0.1a0](https://github.com/simonw/asgi-replay/releases/tag/0.1a0)**—2023-07-24  
  Record and replay ASGI web page loads
* **[sqlite-utils-shell 0.2](https://github.com/simonw/sqlite-utils-shell/releases/tag/0.2)**—2023-07-24  
  Interactive shell for sqlite-utils
* **[sqlite-utils-dateutil 0.1](https://github.com/simonw/sqlite-utils-dateutil/releases/tag/0.1)**—2023-07-24  
  Date utility functions for sqlite-utils
* **[sqlite-migrate 0.1a1](https://github.com/simonw/sqlite-migrate/releases/tag/0.1a1)**—2023-07-23  
  A simple database migration system for SQLite, based on sqlite-utils
* **[sqlite-utils 3.34](https://github.com/simonw/sqlite-utils/releases/tag/3.34)**—2023-07-22  
  Python CLI utility and library for manipulating SQLite databases
* **[llm-replicate 0.3](https://github.com/simonw/llm-replicate/releases/tag/0.3)**—2023-07-20  
  LLM plugin for models hosted on Replicate
* **[symbex 1.3](https://github.com/simonw/symbex/releases/tag/1.3)**—2023-07-19  
  Find the Python code for specified symbols
* **[datasette-auth-tokens 0.4a0](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a0)**—2023-07-17  
  Datasette plugin for authenticating access using API tokens

#### TIL these weeks

* [Checking if something is callable or async callable in Python](https://til.simonwillison.net/python/callable)—2023-08-04
* [axe-core and shot-scraper for accessibility audits](https://til.simonwillison.net/shot-scraper/axe-core)—2023-07-30
* [Exploring the Overture Maps places data using DuckDB, sqlite-utils and Datasette](https://til.simonwillison.net/overture-maps/overture-maps-parquet)—2023-07-27
* [Protocols in Python](https://til.simonwillison.net/python/protocols)—2023-07-26
* [Using pytest-httpx to run intercepted requests through an in-memory Datasette instance](https://til.simonwillison.net/datasette/pytest-httpx-datasette)—2023-07-25
