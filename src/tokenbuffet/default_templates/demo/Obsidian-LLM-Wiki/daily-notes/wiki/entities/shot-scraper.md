---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-11-22-weeknotes_49168f]]"
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"
tags:
  - "project"
  - "other"
aliases:
  - "shot-scraper CLI"
---

# shot-scraper

## Description

shot-scraper is the author's command-line tool for taking screenshots of web pages and running JavaScript scraping code against them. It is built on top of Playwright. Version 1.4 was released on 5 February 2024 and added HTTP Basic authentication support, along with options for browser viewport size, scale factor and extra browser arguments. The author reports that the release bundled several pull requests that had been waiting to be merged. The same post mentions a revived PG&E outage scraper that was built on shot-scraper's release.

shot-scraper 1.3 was released on 2023-11-01 as a command-line utility for taking automated screenshots of websites. It added a `--bypass-csp` option, contributed by Brenton Cleeland, for bypassing any Content Security Policy that prevents further JavaScript from running on the page. The same release changed `shot-scraper --interactive` so it no longer reloads the page before taking a screenshot, and improved the accessibility of the documentation, contributed by Paolo Melchiorre. Simon Willison reproduced the 1.3 release notes in his weeknotes of 2023-11-22 to highlight the contributions of external developers. He lists shot-scraper among the tools he maintains alongside [[entities/sqlite-utils|sqlite-utils]].

Simon Willison used shot-scraper to generate the social media card images for his [[entities/today-i-learned|Today I Learned]] (TIL) site. In 2023 he moved them out of SQLite and into an S3 bucket, combining shot-scraper with his s3-credentials CLI tool to store them there. The cards are now generated with the `--retina` option, which doubles their size to 1600x800 pixels. He documented the full screenshot system in a TIL titled "Social media cards generated with shot-scraper", and the tool forms a supporting part of the TIL section. shot-scraper 1.2 was released on 2023-04-27 as a command-line utility for taking automated screenshots of websites, a release missing from the page's version history, which starts at 1.3.

shot-scraper 1.1.1 was released on 2023-01-30 as a command-line utility for taking automated screenshots of websites. The project had 26 releases in total as of the 2023-02-09 weeknotes. Those weeknotes list 1.1.1 under "Releases this week", linking to the release tag and the total release count, and place shot-scraper alongside [[entities/db-to-sqlite|db-to-sqlite]] and [[entities/datasette-explain|datasette-explain]] among the projects Simon Willison maintains.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/llm|LLM]]
- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/today-i-learned|Today I Learned]]
- [[entities/db-to-sqlite|db-to-sqlite]]
- [[entities/datasette-explain|datasette-explain]]

## Related Concepts

- [[concepts/http-basic-authentication|HTTP Basic authentication]]
- [[concepts/social-media-card-generation|Social media card generation]]
- [[concepts/social-media-cards|Social media cards]]

## Mentions in Source

- "[shot-scraper](https://shot-scraper.datasette.io/) is my CLI tool for taking screenshots of web pages and running scraping code against them using JavaScript, built on top of [Playwright](https://playwright.dev/)." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I dropped into the repo to add HTTP Basic authentication support and found several excellent PRs waiting to be merged, so I bundled those together into a new release." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "New `--bypass-csp` option for bypassing any Content Security Policy on the page that prevents executing further JavaScript." — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]
- "**[shot-scraper 1.3](https://github.com/simonw/shot-scraper/releases/tag/1.3)**—2023-11-01  
  A command-line utility for taking automated screenshots of websites" — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]