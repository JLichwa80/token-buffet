# Three major LLM releases in 24 hours (plus weeknotes)

Source: https://simonwillison.net/2024/Apr/10/weeknotes-llm-releases/

## Three major LLM releases in 24 hours (plus weeknotes)

10th April 2024

I’m a bit behind on my [weeknotes](https://simonwillison.net/tags/weeknotes/), so there’s a lot to cover here. But first... a review of the last 24 hours of Large Language Model news. All times are in US Pacific on April 9th 2024.

* 11:01am: Google Gemini Pro 1.5 hits general availability, here’s [the blog post](https://developers.googleblog.com/2024/04/gemini-15-pro-in-public-preview-with-new-features.html)—their 1 million token context GPT-4 class model now has no waitlist, is available to anyone in 180 countries (not including Europe or the UK as far as I can tell) and most impressively all the API has a **free tier** that allows up to 50 requests a day, though rate limited to 2 per minute. Beyond that you can pay $7/million input tokens and $21/million output tokens, which is slightly less than GPT-4 Turbo and a little more than Claude 3 Sonnet. Gemini Pro also now support audio inputs and system prompts.
* 11:44am: OpenAI finally released the non-preview version of **GPT-4 Turbo**, integrating GPT-4 Vision directly into the model (previously it was separate). Vision mode now supports both functions and JSON output, previously unavailable for image inputs. OpenAI also claim that the new model is [“Majorly improved”](https://twitter.com/OpenAI/status/1777772582680301665) but no-one knows what they mean by that.
* 6:20pm (3:20am in their home country of France): Mistral [tweet a link](https://twitter.com/MistralAI/status/1777869263778291896) to a 281GB magnet BitTorrent of **Mixtral 8x22B**—their latest openly licensed model release, significantly larger than their previous best open model Mixtral 8x7B. I’ve not seen anyone get this running yet but it’s likely to perform extremely well, given how good the original Mixtral was.

And while it wasn’t released today (it came out [last week](https://txt.cohere.com/command-r-plus-microsoft-azure/)), this morning Cohere’s Command R+ (an excellent openly licensed model) [reached position 6 on the LMSYS Chatbot Arena Leaderboard](https://fedi.simonwillison.net/@simon/112242034813525962)—the highest ever ranking for an open weights model.

Since I have a lot of software that builds on these models, I spent a bunch of time today publishing new releases of things.

#### Datasette Extract with GPT-4 Turbo Vision

I’ve been working on [Datasette Extract](https://datasette.io/plugins/datasette-extract) for a while now: it’s a plugin for Datasette that adds structured data extraction from unstructured text, powered by GPT-4 Turbo.

I updated it for the new model releases [this morning](https://github.com/datasette/datasette-extract/releases/tag/0.1a4), and decided to celebrate by making [a video](https://www.youtube.com/watch?v=g3NtJatmQR0) showing what it can do:

 

I want to start publishing videos like this more often, so this felt like a great opportunity to put that into practice.

The Datasette Cloud blog hasn’t had an entry in a while, so I [published screenshots and notes there](https://www.datasette.cloud/blog/2024/datasette-extract/) to accompany the video.

#### Gemini Pro 1.5 system prompts

I really like system prompts—extra prompts you can pass to an LLM that give it instructions about how to process the main input. They’re sadly [not a guaranteed solution for prompt injection](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/#gpt4)—even with instructions separated from data by a system prompt you can still over-ride them in the main prompt if you try hard enough—but they’re still useful for non-adversarial situations.

**[llm-gemini 0.1a2](https://github.com/simonw/llm-gemini/releases/tag/0.1a2)** adds support for them, so now you can do things like this:

```
llm -m p15 'say hi three times three different ways' \
  --system 'in spanish'
```

And get back output like this:

> ¡Hola! 👋 ¡Buenos días! ☀️ ¡Buenas tardes! 😊

Interestingly “in german” doesn’t include emoji, but “in spanish” does.

I had to reverse-engineer the REST format for sending a system prompt from the Python library as the REST documentation hasn’t been updated yet—[notes on that in my issue](https://github.com/simonw/llm-gemini/issues/6#issuecomment-2046460319).

#### datasette-enrichments-gpt using GPT-4 Turbo

Another small release: the [datasette-enrichments-gpt](https://datasette.io/plugins/datasette-enrichments-gpt) plugin can enrich data in a table by running prompts through GPT-3.5, GPT-4 Turbo or GPT-4 Vision. I released [version 0.4](https://github.com/datasette/datasette-enrichments-gpt/releases/tag/0.4) switching to the new GPT-4 Turbo model.

#### Everything else

That covers today... but my last weeknotes were nearly four weeks ago! Here’s everything else, with a few extra annotations:

#### Blog entries

All five of my most recent posts are about ways that I use LLM tools in my own work—see also my [How I use LLMs and ChatGPT](https://simonwillison.net/series/using-llms/) series.

* [Building files-to-prompt entirely using Claude 3 Opus](https://simonwillison.net/2024/Apr/8/files-to-prompt/)
* [Running OCR against PDFs and images directly in your browser](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/)
* [llm cmd undo last git commit—a new plugin for LLM](https://simonwillison.net/2024/Mar/26/llm-cmd/)
* [Building and testing C extensions for SQLite with ChatGPT Code Interpreter](https://simonwillison.net/2024/Mar/23/building-c-extensions-for-sqlite-with-chatgpt-code-interpreter/)
* [Claude and ChatGPT for ad-hoc sidequests](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/)

#### Releases

Many of these releases relate to ongoing work on [Datasette Cloud](https://www.datasette.cloud/). In particular there’s a flurry of minor releases to add descriptions to the action menu items added by various plugins, best illustrated by this screenshot:

![A screenshot showing the database actions, table actions and row actions menus in Datasette running on Datasette Cloud. The database menu items are: Upload CSV. Create a new table by uploading a CSV file. Execute SQL write. Run queries like insert/update/delete against this database. Query this database with Al assistance. Ask a question to build a SQL query. Create table with Al extracted data. Paste in text or an image to extract structured data. Edit database metadata. Set the description, source and license for this database. Create a table. Define a new table with specified columns. Create table with pasted data. Paste in JSON, CSV or TSV data (e.g. from Google Sheets). Export this database. Create and download a snapshot of this SQLite database (1.3 GB). The table menu items: Delete this table. Delete table and all rows within it. Enrich selected data. Run a data cleaning operation against every selected row. Query this table with Al assistance. Ask a question to build a SQL query. Extract data into this table with Al. Paste in text or an image to extract structured data. Edit table metadata. Set the description, source and license for this table. Edit table schema. Rename the table, add and remove columns.... Make table public. Allow anyone to view this table. Configure full-text search. Select columns to make searchable for this table. The row menu items: Enrich this row. Run a dat acleaning operation against this row.](https://static.simonwillison.net/static/2024/action-menus.png)

* **[datasette-enrichments-gpt 0.4](https://github.com/datasette/datasette-enrichments-gpt/releases/tag/0.4)**—2024-04-10  
  Datasette enrichment for analyzing row data using OpenAI’s GPT models
* **[llm-gemini 0.1a2](https://github.com/simonw/llm-gemini/releases/tag/0.1a2)**—2024-04-10  
  LLM plugin to access Google’s Gemini family of models
* **[datasette-public 0.2.3](https://github.com/simonw/datasette-public/releases/tag/0.2.3)**—2024-04-09  
  Make specific Datasette tables visible to the public
* **[datasette-enrichments 0.3.2](https://github.com/datasette/datasette-enrichments/releases/tag/0.3.2)**—2024-04-09  
  Tools for running enrichments against data stored in Datasette
* **[datasette-extract 0.1a4](https://github.com/datasette/datasette-extract/releases/tag/0.1a4)**—2024-04-09  
  Import unstructured data (text and images) into structured tables
* **[datasette-cors 1.0](https://github.com/simonw/datasette-cors/releases/tag/1.0)**—2024-04-08  
  Datasette plugin for configuring CORS headers
* **[asgi-cors 1.0](https://github.com/simonw/asgi-cors/releases/tag/1.0)**—2024-04-08  
  ASGI middleware for applying CORS headers to an ASGI application
* **[files-to-prompt 0.2.1](https://github.com/simonw/files-to-prompt/releases/tag/0.2.1)**—2024-04-08  
  Concatenate a directory full of files into a single prompt for use with LLMs
* **[datasette-embeddings 0.1a3](https://github.com/datasette/datasette-embeddings/releases/tag/0.1a3)**—2024-04-08  
  Store and query embedding vectors in Datasette tables
* **[datasette-studio 0.1a3](https://github.com/datasette/datasette-studio/releases/tag/0.1a3)**—2024-04-06  
  Datasette pre-configured with useful plugins. Experimental alpha.
* **[datasette-paste 0.1a5](https://github.com/datasette/datasette-paste/releases/tag/0.1a5)**—2024-04-06  
  Paste data to create tables in Datasette
* **[datasette-import 0.1a4](https://github.com/datasette/datasette-import/releases/tag/0.1a4)**—2024-04-06  
  Tools for importing data into Datasette
* **[datasette-enrichments-quickjs 0.1a2](https://github.com/datasette/datasette-enrichments-quickjs/releases/tag/0.1a2)**—2024-04-05  
  Enrich data with a custom JavaScript function
* **[s3-credentials 0.16.1](https://github.com/simonw/s3-credentials/releases/tag/0.16.1)**—2024-04-05  
  A tool for creating credentials for accessing S3 buckets
* **[llm-command-r 0.2](https://github.com/simonw/llm-command-r/releases/tag/0.2)**—2024-04-04  
  Access the Cohere Command R family of models
* **[llm-nomic-api-embed 0.1](https://github.com/simonw/llm-nomic-api-embed/releases/tag/0.1)**—2024-03-30  
  Create embeddings for LLM using the Nomic API
* **[textract-cli 0.1](https://github.com/simonw/textract-cli/releases/tag/0.1)**—2024-03-29  
  CLI for running files through AWS Textract
* **[llm-cmd 0.1a0](https://github.com/simonw/llm-cmd/releases/tag/0.1a0)**—2024-03-26  
  Use LLM to generate and execute commands in your shell
* **[datasette-write 0.3.2](https://github.com/simonw/datasette-write/releases/tag/0.3.2)**—2024-03-18  
  Datasette plugin providing a UI for executing SQL writes against the database

#### TILs

* [impaste: pasting images to piped commands on macOS](https://til.simonwillison.net/macos/impaste)—2024-04-04
* [Installing tools written in Go](https://til.simonwillison.net/go/installing-tools)—2024-03-26
* [Google Chrome --headless mode](https://til.simonwillison.net/chrome/headless)—2024-03-24
* [Reviewing your history of public GitHub repositories using ClickHouse](https://til.simonwillison.net/clickhouse/github-public-history)—2024-03-20
* [Running self-hosted QuickJS in a browser](https://til.simonwillison.net/npm/self-hosted-quickjs)—2024-03-20
* [Programmatically comparing Python version strings](https://til.simonwillison.net/python/comparing-version-numbers)—2024-03-17
