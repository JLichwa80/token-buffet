# Weeknotes: sqlite-utils 3.31, download-esm, Python in a sandbox

Source: https://simonwillison.net/2023/May/10/weeknotes/

## Weeknotes: sqlite-utils 3.31, download-esm, Python in a sandbox

10th May 2023

A couple of speaking appearances last week—one planned, one unplanned. Plus `sqlite-utils 3.31`, `download-esm` and a new TIL.

#### Prompt injection video, Leaked Google document audio

I participated in the LangChain webinar about prompt injection. The session was recorded, so I extracted my 12 minute introduction to the topic and turned it into [a blog post](https://simonwillison.net/2023/May/2/prompt-injection-explained/) complete with a Whisper transcription, a video and the slides I used in the talk.

Then on Thursday I wrote about [the leaked internal Google document](https://simonwillison.net/2023/May/4/no-moat/) that argued that Google and OpenAI have no meaningful moat given the accelerating pace of open source LLM research.

This lead to a last minute invitation to participate in a Latent Space Twitter Space about the document, which is now available [as a podcast](https://www.latent.space/p/no-moat#details).

#### sqlite-utils 3.31

I realized that [sqlite-utils](https://sqlite-utils.datasette.io/) had been quietly accumulating small fixes and pull requests since the 3.30 release last October, and spent a day tidying those up and turning them into a release.

Notably, four contributors get credited in [the release notes](https://sqlite-utils.datasette.io/en/stable/changelog.html#v3-31): Chris Amico, Kenny Song, Martin Carpenter and Scott Perry.

Key changes are listed below:

> * Automatically locates the SpatiaLite extension on Apple Silicon. Thanks, Chris Amico. ([#536](https://github.com/simonw/sqlite-utils/pull/536))
> * New `--raw-lines` option for the `sqlite-utils query` and `sqlite-utils memory` commands, which outputs just the raw value of the first column of evy row. ([#539](https://github.com/simonw/sqlite-utils/issues/539))
> * Fixed a bug where `table.upsert_all()` failed if the `not_null=` option was passed. ([#538](https://github.com/simonw/sqlite-utils/issues/538))
> * `table.convert(..., skip_false=False)` and `sqlite-utils convert --no-skip-false` options, for avoiding a misfeature where the [convert()](http://127.0.0.1:8000/python-api.html#python-api-convert) mechanism skips rows in the database with a falsey value for the specified column. Fixing this by default would be a backwards-incompatible change and is under consideration for a 4.0 release in the future. ([#527](https://github.com/simonw/sqlite-utils/issues/527))
> * Tables can now be created with self-referential foreign keys. Thanks, Scott Perry. ([#537](https://github.com/simonw/sqlite-utils/pull/537))
> * `sqlite-utils transform` no longer breaks if a table defines default values for columns. Thanks, Kenny Song. ([#509](https://github.com/simonw/sqlite-utils/issues/509))
> * Fixed a bug where repeated calls to `table.transform()` did not work correctly. Thanks, Martin Carpenter. ([#525](https://github.com/simonw/sqlite-utils/issues/525))

#### download-esm

As part of my ongoing mission to figure out how to write modern JavaScript without surrendering to one of the many different JavaScript build tools, I built [download-esm](https://github.com/simonw/download-esm)—a Python CLI tool for downloading the ECMAScript module versions of an npm package along with all of their module dependencies.

I wrote more about my justification for building that tool in [download-esm: a tool for downloading ECMAScript modules](https://simonwillison.net/2023/May/2/download-esm/).

#### Running Python in a Deno/Pyodide sandbox

I’m still trying to find the best way to run untrusted Python code in a safe WebAssembly sandbox.

My latest attempt takes advantage of Pyodide and Deno. It was inspired by [this comment](https://github.com/pyodide/pyodide/issues/3420#issuecomment-1542742906) by Milan Raj, showing how Deno can load Pyodide now. Pyodide was previously only available in web browsers.

I came up with a somewhat convoluted mechanism that starts a Deno process running in a Python `subprocess` and then runs Pyodide inside of Deno.

See [Running Python code in a Pyodide sandbox via Deno](https://til.simonwillison.net/deno/pyodide-sandbox) for the code and my thoughts on next steps for that prototype.

#### Blog entries this week

* [Leaked Google document: “We Have No Moat, And Neither Does OpenAI”](https://simonwillison.net/2023/May/4/no-moat/)
* [Midjourney 5.1](https://simonwillison.net/2023/May/4/midjourney-51/)
* [Prompt injection explained, with video, slides, and a transcript](https://simonwillison.net/2023/May/2/prompt-injection-explained/)
* [download-esm: a tool for downloading ECMAScript modules](https://simonwillison.net/2023/May/2/download-esm/)
* [Let’s be bear or bunny](https://simonwillison.net/2023/May/1/lets-be-bear-or-bunny/)

#### Releases this week

* **[sqlite-utils 3.31](https://github.com/simonw/sqlite-utils/releases/tag/3.31)**—2023-05-08  
  Python CLI utility and library for manipulating SQLite databases

#### TIL this week

* [Running Python code in a Pyodide sandbox via Deno](https://til.simonwillison.net/deno/pyodide-sandbox)—2023-05-10
