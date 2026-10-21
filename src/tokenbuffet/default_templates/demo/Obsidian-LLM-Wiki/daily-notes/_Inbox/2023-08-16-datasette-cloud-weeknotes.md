# Datasette Cloud, Datasette 1.0a3, llm-mlc and more

Source: https://simonwillison.net/2023/Aug/16/datasette-cloud-weeknotes/

## Datasette Cloud, Datasette 1.0a3, llm-mlc and more

16th August 2023

Datasette Cloud is now a significant step closer to general availability. The Datasette 1.03 alpha release is out, with a mostly finalized JSON format for 1.0. Plus new plugins for LLM and sqlite-utils and a flurry of things I’ve learned.

#### Datasette Cloud

Yesterday morning we unveiled the new [Datasette Cloud blog](https://www.datasette.cloud/blog/), and kicked things off there with two posts:

* [Welcome to Datasette Cloud](https://www.datasette.cloud/blog/2023/welcome/) provides an introduction to the product: what it can do so far, what’s coming next and how to sign up to try it out.
* [Introducing datasette-write-ui: a Datasette plugin for editing, inserting, and deleting rows](https://www.datasette.cloud/blog/2023/datasette-write-ui/) introduces a brand new plugin, [datasette-write-ui](https://datasette.io/plugins/datasette-write-ui)—which finally adds a user interface for editing, inserting and deleting rows to Datasette.

Here’s a screenshot of the interface for creating a new private space in Datasette Cloud:

![Create a space A space is a private area where you can import, explore and analyze data and share it with invited collaborators. Space name Subdomain Region  .datasette.cloud  Your data will be hosted in a region. Pick somewhere geographically close to you for optimal performance.](https://static.simonwillison.net/static/2023/pick-region.jpg)

`datasette-write-ui` is particularly notable because it was written by Alex Garcia, who is now working with me to help get Datasette Cloud ready for general availability.

Alex’s work on the project is being supported by [Fly.io](https://fly.io/), in a particularly exciting form of open source sponsorship. Datasette Cloud is already being built on Fly, but as part of Alex’s work we’ll be extensively documenting what we learn along the way about using Fly to build a multi-tenant SaaS platform.

Alex has some very cool work with Fly’s [Litestream](https://litestream.io/) in the pipeline which we hope to talk more about shortly.

Since this is my first time building a blog from scratch in quite a while, I also put together a new TIL on [Building a blog in Django](https://til.simonwillison.net/django/building-a-blog-in-django).

The Datasette Cloud work has been driving a lot of improvements to other parts of the Datasette ecosystem, including improvements to [datasette-upload-dbs](https://datasette.io/plugins/datasette-upload-dbs) and the other big news this week: Datasette 1.0a3.

#### Datasette 1.0a3

Datasette 1.0 is the first version of Datasette that will be marked as “stable”: if you build software on top of Datasette I want to guarantee as much as possible that it won’t break until Datasette 2.0, which I hope to avoid ever needing to release.

The three big aspects of this are:

* A stable [plugins interface](https://docs.datasette.io/en/1.0a3/plugin_hooks.html), so custom plugins continue to work
* A stable [JSON API format](https://docs.datasette.io/en/1.0a3/json_api.html), for integrations built against Datasette
* Stable template contexts, so that [custom templates](https://docs.datasette.io/en/1.0a3/custom_templates.html) won’t be broken by minor changes

The [1.0 alpha 3 release](https://docs.datasette.io/en/1.0a3/changelog.html#a3-2023-08-09) primarily focuses on the JSON support. There’s a new, much more intuitive default shape for both the table and the arbitrary query pages, which looks like this:

```
{
  "ok": true,
  "rows": [
    {
      "id": 3,
      "name": "Detroit"
    },
    {
      "id": 2,
      "name": "Los Angeles"
    },
    {
      "id": 4,
      "name": "Memnonia"
    },
    {
      "id": 1,
      "name": "San Francisco"
    }
  ],
  "truncated": false
}
```

This is a huge improvement on the old format, which featured a vibrant mess of top-level keys and served the rows up as an array-of-arrays, leaving the user to figure out which column was which by matching against `"columns"`.

The new format is [documented here](https://docs.datasette.io/en/1.0a3/json_api.html#json-api-default). I wanted to get this in place as soon as possible for Datasette Cloud (which is running this alpha), since I don’t want to risk paying customers building integrations that would later break due to 1.0 API changes.

#### llm-mlc

My [LLM](https://llm.datasette.io/) tool provides a CLI utility and Python library for running prompts through Large Language Models. I [added plugin support](https://simonwillison.net/2023/Jul/12/llm/) to it a few weeks ago, so now it can support additional models through plugins—including a variety of models that can run directly on your own device.

For a while now I’ve been trying to work out the easiest recipe to get a Llama 2 model running on my M2 Mac with GPU acceleration.

I finally figured that out the other week, using the excellent [MLC Python library](https://mlc.ai/mlc-llm/docs/deploy/python.html).

I built a new plugin for LLM called [llm-mlc](https://github.com/simonw/llm-mlc). I think this may now be one of the easiest ways to run Llama 2 on an Apple Silicon Mac with GPU acceleration.

Here are the steps to try it out. First, install LLM—which is easiest with Homebrew:

```
brew install llm
```

If you have a Python 3 environment you can run `pip install llm` or `pipx install llm` instead.

Next, install the new plugin:

```
llm install llm-mlc
```

There’s an additional installation step which I’ve not yet been able to automate fully—on an M1/M2 Mac run the following:

```
llm mlc pip install --pre --force-reinstall \
  mlc-ai-nightly \
  mlc-chat-nightly \
  -f https://mlc.ai/wheels
```

Instructions for other platforms [can be found here](https://mlc.ai/package/).

Now run this command to finish the setup (which configures `git-lfs` ready to download the models):

```
llm mlc setup
```

And finally, you can download the Llama 2 model using this command:

```
llm mlc download-model Llama-2-7b-chat --alias llama2
```

And run a prompt like this:

```
llm -m llama2 'five names for a cute pet ferret'
```

It’s still more steps than I’d like, but it seems to be working for people!

As always, my goal for LLM is to grow a community of enthusiasts who write plugins like this to help support new models as they are released. That’s why I put a lot of effort into building this tutorial about [Writing a plugin to support a new model](https://llm.datasette.io/en/stable/plugins/tutorial-model-plugin.html).

Also out now: [llm 0.7](https://github.com/simonw/llm/releases/tag/0.7), which mainly adds a new mechanism for adding custom aliases to existing models:

```
llm aliases set turbo gpt-3.5-turbo-16k
llm -m turbo 'An epic Greek-style saga about a cheesecake that builds a SQL database from scratch'
```

#### openai-to-sqlite and embeddings for related content

A smaller release this week: [openai-to-sqlite 0.4](https://github.com/simonw/openai-to-sqlite/releases/tag/0.4), an update to my CLI tool for loading data from various OpenAI APIs into a SQLite database.

My inspiration for this release was a desire to add better related content to my [TIL website](https://til.simonwillison.net/).

Short version: I did exactly that! Each post on that site now includes a list of related posts that are generated using OpenAI embeddings, which help me plot posts that are semantically similar to each other.

I wrote up a full TIL about how that all works: [Storing and serving related documents with openai-to-sqlite and embeddings](https://til.simonwillison.net/llms/openai-embeddings-related-content)—scroll to the bottom of that post to see the new related content in action.

I’m fascinated by embeddings. They’re not difficult to run using locally hosted models either—I hope to add a feature to LLM to help with that soon.

[Getting creative with embeddings](https://wattenberger.com/thoughts/yay-embeddings-math) by Amelia Wattenberger is a great example of some of the more interesting applications they can be put to.

#### sqlite-utils-jq

A tiny new plugin for [sqlite-utils](https://sqlite-utils.datasette.io/), inspired by [this Hacker News comment](https://news.ycombinator.com/item?id=37083501) and written mainly as an excuse for me to exercise that [new plugins framework](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/) a little more.

[sqlite-utils-jq](https://github.com/simonw/sqlite-utils-jq) adds a new `jq()` function which can be used to execute [jq](https://jqlang.github.io/jq/) programs as part of a SQL query.

Install it like this:

```
sqlite-utils install sqlite-utils-jq
```

Now you can do things like this:

```
sqlite-utils memory "select jq(:doc, :expr) as result" \
  -p doc '{"foo": "bar"}' \
  -p expr '.foo'
```

You can also use it in combination with [sqlite-utils-litecli](https://github.com/simonw/sqlite-utils-litecli) to run that new function as part of an interactive shell:

```
sqlite-utils install sqlite-utils-litecli
sqlite-utils litecli data.db
# ...
Version: 1.9.0
Mail: https://groups.google.com/forum/#!forum/litecli-users
GitHub: https://github.com/dbcli/litecli
data.db> select jq('{"foo": "bar"}', '.foo')
+------------------------------+
| jq('{"foo": "bar"}', '.foo') |
+------------------------------+
| "bar"                        |
+------------------------------+
1 row in set
Time: 0.031s
```

#### Other entries this week

[How I make annotated presentations](https://simonwillison.net/2023/Aug/6/annotated-presentations/) describes the process I now use to create annotated presentations like this one for [Catching up on the weird world of LLMs](https://simonwillison.net/2023/Aug/3/weird-world-of-llms/) (now up to over 17,000 views [on YouTube](https://www.youtube.com/watch?v=h8Jth_ijZyY)!) using a new custom annotation tool I put together with the help of GPT-4.

A couple of highlights from my TILs:

* [Catching up with the Cosmopolitan ecosystem](https://til.simonwillison.net/cosmopolitan/ecosystem) describes my latest explorations of Cosmopolitan and Actually Portable Executable, based on an update I heard from Justine Tunney.
* [Running a Django and PostgreSQL development environment in GitHub Codespaces](https://til.simonwillison.net/github/django-postgresql-codespaces) shares what I’ve learned about successfully running a Django and PostgreSQL development environment entirely through the browser using Codespaces.

#### Releases this week

* **[openai-to-sqlite 0.4](https://github.com/simonw/openai-to-sqlite/releases/tag/0.4)**—2023-08-15  
  Save OpenAI API results to a SQLite database
* **[llm-mlc 0.5](https://github.com/simonw/llm-mlc/releases/tag/0.5)**—2023-08-15  
  LLM plugin for running models using MLC
* **[datasette-render-markdown 2.2.1](https://github.com/simonw/datasette-render-markdown/releases/tag/2.2.1)**—2023-08-15  
  Datasette plugin for rendering Markdown
* **[db-build 0.1](https://github.com/simonw/db-build/releases/tag/0.1)**—2023-08-15  
  Tools for building SQLite databases from files and directories
* **[paginate-json 0.3.1](https://github.com/simonw/paginate-json/releases/tag/0.3.1)**—2023-08-12  
  Command-line tool for fetching JSON from paginated APIs
* **[llm 0.7](https://github.com/simonw/llm/releases/tag/0.7)**—2023-08-12  
  Access large language models from the command-line
* **[sqlite-utils-jq 0.1](https://github.com/simonw/sqlite-utils-jq/releases/tag/0.1)**—2023-08-11  
  Plugin adding a jq() SQL function to sqlite-utils
* **[datasette-upload-dbs 0.3](https://github.com/simonw/datasette-upload-dbs/releases/tag/0.3)**—2023-08-10  
  Upload SQLite database files to Datasette
* **[datasette 1.0a3](https://github.com/simonw/datasette/releases/tag/1.0a3)**—2023-08-09  
  An open source multi-tool for exploring and publishing data

#### TIL this week

* [Processing a stream of chunks of JSON with ijson](https://til.simonwillison.net/json/ijson-stream)—2023-08-16
* [Building a blog in Django](https://til.simonwillison.net/django/building-a-blog-in-django)—2023-08-15
* [Storing and serving related documents with openai-to-sqlite and embeddings](https://til.simonwillison.net/llms/openai-embeddings-related-content)—2023-08-15
* [Combined release notes from GitHub with jq and paginate-json](https://til.simonwillison.net/jq/combined-github-release-notes)—2023-08-12
* [Catching up with the Cosmopolitan ecosystem](https://til.simonwillison.net/cosmopolitan/ecosystem)—2023-08-10
* [Running a Django and PostgreSQL development environment in GitHub Codespaces](https://til.simonwillison.net/github/django-postgresql-codespaces)—2023-08-10
* [Scroll to text fragments](https://til.simonwillison.net/html/scroll-to-text)—2023-08-08
