---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "datasette-proxy-url 0.1.1"
  - "datasette-proxy-url plugin"
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"

generation_complete: true
---

# datasette-proxy-url

## Description

datasette-proxy-url is a [[Datasette]] plugin released in January 2024 (version 0.1.1, dated 2024-01-23). It lets an operator configure a path within a Datasette instance so that it serves content proxied from another URL. Simon Willison built it to work around [[Substack]] denying requests to his newsletter's RSS feed from code running in GitHub Actions. The fix was to deploy a small proxy onto a Datasette instance he already ran. The plugin is an example of the approach described in [[Datasette as a cheap deployment platform]], where Datasette serves as a low-cost host for small proxying infrastructure. It is listed under the "New plugins for Datasette" section of the weeknotes.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/substack|Substack]]

## Related Concepts

- [[concepts/datasette-as-a-cheap-deployment-platform|Datasette as a cheap deployment platform]]

## Mentions in Source

- "datasette-proxy-url is a very simple plugin that simple lets you configure a path within Datasette that serves content proxied from another URL." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I built this one because I ran into a bug with Substack where Substack were denying requests to my newsletter’s RSS feed from code running in GitHub Actions!" — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]