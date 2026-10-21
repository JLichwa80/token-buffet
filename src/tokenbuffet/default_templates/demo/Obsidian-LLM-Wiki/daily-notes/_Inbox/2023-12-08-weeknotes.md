# Weeknotes: datasette-enrichments, datasette-comments, sqlite-chronicle

Source: https://simonwillison.net/2023/Dec/8/weeknotes/

## Weeknotes: datasette-enrichments, datasette-comments, sqlite-chronicle

8th December 2023

I’ve mainly been working on [Datasette Enrichments](https://enrichments.datasette.io/) and continuing to explore the possibilities enabled by [sqlite-chronicle](https://github.com/simonw/sqlite-chronicle).

#### Enrichments

This is the biggest new Datasette feature to arrive in quite a while, and it’s entirely implemented as a plugin.

I described these in detail in **[Datasette Enrichments: a new plugin framework for augmenting your data](https://simonwillison.net/2023/Dec/1/datasette-enrichments/)** (with an accompanying [YouTube video demo](https://www.youtube.com/watch?v=HqKlJCgdjfg)). The short version: you can now install plugins that can “enrich” data by running transformations (or data fetches) against selected rows—geocoding addresses, or executing a GPT prompt, or applying a regular expression.

The [datasette-enrichments](https://datasette.io/plugins/datasette-enrichments) plugin provides the mechanism for running these enrichments. Other plugins can then depend on it and define all manner of interesting options for enriching and transforming data.

I’ve built four of these so far, and I wrote some [extensive documentation](https://enrichments.datasette.io/en/stable/developing.html) to help people build more. I’m excited to see how people use and build further on this initial foundation.

#### Datasette Comments

Alex Garcia released the first version of [datasette-comments](https://datasette.io/plugins/datasette-comments) as part of our continuing collaboration to build out Datasette Cloud.

He wrote about that on the Datasette Cloud blog: **[Annotate and explore your data with datasette-comments](https://www.datasette.cloud/blog/2023/datasette-comments/)**.

![Three comment threads demonstrating features of Datasette Comments - replies, reaction emoji, hashtags and the ability to mention other users.](https://static.simonwillison.net/static/2023/datasette-comments.jpg)

This is another capability I’ve been looking forward to for years: the plugin lets you leave comments on individual rows within a Datasette instance, in order to collaborate with others on finding stories in data.

#### sqlite-chronicle and datasette-chronicle

I first wrote about [sqlite-chronicle](https://github.com/simonw/sqlite-chronicle) in [weeknotes back in September](https://simonwillison.net/2023/Sep/17/weeknotes-embeddings/#sqlite-chronicle). This week, inspired by my work on embeddings, I spent a bit more time on it and shipped [a 0.2 release](https://github.com/simonw/sqlite-chronicle/releases/tag/0.2).

`sqlite-chronicle` is a Python library that implements a SQL pattern where a table can have a `_chronicle_tablename` companion table created, which is then updated using triggers against the main table.

The chronicle table has a shadow row for every row in the main table, duplicating its primary keys and then storing millisecond timestamp columns for `added_ms` and `updated_ms`, an integer `version` column and a `deleted` boolean indicator.

The goal is to record when a row was last inserted or updated, with an atomically incrementing `version` ID representing the version of the entire table.

This can then enable all sorts of interesting potential use-cases:

* Identify which rows have been updated or inserted since a previously recorded version
* Synchronize a table with another table, only updating/inserting/deleting rows that have changed since last time
* Run scheduled tasks that only consider rows that have changed in some way

The relevance to enrichments is that I’d like to implement a form of “persistent” enrichment—an enrichment which is configured to run repeatedly against new or updated rows, geocoding new addresses for example.

To do that, I need a mechanism to identify which rows have already been enriched and which need to be enriched again. `sqlite-chronicle` is my current plan to provide that mechanism.

It’s still pretty experimental. I recently found that `INSERT OR REPLACE INTO` queries don’t behave how I would expect them to, see [issue #7](https://github.com/simonw/sqlite-chronicle/issues/7).

I also started a new plugin to accompany the feature: [datasette-chronicle](https://datasette.io/plugins/datasette-chronicle), which adds two features to Datasette:

* “enable/disable chronicle tracking” table actions for users with the correct permissions, which can be used in the Datasette UI to turn chronicle tracking on and off for a specific table
* For tables that have chronicle enabled, a `?_since=VERSION` querystring parameter which can be used to filter the table to only rows that have changed since the specified version

I’m running the plugin against the [documents](https://demos.datasette.cloud/data/documents) table on `demos.datasette.cloud`—see [\_chronicle\_documents](https://demos.datasette.cloud/data/_chronicle_documents) there for the result. That table is populated via GitHub scheduled actions and the Datasette API, as described in [Getting started with the Datasette Cloud API](https://www.datasette.cloud/blog/2023/datasette-cloud-api/)—it’s also where I first spotted the `INSERT OR REPLACE INTO` issue I described earlier.

#### Newsroom Robots

I recorded an episode of the [Newsroom Robots](https://www.newsroomrobots.com/) AI in journalism podcast with Nikita Roy a couple of weeks ago.

She split our conversation into two episodes:

* [Simon Willison (Part One): Breaking Down OpenAI’s New Features & Security Risks of Large Language Models](https://www.newsroomrobots.com/p/breaking-down-openais-new-features)—which I ended up using as the basis for two blog entries:
  + [I’m on the Newsroom Robots podcast, with thoughts on the OpenAI board](https://simonwillison.net/2023/Nov/25/newsroom-robots/)
  + [Prompt injection explained, November 2023 edition](https://simonwillison.net/2023/Nov/27/prompt-injection-explained/)
* [Simon Willison (Part Two): How Datasette Helps With Investigative Reporting](https://www.newsroomrobots.com/p/how-datasette-helps-with-investigative) which has the best audio description of Datasette I’ve managed to produce so far.

#### sqlite-utils 3.36

Quoting the [release notes](https://sqlite-utils.datasette.io/en/stable/changelog.html#v3-36).

> * Support for creating tables in [SQLite STRICT mode](https://www.sqlite.org/stricttables.html). Thanks, [Taj Khattra](https://github.com/tkhattra). ([#344](https://github.com/simonw/sqlite-utils/issues/344))
>   + CLI commands `create-table`, `insert` and `upsert` all now accept a `--strict` option.
>   + Python methods that can create a table—`table.create()` and `insert/upsert/insert_all/upsert_all` all now accept an optional `strict=True` parameter.
>   + The `transform` command and `table.transform()` method preserve strict mode when transforming a table.
> * The `sqlite-utils create-table` command now accepts `str`, `int` and `bytes` as aliases for `text`, `integer` and `blob` respectively. ([#606](https://github.com/simonw/sqlite-utils/issues/606))

Taj Khattra’s contribution of the `--strict` and `strict=True` options is a beautiful example of my ideal pull request: a clean implementation, comprehensive tests and thoughtful updates to the documentation [all bundled together in one go](https://github.com/simonw/sqlite-utils/pull/604).

#### Releases

* **[sqlite-utils 3.36](https://github.com/simonw/sqlite-utils/releases/tag/3.36)**—2023-12-08  
  Python CLI utility and library for manipulating SQLite databases
* **[datasette-leaflet-geojson 0.8.1](https://github.com/simonw/datasette-leaflet-geojson/releases/tag/0.8.1)**—2023-12-07  
  Datasette plugin that replaces any GeoJSON column values with a Leaflet map.
* **[datasette-chronicle 0.2](https://github.com/datasette/datasette-chronicle/releases/tag/0.2)**—2023-12-06  
  Enable sqlite-chronicle against tables in Datasette
* **[datasette-enrichments-jinja 0.1](https://github.com/datasette/datasette-enrichments-jinja/releases/tag/0.1)**—2023-12-06  
  Datasette enrichment for evaluating templates in a Jinja sandbox
* **[sqlite-chronicle 0.2.1](https://github.com/simonw/sqlite-chronicle/releases/tag/0.2.1)**—2023-12-06  
  Use triggers to track when rows in a SQLite table were updated or deleted
* **[datasette-enrichments-gpt 0.3](https://github.com/datasette/datasette-enrichments-gpt/releases/tag/0.3)**—2023-12-01  
  Datasette enrichment for analyzing row data using OpenAI’s GPT models
* **[datasette-statistics 0.2.1](https://github.com/simonw/datasette-statistics/releases/tag/0.2.1)**—2023-11-30  
  SQL statistics functions for Datasette
* **[datasette-enrichments-opencage 0.1](https://github.com/datasette/datasette-enrichments-opencage/releases/tag/0.1)**—2023-11-30  
  Geocoding and reverse geocoding using OpenCage
* **[datasette-enrichments-re2 0.1](https://github.com/datasette/datasette-enrichments-re2/releases/tag/0.1)**—2023-11-30  
  Enrich data using regular expressions powered by re2
* **[datasette-enrichments 0.2](https://github.com/datasette/datasette-enrichments/releases/tag/0.2)**—2023-11-29  
  Tools for running enrichments against data stored in Datasette
* **[datasette-pretty-json 0.3](https://github.com/simonw/datasette-pretty-json/releases/tag/0.3)**—2023-11-28  
  Datasette plugin that pretty-prints any column values that are valid JSON objects or arrays

#### TILs

* [Grabbing a transcript of a short snippet of a YouTube video with MacWhisper](https://til.simonwillison.net/macos/quick-whisper-youtube)—2023-12-01
* [Cryptography in Pyodide](https://til.simonwillison.net/pyodide/cryptography-in-pyodide)—2023-11-26
* [Running pip install ’.[docs]’ on ReadTheDocs](https://til.simonwillison.net/readthedocs/pip-install-docs)—2023-11-24
