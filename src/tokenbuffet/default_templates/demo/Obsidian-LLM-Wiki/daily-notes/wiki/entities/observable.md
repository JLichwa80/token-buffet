---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [organization]
aliases:
  - "Observable notebooks"
  - "Observable notebook platform"
sources:
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"

generation_complete: true
---

# Observable

## Description

Observable is the hosted notebook platform on which [[Simon Willison]] built his blog-to-newsletter tool, [[blog-to-newsletter|blog-to-newsletter]]. The notebook runs a SQL query against his [[Datasette]] instance, assembles the resulting HTML, and provides a button that copies a rich-text version to the clipboard. Willison describes this as making it "really easy to tweak the generated HTML" before the content is moved into [[Substack]]. In the architecture of his newsletter automation, Observable is the front-end layer, sitting between the Datasette backend and the Substack editor. The post presents Observable as a working, practical tool rather than a general-purpose subject.

## Related Entities

- [[entities/blog-to-newsletter|blog-to-newsletter]]
- [[entities/datasette|Datasette]]
- [[entities/substack|Substack]]

## Related Concepts

## Mentions in Source

- "[observablehq.com/@simonw/blog-to-newsletter](https://observablehq.com/@simonw/blog-to-newsletter) is an Observable notebook I wrote which assembles most of the newsletter for me." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]