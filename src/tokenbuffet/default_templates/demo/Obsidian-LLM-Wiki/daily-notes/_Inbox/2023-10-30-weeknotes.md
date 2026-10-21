# DALL-E 3, GPT4All, PMTiles, sqlite-migrate, datasette-edit-schema

Source: https://simonwillison.net/2023/Oct/30/weeknotes/

## DALL-E 3, GPT4All, PMTiles, sqlite-migrate, datasette-edit-schema

30th October 2023

I wrote a lot this week. I also did some fun research into new options for self-hosting vector maps and pushed out several new releases of plugins.

#### On the blog

* [Now add a walrus: Prompt engineering in DALL-E 3](https://simonwillison.net/2023/Oct/26/add-a-walrus/) talked about my explorations of the new DALL-E 3 image generation model, including some reverse engineering showing how OpenAI prompt engineered ChatGPT to pass generate its own prompts for DALL-E 3. And a lot of pictures of pelicans. I also wrote a TIL about [the CSS grids I used in that post](https://til.simonwillison.net/css/simple-two-column-grid).
* In [Execute Jina embeddings with a CLI using llm-embed-jina](https://simonwillison.net/2023/Oct/26/llm-embed-jina/) I released [a new plugin](https://github.com/simonw/llm-embed-jina) to run the new Jina AI 8K text embedding model using my [LLM](https://llm.datasette.io/) command-line tool.
* [Embeddings: What they are and why they matter](https://simonwillison.net/2023/Oct/23/embeddings/) is the big write-up of my talk about embeddings from PyBay this year. This has received a lot of traffic, presumably because it provides one of the more accessible answers to the question “what are embeddings?”.

#### PMTiles and MapLibre GL

I saw a post about [Protomaps](https://protomaps.com/) on [Hacker News](https://news.ycombinator.com/item?id=37982621). It’s absolutely fantastic technology.

The Protomaps [PMTiles](https://docs.protomaps.com/pmtiles/) file format lets you bundle together vector tiles in a single file which is designed to be queried using HTTP range header requests.

This means you can drop [a single 107GB file](https://maps.protomaps.com/builds/) on cloud hosting and use it to efficiently serve vector maps to clients, fetching just the data they need for the current map area.

Even better than that, you can create [your own subset](https://docs.protomaps.com/guide/getting-started#_3-extract-any-area) of the larger map covering just the area you care about.

I tried this out against my hometown of Half Moon Bay ond get a building-outline-level vector map for the whole town in just a 2MB file!

You can see the result (which also includes business listing markers [from Overture maps](https://til.simonwillison.net/overture-maps/overture-maps-parquet#user-content-exporting-the-places-to-sqlite)) at **[simonw.github.io/hmb-map](https://simonw.github.io/hmb-map/)**.

![A vector map of El Granada showing the area around the harbor, with lots of little markers for different businesses. Protomaps (c) OpenStreetMap in the corner.](https://static.simonwillison.net/static/2023/protomaps.jpg)

Lots more details of how I built this, including using Vite as a build tool and the [MapLibre GL](https://maplibre.org/) JavaScript library to serve the map, in my TIL [Serving a custom vector web map using PMTiles and maplibre-gl](https://til.simonwillison.net/gis/pmtiles).

I’m so excited about this: we now have the ability to entirely self-host vector maps of any location in the world, using openly licensed data, without depending on anything other than our own static file hosting web server.

#### llm-gpt4all

This was a tiny release—literally a [one line code change](https://github.com/simonw/llm-gpt4all/commit/377ebf5c911e1a6bb8039a23c3ca37bcf83a1b79#diff-945dfb6aca00ffce39b7f0152bb540fce2d1ed1bb569a7a2688f2f9fb0aeb0d2)—with a huge potential impact.

Nomic AI’s [GPT4All](https://gpt4all.io/) is a really cool project. They describe their focus as “a free-to-use, locally running, privacy-aware chatbot. No GPU or internet required.”—they’ve taken [llama.cpp](https://github.com/ggerganov/llama.cpp) (and other libraries) and wrapped them in a much nicer experience, complete with Windows, macOS and Ubuntu installers.

Under the hood it’s mostly Python, and Nomic have done a fantastic job releasing that Python core as an [installable Python package](https://docs.gpt4all.io/gpt4all_python.html)—meaning you can literally `pip install gpt4all` to get almost everything you need to run a local language model!

Unlike alternative Python libraries [MLC](https://llm.mlc.ai/docs/install/mlc_llm.html) and [llama-cpp-python](https://pypi.org/project/llama-cpp-python/), Nomic have done the work to publish compiled binary wheels to PyPI... which means `pip install gpt4all` works without needing a compiler toolchain or any extra steps!

My [LLM](https://llm.datasette.io/) tool has had a [llm-gpt4all](https://github.com/simonw/llm-gpt4all) plugin since I first added alternative model backends via plugins [in July](https://simonwillison.net/2023/Jul/12/llm/). Unfortunately, it spat out weird debugging information that I had been unable to hide (a problem that [still affects llm-llama-cpp](https://github.com/simonw/llm-llama-cpp/issues/22)).

Nomic have [fixed this](https://github.com/nomic-ai/gpt4all/issues/1159)!

As a result, `llm-gpt4all` is now my recommended plugin for getting started running local LLMs:

```
pipx install llm
llm install llm-gpt4all
llm -m mistral-7b-instruct-v0 "ten facts about pelicans"
```

The latest plugin can also now use the GPU on macOS, a key feature of Nomic’s [big release in September](https://blog.nomic.ai/posts/gpt4all-gpu-inference-with-vulkan).

#### sqlite-migrate

[sqlite-migrate](https://github.com/simonw/sqlite-migrate) is my plugin that adds a simple migration system to [sqlite-utils](https://sqlite-utils.datasette.io/), for applying changes to a database schema in a controlled, repeatable way.

Alex Garcia spotted [a bug](https://github.com/simonw/sqlite-migrate/issues/11) in the way it handled multiple migration sets with overlapping migration names, which is now fixed in [sqlite-migrate 0.1b0](https://github.com/simonw/sqlite-migrate/releases/tag/0.1b0).

Ironically the fix involved changing the schema of the `_sqlite_migrations` table used to track which migrations have been applied... which is the one part of the system that isn’t itself managed by its own migration system! I had to implement [a conditional check](https://github.com/simonw/sqlite-migrate/blob/613ecd5c4aa8493525879d2db7363fa5bfbe4ffb/sqlite_migrate/__init__.py#L103-L105) instead that checks if the table needs to be updated.

A [recent thread about SQLite](https://news.ycombinator.com/item?id=38036921) on Hacker News included a surprising number of complaints about the difficulty of running migrations, due to the lack of features of the core `ALTER TABLE` implementation.

The combination `sqlite-migrate` and the [table.transform() method](https://sqlite-utils.datasette.io/en/stable/python-api.html#python-api-transform) in `sqlite-utils` offers a pretty robust solution to this problem. Clearly I need to put more work into promoting it!

#### Homebrew trouble for LLM

I started getting confusing bug reports for my various LLM projects, all of which boiled down to a failure to install plugins that depended on PyTorch.

It turns out the LLM package for Homebrew [upgraded to Python 3.12](https://github.com/Homebrew/homebrew-core/pull/151467) last week... but PyTorch [isn’t yet available for Python 3.12](https://github.com/pytorch/pytorch/issues/110436).

This means that while base LLM installed from Homebrew works fine, attempts to install things like my new [llm-embed-jina](https://github.com/simonw/llm-embed-jina) plugin fail with [weird errors](https://github.com/simonw/llm-embed-jina/issues/5).

I’m not sure the best way to address this. For the moment I’ve removed the recommendation to install using Homebrew and replaced it with [pipx](https://pypa.github.io/pipx/) in a few places. I have [an open issue](https://github.com/simonw/llm/issues/315) to find a better solution for this.

The difficulty of debugging this issue prompted me to ship a new plugin that I’ve been contemplating for a while: [llm-python](https://github.com/simonw/llm-python).

Installing this plugin adds a new `llm python` command, which runs a Python interpreter in same virtual environment as LLM—useful for if you installed LLM via `pipx` or Homebrew and don’t know where that virtual environment is located.

It’s great for debugging: I can ask people to run `llm python -c 'import sys; print(sys.path)'` for example to figure out what their Python path looks like.

It’s also promising as a tool for future tutorials about the [LLM Python library](https://llm.datasette.io/en/stable/python-api.html). I can tell people to `pipx install llm` and then run `llm python` to get a Python interpreter with the library already installed, without them having to mess around with virtual environments directly.

#### Add and remove indexes in datasette-edit-schema

We’re iterating on Datasette Cloud based on feedback from people using the preview. One request was the ability to add and remove indexes from larger tables, to help speed up faceting.

[datasette-edit-schema 0.7](https://github.com/simonw/datasette-edit-schema/releases/tag/0.7) adds that feature.

That plugin [includes this script](https://github.com/simonw/datasette-edit-schema/blob/main/update-screenshot.sh) for automatically updating the screenshot in the README using [shot-scraper](https://shot-scraper.datasette.io/). Here’s the latest result:

![Screenshot of the edit schema UI - you can rename a table, change existing columns, add a column, update foreign key relationships, change the primary key, delete the table and now edit the table indexes.](https://static.simonwillison.net/static/2023/datasette-edit-schema.png)

#### Releases this week

* **[sqlite-migrate 0.1b0](https://github.com/simonw/sqlite-migrate/releases/tag/0.1b0)**—2023-10-27  
  A simple database migration system for SQLite, based on sqlite-utils
* **[llm-python 0.1](https://github.com/simonw/llm-python/releases/tag/0.1)**—2023-10-27  
  “llm python” is a command to run a Python interpreter in the LLM virtual environment
* **[llm-embed-jina 0.1.2](https://github.com/simonw/llm-embed-jina/releases/tag/0.1.2)**—2023-10-26  
  Embedding models from Jina AI
* **[datasette-edit-schema 0.7](https://github.com/simonw/datasette-edit-schema/releases/tag/0.7)**—2023-10-26  
  Datasette plugin for modifying table schemas
* **[datasette-ripgrep 0.8.2](https://github.com/simonw/datasette-ripgrep/releases/tag/0.8.2)**—2023-10-25  
  Web interface for searching your code using ripgrep, built as a Datasette plugin
* **[llm-gpt4all 0.2](https://github.com/simonw/llm-gpt4all/releases/tag/0.2)**—2023-10-24  
  Plugin for LLM adding support for the GPT4All collection of models

#### TIL this week

* [A simple two column CSS grid](https://til.simonwillison.net/css/simple-two-column-grid)—2023-10-27
* [Serving a custom vector web map using PMTiles and maplibre-gl](https://til.simonwillison.net/gis/pmtiles)—2023-10-24
* [Serving a JavaScript project built using Vite from GitHub Pages](https://til.simonwillison.net/github-actions/vite-github-pages)—2023-10-24
