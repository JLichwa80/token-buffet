# Weeknotes: DevDay, GitHub Universe, OpenAI chaos

Source: https://simonwillison.net/2023/Nov/22/weeknotes/

## Weeknotes: DevDay, GitHub Universe, OpenAI chaos

22nd November 2023

Three weeks of conferences and Datasette Cloud work, four days of chaos for OpenAI.

The second week of November was chaotically busy for me. On the Monday I attended the [OpenAI DevDay](https://devday.openai.com/) conference, which saw a bewildering array of announcements. I shipped [LLM 0.12](https://llm.datasette.io/en/stable/changelog.html#v0-12) that day with support for the brand new GPT-4 Turbo model (2-3x cheaper than GPT-4, faster and with a new increased 128,000 token limit), and built [ospeak](https://simonwillison.net/2023/Nov/7/ospeak/) that evening as a CLI tool for working with their excellent new text-to-speech API.

On Tuesday I recorded [a podcast episode](https://www.latent.space/p/devday-recap-clean) with the Latent Space crew talking about what was released at DevDay, and attended a GitHub Universe pre-summit for open source maintainers.

Then on Wednesday I spoke at GitHub Universe itself. I published a full annotated version of my talk here: [Financial sustainability for open source projects at GitHub Universe](https://simonwillison.net/2023/Nov/10/universe/). It was only ten minutes long but it took a lot of work to put together—ten minutes requires a lot of editing and planning to get right.

(I later used the audio from that talk to create a [cloned version of my voice](https://til.simonwillison.net/misc/voice-cloning), with shockingly effective results!)

With all of my conferences for the year out of the way, I spent the next week working with Alex Garcia on [Datasette Cloud](https://www.datasette.cloud/). Alex has been building out [datasette-comments](https://github.com/datasette/datasette-comments), an excellent new plugin which will allow Datasette users to collaborate on data by leaving comments on individual rows—ideal for collaborative investigative reporting.

Meanwhile I’ve been putting together the first working version of *enrichments*—a feature I’ve been threatening to build for a couple of years now. The key idea here is to make it easy to apply enrichment operations—geocoding, language model prompt evaluation, OCR etc—to rows stored in Datasette. I’ll have a lot more to share about this soon.

The biggest announcement at OpenAI DevDay was GPTs—the ability to create and share customized GPT configurations. It took me another week to fully understand those, and I wrote about my explorations in [Exploring GPTs: ChatGPT in a trench coat?](https://simonwillison.net/2023/Nov/15/gpts/).

And then last Friday everything went completely wild, when the board of directors of the non-profit that controls OpenAI fired Sam Altman over a vague accusation that he was “not consistently candid in his communications with the board”.

It’s four days later now and the situation is still shaking itself out. It inspired me to write about a topic I’ve wanted to publish for a while though: [Deciphering clues in a news article to understand how it was reported](https://simonwillison.net/2023/Nov/22/deciphering-clues/).

#### sqlite-utils 3.35.2 and shot-scraper 1.3

I’ll duplicate the full release notes for two of my projects here, because I want to highlight the contributions from external developers.

**[sqlite-utils 3.35.2](https://sqlite-utils.datasette.io/en/stable/changelog.html#v3-35-2)**

> * The `--load-extension=spatialite` option and [find\_spatialite()](https://sqlite-utils.datasette.io/en/stable/python-api.html#python-api-gis-find-spatialite) utility function now both work correctly on `arm64` Linux. Thanks, [Mike Coats](https://github.com/MikeCoats). ([#599](https://github.com/simonw/sqlite-utils/issues/599))
> * Fix for bug where `sqlite-utils insert` could cause your terminal cursor to disappear. Thanks, [Luke Plant](https://github.com/spookylukey). ([#433](https://github.com/simonw/sqlite-utils/issues/433))
> * `datetime.timedelta` values are now stored as `TEXT` columns. Thanks, [Harald Nezbeda](https://github.com/nezhar). ([#522](https://github.com/simonw/sqlite-utils/issues/522))
> * Test suite is now also run against Python 3.12.

**[shot-scraper 1.3](https://github.com/simonw/shot-scraper/releases/tag/1.3)**

> * New `--bypass-csp` option for bypassing any Content Security Policy on the page that prevents executing further JavaScript. Thanks, [Brenton Cleeland](https://github.com/sesh). [#116](https://github.com/simonw/shot-scraper/pull/116)
> * Screenshots taken using `shot-scraper --interactive $URL`—which allows you to interact with the page in a browser window and then hit `<enter>` to take the screenshot—it no longer reloads the page before taking the shot (which ignored your activity). [#125](https://github.com/simonw/shot-scraper/issues/125)
> * Improved accessibility of [documentation](https://shot-scraper.datasette.io). Thanks, [Paolo Melchiorre](https://github.com/pauloxnet). [#120](https://github.com/simonw/shot-scraper/pull/120)

#### Releases these weeks

* **[datasette-sentry 0.4](https://github.com/simonw/datasette-sentry/releases/tag/0.4)**—2023-11-21  
  Datasette plugin for configuring Sentry
* **[datasette-enrichments 0.1a4](https://github.com/datasette/datasette-enrichments/releases/tag/0.1a4)**—2023-11-20  
  Tools for running enrichments against data stored in Datasette
* **[ospeak 0.2](https://github.com/simonw/ospeak/releases/tag/0.2)**—2023-11-07  
  CLI tool for running text through OpenAI Text to speech
* **[llm 0.12](https://github.com/simonw/llm/releases/tag/0.12)**—2023-11-06  
  Access large language models from the command-line
* **[datasette-edit-schema 0.7.1](https://github.com/simonw/datasette-edit-schema/releases/tag/0.7.1)**—2023-11-04  
  Datasette plugin for modifying table schemas
* **[sqlite-utils 3.35.2](https://github.com/simonw/sqlite-utils/releases/tag/3.35.2)**—2023-11-04  
  Python CLI utility and library for manipulating SQLite databases
* **[llm-anyscale-endpoints 0.3](https://github.com/simonw/llm-anyscale-endpoints/releases/tag/0.3)**—2023-11-03  
  LLM plugin for models hosted by Anyscale Endpoints
* **[shot-scraper 1.3](https://github.com/simonw/shot-scraper/releases/tag/1.3)**—2023-11-01  
  A command-line utility for taking automated screenshots of websites

#### TIL these weeks

* [Cloning my voice with ElevenLabs](https://til.simonwillison.net/misc/voice-cloning)—2023-11-16
* [Summing columns in remote Parquet files using DuckDB](https://til.simonwillison.net/duckdb/remote-parquet)—2023-11-14
