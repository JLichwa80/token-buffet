---
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"

generation_complete: true
---

type: entity
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2023-03-22-weeknotes_1bbf6a]]"]
tags: [other]
aliases: ["Blog to newsletter notebook"]
---

# blog-to-newsletter

## Description

blog-to-newsletter is an [[Observable]] notebook written by [[Simon Willison]] that assembles the content of his newsletter from his blog. It runs a SQL query against his [[Datasette]] instance, which holds a SQLite copy of his blog, and renders the results as HTML inside the notebook. A Copy to clipboard button places a rich text version of that HTML on the clipboard, and pasting it into the [[Substack]] editor converts it to Substack's supported HTML subset. The author can then edit the result by hand and add commentary before sending. The notebook is the main example of automation in [[My blog as a newsletter]], and because Substack has no API, it is the workaround the author built.

## Related Entities

- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/my-blog-as-a-newsletter|My blog as a newsletter]]

## Mentions in Source

- "[observablehq.com/@simonw/blog-to-newsletter](https://observablehq.com/@simonw/blog-to-newsletter) is an Observable notebook I wrote which assembles most of the newsletter for me." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "I built myself an automation around copy and paste!" — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]