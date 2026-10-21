# Last weeknotes of 2023

Source: https://simonwillison.net/2023/Dec/31/weeknotes/

## Last weeknotes of 2023

31st December 2023

I’ve slowed down for that last week of the year. Here’s a wrap-up for everything else from the month of December.

#### datasette-plot

Alex Garcia released this new plugin for Datasette as part of our collaboration around Datasette Cloud. He introduced it on the Datasette Cloud blog: [datasette-plot—a new Datasette Plugin for building data visualizations](https://www.datasette.cloud/blog/2023/datasette-plot/).

#### On the blog

* [Recommendations to help mitigate prompt injection: limit the blast radius](https://simonwillison.net/2023/Dec/20/mitigate-prompt-injection/), extracted from a podcast episode I recorded with Kate Holterhoff for RedMonk Conversations.
* [Many options for running Mistral models in your terminal using LLM](https://simonwillison.net/2023/Dec/18/mistral/), demonstrating how LLM’s plugins system has really started to pay off.
* [The AI trust crisis](https://simonwillison.net/2023/Dec/14/ai-trust-crisis/) talking about how Dropbox learned the hard way that people are *extremely* sensitive to any uncertainty about whether or not their data is being used to train a model.

#### Releases

Most of these are minor bug fixes. A few of the more interesting highlights:

* [Django SQL Dashboard](https://django-sql-dashboard.datasette.io/) now [provides a read-only JSON API](https://django-sql-dashboard.datasette.io/en/stable/saved-dashboards.html#json-export) for saved dashboards. This makes it really easy to spin up a quick ad-hoc AI for data in a Django PostgreSQL database.
* The [sqlite-utils-shell](https://github.com/simonw/sqlite-utils-shell) plugin now supports the `--load-extension` option—I added this to let it be used with [Steampipe extensions](https://til.simonwillison.net/sqlite/steampipe).
* My [ospeak](https://github.com/simonw/ospeak) tool for running text-to-speech on the command-line now supports `-m tts-1-hd` for higher quality output, thanks to a [PR](https://github.com/simonw/ospeak/pull/5) from Mikolaj Holysz.
* [llm-llama-cpp](https://github.com/simonw/llm-llama-cpp) now supports a `llm -m gguf -o path una-cybertron-7b-v2-bf16.Q8_0.gguf` option, making it much easier to quickly try out a new model distributed as a GGUF file.

Here’s the full list of releases:

* **[datasette-haversine 0.2.1](https://github.com/simonw/datasette-haversine/releases/tag/0.2.1)**—2023-12-29  
  Datasette plugin that adds a custom SQL function for haversine distances
* **[datasette 0.64.6](https://github.com/simonw/datasette/releases/tag/0.64.6)**—2023-12-22  
  An open source multi-tool for exploring and publishing data
* **[sqlite-utils-shell 0.3](https://github.com/simonw/sqlite-utils-shell/releases/tag/0.3)**—2023-12-21  
  Interactive shell for sqlite-utils
* **[django-sql-dashboard 1.2](https://github.com/simonw/django-sql-dashboard/releases/tag/1.2)**—2023-12-16  
  Django app for building dashboards using raw SQL queries
* **[llm-mistral 0.2](https://github.com/simonw/llm-mistral/releases/tag/0.2)**—2023-12-15  
  LLM plugin providing access to Mistral models busing the Mistral API
* **[datasette-sqlite-authorizer 0.1](https://github.com/datasette/datasette-sqlite-authorizer/releases/tag/0.1)**—2023-12-14  
  Configure Datasette to block operations using the SQLIte set\_authorizer mechanism
* **[llm-anyscale-endpoints 0.4](https://github.com/simonw/llm-anyscale-endpoints/releases/tag/0.4)**—2023-12-14  
  LLM plugin for models hosted by Anyscale Endpoints
* **[llm-gemini 0.1a0](https://github.com/simonw/llm-gemini/releases/tag/0.1a0)**—2023-12-13  
  LLM plugin to access Google’s Gemini family of models
* **[ospeak 0.3](https://github.com/simonw/ospeak/releases/tag/0.3)**—2023-12-13  
  CLI tool for running text through OpenAI Text to speech
* **[github-to-sqlite 2.9](https://github.com/dogsheep/github-to-sqlite/releases/tag/2.9)**—2023-12-10  
  Save data from GitHub to a SQLite database
* **[llm-llama-cpp 0.3](https://github.com/simonw/llm-llama-cpp/releases/tag/0.3)**—2023-12-09  
  LLM plugin for running models using llama.cpp
* **[datasette-chronicle 0.2.1](https://github.com/datasette/datasette-chronicle/releases/tag/0.2.1)**—2023-12-08  
  Enable sqlite-chronicle against tables in Datasette

#### TILs

* [Running Steampipe extensions in sqlite-utils and Datasette](https://til.simonwillison.net/sqlite/steampipe)—2023-12-21
* [Editing an iPhone home screen using macOS](https://til.simonwillison.net/macos/edit-ios-home-screen)—2023-12-12
