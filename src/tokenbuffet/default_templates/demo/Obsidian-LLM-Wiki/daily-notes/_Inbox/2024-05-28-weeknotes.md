# Weeknotes: PyCon US 2024

Source: https://simonwillison.net/2024/May/28/weeknotes/

## Weeknotes: PyCon US 2024

28th May 2024

Earlier this month I attended [PyCon US 2024](https://us.pycon.org/2024/) in Pittsburgh, Pennsylvania. I gave an invited keynote on the Saturday morning titled “Imitation intelligence”, tying together much of what I’ve learned about Large Language Models over the past couple of years and making the case that the Python community has a unique opportunity and responsibility to help try to nudge this technology in a positive direction.

The video isn’t out yet but I’ll publish detailed notes to accompany my talk (using my [annotated presentation format](https://simonwillison.net/tags/annotatedtalks/)) as soon as it goes live on YouTube.

PyCon was a really great conference. Pittsburgh is a fantastic city, and I’m delighted that PyCon will be in the same venue next year so I can really take advantage of the opportunity to explore in more detail.

I also realized that it’s about time Datasette participated in the PyCon sprints—the project is mature enough for that to be a really valuable opportunity now. I’m looking forward to leaning into that next year.

I’m on a family-visiting trip back to the UK at the moment, so taking a bit of time off from my various projects.

#### LLM support for new models

The big new language model releases from May were OpenAI GPT-4o and Google’s Gemini Flash. I released [LLM 0.14](https://github.com/simonw/llm/releases/tag/0.14), [datasette-extract 0.1a7](https://github.com/datasette/datasette-extract/releases/tag/0.1a7) and [datasette-enrichments-gpt 0.5](https://github.com/datasette/datasette-enrichments-gpt/releases/tag/0.5) with support for GPT-4o, and [llm-gemini 0.1a4](https://github.com/simonw/llm-gemini/releases/tag/0.1a4) adding support for the new inexpensive Gemini 1.5 Flash.

Gemini 1.5 Flash is a particularly interesting model: it’s now [ranked 9th](https://twitter.com/lmsysorg/status/1795512202465845686) on the LMSYS leaderboard, beating Llama 3 70b. It’s inexpensive, [priced close to Claude 3 Haiku](https://simonwillison.net/2024/May/14/llm-gemini-01a4/), and can handle up to a million tokens of context.

I’m also excited about GPT-4o—half the price of GPT-4 Turbo, around twice as fast and it appears to be slightly more capable too. I’ve been getting particularly good results from it for structured data extraction using [datasette-extract](https://datasette.io/plugins/datasette-extract)—it seems to be able to more reliably produce a longer sequence of extracted rows from a given input.

#### Blog entries

* [ChatGPT in “4o” mode is not running the new features yet](https://simonwillison.net/2024/May/15/chatgpt-in-4o-mode/)
* [Slop is the new name for unwanted AI-generated content](https://simonwillison.net/2024/May/8/slop/)

#### Releases

* **[datasette-permissions-metadata 0.1](https://github.com/datasette/datasette-permissions-metadata/releases/tag/0.1)**—2024-05-15  
  Configure permissions for Datasette 0.x in metadata.json
* **[datasette-enrichments-gpt 0.5](https://github.com/datasette/datasette-enrichments-gpt/releases/tag/0.5)**—2024-05-15  
  Datasette enrichment for analyzing row data using OpenAI’s GPT models
* **[datasette-extract 0.1a7](https://github.com/datasette/datasette-extract/releases/tag/0.1a7)**—2024-05-15  
  Import unstructured data (text and images) into structured tables
* **[llm-gemini 0.1a4](https://github.com/simonw/llm-gemini/releases/tag/0.1a4)**—2024-05-14  
  LLM plugin to access Google’s Gemini family of models
* **[llm 0.14](https://github.com/simonw/llm/releases/tag/0.14)**—2024-05-13  
  Access large language models from the command-line

#### TILs

* [Listen to a web page in Mobile Safari](https://til.simonwillison.net/ios/listen-to-page)—2024-05-21
* [How I studied for my Ham radio general exam](https://til.simonwillison.net/ham-radio/general)—2024-05-11
