# Calling LLMs from client-side JavaScript, converting PDFs to HTML + weeknotes

Source: https://simonwillison.net/2024/Sep/6/weeknotes/

## Calling LLMs from client-side JavaScript, converting PDFs to HTML + weeknotes

6th September 2024

I’ve been having a bunch of fun taking advantage of CORS-enabled LLM APIs to build client-side JavaScript applications that access LLMs directly. I also span up a new Datasette plugin for advanced permission management.

* [LLMs from client-side JavaScript](https://simonwillison.net/2024/Sep/6/weeknotes/#llms-from-client-side-javascript)
* [Converting PDFs to HTML and Markdown](https://simonwillison.net/2024/Sep/6/weeknotes/#converting-pdfs-to-html-and-markdown)
* [Adding some class to Datasette forms](https://simonwillison.net/2024/Sep/6/weeknotes/#adding-some-class-to-datasette-forms)
* [On the blog](https://simonwillison.net/2024/Sep/6/weeknotes/#on-the-blog)
* [Releases](https://simonwillison.net/2024/Sep/6/weeknotes/#releases)
* [TILs](https://simonwillison.net/2024/Sep/6/weeknotes/#tils)

#### LLMs from client-side JavaScript

Anthropic [recently added CORS support](https://simonwillison.net/2024/Aug/23/anthropic-dangerous-direct-browser-access/) to their Claude APIs. It’s a little hard to use—you have to add `anthropic-dangerous-direct-browser-access: true` to your request headers to enable it—but once you know the trick you can start building web applications that talk to Anthropic’s LLMs directly, without any additional server-side code.

I later found out that both OpenAI and Google Gemini have this capability too, without needing the special header.

The problem with this approach is security: it’s very important not to embed an API key attached to your billing account in client-side HTML and JavaScript for anyone to see!

For my purposes though that doesn’t matter. I’ve been building tools which `prompt()` a user for their own API key (sadly restricting their usage to the tiny portion of people who both understand API keys and have created API accounts with one of the big providers)—then I stash that key in `localStorage` and start using it to make requests.

My [simonw/tools](https://github.com/simonw/tools) repository is home to a growing collection of pure HTML+JavaScript tools, hosted at [tools.simonwillison.net](https://tools.simonwillison.net/) using GitHub Pages. I love not having to even think about hosting server-side code for these tools.

I’ve published three tools there that talk to LLMs directly so far:

* [haiku](https://tools.simonwillison.net/haiku) is a fun demo that requests access to the user’s camera and then writes a Haiku about what it sees. It uses Anthropic’s Claude 3 Haiku model for this—the whole project is one terrible pun. [Haiku source code here](https://github.com/simonw/tools/blob/main/haiku.html).
* [gemini-bbox](https://tools.simonwillison.net/gemini-bbox) uses the Gemini 1.5 Pro (or Flash) API to prompt those models to return bounding boxes for objects in an image, then renders those bounding boxes. Gemini Pro is the only of the vision LLMs that I’ve tried that has reliable support for bounding boxes. I wrote about this in [Building a tool showing how Gemini Pro can return bounding boxes for objects in images](https://simonwillison.net/2024/Aug/26/gemini-bounding-box-visualization/).
* [Gemini Chat App](https://tools.simonwillison.net/gemini-chat) is a more traditional LLM chat interface that again talks to Gemini models (including the new super-speedy `gemini-1.5-flash-8b-exp-0827`). I built this partly to try out those new models and partly to experiment with implementing a streaming chat interface agaist the Gemini API directly in a browser. I wrote more about how that works [in this post](https://simonwillison.net/2024/Aug/27/gemini-chat-app/).

Here’s that Gemini Bounding Box visualization tool:

![Gemini API Image Bounding Box Visualization - browse for file goats.jpeg, prompt is Return bounding boxes as JSON arrays [ymin, xmin, ymax, xmax] - there follows output coordinates and then a red and a green box around the goats in a photo, with grid lines showing the coordinates from 0-1000 on both axes](https://static.simonwillison.net/static/2024/goats-bbox-fixed.jpg)

All three of these tools made heavy use of AI-assisted development: Claude 3.5 Sonnet wrote almost every line of the last two, and the Haiku one was put together a few months ago using Claude 3 Opus.

My personal style of HTML and JavaScript apps turns out to be highly compatible with LLMs: I like using vanilla HTML and JavaScript and keeping everything in the same file, which makes it easy to paste the entire thing into the model and ask it to make some changes for me. This approach also works really well with [Claude Artifacts](https://simonwillison.net/tags/claude-artifacts/), though I have to tell it “no React” to make sure I get an artifact I can hack on without needing to configure a React build step.

#### Converting PDFs to HTML and Markdown

I have a long standing vendetta against PDFs for sharing information. They’re painful to read on a mobile phone, they have poor accessibility, and even things like copying and pasting text from them can be a pain.

Complaining without doing something about it isn’t really my style. Twice in the past few weeks I’ve taken matters into my own hands:

* Google Research released [a PDF paper](https://research.google/pubs/sql-has-problems-we-can-fix-them-pipe-syntax-in-sql/) describing their new pipe syntax for SQL. I ran it through Gemini 1.5 Pro to convert it to HTML ([prompts here](https://simonwillison.net/2024/Aug/24/pipe-syntax-in-sql/)) and [got this](https://static.simonwillison.net/static/2024/Pipe-Syntax-In-SQL.html)—a pretty great initial result for the first prompt I tried!
* Nous Research released [a preliminary report PDF](https://github.com/NousResearch/DisTrO/blob/main/A_Preliminary_Report_on_DisTrO.pdf) about their DisTro technology for distributed training of LLMs over low-bandwidth connections. I [ran a prompt](https://simonwillison.net/2024/Aug/27/distro/) to use Gemini 1.5 Pro to convert that to [this Markdown version](https://gist.github.com/simonw/46a33d66e069efe5c10b63625fdabb4e), which even handled tables.

Within six hours of posting it my Pipe Syntax in SQL conversion was ranked third on Google for the title of the paper, at which point I set it to `<meta name="robots" content="noindex>` to try and keep the unverified clone out of search. Yet more evidence that HTML is better than PDF!

I’ve spent less than a total of ten minutes on using Gemini to convert PDFs in this way and the results have been very impressive. If I were to spend more time on this I’d target figures: I have a hunch that getting Gemini to return bounding boxes for figures on the PDF pages could be the key here, since then each figure could be automatically extracted as an image.

I bet you could build that whole thing as a client-side app against the Gemini Pro API, too...

#### Adding some class to Datasette forms

I’ve been working on a new Datasette plugin for permissions management, [datasette-acl](https://github.com/datasette/datasette-acl), which I’ll write about separately soon.

I wanted to integrate [Choices.js](https://github.com/Choices-js/Choices) with it, to provide a nicer interface for adding permissions to a user or group.

My first attempt at integrating Choices ended up looking like this:

![The choices elements have big upgly blank boxes displayed where the remove icon should be. The Firefox DevTools console is open revealing CSS properties set on form button type=button, explaining the visual glitches](https://static.simonwillison.net/static/2024/datasette-acl-choices-bug.jpg)

The weird visual glitches are caused by Datasette’s core CSS, which included [the following rule](https://github.com/simonw/datasette/blob/92c4d41ca605e0837a2711ee52fde9cf1eea74d0/datasette/static/app.css#L553-L564):

```
form input[type=submit], form button[type=button] {
    font-weight: 400;
    cursor: pointer;
    text-align: center;
    vertical-align: middle;
    border-width: 1px;
    border-style: solid;
    padding: .5em 0.8em;
    font-size: 0.9rem;
    line-height: 1;
    border-radius: .25rem;
}
```

These style rules apply to *any* submit button or button-button that occurs inside a form!

I’m glad I caught this before Datasette 1.0. I’ve now [started the process of fixing that](https://github.com/simonw/datasette/issues/2415), by ensuring these rules only apply to elements with `class="core"` (or that class on a wrapping element). This ensures plugins can style these elements without being caught out by Datasette’s defaults.

The problem is... there are a whole bunch of existing plugins that currently rely on that behaviour. I have [a tricking issue](https://github.com/simonw/datasette/issues/2417) about that, which identified 28 plugins that need updating. I’ve worked my way through 8 of those so far, hence the flurry of releases listed at the bottom of this post.

This is also an excuse to revisit a bunch of older plugins, some of which had partially complete features that I’ve been finishing up.

[datasette-write](https://github.com/simonw/datasette-write) for example now has [a neat row action menu item](https://github.com/simonw/datasette-write/issues/10) for updating a selected row using a pre-canned UPDATE query. Here’s an animated demo of my first prototype of that feature:

![Animated demo - on the row page for a release I click row actions and select Update using SQL, which navigates to a page with a big UPDATE SQL query and a form showing all of the existing values.](https://static.simonwillison.net/static/2024/datasette-write-row.gif)

#### On the blog

**anthropic**

* [Claude’s API now supports CORS requests, enabling client-side applications](https://simonwillison.net/2024/Aug/23/anthropic-dangerous-direct-browser-access)—2024-08-23
* [Explain ACLs by showing me a SQLite table schema for implementing them](https://simonwillison.net/2024/Aug/23/explain-acls)—2024-08-23
* [Musing about OAuth and LLMs on Mastodon](https://simonwillison.net/2024/Aug/24/oauth-llms)—2024-08-24
* [Building a tool showing how Gemini Pro can return bounding boxes for objects in images](https://simonwillison.net/2024/Aug/26/gemini-bounding-box-visualization)—2024-08-26
* [Long context prompting tips](https://simonwillison.net/2024/Aug/26/long-context-prompting-tips)—2024-08-26
* [Anthropic Release Notes: System Prompts](https://simonwillison.net/2024/Aug/26/anthropic-system-prompts)—2024-08-26
* [Alex Albert: We’ve read and heard that you’d appreciate more t...](https://simonwillison.net/2024/Aug/26/alex-albert)—2024-08-26
* [Gemini Chat App](https://simonwillison.net/2024/Aug/27/gemini-chat-app)—2024-08-27
* [System prompt for val.town/townie](https://simonwillison.net/2024/Aug/28/system-prompt-for-townie)—2024-08-28
* [How Anthropic built Artifacts](https://simonwillison.net/2024/Aug/28/how-anthropic-built-artifacts)—2024-08-28
* [Anthropic’s Prompt Engineering Interactive Tutorial](https://simonwillison.net/2024/Aug/30/anthropic-prompt-engineering-interactive-tutorial)—2024-08-30
* [llm-claude-3 0.4.1](https://simonwillison.net/2024/Aug/30/llm-claude-3)—2024-08-30

**ai-assisted-programming**

* [Andy Jassy, Amazon CEO: [...] here’s what we found when we integrated [Am...](https://simonwillison.net/2024/Aug/24/andy-jassy-amazon-ceo)—2024-08-24
* [AI-powered Git Commit Function](https://simonwillison.net/2024/Aug/26/ai-powered-git-commit-function)—2024-08-26
* [OpenAI: Improve file search result relevance with chunk ranking](https://simonwillison.net/2024/Aug/30/openai-file-search)—2024-08-30
* [Forrest Brazeal: I think that AI has killed, or is about to kill, ...](https://simonwillison.net/2024/Aug/31/forrest-brazeal)—2024-08-31

**gemini**

* [SQL Has Problems. We Can Fix Them: Pipe Syntax In SQL](https://simonwillison.net/2024/Aug/24/pipe-syntax-in-sql)—2024-08-24
* [NousResearch/DisTrO](https://simonwillison.net/2024/Aug/27/distro)—2024-08-27

**python**

* [uvtrick](https://simonwillison.net/2024/Sep/1/uvtrick)—2024-09-01
* [Anatomy of a Textual User Interface](https://simonwillison.net/2024/Sep/2/anatomy-of-a-textual-user-interface)—2024-09-02
* [Why I Still Use Python Virtual Environments in Docker](https://simonwillison.net/2024/Sep/2/why-i-still-use-python-virtual-environments-in-docker)—2024-09-02
* [Python Developers Survey 2023 Results](https://simonwillison.net/2024/Sep/3/python-developers-survey-2023)—2024-09-03

**security**

* [Top companies ground Microsoft Copilot over data governance concerns](https://simonwillison.net/2024/Aug/23/microsoft-copilot-data-governance)—2024-08-23
* [Frederik Braun: In 2021 we [the Mozilla engineering team] found “...](https://simonwillison.net/2024/Aug/26/frederik-braun)—2024-08-26
* [OAuth from First Principles](https://simonwillison.net/2024/Sep/5/oauth-from-first-principles)—2024-09-05

**projects**

* [My @covidsewage bot now includes useful alt text](https://simonwillison.net/2024/Aug/25/covidsewage-alt-text)—2024-08-25

**armin-ronacher**

* [MiniJinja: Learnings from Building a Template Engine in Rust](https://simonwillison.net/2024/Aug/27/minijinja)—2024-08-27

**ethics**

* [John Gruber: Everyone alive today has grown up in a world wher...](https://simonwillison.net/2024/Aug/27/john-gruber)—2024-08-27

**open-source**

* [Debate over “open source AI” term brings new push to formalize definition](https://simonwillison.net/2024/Aug/27/open-source-ai)—2024-08-27
* [Elasticsearch is open source, again](https://simonwillison.net/2024/Aug/29/elasticsearch-is-open-source-again)—2024-08-29

**performance**

* [Cerebras Inference: AI at Instant Speed](https://simonwillison.net/2024/Aug/28/cerebras-inference)—2024-08-28

**sqlite**

* [D. Richard Hipp: My goal is to keep SQLite relevant and viable thr...](https://simonwillison.net/2024/Aug/28/d-richard-hipp)—2024-08-28

**aws**

* [Leader Election With S3 Conditional Writes](https://simonwillison.net/2024/Aug/30/leader-election-with-s3-conditional-writes)—2024-08-30

**javascript**

* [Andreas Giammarchi: whenever you do this: `el.innerHTML += HTML` ...](https://simonwillison.net/2024/Aug/31/andreas-giammarchi)—2024-08-31

**openai**

* [OpenAI says ChatGPT usage has doubled since last year](https://simonwillison.net/2024/Aug/31/openai-says-chatgpt-usage-has-doubled-since-last-year)—2024-08-31

**art**

* [Ted Chiang: Art is notoriously hard to define, and so are the...](https://simonwillison.net/2024/Aug/31/ted-chiang)—2024-08-31

**llm**

* [anjor: `history | tail -n 2000 | llm -s "Write aliases f...](https://simonwillison.net/2024/Sep/3/anjor)—2024-09-03

**vision-llms**

* [Qwen2-VL: To See the World More Clearly](https://simonwillison.net/2024/Sep/4/qwen2-vl)—2024-09-04

#### Releases

* **[datasette-import 0.1a5](https://github.com/datasette/datasette-import/releases/tag/0.1a5)**—2024-09-04  
  Tools for importing data into Datasette
* **[datasette-search-all 1.1.3](https://github.com/simonw/datasette-search-all/releases/tag/1.1.3)**—2024-09-04  
  Datasette plugin for searching all searchable tables at once
* **[datasette-write 0.4](https://github.com/simonw/datasette-write/releases/tag/0.4)**—2024-09-04  
  Datasette plugin providing a UI for executing SQL writes against the database
* **[datasette-debug-events 0.1a0](https://github.com/datasette/datasette-debug-events/releases/tag/0.1a0)**—2024-09-03  
  Print Datasette events to standard error
* **[datasette-auth-passwords 1.1.1](https://github.com/simonw/datasette-auth-passwords/releases/tag/1.1.1)**—2024-09-03  
  Datasette plugin for authentication using passwords
* **[datasette-enrichments 0.4.3](https://github.com/datasette/datasette-enrichments/releases/tag/0.4.3)**—2024-09-03  
  Tools for running enrichments against data stored in Datasette
* **[datasette-configure-fts 1.1.4](https://github.com/simonw/datasette-configure-fts/releases/tag/1.1.4)**—2024-09-03  
  Datasette plugin for enabling full-text search against selected table columns
* **[datasette-auth-tokens 0.4a10](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a10)**—2024-09-03  
  Datasette plugin for authenticating access using API tokens
* **[datasette-edit-schema 0.8a3](https://github.com/simonw/datasette-edit-schema/releases/tag/0.8a3)**—2024-09-03  
  Datasette plugin for modifying table schemas
* **[datasette-pins 0.1a4](https://github.com/datasette/datasette-pins/releases/tag/0.1a4)**—2024-09-01  
  Pin databases, tables, and other items to the Datasette homepage
* **[datasette-acl 0.4a2](https://github.com/datasette/datasette-acl/releases/tag/0.4a2)**—2024-09-01  
  Advanced permission management for Datasette
* **[llm-claude-3 0.4.1](https://github.com/simonw/llm-claude-3/releases/tag/0.4.1)**—2024-08-30  
  LLM plugin for interacting with the Claude 3 family of models

#### TILs

* [Testing HTML tables with Playwright Python](https://til.simonwillison.net/playwright/testing-tables)—2024-09-04
* [Using namedtuple for pytest parameterized tests](https://til.simonwillison.net/pytest/namedtuple-parameterized-tests)—2024-08-31
