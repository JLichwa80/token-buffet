# Weeknotes: a Datasette release, an LLM release and a bunch of new plugins

Source: https://simonwillison.net/2024/Feb/9/weeknotes/

## Weeknotes: a Datasette release, an LLM release and a bunch of new plugins

9th February 2024

I wrote extensive annotated release notes for [Datasette 1.0a8](https://simonwillison.net/2024/Feb/7/datasette-1a8/) and [LLM 0.13](https://simonwillison.net/2024/Jan/26/llm/) already. Here’s what else I’ve been up to this past three weeks.

#### New plugins for Datasette

* **[datasette-proxy-url](https://datasette.io/plugins/datasette-proxy-url)** is a very simple plugin that simple lets you configure a path within Datasette that serves content proxied from another URL.

  I built this one because I ran into a bug with Substack where Substack were denying requests to my newsletter’s RSS feed from code running in GitHub Actions! Frustrating, since the whole *point* of RSS is to be retrieved by bots.

  I solved it by deploying a quick proxy to a Datasette instance I already had up and running, effectively treating Datasette as a cheap deployment platform for random pieces of proxying infrastructure.
* **[datasette-homepage-table](https://datasette.io/plugins/datasette-homepage-table)** lets you configure Datasette to display a specific table as the homepage of the instance. I’ve wanted this for a while myself, someone requested it on [Datasette Discord](https://datasette.io/discord) and it turned out to be pretty quick to build.
* **[datasette-events-db](https://datasette.io/plugins/datasette-events-db)** hooks into the new [events mechanism](https://docs.datasette.io/en/1.0a8/plugin_hooks.html#event-tracking) in Datasette 1.0a8 and logs any events (`create-table`, `login` etc) to a `datasette_events` table. I released this partly as a debugging tool and partly because I like to ensure every Datasette plugin hook has at least one released plugin that uses it.
* **[datasette-enrichments-quickjs](https://datasette.io/plugins/datasette-enrichments-quickjs)** was this morning’s project. It’s a plugin for [Datasette Enrichments](https://simonwillison.net/2023/Dec/1/datasette-enrichments/) that takes advantage of the [quickjs](https://pypi.org/project/quickjs/) Python package—a wrapper around the excellent [QuickJS engine](https://bellard.org/quickjs/)—to support running a custom JavaScript function against every row in a table to populate a new column.

  QuickJS appears to provide a robust sandbox, including both memory and time limits! I need to write more about this plugin, it opens up some very exciting new possibilities for Datasette.

I also published some significant updates to existing plugins:

* **[datasette-upload-csvs](https://datasette.io/plugins/datasette-upload-csvs)** got a long-overdue improvement allowing it to upload CSVs to a specified database, rather than just using the first available one. As part of this I completely re-engineered how it works in terms of threading strategies, as described in [issue 38](https://github.com/simonw/datasette-upload-csvs/issues/38). Plus it’s now tested against the Datasette 1.0 alpha series in addition to 0.x stable.

#### Plugins for LLM

[LLM](https://llm.datasette.io/) is my command-line tool and Python library for interacting with Large Language Models. I released one new plugin for that:

* **[llm-embed-onnx](https://github.com/simonw/llm-embed-onnx)** is a thin wrapper on top of [onnx\_embedding\_models](https://github.com/taylorai/onnx_embedding_models) by Benjamin Anderson which itself wraps the powerful [ONNX Runtime](https://onnxruntime.ai/). It makes several new embeddings models available for use with LLM, listed [in the README](https://github.com/simonw/llm-embed-onnx/blob/main/README.md#usage).

I released updates for two LLM plugins as well:

* **[llm-gpt4all](https://github.com/simonw/llm-gpt4all)** got a release with improvements from three contributors. I’ll quote [the release notes](https://github.com/simonw/llm-gpt4all/releases/tag/0.3) in full:

  > + Now provides access to model options such as `-o max_tokens 3`. Thanks, [Mauve Signweaver](https://github.com/RangerMauve). [#3](https://github.com/simonw/llm-gpt4all/issues/3)
  > + Models now work without an internet connection. Thanks, [Cameron Yick](https://github.com/hydrosquall). [#10](https://github.com/simonw/llm-gpt4all/issues/10)
  > + Documentation now includes the location of the model files. Thanks, [Werner Robitza](https://github.com/slhck). [#21](https://github.com/simonw/llm-gpt4all/pull/21)
* **[llm-sentence-transformers](https://github.com/simonw/llm-sentence-transformers)** now has a `llm sentence-transformers register --trust-remote-code` option, which was necessary to support the newly released [nomic-embed-text-v1](https://huggingface.co/nomic-ai/nomic-embed-text-v1) embedding model.

I finally started hacking on a `llm-rag` plugin which will provide an implementation of Retrieval Augmented Generation for LLM, similar to the process I describe in [Embedding paragraphs from my blog with E5-large-v2](https://til.simonwillison.net/llms/embed-paragraphs).

I’ll write more about that once it’s in an interesting state.

#### shot-scraper 1.4

[shot-scraper](https://shot-scraper.datasette.io/) is my CLI tool for taking screenshots of web pages and running scraping code against them using JavaScript, built on top of [Playwright](https://playwright.dev/).

I dropped into the repo to add HTTP Basic authentication support and found several excellent PRs waiting to be merged, so I bundled those together into a new release.

Here are the full release notes for [shot-scraper 1.4](https://github.com/simonw/shot-scraper/releases/tag/1.4):

> * New `--auth-username x --auth-password y` options for each `shot-scraper` command, allowing a username and password to be set for HTTP Basic authentication. [#140](https://github.com/simonw/shot-scraper/issues/140)
> * `shot-scraper URL --interactive` mode now respects the `-w` and `-h` arguments setting the size of the browser viewport. Thanks, [mhalle](https://github.com/mhalle). [#128](https://github.com/simonw/shot-scraper/issues/128)
> * New `--scale-factor` option for setting scale factors other than 2 (for retina). Thanks, [Niel Thiart](https://github.com/nielthiart). [#136](https://github.com/simonw/shot-scraper/issues/136)
> * New `--browser-arg` option for passing extra browser arguments (such as `--browser-args "--font-render-hinting=none"`) through to the underlying browser. Thanks, [Niel Thiart](https://github.com/nielthiart). [#137](https://github.com/simonw/shot-scraper/issues/137)

#### Miscellaneous other projects

* We had some pretty severe storms in the San Francisco Bay Area last week, inspired me to revisit [my old PG&E outage scraper](https://github.com/simonw/shot-scraper/releases/tag/1.4). PG&E’s outage map changed and broke that a couple of years ago, but I got [a new scraper up](https://github.com/simonw/pge-outages) and running just in time to start capturing outages.
* I’ve been wanting a way to quickly create additional labels for my GitHub repositories for a while. I finally put together a simple system for that based on GitHub Actions, described in this TIL: [Creating GitHub repository labels with an Actions workflow](https://til.simonwillison.net/github-actions/creating-github-labels).

#### Releases

* **[datasette-enrichments-quickjs 0.1a0](https://github.com/datasette/datasette-enrichments-quickjs/releases/tag/0.1a0)**—2024-02-09  
  Enrich data with a custom JavaScript function
* **[datasette-events-db 0.1a0](https://github.com/datasette/datasette-events-db/releases/tag/0.1a0)**—2024-02-08  
  Log Datasette events to a database table
* **[datasette 1.0a8](https://github.com/simonw/datasette/releases/tag/1.0a8)**—2024-02-07  
  An open source multi-tool for exploring and publishing data
* **[shot-scraper 1.4](https://github.com/simonw/shot-scraper/releases/tag/1.4)**—2024-02-05  
  A command-line utility for taking automated screenshots of websites
* **[llm-sentence-transformers 0.2](https://github.com/simonw/llm-sentence-transformers/releases/tag/0.2)**—2024-02-04  
  LLM plugin for embeddings using sentence-transformers
* **[datasette-homepage-table 0.2](https://github.com/datasette/datasette-homepage-table/releases/tag/0.2)**—2024-01-31  
  Show a specific Datasette table on the homepage
* **[datasette-upload-csvs 0.9](https://github.com/simonw/datasette-upload-csvs/releases/tag/0.9)**—2024-01-30  
  Datasette plugin for uploading CSV files and converting them to database tables
* **[llm-embed-onnx 0.1](https://github.com/simonw/llm-embed-onnx/releases/tag/0.1)**—2024-01-28  
  Run embedding models using ONNX
* **[llm 0.13.1](https://github.com/simonw/llm/releases/tag/0.13.1)**—2024-01-27  
  Access large language models from the command-line
* **[llm-gpt4all 0.3](https://github.com/simonw/llm-gpt4all/releases/tag/0.3)**—2024-01-24  
  Plugin for LLM adding support for the GPT4All collection of models
* **[datasette-granian 0.1](https://github.com/simonw/datasette-granian/releases/tag/0.1)**—2024-01-23  
  Run Datasette using the Granian HTTP server
* **[datasette-proxy-url 0.1.1](https://github.com/datasette/datasette-proxy-url/releases/tag/0.1.1)**—2024-01-23  
  Proxy a URL through a Datasette instance

#### TILs

* [Creating GitHub repository labels with an Actions workflow](https://til.simonwillison.net/github-actions/creating-github-labels)—2024-02-09
* [Exploring ColBERT with RAGatouille](https://til.simonwillison.net/llms/colbert-ragatouille)—2024-01-28
* [Logging OpenAI API requests and responses using HTTPX](https://til.simonwillison.net/httpx/openai-log-requests-responses)—2024-01-26
