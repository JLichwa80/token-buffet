# Weeknotes: Embeddings, more embeddings and Datasette Cloud

Source: https://simonwillison.net/2023/Sep/17/weeknotes-embeddings/

## Weeknotes: Embeddings, more embeddings and Datasette Cloud

17th September 2023

Since my [last weeknotes](https://simonwillison.net/2023/Aug/30/datasette-plus-weeknotes/), a flurry of activity. LLM has embeddings support now, and Datasette Cloud has driven some major improvements to the wider Datasette ecosystem.

#### Embeddings in LLM

LLM gained embedding support in version 0.9, and then got binary embedding support (for CLIP) in version 0.10. I wrote about those releases in detail in:

* [LLM now provides tools for working with embeddings](https://simonwillison.net/2023/Sep/4/llm-embeddings/)
* [Build an image search engine with llm-clip, chat with models with llm chat](https://simonwillison.net/2023/Sep/12/llm-clip-and-chat/)

Embeddings are a fascinating tool. If you haven’t got your head around them yet the [first of my blog entries](https://simonwillison.net/2023/Sep/4/llm-embeddings/) tries to explain why they are so interesting.

There’s a lot more I want to built on top of embeddings—most notably, LLM (or Datasette, or likely a combination of the two) will be growing support for Retrieval Augmented Generation on top of the LLM embedding mechanism.

#### Annotated releases

I always include a list of new releases in my weeknotes. This time I’m going to use those to illustrate the themes I’ve been working on.

The first group of release relates to LLM and its embedding support. LLM 0.10 extended that support:

* **[llm 0.10](https://github.com/simonw/llm/releases/tag/0.10)**—2023-09-12  
  Access large language models from the command-line

Embedding models can now be [built as LLM plugins](https://llm.datasette.io/en/stable/embeddings/writing-plugins.html). I’ve released two of those so far:

* **[llm-sentence-transformers 0.1.2](https://github.com/simonw/llm-sentence-transformers/releases/tag/0.1.2)**—2023-09-13  
  LLM plugin for embeddings using sentence-transformers
* **[llm-clip 0.1](https://github.com/simonw/llm-clip/releases/tag/0.1)**—2023-09-12  
  Generate embeddings for images and text using CLIP with LLM

The CLIP one is particularly fun, because it genuinely allows you to build a sophisticated image search engine that runs entirely on your own computer!

* **[symbex 1.4](https://github.com/simonw/symbex/releases/tag/1.4)**—2023-09-05  
  Find the Python code for specified symbols

Symbex is my tool for extracting symbols—functions, methods and classes—from Python code. I introduced that in [Symbex: search Python code for functions and classes, then pipe them into a LLM](https://simonwillison.net/2023/Jun/18/symbex/).

Symbex 1.4 adds a tiny but impactful feature: it can now output a list of symbols as JSON, CSV or TSV. These output formats are designed to be compatible with the new [llm embed-multi](https://llm.datasette.io/en/stable/embeddings/cli.html#embedding-data-from-a-csv-tsv-or-json-file) command, which means you can easily create embeddings for all of your functions:

```
symbex '*' '*:*' --nl | \
  llm embed-multi symbols - \
  --format nl --database embeddings.db --store
```

I haven’t fully explored what this enables yet, but it should mean that both related functions and semantic function search (“Find my a function that downloads a CSV”) are now easy to build.

* **[llm-cluster 0.2](https://github.com/simonw/llm-cluster/releases/tag/0.2)**—2023-09-04  
  LLM plugin for clustering embeddings

Yet another thing you can do with embeddings is use them to find clusters of related items.

The neatest feature of `llm-cluster` is that you can ask it to generate names for these clusters by sending the names of the items in each cluster through another language model, something like this:

```
llm cluster issues 10 \
  -d issues.db \
  --summary \
  --prompt 'Short, concise title for this cluster of related documents'
```

One last embedding related project: `datasette-llm-embed` is a tiny plugin that adds a `select llm_embed('sentence-transformers/all-mpnet-base-v2', 'This is some text')` SQL function. I built it to support quickly prototyping embedding-related ideas in Datasette.

* **[datasette-llm-embed 0.1a0](https://github.com/simonw/datasette-llm-embed/releases/tag/0.1a0)**—2023-09-08  
  Datasette plugin adding a llm\_embed(model\_id, text) SQL function

Spending time with embedding models has lead me to spend more time with Hugging Face. I realized last week that the Hugging Face [all models sorted by downloads](https://huggingface.co/models?sort=downloads) page doubles as a list of the models that are most likely to be easy to use.

One of the models I tried out was [Salesforce BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base), an astonishing model that can genuinely produce usable captions for images.

It’s really easy to work with. I ended up building this tiny little CLI tool that wraps the model:

* **[blip-caption 0.1](https://github.com/simonw/blip-caption/releases/tag/0.1)**—2023-09-10  
  Generate captions for images with Salesforce BLIP

#### Releases driven by Datasette Cloud

[Datasette Cloud](https://www.datasette.cloud/) continues to drive improvements to the wider Datasette ecosystem as a whole.

It runs on the latest Datasette 1.0 alpha series, taking advantage of [the JSON write API](https://simonwillison.net/2022/Dec/2/datasette-write-api/).

This also means that it’s been highlighting breaking changes in 1.0 that have caused old plugins to break, either subtly or completely.

This has driven a bunch of new plugin releases. Some of these are compatible with both 0.x and 1.x—the ones that only work with the 1.x alphas are themselves marked as alpha releases.

* **[datasette-export-notebook 1.0.1](https://github.com/simonw/datasette-export-notebook/releases/tag/1.0.1)**—2023-09-15  
  Datasette plugin providing instructions for exporting data to Jupyter or Observable
* **[datasette-cluster-map 0.18a0](https://github.com/simonw/datasette-cluster-map/releases/tag/0.18a0)**—2023-09-11  
  Datasette plugin that shows a map for any data with latitude/longitude columns
* **[datasette-graphql 3.0a0](https://github.com/simonw/datasette-graphql/releases/tag/3.0a0)**—2023-09-07  
  Datasette plugin providing an automatic GraphQL API for your SQLite databases

Datasette Cloud’s API works using database-backed access tokens, to ensure users can revoke tokens if they need to (something that’s not easily done with purely signed tokens) and that each token can record when it was most recently used.

I’ve been building that into the existing `datasette-auth-tokens` plugin:

* **[datasette-auth-tokens 0.4a3](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a3)**—2023-08-31  
  Datasette plugin for authenticating access using API tokens

[Alex Garcia](https://alexgarcia.xyz/) has been working with me building out features for Datasette Cloud, generously sponsored by [Fly.io](https://fly.io/).

We’re beginning to build out social features for Datasette Cloud—feature that will help teams privately collaborate on data investigations together.

Alex has been building [datasette-short-links](https://github.com/datasette/datasette-short-links) as an experimental link shortener. In building that, we realized that we needed a mechanism for resolving actor IDs displayed in a list (e.g. this link created by X) to their actual names.

Datasette doesn’t dictate the shape of [actor](https://docs.datasette.io/en/stable/authentication.html#actors) representations, and there’s no guarantee that actors would be represented in a predictable table.

So... we needed a new plugin hook. I released Datasette 1.06a with a new hook, [actors\_from\_ids(actor\_ids)](https://docs.datasette.io/en/1.0a6/plugin_hooks.html#actors-from-ids-datasette-actor-ids), which can be used to answer the question “who are the actors represented by these IDs”.

Alex is using this in `datasette-short-links`, and I built two plugins to work with the new hook as well:

* **[datasette 1.0a6](https://github.com/simonw/datasette/releases/tag/1.0a6)**—2023-09-08  
  An open source multi-tool for exploring and publishing data
* **[datasette-debug-actors-from-ids 0.1a1](https://github.com/datasette/datasette-debug-actors-from-ids/releases/tag/0.1a1)**—2023-09-08  
  Datasette plugin for trying out the actors\_from\_ids hook
* **[datasette-remote-actors 0.1a1](https://github.com/datasette/datasette-remote-actors/releases/tag/0.1a1)**—2023-09-08  
  Datasette plugin for fetching details of actors from a remote endpoint

Datasette Cloud lets users insert, edit and delete rows from their tables, using the plugin Alex built called [datasette-write-ui](https://github.com/datasette/datasette-write-ui) which he [introduced on the Datasette Cloud blog](https://www.datasette.cloud/blog/2023/datasette-write-ui/).

This inspired me to finally put out a fresh release of [datasette-edit-schema](https://github.com/simonw/datasette-edit-schema)—the plugin which provides the ability to edit table schemas—adding and removing columns, changing column types, even altering the order columns are stored in the table.

[datasette-edit-schema 0.6](https://github.com/simonw/datasette-edit-schema/releases/tag/0.6) is a major release, with three significant new features:

* You can now create a brand new table from scratch!
* You can edit the table’s primary key
* You can modify the foreign key constraints on the table

Those last two became important when I realized that Datasette’s API is much more interesting if there are foreign key relationships to follow.

Combine that with `datasette-write-ui` and Datasette Cloud now has a full set of features for building, populating and editing tables—backed by a comprehensive JSON API.

* **[sqlite-migrate 0.1a2](https://github.com/simonw/sqlite-migrate/releases/tag/0.1a2)**—2023-09-03  
  A simple database migration system for SQLite, based on sqlite-utils

[sqlite-migrate](https://github.com/simonw/sqlite-migrate) is still marked as an alpha, but won’t be for much longer: it’s my attempt at a migration system for SQLite, inspired by [Django migrations](https://docs.djangoproject.com/en/4.2/topics/migrations/) but with a less sophisticated set of features.

I’m using it in LLM now to manage the schema used to store embeddings, and it’s beginning to show up in some Datasette plugins as well. I’ll be promoting this to non-alpha status pretty soon.

* **[sqlite-utils 3.35.1](https://github.com/simonw/sqlite-utils/releases/tag/3.35.1)**—2023-09-09  
  Python CLI utility and library for manipulating SQLite databases

A tiny fix in this, which with hindsight was less impactful than I thought.

I spotted a bug on Datasette Cloud when I configured full-text search on a column, then edited the schema and found that searches no longer returned the correct results.

It turned out the `rowid` column in SQLite was being rewritten by calls to the `sqlite-utils` [table.transform()](https://sqlite-utils.datasette.io/en/stable/python-api.html#transforming-a-table) method. FTS records are related to their underlying row by `rowid`, so this was breaking search!

I pushed out [a fix for this](https://github.com/simonw/sqlite-utils/issues/592) in 3.35.1. But then... I learned that `rowid` in SQLite has always been unstable—they are rewritten any time someone VACUUMs a table!

I’ve been designing future features for Datasette that assume that `rowid` is a useful stable identifier for a row. This clearly isn’t going to work! I’m still thinking through the consequences of it, but I think there may be Datasette features (like the ability to comment on a row) that will only work for tables with a proper foreign key.

#### sqlite-chronicle

* **[sqlite-chronicle 0.1](https://github.com/simonw/sqlite-chronicle/releases/tag/0.1)**—2023-09-11  
  Use triggers to track when rows in a SQLite table were updated or deleted

This is very early, but I’m excited about the direction it’s going in.

I keep on finding problems where I want to be able to synchronize various processes with the data in a table.

I built [sqlite-history](https://simonwillison.net/2023/Apr/15/sqlite-history/) a few months ago, which uses SQLite triggers to create a full copy of the updated data every time a row in a table is edited.

That’s a pretty heavy-weight solution. What if there was something lighter that could achieve a lot of the same goals?

`sqlite-chronicle` uses triggers to instead create what I’m calling a “chronicle table”. This is a shadow table that records, for every row in the main table, four integer values:

* `added_ms`—the timestamp in milliseconds when the row was added
* `updated_ms`—the timestamp in milliseconds when the row was last updated
* `version`—a constantly incrementing version number, global across the entire table
* `deleted`—set to `1` if the row has been deleted

Just storing four integers (plus copies of the primary key) makes this a pretty tiny table, and hopefully one that’s cheap to update via triggers.

But... having this table enables some pretty interesting things—because external processes can track the last version number that they saw and use it to see just which rows have been inserted and updated since that point.

I gave a talk at DjangoCon a few years ago called [the denormalized query engine pattern](https://2017.djangocon.us/talks/the-denormalized-query-engine-design-pattern/), describing the challenge of syncing an external search index like Elasticsearch with data held in a relational database.

These chronicle tables can solve that problem, and can be applied to a whole host of other problems too. So far I’m thinking about the following:

* Publishing SQLite databases up to Datasette, sending only the rows that have changed since the last sync. I [wrote a prototype that does this](https://github.com/simonw/sqlite-chronicle/issues/2#issuecomment-1721557623) and it seems to work very well.
* Copying a table from Datasette Cloud to other places—a desktop copy, or another instance, or even into an alternative database such as PostgreSQL or MySQL, in a way that only copies and deletes rows that have changed.
* Saved search alerts: run a SQL query against just rows that were modified since the last time that query ran, then send alerts if any rows are matched.
* Showing users a note that “34 rows in this table have changed since your last visit”, then displaying those rows.

I’m sure there are many more applications for this. I’m looking forward to finding out what they are!

* **[sqlite-utils-move-tables 0.1](https://github.com/simonw/sqlite-utils-move-tables/releases/tag/0.1)**—2023-09-01  
  sqlite-utils plugin adding a move-tables command

I needed to fix a bug in Datasette Cloud by moving a table from one database to another... so I built a little plugin for `sqlite-utils` that adds a `sqlite-utils move-tables origin.db destination.db tablename` command. I love being able to build single-use features [as plugins like this](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/).

#### And some TILs

* [Embedding paragraphs from my blog with E5-large-v2](https://til.simonwillison.net/llms/embed-paragraphs)—2023-09-08

This was a fun TIL exercising the new embeddings feature in LLM. I used [Django SQL Dashboard](https://django-sql-dashboard.datasette.io/)to break up my blog entries into paragraphs and exported those as CSV which could then be piped into `llm embed-multi`, then used that to build a CLI-driven semantic search engine for my blog.

* [Using llama-cpp-python grammars to generate JSON](https://til.simonwillison.net/llms/llama-cpp-python-grammars)—2023-09-13

`llama-cpp` has grammars now, which enable you to control the exact output format of the LLM. I’m optimistic that these could be used to implement an equivalent to [OpenAI Functions](https://openai.com/blog/function-calling-and-other-api-updates) on top of Llama 2 and similar models. So far I’ve just got them to output arrays of JSON objects.

* [Summarizing Hacker News discussion themes with Claude and LLM](https://til.simonwillison.net/llms/claude-hacker-news-themes)—2023-09-09

I’m using this trick a lot at the moment. I have API access to [Claude](https://claude.ai/) now, which has a 100,000 token context limit (GPT-4 is just 8,000 by default). That’s enough to summarize 100+ comment threads from Hacker News, for which I’m now using this prompt:

> Summarize the themes of the opinions expressed here, including quotes (with author attribution) where appropriate.

The quotes part has been working really well—it turns out summaries of themes with illustrative quotes are much more interesting, and so far my spot checks haven’t found any that were hallucinated.

* [Trying out cr-sqlite on macOS](https://til.simonwillison.net/sqlite/cr-sqlite-macos)—2023-09-13

[cr-sqlite](https://github.com/vlcn-io/cr-sqlite) adds full CRDTs to SQLite, which should enable multiple databases to accept writes independently and then seamlessly merge them together. It’s a very exciting capability!

* [Running Datasette on Hugging Face Spaces](https://til.simonwillison.net/datasette/hugging-face-spaces)—2023-09-08

It turns out Hugging Faces offer free scale-to-zero hosting for demos that run in Docker containers on machines with a full 16GB of RAM! I’m used to optimizing Datasette for tiny 256MB containers, so having this much memory available is a real treat.

And the rest:

* [Limited JSON API for Google searches using Programmable Search Engine](https://til.simonwillison.net/google/json-api-programmable-search-engine)—2023-09-17
* [Running tests against multiple versions of a Python dependency in GitHub Actions](https://til.simonwillison.net/github-actions/running-tests-against-multiple-verisons-of-dependencies)—2023-09-15
* [Remember to commit when using datasette.execute\_write\_fn()](https://til.simonwillison.net/datasette/remember-to-commit)—2023-08-31
