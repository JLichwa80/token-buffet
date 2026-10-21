---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"
tags:
  - "project"
aliases:
  - "TIL"
  - "TILs"
---

# Today I Learned

## Description

Today I Learned (TIL) is [[Simon Willison]]'s website of short technical notes, which he publishes as TILs. The site has long shown social media cards, which are screenshots of its pages used in link previews. The images were originally stored as PNG files in the SQLite database, and they pushed the database past [[entities/vercel|Vercel]]'s 50MB deployment limit. Willison moved the images to an S3 bucket and regenerated them at 1600x800 using the [[entities/shot-scraper|shot-scraper]] `--retina` option. The week's entry also lists several TILs, including those on [[entities/rye|Rye]], Deno KV, the pip cache location, and code interpreter expansions.

## Related Entities

- [[entities/shot-scraper|shot-scraper]]
- [[entities/chatgpt-code-interpreter|ChatGPT Code Interpreter]]
- [[entities/rye|Rye]]

## Related Concepts

- [[concepts/social-media-cards|Social media cards]]

## Mentions in Source

- "My [Today I Learned](https://til.simonwillison.net/) site has had social media cards—images that show up in link previews when URLs are shared—for a long time now." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "Until recently it stored these images as PNG files directly in the SQLite database itself. Vercel has a 50MB size limit on deployments and the other day the screenshots finally tipped the database over that limit." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]