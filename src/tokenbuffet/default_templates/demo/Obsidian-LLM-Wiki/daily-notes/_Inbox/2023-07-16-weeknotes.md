# Weeknotes: Self-hosted language models with LLM plugins, a new Datasette tutorial, a dozen package releases, a dozen TILs

Source: https://simonwillison.net/2023/Jul/16/weeknotes/

## Weeknotes: Self-hosted language models with LLM plugins, a new Datasette tutorial, a dozen package releases, a dozen TILs

16th July 2023

A lot of stuff to cover from the past two and a half weeks.

#### LLM and self-hosted language model plugins

My biggest project was the [new version of my LLM tool for interacting with Large Language Models](https://simonwillison.net/2023/Jul/12/llm/). LLM now accepts plugins for adding alternative language models to the tool, meaning it’s now applicable to more than just the OpenAI collection.

I figured out quite a few of the details of this while offline on a camping trip up in the Northern California redwoods, which forced the issue on figuring out how to work with LLMs that I could host on my own computer because I didn’t have a connection to access the OpenAI APIs.

Comprehensive documentation is sorely lacking in the world of generative AI. I’ve decided to push back against that for LLM, so I spent a bunch of time working on an extremely comprehensive tutorial for writing a plugin that adds a new language model to the tool:

* **[Writing a plugin to support a new model](https://llm.datasette.io/en/stable/plugins/tutorial-model-plugin.html)**

As part of researching this tutorial I finally figured out how to build a Python package using just a `pyproject.toml` file, with no `setup.py` or `setup.cfg` or anything else like that. I wrote that up in detail in [Python packages with pyproject.toml and nothing else](https://til.simonwillison.net/python/pyproject), and I’ve started using that pattern for all of my new Python packages.

LLM also now includes a Python API for interacting with models, which provides an abstraction that works the same for the OpenAI models and for other models (including self-hosted models) installed via plugins. Here’s [the documentation for that](https://llm.datasette.io/en/stable/python-api.html)—it ends up looking like this:

```
import llm

model = llm.get_model("gpt-3.5-turbo")
model.key = 'YOUR_API_KEY_HERE'
response = model.prompt("Five surprising names for a pet pelican")
for chunk in response:
    print(chunk, end="")
```

To use another model, just swap its name in for `gpt-3.5-turbo`. The self-hosted models provided by the [llm-gpt4all](https://github.com/simonw/llm-gpt4all) plugin work the same way:

```
pip install llm-gpt4all
```

Then:

```
import llm

model = llm.get_model("ggml-vicuna-7b-1")
response = model.prompt("Five surprising names for a pet pelican")
# You can do this instead of looping through the chunks:
print(response.text())
```

I’ve released three plugins so far:

* [llm-gpt4all](https://github.com/simonw/llm-gpt4all) with 17 self-hosted models from the [GPT4All](https://gpt4all.io/) project.
* [llm-palm](https://github.com/simonw/llm-palm) with Google’s [PaLM 2](https://blog.google/technology/ai/google-palm-2-ai-large-language-model/) language model, via their API.
* [llm-mpt30b](https://github.com/simonw/llm-mpt30b) providing the 19GB MPT-30B model, using [TheBloke/mpt-30B-GGML](https://huggingface.co/TheBloke/mpt-30B-GGML).

I’m looking forward to someone else [following the tutorial](https://llm.datasette.io/en/stable/plugins/tutorial-model-plugin.html) and releasing their own plugin!

#### A new tutorial: Data analysis with SQLite and Python

I presented this as a 2hr45m tutorial at PyCon a few months ago. The video is now available, and I like to try to turn these kinds of things into more permanent documentation.

The Datasette website has [a growing collection of tutorials](https://datasette.io/tutorials), and I decided to make that the final home for this one too.

[Data analysis with SQLite and Python](https://datasette.io/tutorials/data-analysis) now has the full 2hr45m video plus an improved version of the handout I used for the talk. The written material there there should also be valuable for people who don’t want to spend nearly three hours watching the video!

As part of putting that page together I solved a problem I’ve been wanting to figure out for a long time: I figured out a way to build a custom Jinja block tag that looks like this:

```
{% markdown %}
# This will be rendered as markdown

- Bulleted
- List
{% endmarkdown %}
```

I released that in [datasette-render-markdown 2.2](https://github.com/simonw/datasette-render-markdown/releases/tag/2.2). I also wrote up a TIL on [Custom Jinja template tags with attributes](https://til.simonwillison.net/jinja/custom-jinja-tags-with-attributes) describing the pattern I used.

One bonus feature for that tutorial: I decided to drop in a nested table of contents, automatically derived from the HTML headers on the page.

![ What you'll need python3 and pip Optional: GitHub Codespaces sqlite-utils Using the command-line tools to clean data Exploring data with Datasette Installing Datasette locally Try a database: legislators.db Install some plugins Learning SQL with Datasette Using sqlite-utils as a Python library, to import all the PEPs Enabling full-text search Publishing a database to Vercel Other publishing options Datasette Lite Loading SQLite, CSV and JSON data Installing plugins Further reading Advanced SQL Aggregations Subqueries CTEs JSON Window functions Baked Data Niche Museums and TILs Generating a newsletter with an Observable notebook More demos and further reading Fun demos SpatiaLite ](https://static.simonwillison.net/static/2023/toc.jpg)

I wrote the code for this entirely using the new ChatGPT Code Interpreter, which can write Python based on your description and, crucially, *execute it and see if it works*.

Here’s [my ChatGPT transcript](https://chat.openai.com/share/e41efb6d-eae7-454d-9aa2-5284683ba9f9) showing how I built the feature.

I’ve been using ChatGPT Code Interpreter for a few months now, and I’m completely hooked: I think it’s the most interesting thing in the whole AI space at the moment.

I participated in a [Code Interpreter Latent Space](https://www.latent.space/p/code-interpreter) episode to talk about it, which ended up drawing 17,000 listeners on Twitter Spaces and is now also available as a podcast episode, neatly edited together by swyx.

#### Symbex --check and --rexec

[Symbex](https://github.com/simonw/symbex) is my Python CLI tool for quickly finding Python functions and classes and outputting either the full code or just the signature of the matching symbol. I first [wrote about that here](https://simonwillison.net/2023/Jun/18/symbex/).

[symbex 1.1](https://github.com/simonw/symbex/releases/tag/1.1) adds two new features.

```
symbex --function --undocumented --check
```

This new `--check` mode is designed to run in Continuous Integration environments. If it finds any symbols matching the filters (in this case functions that are missing their docstring) it returns a non-zero exit code, which will fail the CI step.

It’s an imitation of `black . --check`—the idea is that Symbex can now be used to enforce code quality issues like docstrings and the presence of type annotations.

The other new feature is `--rexec`. This is an extension of the existing `--replace` feature, which lets you find a symbol in your code and replace its body with new code.

`--rexec` takes a shell expression. The body of the matching symbol will be piped into that command, and its output will be used as the replacement.

Which means you can do things like this:

```
symbex my_function \
  --rexec "llm --system 'add type hints and a docstring'"
```

This will find `def my_function()` and its body, pass that through `llm` (using the `gpt-3.5-turbo` default model, but you can specify `-m gpt-4` or any other model to use something else), and then take the output and update the file in-place with the new implementation.

As a demo, I ran it against this:

```
def my_function(a, b):
    return a + b + 3
```

And got back:

```
def my_function(a: int, b: int) -> int:
    """
    Returns the sum of two integers (a and b) plus 3.

    Parameters:
    a (int): The first integer.
    b (int): The second integer.

    Returns:
    int: The sum of a and b plus 3.
    """
    return a + b + 3
```

Obviously this is fraught with danger, and you should only run this against code that has already been committed to Git and hence can be easily recovered... but it’s a really fun trick!

#### ttok --encode --decode

`ttok` is my CLI tool for counting tokens, as used by LLM models such as GPT-4. [ttok 0.2](https://github.com/simonw/ttok/releases/tag/0.2) adds a requested feature to help make tokens easier to understand, best illustrated by this demo:

```
ttok Hello world
# Outputs 2 - the number of tokens
ttok Hello world --encode
# Outputs 9906 1917 - the encoded tokens
ttok 9906 1917 --decode
# Outputs Hello world - decoding the tokens back again
ttok Hello world --encode --tokens
# Outputs [b'Hello', b' world']
```

Being able to easily see the encoded tokens including whitespace (the `b' world'` part) is particularly useful for understanding how the tokens all fit together.

I wrote more about GPT tokenization in [understanding GPT tokenizers](https://simonwillison.net/2023/Jun/8/gpt-tokenizers/).

#### TIL this week

* [Using tree-sitter with Python](https://til.simonwillison.net/python/tree-sitter)—2023-07-14
* [Auto-formatting YAML files with yamlfmt](https://til.simonwillison.net/yaml/yamlfmt)—2023-07-13
* [Quickly testing code in a different Python version using pyenv](https://til.simonwillison.net/python/quick-testing-pyenv)—2023-07-10
* [Using git-filter-repo to set commit dates to author dates](https://til.simonwillison.net/git/git-filter-repo)—2023-07-10
* [Using OpenAI functions and their Python library for data extraction](https://til.simonwillison.net/gpt3/openai-python-functions-data-extraction)—2023-07-10
* [Python packages with pyproject.toml and nothing else](https://til.simonwillison.net/python/pyproject)—2023-07-08
* [Syntax highlighted code examples in Datasette](https://til.simonwillison.net/datasette/syntax-highlighted-code-examples)—2023-07-02
* [Custom Jinja template tags with attributes](https://til.simonwillison.net/jinja/custom-jinja-tags-with-attributes)—2023-07-02
* [Local wildcard DNS on macOS with dnsmasq](https://til.simonwillison.net/macos/wildcard-dns-dnsmasq)—2023-06-30
* [A Discord bot to expand issue links to a private GitHub repository](https://til.simonwillison.net/discord/discord-github-issues-bot)—2023-06-30
* [Bulk editing status in GitHub Projects](https://til.simonwillison.net/github/bulk-edit-github-projects)—2023-06-29
* [CLI tools hidden in the Python standard library](https://til.simonwillison.net/python/stdlib-cli-tools)—2023-06-29

#### Releases this week

* **[symbex 1.1](https://github.com/simonw/symbex/releases/tag/1.1)**—2023-07-16  
  Find the Python code for specified symbols
* **[llm-mpt30b 0.1](https://github.com/simonw/llm-mpt30b/releases/tag/0.1)**—2023-07-12  
  LLM plugin adding support for the MPT-30B language model
* **[llm-markov 0.1](https://github.com/simonw/llm-markov/releases/tag/0.1)**—2023-07-12  
  Plugin for LLM adding a Markov chain generating model
* **[llm-gpt4all 0.1](https://github.com/simonw/llm-gpt4all/releases/tag/0.1)**—2023-07-12  
  Plugin for LLM adding support for the GPT4All collection of models
* **[llm-palm 0.1](https://github.com/simonw/llm-palm/releases/tag/0.1)**—2023-07-12  
  Plugin for LLM adding support for Google’s PaLM 2 model
* **[llm 0.5](https://github.com/simonw/llm/releases/tag/0.5)**—2023-07-12  
  Access large language models from the command-line
* **[ttok 0.2](https://github.com/simonw/ttok/releases/tag/0.2)**—2023-07-10  
  Count and truncate text based on tokens
* **[strip-tags 0.5.1](https://github.com/simonw/strip-tags/releases/tag/0.5.1)**—2023-07-09  
  CLI tool for stripping tags from HTML
* **[pocket-to-sqlite 0.2.3](https://github.com/dogsheep/pocket-to-sqlite/releases/tag/0.2.3)**—2023-07-09  
  Create a SQLite database containing data from your Pocket account
* **[datasette-render-markdown 2.2](https://github.com/simonw/datasette-render-markdown/releases/tag/2.2)**—2023-07-02  
  Datasette plugin for rendering Markdown
* **[asgi-proxy-lib 0.1a0](https://github.com/simonw/asgi-proxy-lib/releases/tag/0.1a0)**—2023-07-01  
  An ASGI function for proxying to a backend over HTTP
* **[datasette-upload-csvs 0.8.3](https://github.com/simonw/datasette-upload-csvs/releases/tag/0.8.3)**—2023-06-28  
  Datasette plugin for uploading CSV files and converting them to database tables
