# Weeknotes: Miscellaneous research into Rye, ChatGPT Code Interpreter and openai-to-sqlite

Source: https://simonwillison.net/2023/May/1/weeknotes/

## Weeknotes: Miscellaneous research into Rye, ChatGPT Code Interpreter and openai-to-sqlite

1st May 2023

I gave myself some time off stressing about my core responsibilities this week after PyCon, which meant allowing myself to be distracted by some miscellaneous research projects.

#### Rye

[Rye](https://github.com/mitsuhiko/rye) is a new experimental twist on Python packaging from Armin Ronacher. He’s been quite apologetic about it, asking [Should Rye Exist?](https://github.com/mitsuhiko/rye/discussions/6)—Python packaging is a crowded space right now!

Personally, I think a working prototype of an interesting idea is always worthwhile. My experience is that running code increases the quality of the discussion around an idea enormously, because it gives people something concrete to talk about.

Rye has some *really* interesting ideas. By far my favourite is how it bundles Python itself: it doesn’t depend on a system Python, instead downloading a standalone Python build from the [python-build-standalone](https://github.com/indygreg/python-build-standalone) project and stashing it away in a `~/.rye` directory.

I love this. Getting Python running on a system is often way harder than it should be. Rye provides a single binary (written in Rust) which can bootstrap a working Python environment, without interfering with the system Python or any other Python environments that might already be installed.

I wrote up [a few notes on Rye](https://til.simonwillison.net/python/rye) in a TIL earlier this week, mainly detailing how it works and where it puts things.

I also released [Datasette 0.64.3](https://github.com/simonw/datasette/releases/tag/0.64.3) with a [tiny fix](https://github.com/simonw/datasette/issues/2065) to ensure it would install cleanly using `rye install datasette`.

#### ChatGPT Code Interpreter

I’ve been having a whole lot of fun exploring this. I wrote about how [I’ve been using it to run micro-benchmarks](https://simonwillison.net/2023/Apr/12/code-interpreter/) a few weeks ago—today I [figured out a pattern](https://til.simonwillison.net/llms/code-interpreter-expansions) for installing additional Python packages (despite its lack of an internet connection) and even uploading binaries for Deno and Lua to grant it the ability to run code in other languages!

I think it’s the most interesting thing in all of ChatGPT/LLM world at the moment, which is a big statement.

#### openai-to-sqlite

Inspired by a Datasette [Office Hours](https://simonwillison.net/2021/Feb/19/office-hours/) conversation on Friday I decided to see if I could figure out a way to run simple sentiment analysis against data in a SQLite database using any of my various tools.

I ended up adding a new mechanism to my `openai-to-sqlite` CLI tool—it can now execute SQL queries that can update existing tables with the results of a `chatgpt()` API call using a custom SQL function.

I wrote more about that in [Enriching data with GPT3.5 and SQLite SQL functions](https://simonwillison.net/2023/Apr/29/enriching-data/).

#### Upgraded social media cards for my TILs

My [Today I Learned](https://til.simonwillison.net/) site has had social media cards—images that show up in link previews when URLs are shared—for a long time now. Since few of my TILs have images of their own it generates these as screenshots of the pages themselves.

Until recently it stored these images as PNG files directly in the SQLite database itself. Vercel has a 50MB size limit on deployments and the other day the screenshots finally tipped the database over that limit.

To fix it, I moved the images out of the SQLite database and put them in an S3 bucket instead. This also meant I could increase their size and resolution—they are now generated with the [shot-scraper](https://shot-scraper.datasette.io/) `--retina` option which doubles their size to 1600x800 pixels.

This ended up being a fun exercise in combining both `shot-scraper` and my [s3-credentials](https://s3-credentials.readthedocs.io/) CLI tools. I wrote up full details of how the new screenshot system works in a new TIL, [Social media cards generated with shot-scraper](https://til.simonwillison.net/shot-scraper/social-media-cards).

#### Next week: a webinar on Prompt Injection

My other blog entry this week introduced [The Dual LLM pattern for building AI assistants that can resist prompt injection](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)—my latest thinking on how we might be able to build AI assistants even without a robust solution to the prompt injection problem.

I have a speaking engagement lined up for next week: the [LangChain Prompt Injection Webinar](https://www.crowdcast.io/c/ht7qt3rvesvg).

I’ll be discussing [prompt injection attacks](https://simonwillison.net/series/prompt-injection/) against LLMs on a panel with Willem Pienaar, Kojin Oshiba and Jonathan Cohen and Christopher Parisien from NVIDIA.

I think it will be an interesting conversation. I’m going to reiterate my argument that [You can’t solve AI security problems with more AI](https://simonwillison.net/2022/Sep/17/prompt-injection-more-ai/)—a position that I’m not sure is shared by the other members of the panel!

#### Entries this week

* [Enriching data with GPT3.5 and SQLite SQL functions](https://simonwillison.net/2023/Apr/29/enriching-data/)
* [The Dual LLM pattern for building AI assistants that can resist prompt injection](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)

#### Releases this week

* **[s3-credentials 0.15](https://github.com/simonw/s3-credentials/releases/tag/0.15)**—2023-04-30  
  A tool for creating credentials for accessing S3 buckets
* **[openai-to-sqlite 0.3](https://github.com/simonw/openai-to-sqlite/releases/tag/0.3)**—2023-04-29  
  Save OpenAI API results to a SQLite database
* **[datasette 0.64.3](https://github.com/simonw/datasette/releases/tag/0.64.3)**—2023-04-27  
  An open source multi-tool for exploring and publishing data
* **[shot-scraper 1.2](https://github.com/simonw/shot-scraper/releases/tag/1.2)**—2023-04-27  
  A command-line utility for taking automated screenshots of websites
* **[datasette-explain 0.1a2](https://github.com/simonw/datasette-explain/releases/tag/0.1a2)**—2023-04-24  
  Explain and validate SQL queries as you type them into Datasette

#### TIL this week

* [Expanding ChatGPT Code Interpreter with Python packages, Deno and Lua](https://til.simonwillison.net/llms/code-interpreter-expansions)—2023-05-01
* [Social media cards generated with shot-scraper](https://til.simonwillison.net/shot-scraper/social-media-cards)—2023-04-30
* [Deno KV](https://til.simonwillison.net/deno/deno-kv)—2023-04-28
* [The location of the pip cache directory](https://til.simonwillison.net/python/pip-cache)—2023-04-28
* [A few notes on Rye](https://til.simonwillison.net/python/rye)—2023-04-27
