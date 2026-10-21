# Weeknotes: Getting ready for NICAR

Source: https://simonwillison.net/2024/Feb/27/weeknotes-getting-ready-for-nicar/

## Weeknotes: Getting ready for NICAR

27th February 2024

Next week is [NICAR 2024](https://www.ire.org/training/conferences/nicar-2024/) in Baltimore—the annual data journalism conference hosted by [Investigative Reporters and Editors](https://www.ire.org/). I’m running [a workshop](https://schedules.ire.org/nicar-2024/index.html#1110) on Datasette, and I plan to spend most of my time in the hallway track talking to people about Datasette, Datasette Cloud and how the Datasette ecosystem can best help support their work.

I’ve been working with Alex Garcia to get [Datasette Cloud](http://www.datasette.cloud/) ready for the conference. We have a few new features that we’re putting the final touches on, in addition to ensuring features like [Datasette Enrichments](https://enrichments.datasette.io/) and [Datasette Comments](https://github.com/datasette/datasette-comments) are in good shape for the event.

#### Releases

> * **[llm-mistral 0.3](https://github.com/simonw/llm-mistral/releases/tag/0.3)**—2024-02-26  
>   LLM plugin providing access to Mistral models using the Mistral API

[Mistral](https://mistral.ai/) released [Mistral Large](https://mistral.ai/news/mistral-large/) this morning, so I rushed out a new release of my [llm-mistral plugin](https://github.com/simonw/llm-mistral) to add support for it.

```
pipx install llm
llm install llm-mistral --upgrade
llm keys set mistral
# <Paste in your Mistral API key>
llm -m mistral-large 'Prompt goes here'
```

The plugin now hits the Mistral API endpoint that lists models (via a cache), which means future model releases should be supported automatically without needing a new plugin release.

> * **[dclient 0.3](https://github.com/simonw/dclient/releases/tag/0.3)**—2024-02-25  
>   A
>   client CLI utility for Datasette instances

[dclient](https://dclient.datasette.io/) provides a tool for interacting with a remote Datasette instance. You can use it to run queries:

```
dclient query https://datasette.io/content \
  "select * from news limit 3"
```

You can set aliases for your Datasette instances:

```
dclient alias add simon https://simon.datasette.cloud/data
```

And for Datasette 1.0 alpha instances with the [write API](https://docs.datasette.io/en/latest/json_api.html#the-json-write-api) (as seen on Datasette Cloud) you can insert data into a new or an existing table:

```
dclient auth add simon
# <Paste in your API token>
dclient insert simon my_new_table data.csv --create
```

The 0.3 release adds improved support for streaming data into a table. You can run a command like this:

```
tail -f log.ndjson | dclient insert simon my_table \
  --nl - --interval 5 --batch-size 20
```

The `--interval 5` option is new: it means that records will be written to the API if 5 seconds have passed since the last write. `--batch-size 20` means that records will be written in batches of 20, and will be sent as soon as the batch is full or the interval has passed.

> * **[datasette-events-forward 0.1a1](https://github.com/datasette/datasette-events-forward/releases/tag/0.1a1)**—2024-02-20  
>   Forward Datasette analytical events on to another Datasette instance

I wrote about the new [Datasette Events](https://simonwillison.net/2024/Feb/7/datasette-1a8/#datasette-events) mechanism in the 1.0a8 release notes. This new plugin was originally built for Datasette Cloud—it forwards analytical events from an instance to a central analytics instance. Using Datasette Cloud for analytics for Datasette Cloud is a pleasing exercise in [dogfooding](https://en.wikipedia.org/wiki/Eating_your_own_dog_food).

> * **[datasette-auth-tokens 0.4a9](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a9)**—2024-02-20  
>   Datasette plugin for authenticating access using API tokens

A tiny cosmetic bug fix.

> * **[datasette 1.0a11](https://github.com/simonw/datasette/releases/tag/1.0a11)**—2024-02-19  
>   An open source multi-tool for exploring and publishing data

I’m increasing the frequency of the Datasette 1.0 alphas. This one has a minor permissions fix (the ability to replace a row using the insert API now requires the `update-row` permission) and a small cosmetic fix which I’m really pleased with: the menus displayed by the column action menu now align correctly with their cog icon!

![Clicking on a cog icon now shows a menu directly below that icon, with a little grey arrow in the right place to align with the icon that was clicked](https://static.simonwillison.net/static/2024/cog-alignment.gif)

> * **[datasette-edit-schema 0.8a0](https://github.com/simonw/datasette-edit-schema/releases/tag/0.8a0)**—2024-02-18  
>   Datasette plugin for modifying table schemas

This is a pretty significant release: it adds finely-grained permission support such that Datasette’s core `create-table`, `alter-table` and `drop-table` permissions are now respected by the plugin.

The `alter-table` permission was introduced in [Datasette 1.0a9](https://docs.datasette.io/en/latest/changelog.html#a9-2024-02-16) a couple of weeks ago.

> * **[datasette-unsafe-actor-debug 0.2](https://github.com/datasette/datasette-unsafe-actor-debug/releases/tag/0.2)**—2024-02-18  
>   Debug plugin that lets you imitate any actor

When testing permissions it’s useful to have a really convenient way to sign in to Datasette using different accounts. This plugin provides that, but only if you start Datasette with custom plugin configuration or by using this new 1.0 alpha shortcut setting option:

```
datasette -s plugins.datasette-unsafe-actor-debug.enabled 1
```

> * **[datasette-studio 0.1a0](https://github.com/datasette/datasette-studio/releases/tag/0.1a0)**—2024-02-18  
>   Datasette pre-configured with useful plugins. Experimental alpha.

An experiment in bundling plugins. `pipx install datasette-studio` gets you an installation of Datasette under a separate alias—`datasette-studio`—which comes preconfigured with a set of useful plugins.

The really fun thing about this one is that the entire package is defined by a [pyproject.toml](https://github.com/datasette/datasette-studio/blob/0.1a0/pyproject.toml) file, with no additional Python code needed. Here’s a truncated copy of that TOML:

```
[project]
name = "datasette-studio"
version = "0.1a0"
description = "Datasette pre-configured with useful plugins"
requires-python = ">=3.8"
dependencies = [
    "datasette>=1.0a10",
    "datasette-edit-schema",
    "datasette-write-ui",
    "datasette-configure-fts",
    "datasette-write",
]

[project.entry-points.console_scripts]
datasette-studio = "datasette.cli:cli"
```

I think it’s pretty neat that a full application can be defined like this in terms of 5 dependencies and a custom `console_scripts` entry point.

Datasette Studio is still *very* experimental, but I think it’s pointing in a promising direction.

> * **[datasette-enrichments-opencage 0.1.1](https://github.com/datasette/datasette-enrichments-opencage/releases/tag/0.1.1)**—2024-02-16  
>   Geocoding and reverse geocoding using OpenCage

This resolves a dreaded “database locked” error I was seeing occasionally in Datasette Cloud.

Short version: SQLite, when running in WAL mode, is almost immune to those errors... provided you remember to run all write operations in short, well-defined transactions.

I’d forgotten to do that in this plugin and it was causing problems.

After shipping this release I decided to make it much harder to make this mistake in the future, so I released [Datasette 1.0a10](https://docs.datasette.io/en/latest/changelog.html#a10-2024-02-17) which now automatically wraps calls to `database.execute_write_fn()` in a transaction even if you forget to do so yourself.

#### Blog entries

> * [The killer app of Gemini Pro 1.5 is video](https://simonwillison.net/2024/Feb/21/gemini-pro-video/)

My first full blog post of the year to end up on Hacker News, where it sparked [a lively conversation](https://news.ycombinator.com/item?id=39458264) with 489 comments!

#### TILs

> * [Tracking SQLite table history using a JSON audit log](https://til.simonwillison.net/sqlite/json-audit-log)—2024-02-27

Yet another experiment with audit tables in SQLite. This one uses a terrifying nested sequenc of `json_patch()` calls to assemble a JSON document describing the change made to the table.

> * [Running a scheduled function on Val Town to import Atom feeds into Datasette Cloud](https://til.simonwillison.net/valtown/scheduled)—2024-02-21

[Val Town](https://www.val.town/) is a very neat attempt at solving another of my favourite problems: how to execute user-provided code safely in a sandbox. It turns out to be the perfect mechanism for running simple scheduled functions such as code that reads data and writes it to Datasette Cloud using the write API.

> * [Getting Python MD5 to work with FIPS systems](https://til.simonwillison.net/python/md5-fips)—2024-02-14

FIPS is [the Federal Information Processing Standard](https://en.wikipedia.org/wiki/FIPS_140-2), and systems that obey it refuse to run Datasette due to its use of MD5 hash functions. I figured out how to get that to work anyway, since Datasette’s MD5 usage is purely cosmetic, not cryptographic.

> * [Running Ethernet over existing coaxial cable](https://til.simonwillison.net/networking/ethernet-over-coaxial-cable)—2024-02-13

This actually [showed up on Hacker News](https://news.ycombinator.com/item?id=39355041) without me noticing until a few days later, where many people told me that I should rewire my existing Ethernet cables rather than resorting to more exotic solutions.

> * [Piping from rg to llm to answer questions about code](https://til.simonwillison.net/llms/rg-pipe-llm-trick)—2024-02-11

I guess this is another super lightweight form of RAG: you can use the `rg` context options (include X lines before/after each match) to assemble just enough context to get useful answers to questions about code.
