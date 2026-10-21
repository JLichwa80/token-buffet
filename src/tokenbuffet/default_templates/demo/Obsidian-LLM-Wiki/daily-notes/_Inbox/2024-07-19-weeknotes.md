# Weeknotes: GPT-4o mini, LLM 0.15, sqlite-utils 3.37 and building a staging environment

Source: https://simonwillison.net/2024/Jul/19/weeknotes/

## Weeknotes: GPT-4o mini, LLM 0.15, sqlite-utils 3.37 and building a staging environment

19th July 2024

Upgrades to [LLM](https://llm.datasette.io/) to support the latest models, and a whole bunch of invisible work building out a staging environment for Datasette Cloud.

#### GPT-4o mini and LLM 0.15

Today’s big news was the release of [GPT-4o mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/), which I [wrote about here](https://simonwillison.net/2024/Jul/18/gpt-4o-mini/). If you build applications on top of LLMs this is a very significant release—it’s the cheapest of the high performing hosted models (cheaper even than Claude 3 Haiku and Gemini 1.5 Flash) and has some notable characteristics, most importantly the 16,000 token output limit.

I shipped a [new LLM release](https://simonwillison.net/2024/Jul/18/llm-015/) to support the new model. Full release notes for [LLM 0.15](https://llm.datasette.io/en/stable/changelog.html#v0-15):

> * Support for OpenAI’s [new GPT-4o mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/) model: `llm -m gpt-4o-mini 'rave about pelicans in French'` [#536](https://github.com/simonw/llm/issues/536)
> * `gpt-4o-mini` is now the default model if you do not [specify your own default](https://llm.datasette.io/en/stable/setup.html#setting-a-custom-default-model), replacing GPT-3.5 Turbo. GPT-4o mini is both cheaper and better than GPT-3.5 Turbo.
> * Fixed a bug where `llm logs -q 'flourish' -m haiku` could not combine both the `-q` search query and the `-m` model specifier. [#515](https://github.com/simonw/llm/issues/515)

#### sqlite-utils 3.37

LLM had a frustrating bug involving [a weird numpy issue](https://github.com/simonw/llm/issues/531) that only manifested on LLM when installed via Homebrew. I ended up fixing that in its `sqlite-utils` dependency—here are the full release notes for [sqlite-utils 3.37](https://sqlite-utils.datasette.io/en/stable/changelog.html#v3-37):

> * The `create-table` and `insert-files` commands all now accept multiple `--pk` options for compound primary keys. ([#620](https://github.com/simonw/sqlite-utils/issues/620))
> * Now tested against Python 3.13 pre-release. ([#619](https://github.com/simonw/sqlite-utils/pull/619))
> * Fixed a crash that can occur in environments with a broken `numpy` installation, producing a `module 'numpy' has no attribute 'int8'`. ([#632](https://github.com/simonw/sqlite-utils/issues/632))

#### Datasette Cloud staging environment

I’m a big believer in reducing the friction involved in making changes to code. The main reason I’m so keen on the combination of automated tests, GitHub Actions for CI/CD and extensive documentation (as described in [Coping strategies for the serial project hoarder](https://simonwillison.net/2022/Nov/26/productivity/)) is that

Sadly, [Datasette Cloud](https://www.datasette.cloud/) hasn’t been living up these standards as much as I would like. I have great comprehensive tests for it, continuous deployment that deploys when those tests pass and pretty solid internal documentation (mainly spread out across dozens of GitHub Issues)—but the thing I’ve been missing is a solid staging environment.

This matters because a lot of the most complex code in Datasette Cloud involves deploying new instances of Datasette to [Fly Machines](https://fly.io/docs/machines/). The thing that’s been missing is a separate environment where I can exercise my Fly deployment code independently of the production cluster.

I’ve been working towards this over the past week, and in doing so have found all sorts of pieces of the codebase that are hard-coded in a way that needs to be unwrapped to correctly support that alternative environment.

I’m getting there, but it’s been one of those frustrating projects where every step forward uncovers at least one more tiny problem that needs to be resolved.

A lot of these problems relate to the GitHub Actions workflows being used to build, test and deploy my containers. Thankfully Claude 3.5 Sonnet is great at helping refactor GitHub Actions YAML, which has been saving me a lot of time.

I’m really looking forward to wrapping this up, because I plan to celebrate by shipping a flurry of Datasette Cloud features that have been held up by the lack of a robust way to extensively test them before sending them out into the world.

#### Blog entries

* [Imitation Intelligence, my keynote for PyCon US 2024](https://simonwillison.net/2024/Jul/14/pycon/)
* [Give people something to link to so they can talk about your features and ideas](https://simonwillison.net/2024/Jul/13/give-people-something-to-link-to/)

I also updated my [write-up of my recent AI World’s Fair keynote](https://simonwillison.net/2024/Jun/27/ai-worlds-fair/) to include a link to the standalone YouTube video of the talk.

#### Releases

* **[llm 0.15](https://github.com/simonw/llm/releases/tag/0.15)**—2024-07-18  
  Access large language models from the command-line
* **[sqlite-utils 3.37](https://github.com/simonw/sqlite-utils/releases/tag/3.37)**—2024-07-18  
  Python CLI utility and library for manipulating SQLite databases
* **[llm-mistral 0.4](https://github.com/simonw/llm-mistral/releases/tag/0.4)**—2024-07-16  
  LLM plugin providing access to Mistral models using the Mistral API
* **[datasette-python 0.1](https://github.com/datasette/datasette-python/releases/tag/0.1)**—2024-07-12  
  Run a Python interpreter in the Datasette virtual environment

#### TILs

* [Trying out free-threaded Python on macOS](https://til.simonwillison.net/python/trying-free-threaded-python)—2024-07-13
* [Accessing 1Password items from the terminal](https://til.simonwillison.net/macos/1password-terminal)—2024-07-10
