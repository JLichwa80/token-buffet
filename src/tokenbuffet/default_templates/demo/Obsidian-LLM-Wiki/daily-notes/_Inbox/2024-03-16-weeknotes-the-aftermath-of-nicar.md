# Weeknotes: the aftermath of NICAR

Source: https://simonwillison.net/2024/Mar/16/weeknotes-the-aftermath-of-nicar/

## Weeknotes: the aftermath of NICAR

16th March 2024

[NICAR](https://schedules.ire.org/nicar-2024/index.html) was fantastic this year. Alex and I ran [a successful workshop](https://github.com/datasette/nicar-2024-datasette) on Datasette and Datasette Cloud, and I gave a lightning talk demonstrating two new GPT-4 powered Datasette plugins—[datasette-enrichments-gpt](https://datasette.io/plugins/datasette-enrichments-gpt) and [datasette-extract](https://datasette.io/plugins/datasette-extract). I need to write more about the latter one: it enables populating tables from unstructured content (using a variant of [this technique](https://til.simonwillison.net/gpt3/openai-python-functions-data-extraction)) and it’s really effective. I got it working just in time for the conference.

I also solved the conference follow-up problem! I’ve long suffered from poor habits in dropping the ball on following up with people I meet at conferences. This time I used a trick I first learned at a YC demo day many years ago: if someone says they’d like to follow up, get out a calendar and book a future conversation with them right there on the spot.

I have a bunch of exciting conversations lined up over the next few weeks thanks to that, with a variety of different sizes of newsrooms who are either using or want to use Datasette.

#### Action menus in the Datasette 1.0 alphas

I released two new Datasette 1.0 alphas in the run-up to NICAR: [1.0a12](https://docs.datasette.io/en/latest/changelog.html#a12-2024-02-29) and [1.0a13](https://docs.datasette.io/en/latest/changelog.html#changelog).

The main theme of these two releases was improvements to Datasette’s “action buttons”.

Datasette plugins have long been able to register additional menu items that should be shown on the database and table pages. These were previously hidden behind a “cog” icon in the title of the page—once clicked it would reveal a menu of extra actions.

The cog wasn’t discoverable enough, and felt too much like mystery meat navigation. I decided to turn it into a much more clear button.

Here’s a GIF showing that new button in action across several different pages on Datasette Cloud (which has a bunch of plugins that use it):

![Animation starts on the page for the content database. A database actions blue button is clicked, revealing a menu of items such as Upload CSVs and Execute SQL Write. On a table page the button is called Table actions and has options such as Delete table. Executing a SQL query shows a Query actions button with an option to Create SQL view from this query.](https://static.simonwillison.net/static/2024/action-buttons.gif)

Prior to 1.0a12 Datasette had plugin hooks for just the database and table actions menus. I’ve added four more:

* [query\_actions()](https://docs.datasette.io/en/latest/plugin_hooks.html#query-actions-datasette-actor-database-query-name-request-sql-params) for actions that apply to the query results page. ([#2283](https://github.com/simonw/datasette/issues/2283))
* [view\_actions()](https://docs.datasette.io/en/latest/plugin_hooks.html#plugin-hook-view-actions) for actions that can be applied to a SQL view. ([#2297](https://github.com/simonw/datasette/issues/2297))
* [row\_actions()](https://docs.datasette.io/en/latest/plugin_hooks.html#plugin-hook-row-actions) for actions that apply to the row page. ([#2299](https://github.com/simonw/datasette/issues/2299))
* [homepage\_actions()](https://docs.datasette.io/en/latest/plugin_hooks.html#plugin-hook-homepage-actions) for actions that apply to the instance homepage. ([#2298](https://github.com/simonw/datasette/issues/2298))

Menu items can now also include an optional description, which is displayed below their label in the actions menu.

#### It’s always DNS

This site was offline for 24 hours this week due to a DNS issue. Short version: while I’ve been paying close attention to the management of domains I’ve bought in the past few years ([datasette.io](https://datasette.io/), [datasette.cloud](https://www.datasette.cloud/) etc) I hadn’t been paying attention to `simonwillison.net`.

... until it turned out I had it on a registrar with an old email address that I no longer had access to, and the domain was switched into “parked” mode because I had failed to pay for renewal!

(I haven’t confirmed this yet but I think I may have paid for a ten year renewal at some point, which gives you a full decade to lose track of how it’s being paid for.)

I’ll give credit to [123-reg](https://www.123-reg.co.uk/) (these days a subsidiary of GoDaddy)—they have a [well documented domain recovery policy](https://www.123-reg.co.uk/support/domains/what-is-the-domain-recovery-period-and-how-can-i-restore-my-domain-names/) and their support team got me back in control reasonably promptly—only slightly delayed by their UK-based account recovery team operating in a timezone separate from my own.

I registered `simonwillison.org` and configured that and `til.simonwillison.org` during the blackout, mainly because it turns out I refer back to my own written content a whole lot during my regular work! Once `.net` came back I [set up redirects using Cloudflare](https://til.simonwillison.net/cloudflare/redirect-whole-domain).

Thankfully I don’t usually use my domain for my personal email, or sorting this out would have been a whole lot more painful.

The most inconvenient impact was Mastodon: I run my own instance at [fedi.simonwillison.net](https://fedi.simonwillison.net/) ([previously](https://til.simonwillison.net/mastodon/custom-domain-mastodon)) and losing DNS broke everything, both my ability to post but also my ability to even read posts on my timeline.

#### Blog entries

I published three articles since my last weeknotes:

* [The GPT-4 barrier has finally been broken](https://simonwillison.net/2024/Mar/8/gpt-4-barrier/)
* [Prompt injection and jailbreaking are not the same thing](https://simonwillison.net/2024/Mar/5/prompt-injection-jailbreaking/)
* [Interesting ideas in Observable Framework](https://simonwillison.net/2024/Mar/3/interesting-ideas-in-observable-framework/)

#### Releases

I have released *so much stuff* recently. A lot of this was in preparation for NICAR—I wanted to polish all sorts of corners of Datasette Cloud, which is itself a huge bundle of pre-configured Datasette plugins. A lot of those plugins got a bump!

A few releases deserve a special mention:

* [datasette-extract](https://datasette.io/plugins/datasette-extract), hinted at above, is a new plugin that enables tables in Datasette to be populated from unstructured data in pasted text or images.
* [datasette-export-database](https://datasette.io/plugins/datasette-export-database) provides a way to export a current snapshot of a SQLite database from Datasette—something that previously wasn’t safe to do for databases that were accepting writes. It works by kicking off a background process to use `VACUUM INTO` in SQLite to create a temporary file with a transactional snapshot of the database state, then lets the user download that file.
* [llm-claude-3](https://github.com/simonw/llm-claude-3) provides access to the new Claude 3 models from my [LLM](https://llm.datasette.io/) tool. These models are really exciting: Opus feels better than GPT-4 at most things I’ve thrown at it, and Haiku is both slightly cheaper than GPT-3.5 Turbo and provides image input support at the lowest price point I’ve seen anywhere.
* [datasette-create-view](https://datasette.io/plugins/datasette-create-view) is a new plugin that helps you create a SQL view from a SQL query. I shipped the new [query\_actions()](https://docs.datasette.io/en/latest/plugin_hooks.html#query-actions-datasette-actor-database-query-name-request-sql-params) plugin hook to make this possible.

Here’s the full list of recent releases:

* **[datasette-packages 0.2.1](https://github.com/simonw/datasette-packages/releases/tag/0.2.1)**—2024-03-16  
  Show a list of currently installed Python packages
* **[datasette-export-database 0.2.1](https://github.com/datasette/datasette-export-database/releases/tag/0.2.1)**—2024-03-16  
  Export a copy of a mutable SQLite database on demand
* **[datasette-configure-fts 1.1.3](https://github.com/simonw/datasette-configure-fts/releases/tag/1.1.3)**—2024-03-14  
  Datasette plugin for enabling full-text search against selected table columns
* **[datasette-upload-csvs 0.9.1](https://github.com/simonw/datasette-upload-csvs/releases/tag/0.9.1)**—2024-03-14  
  Datasette plugin for uploading CSV files and converting them to database tables
* **[datasette-write 0.3.1](https://github.com/simonw/datasette-write/releases/tag/0.3.1)**—2024-03-14  
  Datasette plugin providing a UI for executing SQL writes against the database
* **[datasette-edit-schema 0.8a1](https://github.com/simonw/datasette-edit-schema/releases/tag/0.8a1)**—2024-03-14  
  Datasette plugin for modifying table schemas
* **[llm-claude-3 0.3](https://github.com/simonw/llm-claude-3/releases/tag/0.3)**—2024-03-13  
  LLM plugin for interacting with the Claude 3 family of models
* **[datasette-extract 0.1a3](https://github.com/datasette/datasette-extract/releases/tag/0.1a3)**—2024-03-13  
  Import unstructured data (text and images) into structured tables
* **[datasette 1.0a13](https://github.com/simonw/datasette/releases/tag/1.0a13)**—2024-03-13  
  An open source multi-tool for exploring and publishing data
* **[datasette-enrichments-quickjs 0.1a1](https://github.com/datasette/datasette-enrichments-quickjs/releases/tag/0.1a1)**—2024-03-09  
  Enrich data with a custom JavaScript function
* **[dclient 0.4](https://github.com/simonw/dclient/releases/tag/0.4)**—2024-03-08  
  A client CLI utility for Datasette instances
* **[datasette-saved-queries 0.2.2](https://github.com/simonw/datasette-saved-queries/releases/tag/0.2.2)**—2024-03-07  
  Datasette plugin that lets users save and execute queries
* **[datasette-create-view 0.1](https://github.com/datasette/datasette-create-view/releases/tag/0.1)**—2024-03-07  
  Create a SQL view from a query
* **[pypi-to-sqlite 0.2.3](https://github.com/simonw/pypi-to-sqlite/releases/tag/0.2.3)**—2024-03-06  
  Load data about Python packages from PyPI into SQLite
* **[datasette-uptime 0.1.1](https://github.com/datasette/datasette-uptime/releases/tag/0.1.1)**—2024-03-06  
  Datasette plugin showing uptime at /-/uptime
* **[datasette-sqlite-authorizer 0.2](https://github.com/datasette/datasette-sqlite-authorizer/releases/tag/0.2)**—2024-03-05  
  Configure Datasette to block operations using the SQLIte set\_authorizer mechanism
* **[datasette-sqlite-debug-authorizer 0.1.1](https://github.com/datasette/datasette-sqlite-debug-authorizer/releases/tag/0.1.1)**—2024-03-05  
  Debug SQLite authorizer calls
* **[datasette-expose-env 0.2](https://github.com/simonw/datasette-expose-env/releases/tag/0.2)**—2024-03-03  
  Datasette plugin to expose selected environment variables at /-/env for debugging
* **[datasette-tail 0.1a0](https://github.com/datasette/datasette-tail/releases/tag/0.1a0)**—2024-03-01  
  Tools for tailing your database
* **[datasette-column-sum 0.1a0](https://github.com/datasette/datasette-column-sum/releases/tag/0.1a0)**—2024-03-01  
  Sum the values in numeric Datasette columns
* **[datasette-schema-versions 0.3](https://github.com/simonw/datasette-schema-versions/releases/tag/0.3)**—2024-03-01  
  Datasette plugin that shows the schema version of every attached database
* **[datasette-studio 0.1a1](https://github.com/datasette/datasette-studio/releases/tag/0.1a1)**—2024-02-29  
  Datasette pre-configured with useful plugins. Experimental alpha.
* **[datasette-scale-to-zero 0.3.1](https://github.com/simonw/datasette-scale-to-zero/releases/tag/0.3.1)**—2024-02-29  
  Quit Datasette if it has not received traffic for a specified time period
* **[datasette-explain 0.2.1](https://github.com/simonw/datasette-explain/releases/tag/0.2.1)**—2024-02-28  
  Explain and validate SQL queries as you type them into Datasette

#### TILs

* [Redirecting a whole domain with Cloudflare](https://til.simonwillison.net/cloudflare/redirect-whole-domain)—2024-03-15
* [SQLite timestamps with floating point seconds](https://til.simonwillison.net/sqlite/floating-point-seconds)—2024-03-14
* [Generating URLs to a Gmail compose window](https://til.simonwillison.net/google/gmail-compose-url)—2024-03-13
* [Using packages from JSR with esbuild](https://til.simonwillison.net/javascript/jsr-esbuild)—2024-03-02
