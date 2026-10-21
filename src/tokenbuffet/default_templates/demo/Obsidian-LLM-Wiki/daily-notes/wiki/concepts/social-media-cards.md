---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Social media cards"
  - "Social cards"
sources:
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"

generation_complete: true
---

# Social media cards

## Definition

Images that appear in link previews when a URL is shared on social media.

## Key Characteristics

- Displayed as part of a link preview when a URL is shared.
- Often absent for pages that have no images of their own, so they can be generated, for example as screenshots of each page.
- Can be stored as image files, which takes up storage space that may matter for hosting limits.

## Applications

- Simon Willison's [[Today I Learned]] site generates a social media card for each page as a screenshot, since few TILs have images of their own.
- The original images were stored as PNG files inside the SQLite database, which contributed to exceeding Vercel's 50MB deployment limit.
- Willison moved the images to an S3 bucket and regenerated them at 1600x800 pixels using the `--retina` option of [[shot-scraper]].
- The full system is documented in a separate TIL.

## Related Concepts

## Related Entities

- [[entities/today-i-learned|Today I Learned]]
- [[entities/shot-scraper|shot-scraper]]

## Mentions in Source

- "My [Today I Learned](https://til.simonwillison.net/) site has had social media cards—images that show up in link previews when URLs are shared—for a long time now." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "Until recently it stored these images as PNG files directly in the SQLite database itself." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]