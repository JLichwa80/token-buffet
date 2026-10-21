# Weeknotes: Three podcasts, two trips and a new plugin system

Source: https://simonwillison.net/2024/Sep/30/weeknotes/

## Weeknotes: Three podcasts, two trips and a new plugin system

30th September 2024

I fell behind a bit on my weeknotes. Here’s most of what I’ve been doing in September.

#### Lisbon, Portugal and Durham, North Carolina

I had two trips this month. The first was a short visit to Lisbon, Portugal for the Python Software Foundation’s annual board retreat. This inspired me to write about [Things I’ve learned serving on the board of the Python Software Foundation](https://simonwillison.net/2024/Sep/18/board-of-the-python-software-foundation/).

The second was to Durham, North Carolina for DjangoCon US 2024. I wrote about that one in [Themes from DjangoCon US 2024](https://simonwillison.net/2024/Sep/27/themes-from-djangocon-us-2024/).

My talk at DjangoCon was about plugin systems, and in a classic example of conference-driven development I ended up writing and releasing a new plugin system for Django in preparation for that talk. I introduced that in [DJP: A plugin system for Django](https://simonwillison.net/2024/Sep/25/djp-a-plugin-system-for-django/).

#### Podcasts

I haven’t been a podcast guest [since January](https://simonwillison.net/search/?year=2024&month=1&tag=podcasts), and then three came along at once! All three appearences involved LLMs in some way but I don’t think there was a huge amount of overlap in terms of what I actually said.

* I went on [The Software Misadventures Podcast](https://simonwillison.net/2024/Sep/10/software-misadventures/) to talk about my career to-date.
* My appearance [on TWIML](https://simonwillison.net/2024/Sep/20/using-llms-for-code/) dug into ways in which I use Claude and ChatGPT to help me write code.
* I was the guest for the inaugral episode of Gergely Orosz’s [Pragmatic Engineer Podcast](https://newsletter.pragmaticengineer.com/p/ai-tools-for-software-engineers-simon-willison), which ended up touching on a whole array of different topics relevant to modern software engineering, from the importance of open source to the impact AI tools are likely to have on our industry.

Gergely has been sharing neat edited snippets from our conversation on Twitter. Here’s [one on RAG](https://twitter.com/GergelyOrosz/status/1839682428471779596) and another about [how open source has been the the biggest productivity boost](https://twitter.com/GergelyOrosz/status/1840779737297260646) of my career.

#### On the blog

* [NotebookLM’s automatically generated podcasts are surprisingly effective](https://simonwillison.net/2024/Sep/29/notebooklm-audio-overview/)—Sept. 29, 2024
* [Themes from DjangoCon US 2024](https://simonwillison.net/2024/Sep/27/themes-from-djangocon-us-2024/)—Sept. 27, 2024
* [DJP: A plugin system for Django](https://simonwillison.net/2024/Sep/25/djp-a-plugin-system-for-django/)—Sept. 25, 2024
* [Notes on using LLMs for code](https://simonwillison.net/2024/Sep/20/using-llms-for-code/)—Sept. 20, 2024
* [Things I’ve learned serving on the board of the Python Software Foundation](https://simonwillison.net/2024/Sep/18/board-of-the-python-software-foundation/)—Sept. 18, 2024
* [Notes on OpenAI’s new o1 chain-of-thought models](https://simonwillison.net/2024/Sep/12/openai-o1/)—Sept. 12, 2024
* [Notes from my appearance on the Software Misadventures Podcast](https://simonwillison.net/2024/Sep/10/software-misadventures/)—Sept. 10, 2024
* [Teresa T is name of the whale in Pillar Point Harbor near Half Moon Bay](https://simonwillison.net/2024/Sep/8/teresa-t-whale-pillar-point/)—Sept. 8, 2024

#### Museums

* [The Vincent and Ethel Simonetti Historic Tuba Collection](https://www.niche-museums.com/112)

#### Releases

* **[shot-scraper 1.5](https://github.com/simonw/shot-scraper/releases/tag/1.5)**—2024-09-27  
  A command-line utility for taking automated screenshots of websites
* **[django-plugin-datasette 0.2](https://github.com/simonw/django-plugin-datasette/releases/tag/0.2)**—2024-09-26  
  Django plugin to run Datasette inside of Django
* **[djp 0.3.1](https://github.com/simonw/djp/releases/tag/0.3.1)**—2024-09-26  
  A plugin system for Django
* **[llm-gemini 0.1a5](https://github.com/simonw/llm-gemini/releases/tag/0.1a5)**—2024-09-24  
  LLM plugin to access Google’s Gemini family of models
* **[django-plugin-blog 0.1.1](https://github.com/simonw/django-plugin-blog/releases/tag/0.1.1)**—2024-09-24  
  A blog for Django as a DJP plugin.
* **[django-plugin-database-url 0.1](https://github.com/simonw/django-plugin-database-url/releases/tag/0.1)**—2024-09-24  
  Django plugin for reading the DATABASE\_URL environment variable
* **[django-plugin-django-header 0.1.1](https://github.com/simonw/django-plugin-django-header/releases/tag/0.1.1)**—2024-09-23  
  Add a Django-Compositions HTTP header to a Django app
* **[llm-jina-api 0.1a0](https://github.com/simonw/llm-jina-api/releases/tag/0.1a0)**—2024-09-20  
  Access Jina AI embeddings via their API
* **[llm 0.16](https://github.com/simonw/llm/releases/tag/0.16)**—2024-09-12  
  Access large language models from the command-line
* **[datasette-acl 0.4a4](https://github.com/datasette/datasette-acl/releases/tag/0.4a4)**—2024-09-10  
  Advanced permission management for Datasette
* **[llm-cmd 0.2a0](https://github.com/simonw/llm-cmd/releases/tag/0.2a0)**—2024-09-09  
  Use LLM to generate and execute commands in your shell
* **[files-to-prompt 0.3](https://github.com/simonw/files-to-prompt/releases/tag/0.3)**—2024-09-09  
  Concatenate a directory full of files into a single prompt for use with LLMs
* **[json-flatten 0.3.1](https://github.com/simonw/json-flatten/releases/tag/0.3.1)**—2024-09-07  
  Python functions for flattening a JSON object to a single dictionary of pairs, and unflattening that dictionary back to a JSON object
* **[csv-diff 1.2](https://github.com/simonw/csv-diff/releases/tag/1.2)**—2024-09-06  
  Python CLI tool and library for diffing CSV and JSON files
* **[datasette 1.0a16](https://github.com/simonw/datasette/releases/tag/1.0a16)**—2024-09-06  
  An open source multi-tool for exploring and publishing data
* **[datasette-search-all 1.1.4](https://github.com/simonw/datasette-search-all/releases/tag/1.1.4)**—2024-09-06  
  Datasette plugin for searching all searchable tables at once

#### TILs

* [How streaming LLM APIs work](https://til.simonwillison.net/llms/streaming-llm-apis)—2024-09-21
