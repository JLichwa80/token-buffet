---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-12-08-weeknotes_cbd558]]"
  - "[[sources/2023-11-22-weeknotes_49168f]]"
  - "[[sources/2023-10-22-weeknotes_1435b6]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
tags:
  - "person"
aliases:
  - "Alex Garcia"
---

# Alex Garcia

## Description

Alex Garcia is a developer who built the [[datasette-plot]] plugin for [[Datasette]]. The source credits him with releasing the plugin as part of the collaboration between Simon Willison and the [[datasette-cloud|Datasette Cloud]] team. He introduced the plugin on the Datasette Cloud blog, which positions him as a contributor to the Datasette ecosystem. His work is the main featured item in the opening section of the December 31, 2023 weeknotes. He is a secondary subject of that post, whose focus is Willison's own December output.

Alex Garcia also released the first version of datasette-comments as part of the continuing collaboration to build out Datasette Cloud, extending his Datasette ecosystem work beyond datasette-plot.

Alex Garcia has been developing datasette-comments, a plugin that lets Datasette users collaborate on data by leaving comments on individual rows, which the source describes as well suited to collaborative investigative reporting. In the week after GitHub Universe, Willison worked with Alex Garcia on Datasette Cloud, a collaboration the November 22, 2023 weeknotes record.

Alex Garcia is leading a major Datasette improvement ahead of the 1.0 release: cleaning up the metadata system by splitting non-metadata configuration into a new `datasette.json` or `datasette.yaml` file.

In the October 22, 2023 weeknotes, Alex Garcia landed a large part of this metadata cleanup, moving permissions, allow blocks, canned queries, and more out of `metadata.yaml`. A `datasette publish` upgrade and an alpha release were still to come.

Alex Garcia has been working with Simon Willison on Datasette Cloud features, sponsored by Fly.io. He also built the datasette-write-ui plugin, which lets Datasette Cloud users insert, edit, and delete table rows. In addition, he is building datasette-short-links, an experimental link shortener that motivated the actors_from_ids plugin hook.

Alex Garcia drove two changes in Datasette 1.0a5: the `datasette.yaml` configuration file and the expanded `_internal` database for plugin storage. He also proposed that `_internal` could hold plugin data that regular users should not see, such as tokens created by datasette-auth-tokens or progress bar state for datasette-upload-csvs.

Alex Garcia has also planned work involving Fly's Litestream tool. As part of this work, the [[datasette-cloud|Datasette Cloud]] team will extensively document what they learn about using Fly to build a multi-tenant SaaS platform.
## Related Entities

- [[entities/datasette-plot|datasette-plot]]
- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|datasette-cloud]]
- [[entities/datasette-comments|datasette-comments]]

## Related Concepts

## Mentions in Source

- "Alex pointed out that the existing `_internal` database for Datasette could be expanded to cover these use-cases as well." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "Alex [expressed interest in fixing it](https://github.com/simonw/datasette/issues/2093), and has started to put a plan into motion for cleaning it up." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "[Alex Garcia](https://alexgarcia.xyz/) has been working with me building out features for Datasette Cloud, generously sponsored by [Fly.io](https://fly.io/)." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "Alex is using this in `datasette-short-links`, and I built two plugins to work with the new hook as well:" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "[Alex Garcia](https://github.com/asg017) has been driving a major improvement to Datasette in preparation for the 1.0 release: cleaning up Datasette’s ungainly metadata system." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]
- "Alex is fixing this by splitting all of those non-metadata parts of metadata out into a new, separate configuration file, which we’ve agreed should be called `datasette.json` or `datasette.yaml`." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]
- "With all of my conferences for the year out of the way, I spent the next week working with Alex Garcia on [Datasette Cloud](https://www.datasette.cloud/)." — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]
- "Alex Garcia released the first version of [datasette-comments](https://datasette.io/plugins/datasette-comments) as part of our continuing collaboration to build out Datasette Cloud." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "He wrote about that on the Datasette Cloud blog: **[Annotate and explore your data with datasette-comments](https://www.datasette.cloud/blog/2023/datasette-comments/)**." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "Alex Garcia released this new plugin for Datasette as part of our collaboration around Datasette Cloud." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "He introduced it on the Datasette Cloud blog: [datasette-plot—a new Datasette Plugin for building data visualizations](https://www.datasette.cloud/blog/2023/datasette-plot/)." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "`datasette-write-ui` is particularly notable because it was written by Alex Garcia, who is now working with me to help get Datasette Cloud ready for general availability." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]