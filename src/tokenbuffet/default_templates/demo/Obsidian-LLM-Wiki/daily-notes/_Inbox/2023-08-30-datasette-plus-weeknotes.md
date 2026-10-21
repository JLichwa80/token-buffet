# Datasette 1.0a4 and 1.0a5, plus weeknotes

Source: https://simonwillison.net/2023/Aug/30/datasette-plus-weeknotes/

## Datasette 1.0a4 and 1.0a5, plus weeknotes

30th August 2023

Two new alpha releases of Datasette, plus a keynote at WordCamp, a new LLM release, two new LLM plugins and a flurry of TILs.

#### Datasette 1.0a5

Released this morning, [Datasette 1.0a5](https://docs.datasette.io/en/1.0a5/changelog.html) has some exciting new changes driven by Datasette Cloud and the ongoing march towards Datasette 1.0.

[Alex Garcia](https://alexgarcia.xyz/) is working with me on Datasette Cloud and Datasette generally, generously sponsored by [Fly](https://fly.io/).

Two of the changes in 1.0a5 were driven by Alex:

> New `datasette.yaml` (or `.json`) configuration file, which can be specified using `datasette -c path-to-file`. The goal here to consolidate settings, plugin configuration, permissions, canned queries, and other Datasette configuration into a single single file, separate from `metadata.yaml`. The legacy `settings.json` config file used for [Configuration directory mode](https://docs.datasette.io/en/1.0a5/settings.html#config-dir) has been removed, and `datasette.yaml` has a `"settings"` section where the same settings key/value pairs can be included. In the next future alpha release, more configuration such as plugins/permissions/canned queries will be moved to the `datasette.yaml` file. See [#2093](https://github.com/simonw/datasette/issues/2093) for more details.

Right from the very start of the project, Datasette has supported specifying metadata about databases—sources, licenses, etc, as a `metadata.json` file that can be passed to Datasette like this:

```
datasette data.db -m metadata.json
```

Over time, the purpose and uses of that file has expanded in all kinds of different directions. It can be used [for plugin settings](https://docs.datasette.io/en/1.0a5/plugins.html#plugin-configuration), and to set preferences for a table default page size, [default facets](https://docs.datasette.io/en/1.0a5/facets.html#facets-in-metadata) etc), and even to [configure access permissions](https://docs.datasette.io/en/1.0a5/authentication.html#access-permissions-in-metadata) for who can view what.

The name `metadata.json` is entirely inappropriate for what the file actually does. It’s a mess.

I’ve always had a desire to fix this before Datasette 1.0, but it never quite got high up enough the priority list for me to spend time on it.

Alex [expressed interest in fixing it](https://github.com/simonw/datasette/issues/2093), and has started to put a plan into motion for cleaning it up.

More details [in the issue](https://github.com/simonw/datasette/issues/2093).

> The Datasette `_internal` database has had some changes. It no longer shows up in the `datasette.databases` list by default, and is now instead available to plugins using the `datasette.get_internal_database()`. Plugins are invited to use this as a private database to store configuration and settings and secrets that should not be made visible through the default Datasette interface. Users can pass the new `--internal internal.db` option to persist that internal database to disk. ([#2157](https://github.com/simonw/datasette/issues/2157)).

This was the other initiative driven by Alex. In working on Datasette Cloud we realized that it’s actually quite common for plugins to need somewhere to store data that shouldn’t necessarily be visible to regular users of a Datasette instance—things like tokens created by [datasette-auth-tokens](https://datasette.io/plugins/datasette-auth-tokens), or the progress bar mechanism used by [datasette-upload-csvs](https://datasette.io/plugins/datasette-upload-csvs).

Alex pointed out that the existing `_internal` database for Datasette could be expanded to cover these use-cases as well. [#2157](https://github.com/simonw/datasette/issues/2157) has more details on how we agreed this should work.

The other changes in 1.0a5 were driven by me:

> When restrictions are applied to [API tokens](https://docs.datasette.io/en/1.0a5/authentication.html#createtokenview), those restrictions now behave slightly differently: applying the `view-table` restriction will imply the ability to `view-database` for the database containing that table, and both `view-table` and `view-database` will imply `view-instance`. Previously you needed to create a token with restrictions that explicitly listed `view-instance` and `view-database` and `view-table` in order to view a table without getting a permission denied error. ([#2102](https://github.com/simonw/datasette/issues/2102))

I [described finely-grained permissions](https://simonwillison.net/2022/Dec/15/datasette-1a2/#finely-grained-permissions) for access tokens in my annotated release notes for 1.0a2.

They provide a mechanism for creating an API token that’s only allowed to perform a subset of actions on behalf of the user.

In trying these out for Datasette Cloud I came across a nasty usability flaw. You could create a token that was restricted to `view-table` access for a specific table... and it wouldn’t work. Because the access code for that view would check for `view-instance` and `view-database` permission first.

1.0a5 fixes that, by adding logic that says that if a token can `view-table` that implies it can `view-database` for the database containing that table, and `view-instance` for the overall instance.

This change took quite some time to develop, because any time I write code involving permissions I like to also include extremely comprehensive automated tests.

> The `-s/--setting` option can now take dotted paths to nested settings. These will then be used to set or over-ride the same options as are present in the new configuration file. ([#2156](https://github.com/simonw/datasette/issues/2156))

This is a fun little detail inspired by Alex’s configuration work.

I run a lot of different Datasette instances, often on an ad-hoc basis.

I sometimes find it frustrating that to use certain features I need to create a `metadata.json` (soon to be `datasette.yml`) configuration file, just to get something to work.

Wouldn’t it be neat if every possible setting for Datasette could be provided both in a configuration file or as command-line options?

That’s what the new `--setting` option aims to solve. Anything that can be represented as a JSON or YAML configuration can now also be represented as key/value pairs on the command-line.

Here’s an example [from my initial issue comment](https://github.com/simonw/datasette/issues/2143#issuecomment-1690792514):

```
datasette \
  -s settings.sql_time_limit_ms 1000 \
  -s plugins.datasette-auth-tokens.manage_tokens true \
  -s plugins.datasette-auth-tokens.manage_tokens_database tokens \
  -s plugins.datasette-ripgrep.path "/home/simon/code-to-search" \
  -s databases.mydatabase.tables.example_table.sort created \
  mydatabase.db tokens.db
```

Once this feature is complete, the above will behave the same as a `datasette.yml` file containing this:

```
plugins:
  datasette-auth-tokens:
    manage_tokens: true
    manage_tokens_database: tokens
  datasette-ripgrep:
    path: /home/simon/code-to-search
databases:
  mydatabase:
    tables:
      example_table:
        sort: created
settings:
  sql_time_limit_ms: 1000
```

I’ve experimented with ways of turning key/value pairs into nested JSON objects before, with my [json-flatten](https://github.com/simonw/json-flatten) library.

This time I took a slightly different approach. In particular, if you need to pass a nested JSON object (such as an array) which isn’t easily represented using `key.nested` notation, you can pass it like this instead:

```
datasette data.db \
  -s plugins.datasette-complex-plugin.configs \
  '{"foo": [1,2,3], "bar": "baz"}'
```

Which would convert to the following equivalent YAML:

```
plugins:
  datasette-complex-plugin:
    configs:
      foo:
        - 1
        - 2
        - 3
      bar: baz
```

These examples don’t quite work yet, because the plugin configuration hasn’t migrated to `datasette.yml`—but it should work for the next alpha.

> New `--actor '{"id": "json-goes-here"}'` option for use with `datasette --get` to treat the simulated request as being made by a specific actor, see [datasette --get](https://docs.datasette.io/en/1.0a5/cli-reference.html#cli-datasette-get). ([#2153](https://github.com/simonw/datasette/issues/2153))

This is a fun little debug helper I built while working on restricted tokens.

The `datasette --get /...` option is a neat trick that can be used to simulate an HTTP request through the Datasette instance, without even starting a server running on a port.

I use it for things like [generating social media card images](https://til.simonwillison.net/shot-scraper/social-media-cards) for my TILs website.

The new `--actor` option lets you add a simulated [actor](https://docs.datasette.io/en/latest/authentication.html#actors) to the request, which is useful for testing out things like configured authentication and permissions.

#### A security fix in Datasette 1.0a4

[Datasette 1.0a4](https://docs.datasette.io/en/latest/changelog.html#a4-2023-08-21) has a security fix: I realized that the API explorer I added in the 1.0 alpha series was exposing the names of databases and tables (though not their actual content) to unauthenticated users, even for Datasette instances that were protected by authentication.

I issued a GitHub security advisory for this: [Datasette 1.0 alpha series leaks names of databases and tables to unauthenticated users](https://github.com/simonw/datasette/security/advisories/GHSA-7ch3-7pp7-7cpq), which has since been issued a CVE, [CVE-2023-40570](https://nvd.nist.gov/vuln/detail/CVE-2023-40570)—GitHub is [a CVE Numbering Authority](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories#cve-identification-numbers) which means their security team are trusted to review such advisories and issue CVEs where necessary.

I expect the impact of this vulnerability to be very small: outside of [Datasette Cloud](https://www.datasette.cloud/) very few people are running the Datasette 1.0 alphas on the public internet, and it’s possible that the set of those users who are also authenticating their instances to provide authenticated access to private data—especially where just the database and table names of that data is considered sensitive—is an empty set.

Datasette Cloud itself has detailed access logs primarily to help evaluate this kind of threat. I’m pleased to report that those logs showed no instances of an unauthenticated user accessing the pages in question prior to the bug being fixed.

#### A keynote at WordCamp US

Last Friday I gave a keynote at [WordCamp US](https://us.wordcamp.org/2023/) on the subject of Large Language Models.

I used [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper) and my [annotated presentation tool](https://simonwillison.net/2023/Aug/6/annotated-presentations/) to turn that into a detailed transcript, complete with additional links and context: [Making Large Language Models work for you](https://simonwillison.net/2023/Aug/27/wordcamp-llms/).

#### llm-openrouter and llm-anyscale-endpoints

I released two new plugins for [LLM](https://llm.datasette.io/), which lets you run large language models either locally or via APIs, as both a CLI tool and a Python library.

Both plugins provide access to API-hosted models:

* **[llm-openrouter](https://github.com/simonw/llm-openrouter)** provides access to [models](https://openrouter.ai/docs#models) hosted by [OpenRouter](https://openrouter.ai/). Of particular interest here is Claude—I’m still on the waiting list for the official Claude API, but in the meantime I can pay for access to it via OpenRouter and it works just fine. Claude has a 100,000 token context, making it a really great option for working with larger documents.
* **[llm-anyscale-endpoints](https://github.com/simonw/llm-anyscale-endpoints)** is a similar plugin that instead works with [Anyscale Endpoints](https://app.endpoints.anyscale.com/). Anyscale provide Llama 2 and Code Llama at extremely low prices—between $0.25 and $1 per million tokens, depending on the model.

These plugins were very quick to develop.

Both OpenRouter and Anyscale Endpoints provide API endpoints that emulate the official OpenAI APIs, including the way the handle streaming tokens.

LLM already has code for talking to those endpoints via the [openai](https://github.com/openai/openai-python) Python library, which can be re-pointed to another backend using the officially supported `api_base` parameter.

So the core code for the plugins ended up being less than 30 lines each: [llm\_openrouter.py](https://github.com/simonw/llm-openrouter/blob/main/llm_openrouter.py) and [llm\_anyscale\_endpoints.py](https://github.com/simonw/llm-anyscale-endpoints/blob/main/llm_anyscale_endpoints.py).

#### llm 0.8

I shipped [LLM 0.8](https://llm.datasette.io/en/stable/changelog.html#v0-8) a week and a half ago, with a bunch of small changes.

The most significant of these was a change to the default `llm logs` output, which shows the logs (recorded in SQLite) of the previous prompts and responses you have sent through the tool.

This output used to be JSON. It’s [now Markdown](https://github.com/simonw/llm/issues/160#issuecomment-1682991314), which is both easier to read and can be pasted into GitHub Issue comments or Gists or similar to share the results with other people.

[The release notes for 0.8](https://llm.datasette.io/en/stable/changelog.html#v0-8) describe all of the other improvements.

#### sqlite-utils 3.35

The [3.35 release of sqlite-utils](https://github.com/simonw/sqlite-utils/releases/tag/3.35) was driven by LLM.

`sqlite-utils` has a mechanism for adding foreign keys to an existing table—something that’s not supported by SQLite out of the box.

That implementation used to work using a deeply gnarly hack: it would switch the `sqlite_master` table over to being writable (using `PRAGMA writable_schema = 1`), update that schema in place to reflect the new foreign keys and then toggle `writable_schema = 0` back again.

It turns out there are Python installations out there—most notably the system Python on macOS—which completely disable the ability to write to that table, no matter what the status of the various pragmas.

I was getting bug reports from LLM users who were running into this. I realized that I had a solution for this mostly implemented already: the [sqlite-utils transform() method](https://sqlite-utils.datasette.io/en/stable/python-api.html#transforming-a-table), which can apply all sorts of complex schema changes by creating a brand new table, copying across the old data and then renaming it to replace the old one.

So I dropped the old `writable_schema` mechanism entirely in favour of `.transform()`—it’s slower, because it requires copying the entire table, but it doesn’t have weird edge-cases where it doesn’t work.

Since [sqlite-utils supports plugins now](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/), I realized I could set a healthy precedent by making the removed feature available in a new plugin: [sqlite-utils-fast-fks](https://github.com/simonw/sqlite-utils-fast-fks), which provides the following command for adding foreign keys the fast, old way (provided your installation supports it):

```
sqlite-utils install sqlite-utils-fast-fks
sqlite-utils fast-fks my_database.db places country_id country id
```

I’ve always admired how [jQuery](https://jquery.com/) uses plugins to keep old features working on an opt-in basis after major version upgrades. I’m excited to be able to apply the same pattern for `sqlite-utils`.

#### paginate-json 1.0

[paginate-json](https://github.com/simonw/paginate-json) is a tiny tool I first released a few years ago to solve a very specific problem.

There’s a neat pattern in some JSON APIs where the [HTTP link header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link) is used to indicate subsequent pages of results.

The best example I know of this is the GitHub API. Run this to see what it looks like here I’m using the [events API](https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-public-events-for-a-user)):

```
curl -i \
  https://api.github.com/users/simonw/events
```

Here’s a truncated example of the output:

```
HTTP/2 200 
server: GitHub.com
content-type: application/json; charset=utf-8
link: <https://api.github.com/user/9599/events?page=2>; rel="next", <https://api.github.com/user/9599/events?page=9>; rel="last"

[
  {
    "id": "31467177730",
    "type": "PushEvent",
```

The `link` header there specifies a `next` and `last` URL that can be used for pagination.

To fetch all available items, you can follow the `next` link repeatedly until it runs out.

My `paginate-json` tool can follow these links for you. If you run it like this:

```
paginate-json \
  https://api.github.com/users/simonw/events
```

It will output a single JSON array consisting of the results from every available page.

The 1.0 release adds [a bunch of small features](https://github.com/simonw/paginate-json/releases/tag/1.0), but also marks my confidence in the stability of the design of the tool.

The [Datasette JSON API](https://docs.datasette.io/en/latest/json_api.html) has supported [link pagination](https://docs.datasette.io/en/latest/json_api.html#pagination) for a while—you can use `paginate-json` with Datasette like this, taking advantage of the new `--key` option to paginate over the array of objects returned in the `"rows"` key:

```
paginate-json \
  'https://datasette.io/content/pypi_releases.json?_labels=on' \
  --key rows \
  --nl
```

The `--nl` option here causes `paginate-json` to output the results as newline-delimited JSON, instead of bundling them together into a JSON array.

Here’s how to use [sqlite-utils insert](https://sqlite-utils.datasette.io/en/stable/cli.html#inserting-newline-delimited-json) to insert that data directly into a fresh SQLite database:

```
paginate-json \
  'https://datasette.io/content/pypi_releases.json?_labels=on' \
  --key rows \
  --nl | \
    sqlite-utils insert data.db releases - \
      --nl --flatten
```

#### Releases this week

* **[paginate-json 1.0](https://github.com/simonw/paginate-json/releases/tag/1.0)**—2023-08-30  
  Command-line tool for fetching JSON from paginated APIs
* **[datasette-auth-tokens 0.4a2](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a2)**—2023-08-29  
  Datasette plugin for authenticating access using API tokens
* **[datasette 1.0a5](https://github.com/simonw/datasette/releases/tag/1.0a5)**—2023-08-29  
  An open source multi-tool for exploring and publishing data
* **[llm-anyscale-endpoints 0.2](https://github.com/simonw/llm-anyscale-endpoints/releases/tag/0.2)**—2023-08-25  
  LLM plugin for models hosted by Anyscale Endpoints
* **[datasette-jellyfish 2.0](https://github.com/simonw/datasette-jellyfish/releases/tag/2.0)**—2023-08-24  
  Datasette plugin adding SQL functions for fuzzy text matching powered by Jellyfish
* **[datasette-configure-fts 1.1.2](https://github.com/simonw/datasette-configure-fts/releases/tag/1.1.2)**—2023-08-23  
  Datasette plugin for enabling full-text search against selected table columns
* **[datasette-ripgrep 0.8.1](https://github.com/simonw/datasette-ripgrep/releases/tag/0.8.1)**—2023-08-21  
  Web interface for searching your code using ripgrep, built as a Datasette plugin
* **[datasette-publish-fly 1.3.1](https://github.com/simonw/datasette-publish-fly/releases/tag/1.3.1)**—2023-08-21  
  Datasette plugin for publishing data using Fly
* **[llm-openrouter 0.1](https://github.com/simonw/llm-openrouter/releases/tag/0.1)**—2023-08-21  
  LLM plugin for models hosted by OpenRouter
* **[llm 0.8](https://github.com/simonw/llm/releases/tag/0.8)**—2023-08-21  
  Access large language models from the command-line
* **[sqlite-utils-fast-fks 0.1](https://github.com/simonw/sqlite-utils-fast-fks/releases/tag/0.1)**—2023-08-18  
  Fast foreign key addition for sqlite-utils
* **[datasette-edit-schema 0.5.3](https://github.com/simonw/datasette-edit-schema/releases/tag/0.5.3)**—2023-08-18  
  Datasette plugin for modifying table schemas
* **[sqlite-utils 3.35](https://github.com/simonw/sqlite-utils/releases/tag/3.35)**—2023-08-18  
  Python CLI utility and library for manipulating SQLite databases

#### TIL this week

* [Streaming output of an indented JSON array](https://til.simonwillison.net/json/streaming-indented-json-array)—2023-08-30
* [Downloading partial YouTube videos with ffmpeg](https://til.simonwillison.net/macos/downloading-partial-youtube-videos)—2023-08-26
* [Compile and run a new SQLite version with the existing sqlite3 Python library on macOS](https://til.simonwillison.net/sqlite/sqlite-version-macos-python)—2023-08-22
* [Configuring Django SQL Dashboard for Fly PostgreSQL](https://til.simonwillison.net/fly/django-sql-dashboard)—2023-08-22
* [Calculating the size of a SQLite database file using SQL](https://til.simonwillison.net/sqlite/database-file-size)—2023-08-21
* [Updating stable docs in ReadTheDocs without pushing a release](https://til.simonwillison.net/readthedocs/stable-docs)—2023-08-21
* [A shell script for running Go one-liners](https://til.simonwillison.net/bash/go-script)—2023-08-20
* [A one-liner to output details of the current Python’s SQLite](https://til.simonwillison.net/sqlite/python-sqlite-environment)—2023-08-19
* [A simple pattern for inlining binary content in a Python script](https://til.simonwillison.net/python/inlining-binary-data)—2023-08-19
* [Running multiple servers in a single Bash script](https://til.simonwillison.net/bash/multiple-servers)—2023-08-17
