---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Weeknotes: Miscellaneous research into Rye"
  - "ChatGPT Code Interpreter and openai-to-sqlite"
  - "2023-05-01 weeknotes"
contentHash: 1b29-498289eb
source_file: "[[_Inbox/2023-05-01-weeknotes.md]]"
generation_complete: true
---

# 2023-05-01-weeknotes - Summary

## Source

- Original file: [[_Inbox/2023-05-01-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

Simon Willison's weeknotes for the week ending 1 May 2023 cover side research he pursued after PyCon. The first topic is [[entities/rye|Rye]], an experimental Python packaging tool by [[entities/armin-ronacher|Armin Ronacher]] that downloads its own standalone Python build from [[entities/python-build-standalone|python-build-standalone]] instead of relying on a system Python. Willison also released Datasette 0.64.3 so it installs cleanly with Rye. The second topic is [[entities/chatgpt-code-interpreter|ChatGPT Code Interpreter]], which he calls the most interesting thing in the ChatGPT and LLM world. He found a way to install extra Python packages and add Deno and Lua binaries. The third topic is [[entities/openai-to-sqlite|openai-to-sqlite]], which gained a [[concepts/custom-sql-functions|custom SQL function]] that calls the chatgpt() API, enabling [[concepts/sentiment-analysis|sentiment analysis]] inside [[entities/sqlite|SQLite]]. Social media card images for [[entities/today-i-learned|Today I Learned]] moved from SQLite to S3 to get under [[entities/vercel|Vercel]]'s 50MB deployment limit, and were regenerated at 1600x800 with [[entities/shot-scraper|shot-scraper]]. The note closes by previewing a [[entities/langchain-prompt-injection-webinar|LangChain webinar]] on [[concepts/prompt-injection|prompt injection]], where he plans to argue that AI security problems cannot be solved with more AI.

## Key Entities

- [[entities/rye|Rye]]: experimental Python packaging tool, the first topic of the entry
- [[entities/armin-ronacher|Armin Ronacher]]: creator of Rye
- [[entities/python-build-standalone|python-build-standalone]]: source of the standalone Python builds that Rye downloads
- [[entities/chatgpt-code-interpreter|ChatGPT Code Interpreter]]: ChatGPT feature for running code, extended with packages, Deno and Lua
- [[entities/openai-to-sqlite|openai-to-sqlite]]: CLI tool for saving OpenAI API results to SQLite, now with a SQL function for chatgpt()
- [[entities/sqlite|SQLite]]: embedded database used by the tools and the TIL site
- [[entities/today-i-learned|Today I Learned]]: Willison's TIL website, whose social media cards moved to S3
- [[entities/shot-scraper|shot-scraper]]: screenshot tool used to generate the social media cards
- [[entities/vercel|Vercel]]: hosting platform whose 50MB deployment limit drove the migration
- [[entities/s3-credentials|s3-credentials]]: CLI tool combined with shot-scraper to store images in S3
- [[entities/langchain-prompt-injection-webinar|LangChain Prompt Injection Webinar]]: upcoming panel where Willison planned to speak

## Key Concepts

- [[concepts/prompt-injection|Prompt injection]]: attack class in which malicious input text overrides an LLM's intended behaviour
- [[concepts/dual-llm-pattern|Dual LLM pattern]]: design for AI assistants that can resist prompt injection, introduced the week before
- [[concepts/social-media-cards|Social media cards]]: images shown in link previews, generated as screenshots for TIL pages
- [[concepts/custom-sql-functions|Custom SQL function]]: user-defined SQL function, here calling chatgpt() to enrich data
- [[concepts/weeknotes|Weeknotes]]: Willison's weekly summary blog format
- [[concepts/python-packaging|Python packaging]]: tools and processes for distributing and installing Python libraries
- [[concepts/sentiment-analysis|Sentiment analysis]]: the experiment run on SQLite data through openai-to-sqlite

## Main Points

- Willison spent a week on miscellaneous research projects after PyCon instead of his core responsibilities.
- **Rye** stands out for bundling a standalone Python build, so it works without a system Python. Willison calls this his favourite idea in the tool.
- **ChatGPT Code Interpreter** can be extended with extra Python packages and with Deno and Lua binaries, despite having no internet connection.
- **openai-to-sqlite** gained a custom SQL function that calls chatgpt(), so SQLite tables can be updated with model results, for example for sentiment analysis.
- **Today I Learned** social media cards moved from SQLite to S3 because the database pushed the deployment past Vercel's 50MB limit. They were regenerated at 1600x800 using shot-scraper's `--retina` option.
- The [[concepts/dual-llm-pattern|Dual LLM pattern]] was proposed as a way to build assistants that resist prompt injection without a robust solution to the problem.
- Willison planned to argue on a LangChain webinar panel that AI security problems cannot be solved with more AI.

## Mentions in Source

- "I gave myself some time off stressing about my core responsibilities this week after PyCon, which meant allowing myself to be distracted by some miscellaneous research projects." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "Personally, I think a working prototype of an interesting idea is always worthwhile." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "My experience is that running code increases the quality of the discussion around an idea enormously, because it gives people something concrete to talk about." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "I think it’s the most interesting thing in all of ChatGPT/LLM world at the moment, which is a big statement." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "[Rye](https://github.com/mitsuhiko/rye) is a new experimental twist on Python packaging from Armin Ronacher." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "He’s been quite apologetic about it, asking [Should Rye Exist?](https://github.com/mitsuhiko/rye/discussions/6)—Python packaging is a crowded space right now!" — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "Rye has some *really* interesting ideas. By far my favourite is how it bundles Python itself: it doesn’t depend on a system Python, instead downloading a standalone Python build from the [python-build-standalone](https://github.com/indygreg/python-build-standalone) project and stashing it away in a `~/.rye` directory." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "Rye provides a single binary (written in Rust) which can bootstrap a working Python environment, without interfering with the system Python or any other Python environments that might already be installed." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]