# Weeknotes: symbex, LLM prompt templates, a bit of a break

Source: https://simonwillison.net/2023/Jun/27/weeknotes/

## Weeknotes: symbex, LLM prompt templates, a bit of a break

27th June 2023

I had a holiday to the UK for a family wedding anniversary and mostly took the time off... except for building **symbex**, which became one of those projects that kept on inspiring new features.

I’ve also been working on some major improvements to my [LLM](https://llm.datasette.io/) tool for working with language models from the command-line.

#### symbex

I introduced [symbex](https://github.com/simonw/symbex) in [symbex: search Python code for functions and classes, then pipe them into a LLM](https://simonwillison.net/2023/Jun/18/symbex/). It’s since grown a bunch more features across [12 total releases](https://github.com/simonw/symbex/releases).

`symbex` is a tool for searching Python code. The initial goal was to make it quick to find and output the body of a specific Python function or class, such that you could then pipe it to [LLM](https://llm.datasette.io/) to process it with GPT-3.5 or GPT-4:

```
symbex find_symbol_nodes \
  | llm -m gpt4 --system 'Describe this code succinctly'
```

Output:

> This code defines a function `find_symbol_nodes` that takes in three arguments: code (string), filename (string), and symbols (iterable of strings). The function parses the given code and searches for AST nodes (Class, Function, AsyncFunction) that match the provided symbols. It returns a list of tuple pairs containing matched nodes and their corresponding class names or None.

When piping to a language model token count is really important—the goal is to provide the shortest amount of text that gives the model enough to produce interesting results.

So... I added a `-s/--signatures` option which returns just the function or class signature:

```
symbex find_symbol_nodes -s
```

Output:

```
# File: symbex/lib.py Line: 13
def find_symbol_nodes(code: str, filename: str, symbols: Iterable[str]) -> List[Tuple[(AST, Optional[str])]]
```

Add `--docstrings` to include the docstring. Add `-i/--imports` for an import line, and `-n/--no-file` to suppress that `# File` comment—so `-in` combines both of hose options:

```
symbex find_symbol_nodes -s --docstrings -in
```

```
# from symbex.lib import find_symbol_nodes
def find_symbol_nodes(code: str, filename: str, symbols: Iterable[str]) -> List[Tuple[(AST, Optional[str])]]
    "Returns ast Nodes matching symbols"
```

Being able to see type annotations and docstrings tells you a lot about the code. This gave me an idea for an extra set of features: filters that could be used to only return symbols that were documented, or undocumented, or included or were missing type signatures:

* `--async`: Filter async functions
* `--function`: Filter functions
* `--class`: Filter classes
* `--documented`: Filter functions with docstrings
* `--undocumented`: Filter functions without docstrings
* `--typed`: Filter functions with type annotations
* `--untyped`: Filter functions without type annotations
* `--partially-typed`: Filter functions with partial type annotations
* `--fully-typed`: Filter functions with full type annotations

So now you can use `symbex` to get a feel for how well typed or documented your code is:

```
# See all symbols lacking a docstring:
symbex -s --undocumented

# All functions that are missing type annotations:
symbex -s --function --untyped
```

The [README](https://github.com/simonw/symbex/blob/main/README.md) has comprehensive documentation on everything else the tool can do.

#### LLM prompt templates

My [LLM](https://llm.datasette.io/) tool is shaping up in some interesting directions as well.

The big new released feature is [prompt templates](https://llm.datasette.io/en/stable/templates.html).

A template is a file that looks like this:

```
system: Summarize this text in the voice of $voice
model: gpt-4
```

This can be installed using `llm templates edit summary`, which opens a text editor (using the `$EDITOR` environment variable).

Once installed, you can use it like this:

```
curl -s 'https://til.simonwillison.net/macos/imovie-slides-and-audio' | \
  strip-tags -m | \
  llm -t summarize -p voice 'Extremely sarcastic GlaDOS'
```

> Oh, *bravo*, Simon. You’ve really outdone yourself. Apparently, the highlight of his day was turning an old talk into a video using iMovie. After a truly heart-stopping struggle with the Ken Burns effect, he finally, and I mean *finally*, tuned the slide duration to match the audio. And then, hold your applause, he met the enormous challenge of publishing it on YouTube. We were all waiting with bated breath. Oh, but wouldn’t it be exciting to note that his estimated 1.03GB video was actually a shockingly smaller size? I can’t contain my excitement. He also used Pixelmator for a custom title slide, as YouTube prefers a size of 1280x720px—ground-breaking information, truly.

The idea here is to make it easy to create reusable template snippets, for all sorts of purposes. `git diff | llm -t diff` could generate a commit message, `cat file.py | llm -t explain` could explain code etc.

#### LLM plugins

These are still baking, but this is the feature I’m most excited about. I’m adding plugins to LLM, inspired by [plugins in Datasette](https://docs.datasette.io/en/stable/plugins.html).

I’m planning the following categories of plugins to start with:

* **Command plugins**. These will allow extra commands to be added to the `llm` tool—`llm search` or `llm embed` or similar.
* **Template plugins**. Imagine being able to install extra prompt templates using `llm install name-of-package`.
* **Model plugins**. I want LLM to be able to use more than just GPT-3.5 and GPT-4. I have a branch with [an example plugin](https://github.com/simonw/llm/blob/ce2a322126f98a2702077eb06d0b57c8a8414d42/llm/vertex_models.py) that can call Google’s PaLM 2 model via [Google Vertex](https://cloud.google.com/vertex-ai), and I hope to support many other LLM families with additional plugins, including models that can run locally via [llama.cpp](https://github.com/ggerganov/llama.cpp) and similar.
* **Function plugins**. Once I get the new OpenAI functions mechanism working, I’d like to be able to install plugins that make new functions available to be executed by the LLM!

All of this is under active development at the moment. I’ll write more about it once I get it working.

#### Entries these weeks

* [symbex: search Python code for functions and classes, then pipe them into a LLM](https://simonwillison.net/2023/Jun/18/symbex/)
* [Understanding GPT tokenizers](https://simonwillison.net/2023/Jun/8/gpt-tokenizers/)

#### Releases these weeks

* **[sqlite-utils 3.33](https://github.com/simonw/sqlite-utils/releases/tag/3.33)**—2023-06-26  
  Python CLI utility and library for manipulating SQLite databases
* **[datasette-render-images 0.4](https://github.com/simonw/datasette-render-images/releases/tag/0.4)**—2023-06-14  
  Datasette plugin that renders binary blob images using data-uris

#### TIL these weeks

* [TOML in Python](https://til.simonwillison.net/python/toml)—2023-06-26
* [Automatically maintaining Homebrew formulas using GitHub Actions](https://til.simonwillison.net/homebrew/auto-formulas-github-actions)—2023-06-21
* [Using ChatGPT Browse to name a Python package](https://til.simonwillison.net/gpt3/picking-python-project-name-chatgpt)—2023-06-18
* [Syncing slide images and audio in iMovie](https://til.simonwillison.net/macos/imovie-slides-and-audio)—2023-06-15
* [Using fs\_usage to see what files a process is using](https://til.simonwillison.net/macos/fs-usage)—2023-06-15
* [Running OpenAI’s large context models using llm](https://til.simonwillison.net/llms/larger-context-openai-models-llm)—2023-06-13
* [Consecutive groups in SQL using window functions](https://til.simonwillison.net/sql/consecutive-groups)—2023-06-08
