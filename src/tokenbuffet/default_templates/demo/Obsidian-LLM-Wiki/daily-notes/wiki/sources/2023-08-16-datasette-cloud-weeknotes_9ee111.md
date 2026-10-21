---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Datasette Cloud"
  - "Datasette 1.0a3"
  - "llm-mlc and more"
  - "2023-08-16 Datasette weeknotes"
contentHash: 3134-1e182823
source_file: "[[_Inbox/2023-08-16-datasette-cloud-weeknotes.md]]"
generation_complete: true
---

# 2023-08-16-datasette-cloud-weeknotes - Summary

## Source

- Original file: [[_Inbox/2023-08-16-datasette-cloud-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

Simon Willison's weeknotes for 16 August 2023 cover a busy week across the Datasette ecosystem. [[entities/datasette-cloud|Datasette Cloud]] moved significantly closer to general availability. [[entities/alex-garcia|Alex Garcia]] wrote the [[entities/datasette-write-ui|datasette-write-ui]] plugin while helping prepare the product, and [[entities/fly-io|Fly.io]] supports his work as [[concepts/open-source-sponsorship|open source sponsorship]]. The post announces [[entities/datasette|Datasette 1.0a3]], which focuses on a stable JSON API, plugin interface, and template contexts. On the LLM side, it introduces [[entities/llm-mlc|llm-mlc]], which runs [[entities/llama-2|Llama 2]] on Apple Silicon through [[entities/mlc|MLC]], and [[entities/llm|LLM]] 0.7, which adds custom model aliases. Smaller items include [[entities/openai-to-sqlite|openai-to-sqlite]] 0.4, which powers related-content recommendations, and [[entities/sqlite-utils-jq|sqlite-utils-jq]], which adds a jq SQL function to [[entities/sqlite-utils|sqlite-utils]]. The post also mentions [[entities/jq|jq]], [[entities/datasette-upload-dbs|datasette-upload-dbs]], and [[entities/cosmopolitan|Cosmopolitan]].

## Key Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/alex-garcia|Alex Garcia]]
- [[entities/datasette-write-ui|datasette-write-ui]]
- [[entities/fly-io|Fly.io]]
- [[entities/datasette|Datasette]]
- [[entities/llm|LLM]]
- [[entities/llm-mlc|llm-mlc]]
- [[entities/llama-2|Llama 2]]
- [[entities/mlc|MLC]]
- [[entities/openai-to-sqlite|openai-to-sqlite]]
- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/sqlite-utils-jq|sqlite-utils-jq]]
- [[entities/datasette-upload-dbs|datasette-upload-dbs]]
- [[entities/jq|jq]]
- [[entities/cosmopolitan|Cosmopolitan]]

## Key Concepts

- [[concepts/open-source-sponsorship|Open source sponsorship]]
- [[concepts/annotated-presentation-format|Annotated presentations]]
- [[concepts/multi-tenant-saas-platform|Multi-tenant SaaS platform]]

## Main Points

- **Datasette Cloud is nearing general availability**, with [[entities/datasette-write-ui|datasette-write-ui]] adding row editing, insertion, and deletion to Datasette.
- **Datasette 1.0a3 focuses on JSON support**, with a more intuitive default JSON shape for table and query pages.
- **Datasette 1.0 aims to stabilize** the plugin interface, JSON API format, and template contexts, so software built on it will not break before Datasette 2.0.
- **[[entities/llm-mlc|llm-mlc]] is presented as one of the easiest ways** to run [[entities/llama-2|Llama 2]] on an Apple Silicon Mac with GPU acceleration, though the setup still has more steps than the author would like.
- **[[entities/llm|LLM]] 0.7 adds custom model aliases**, and plugin support lets the community add new models as they are released.
- **[[entities/openai-to-sqlite|openai-to-sqlite]] 0.4 powers related-content recommendations** on the author's TIL site, generated from OpenAI embeddings.
- **[[entities/sqlite-utils-jq|sqlite-utils-jq]] adds a jq() SQL function**, written partly to exercise sqlite-utils' new plugins framework.

I didn't save this to a file because no output path was given. Tell me where you want it and I'll write it there.

## Mentions in Source

- "`datasette-write-ui` is particularly notable because it was written by Alex Garcia, who is now working with me to help get Datasette Cloud ready for general availability." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "As always, my goal for LLM is to grow a community of enthusiasts who write plugins like this to help support new models as they are released." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "I’m fascinated by embeddings. They’re not difficult to run using locally hosted models either—I hope to add a feature to LLM to help with that soon." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "Datasette Cloud is already being built on Fly, but as part of Alex’s work we’ll be extensively documenting what we learn along the way about using Fly to build a multi-tenant SaaS platform." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "Datasette Cloud is now a significant step closer to general availability." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "I wanted to get this in place as soon as possible for Datasette Cloud (which is running this alpha), since I don’t want to risk paying customers building integrations that would later break due to 1.0 API changes." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "Datasette 1.0 is the first version of Datasette that will be marked as “stable”: if you build software on top of Datasette I want to guarantee as much as possible that it won’t break until Datasette 2.0, which I hope to avoid ever needing to release." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]