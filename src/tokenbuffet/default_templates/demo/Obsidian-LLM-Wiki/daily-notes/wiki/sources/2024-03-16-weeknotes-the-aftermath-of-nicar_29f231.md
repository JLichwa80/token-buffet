---
type: source
created: 2026-10-20
updated: 2026-10-20
sources:
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar]]"
tags: [other]
aliases:
  - "Weeknotes: the aftermath of NICAR"
  - "2024-03-16 weeknotes"
contentHash: 30be-7d50a187
source_file: "[[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar.md]]"
generation_complete: true
---

# 2024-03-16-weeknotes-the-aftermath-of-nicar - Summary

## Source

- Original file: [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar.md]]
- Ingested: 2026-10-20

## Core Content

Simon Willison's weeknotes of 16 March 2024 cover the aftermath of the NICAR data journalism conference. He and Alex ran a [[entities/datasette|Datasette]] and [[entities/datasette-cloud|Datasette Cloud]] workshop, and he gave a lightning talk on two GPT-4 powered plugins, [[entities/datasette-enrichments-gpt|datasette-enrichments-gpt]] and [[entities/datasette-extract|datasette-extract]]. He solved his conference follow-up problem by booking calls with contacts on the spot, which produced a set of newsroom conversations. The main theme of the [[entities/datasette|Datasette]] 1.0a12 and 1.0a13 alphas was turning the cog menus into clearer [[concepts/action-buttons|action buttons]], backed by new [[concepts/plugin-hook|plugin hooks]]. The post also recounts a 24-hour outage of simonwillison.net. The domain had lapsed at a [[entities/123-reg|123-reg]] account tied to an old email address. The domain was recovered, and redirects were set up through [[entities/cloudflare|Cloudflare]]. The release list includes [[entities/datasette-export-database|datasette-export-database]], which uses [[concepts/vacuum-into|VACUUM INTO]] for consistent snapshots, and [[entities/llm-claude-3|llm-claude-3]], which gives the [[entities/llm|LLM]] tool access to [[entities/claude-3|Claude 3]] models.

## Key Entities

- [[entities/datasette|Datasette]]: the open source data exploration tool at the centre of the post
- [[entities/datasette-cloud|Datasette Cloud]]: the hosted bundle of Datasette plugins used for the NICAR demos
- [[entities/nicar|NICAR]]: the data journalism conference the post reflects on
- [[entities/datasette-extract|datasette-extract]]: plugin that populates tables from unstructured text and images
- [[entities/datasette-enrichments-gpt|datasette-enrichments-gpt]]: GPT-4 powered Datasette plugin demoed at NICAR
- [[entities/datasette-create-view|datasette-create-view]]: plugin that creates SQL views, built on the new `query_actions()` hook
- [[entities/datasette-export-database|datasette-export-database]]: plugin that exports consistent database snapshots
- [[entities/llm|LLM]]: Willison's command-line tool for large language models
- [[entities/llm-claude-3|llm-claude-3]]: LLM plugin that provides access to Claude 3 models
- [[entities/claude-3|Claude 3]]: Anthropic's model family, with Opus praised over GPT-4
- [[entities/gpt-4|GPT-4]]: the model behind the two Datasette plugins demoed at NICAR
- [[entities/123-reg|123-reg]]: the domain registrar where simonwillison.net lapsed
- [[entities/cloudflare|Cloudflare]]: the service used to set up redirects after the outage
- [[entities/mastodon|Mastodon]]: the self-hosted instance that was disrupted by the DNS outage
- [[entities/sqlite|SQLite]]: the database engine behind Datasette and its `VACUUM INTO` command

## Key Concepts

- [[concepts/action-buttons|Action buttons]]: Datasette's redesigned plugin-driven menus that replaced the cog icon
- [[concepts/plugin-hook|Plugin hook]]: extension points such as `query_actions()`, `view_actions()`, `row_actions()`, and `homepage_actions()`
- [[concepts/conference-follow-up|Conference follow-up]]: booking future calls with contacts on the spot
- [[concepts/vacuum-into|VACUUM INTO]]: the SQLite command used to create transactional snapshots
- [[concepts/dns|DNS]]: the failure mode that took simonwillison.net and Mastodon offline

## Main Points

- **Datasette 1.0a12 and 1.0a13** focused on turning cog menus into clearer [[concepts/action-buttons|action buttons]], and added four new [[concepts/plugin-hook|plugin hooks]] for query, view, row, and homepage pages.
- **datasette-extract** fills [[entities/datasette|Datasette]] tables from unstructured text or images. It was demonstrated at [[entities/nicar|NICAR]].
- **datasette-export-database** uses [[concepts/vacuum-into|VACUUM INTO]] to export a consistent snapshot of a database that is still accepting writes.
- **Conference follow-up:** booking a future call on the spot with each contact produced many newsroom conversations.
- **Outage:** simonwillison.net was offline for 24 hours after its domain was parked for a missed renewal at a registrar tied to an old email address. The author notes this as a cautionary example of domain management.
- **Recovery:** [[entities/123-reg|123-reg]]'s domain recovery process restored control. A temporary domain was registered and redirects were configured with [[entities/cloudflare|Cloudflare]].
- **Claude 3:** the author reports that Opus feels better than GPT-4 for most tasks, and that Haiku offers image input at the lowest price he has seen.

## Mentions in Source

- "I released two new Datasette 1.0 alphas in the run-up to NICAR: [1.0a12](https://docs.datasette.io/en/latest/changelog.html#a12-2024-02-29) and [1.0a13](https://docs.datasette.io/en/latest/changelog.html#changelog)." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "Datasette plugins have long been able to register additional menu items that should be shown on the database and table pages." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "Alex and I ran [a successful workshop](https://github.com/datasette/nicar-2024-datasette) on Datasette and Datasette Cloud, and I gave a lightning talk demonstrating two new GPT-4 powered Datasette plugins—[datasette-enrichments-gpt](https://datasette.io/plugins/datasette-enrichments-gpt) and [datasette-extract](https://datasette.io/plugins/datasette-extract)." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "Here’s a GIF showing that new button in action across several different pages on Datasette Cloud (which has a bunch of plugins that use it):" — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "A lot of this was in preparation for NICAR—I wanted to polish all sorts of corners of Datasette Cloud, which is itself a huge bundle of pre-configured Datasette plugins." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "I’ve been paying close attention to the management of domains I’ve bought in the past few years ([datasette.io](https://datasette.io/), [datasette.cloud](https://www.datasette.cloud/) etc) I hadn’t been paying attention to `simonwillison.net`." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]