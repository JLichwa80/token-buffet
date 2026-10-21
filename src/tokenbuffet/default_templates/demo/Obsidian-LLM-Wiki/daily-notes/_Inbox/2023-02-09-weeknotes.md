# Weeknotes: A bunch of things I learned this week, plus datasette-explain

Source: https://simonwillison.net/2023/Feb/9/weeknotes/

## Weeknotes: A bunch of things I learned this week, plus datasette-explain

9th February 2023

The Datasette table view refactor, JSON redesign and `?_extra=` continues this week, mainly in [this ongoing pull request](https://github.com/simonw/datasette/pull/1999) and [this tracking issue](https://github.com/simonw/datasette/issues/262).

I’ve also written an unusually large number of TILs, which reflect some of the other pieces of research I’ve been digging into.

I’m going to start these weeknotes with an annotated set of links to TILs.

**TIL: [Using recursive CTEs to explore hierarchical Twitter threads](https://til.simonwillison.net/sql/recursive-cte-twitter-threads)**

This TIL is actually a learned-several-years-ago: I wrote up notes on hierarchical CTEs in SQLite in [an old Gist](https://gist.github.com/simonw/656a8c6e4688f720773c474080abe1b0), long before I started my TIL website. I’ve now promoted that to a full article.

**TIL: [Calculating embeddings with gtr-t5-large in Python](https://til.simonwillison.net/python/gtr-t5-large)**

I’ve been wanting to run some form of language model on my own hardware for ages... and I finally found one that works!

[gtr-t5-large](https://huggingface.co/sentence-transformers/gtr-t5-large) isn’t a full GPT-3 style generative text language model: it’s an embeddings model, similar to the OpenAI embeddings API I [described a few weeks ago](https://simonwillison.net/2023/Jan/13/semantic-search-answers/).

Crucially though, it’s small enough to run on a MacBook M2 (and likely on less powerful machines as well, though I haven’t tried that). And the embeddings it generates seem to provide really good results for finding similar content, which is exactly what I want to use them for.

**TIL: [Running nanoGPT on a MacBook M2 to generate terrible Shakespeare](https://til.simonwillison.net/llms/nanogpt-shakespeare-m2)**

... even more exciting, I *did* manage to train and run a GPT-style generative language model! I used [nanoGPT](https://github.com/karpathy/nanoGPT) by Andrej Karpathy, which trains really nicely on an M2. I managed to get it to spit out some terrible Shakespeare, which you can see in the TIL.

Not mentioned in the TIL: I also tried training a model against the full text content of my blog. Here’s some text I managed to get it to output:

> Google is a group of software as it looks further reading as PHP’s enough for Linux, but I need it’s pretty much more for me to be served for me than Pingback. I’ll put out a background idea with a problem with a new tool (in group time accessible). I am getting a web page for that it’s great site in my HTML. I’m done using an entry interface for their mouse gestures (which is done) I have a few more of the site.

I mean, it’s total junk... but it does have a hint of my voice to it.

***Update 9th Feb 2023:** A few people asked for more details about this so I wrote them up in another TIL: [Training nanoGPT entirely on content from my blog](https://til.simonwillison.net/llms/training-nanogpt-on-my-blog)*.

This is trained from scratch, it’s not from a pre-existing language model. Training it to the point where it can output meaningful sentences would require mixing in TBs of text and training for many years. But it’s cool to have got something working!

**TIL: [Run Python code in a WebAssembly sandbox](https://til.simonwillison.net/webassembly/python-in-a-wasm-sandbox)**

This TIL represented another of my long-term goals.

The thing that excites me most about WebAssembly is sandboxing: I want to be able to run untrusted code safely my own hardware—both for personal use and for things like server-side web applications I build that might want to let users customize with their own code.

There are multiple builds of Python in WebAssembly now—I use one of them in my [Datasette Lite](https://simonwillison.net/2022/May/4/datasette-lite/) web application. But until recently I’ve been unable to figure out how to run them in a sandbox inside a regular Python script, using a WebAssembly library such as [wasmer-python](https://github.com/wasmerio/wasmer-python) or [wasmtime-py](https://github.com/bytecodealliance/wasmtime-py) or [pywasm3](https://github.com/wasm3/pywasm3) (all three of which are [frustratingly under-documented](https://fedi.simonwillison.net/@simon/109826187666456424)).

After I complained about how hard this was noisily in a few different places, Tim Bart stepped in and figured out [this example](https://gist.github.com/pims/711549577759ad1341f1a90860f1f3a5) using `wasmtime` and the new Python WASM build [released by VMware labs](https://wasmlabs.dev/articles/python-wasm32-wasi/).

It works! My TIL shows my own version inspired by that example. It’s a little inelegant—in particular, you have to redirect standard output and standard error to temporary files—but I do now at least have a way to run untrusted Python code in a sandbox, for the first time.

**TIL: [Building Mastodon bots with GitHub Actions and toot](https://til.simonwillison.net/mastodon/mastodon-bots-github-actions)**

Twitter announced they were ending all free bots. Then they un-announced that a few days later, but by then I’d already decided to move my bot to Mastodon.

<https://fedi.simonwillison.net/@covidsewage> is my Mastodon bot that posts a screenshot of the latest Covid sewage numbers for parts of the Bay Area every morning.

My TIL describes how I built it, using scheduled GitHub Actions. I was about to build a new tiny Python CLI tool for this, but in checking for available names on PyPI I found [toot](https://toot.readthedocs.io/) which is a superset of the tool I had been planning to build myself (a Mastodon version of my [tweet-images](https://github.com/simonw/tweet-images) utility.)

**TIL: [The SQLite now argument is stable within the same query](https://til.simonwillison.net/sqlite/now-argument-stability)**

Not much to say about this one: it relates to `select datetime('now')` in SQLite. There’s nothing that’s too small for the TIL format!

**TIL: [Avoiding “length” errors in Apache Bench with the -l option](https://til.simonwillison.net/ab/apache-bench-length-errors)**

Another tiny one. I write TILs like this one mainly to ensure that when I (or anyone else) searches for a confusing error message in the future there’s an obvious explanation of what it means.

**TIL: [Subqueries in select expressions in SQLite](https://til.simonwillison.net/sqlite/subqueries-in-select)**

This one is a lot more substantial: I wrote up a detailed explanation of a pattern I’ve been exploring in SQLite that lets you fetch back a row AND a limited number of related rows in a single SELECT query. If you’ve ever used Django’s [prefetch\_related](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#prefetch-related) you’ll recognise the problem.

As part of working on this I built a little Datasette plugin for running and showing `explain query plan ...` output for a query, which deserves its own mention...

#### datasette-explain

Just one new plugin this week: [datasette-explain](https://github.com/simonw/datasette-explain), which adds a feature to the Datasette SQL query editing page which constantly runs `explain query plan ...` on the query you’re typing and shows the results.

This is partly an experiment in what it feels like for Datasette to run interactive code relating to queries as you type them.

Here’s a demo as an animated GIF:

![Animated demo showing Datasette's query editing interface. As I type a select query the page updates to show warning messages ("incomplete input", "no such table rel etc") - then when the query is a valid query it shows the output of explain query plan and a list of the tables mentioned in the query so far and their columns.](https://static.simonwillison.net/static/2023/datasette-explain.gif)

The plugin works by sending the SQL query you have typed to a `/db/-/explain` endpoint in the background. This endpoint does a few things:

* It runs `explain query plan ...` on the query you have typed so far. If this returns an error message (because the query isn’t complete or includes problems) that message is displayed to the end user.
* If there’s no error, the output of that explanation is shown on the page. This gets pretty interesting as queries touch on more features, like the subquery select expression described earlier—[demo of that here](https://latest-with-plugins.datasette.io/github?sql=select%0D%0A++repos.full_name%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++max%28created_at%29%0D%0A++++from%0D%0A++++++releases%0D%0A++++where%0D%0A++++++repo+%3D+repos.id%0D%0A++%29+as+max_created_at%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++count%28*%29%0D%0A++++from%0D%0A++++++releases%0D%0A++++where%0D%0A++++++repo+%3D+repos.id%0D%0A++%29+as+releases_count%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++json_group_array%28%0D%0A++++++++json_object%28%0D%0A++++++++++%27id%27%2C%0D%0A++++++++++id%2C%0D%0A++++++++++%27name%27%2C%0D%0A++++++++++name%2C%0D%0A++++++++++%27created_at%27%2C%0D%0A++++++++++created_at%0D%0A++++++++%29%0D%0A++++++%29%0D%0A++++from%0D%0A++++++%28%0D%0A++++++++select%0D%0A++++++++++*%0D%0A++++++++from%0D%0A++++++++++releases%0D%0A++++++++where%0D%0A++++++++++repo+%3D+repos.id%0D%0A++++++++order+by%0D%0A++++++++++created_at+desc%0D%0A++++++++limit%0D%0A++++++++++3%0D%0A++++++%29%0D%0A++%29+as+recent_releases%0D%0Afrom%0D%0A++repos%0D%0Aorder+by%0D%0A++releases_count+desc%0D%0Alimit%0D%0A++10).
* It has one more trick up its sleeve: it runs a `explain select ...` query and uses the results from that to figure out which SQLite tables are referenced in the query—then fetches a full list of columns for those tables and shows them on the page as well. The intent here is to help remind you of which columns are available on the tables you are querying or joining against, as you type.

This plugin is very much an alpha: I’m not convinced it’s displaying the right data in the right way yet.

I really like the error checking mode—much more so than the explain output and table and columns. I’m tempted to bring live error checking like this to Datasette core.

It’s worth highlighting that the queries themselves are *really* fast—no matter how complex the SQL query, running `explain query plan ...` against it is very quick. That’s why I’m currently not thinking too hard about having the full results of the query show live on the page while the query is being typed.

... although, that might be worth exploring in another prototype at some point. Datasette has a good mechanism for cutting off queries that take too long to load, so I could try previewing queries but only if they can be run in less than 100ms or so.

At any rate, it’s an interesting direction to explore.

#### Releases this week

* **[datasette-explain](https://github.com/simonw/datasette-explain)**: [0.1a0](https://github.com/simonw/datasette-explain/releases/tag/0.1a0)—2023-02-09
    
  Explain and validate SQL queries as you type them into Datasette
* **[db-to-sqlite](https://github.com/simonw/db-to-sqlite)**: [1.5](https://github.com/simonw/db-to-sqlite/releases/tag/1.5)—([17 releases total](https://github.com/simonw/db-to-sqlite/releases))—2023-02-07
    
  CLI tool for exporting tables or queries from any SQL database to a SQLite file
* **[shot-scraper](https://github.com/simonw/shot-scraper)**: [1.1.1](https://github.com/simonw/shot-scraper/releases/tag/1.1.1)—([26 releases total](https://github.com/simonw/shot-scraper/releases))—2023-01-30
    
  A command-line utility for taking automated screenshots of websites
