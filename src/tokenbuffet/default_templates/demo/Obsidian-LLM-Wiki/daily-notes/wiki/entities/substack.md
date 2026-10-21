---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"
tags:
  - "organization"
---

# Substack

## Description

Substack is the newsletter platform the author uses to publish their newsletter. The author ran into a bug in which Substack denied requests to the newsletter's RSS feed when the requests came from code running in GitHub Actions. That blocking led to the creation of [[datasette-proxy-url]], which the author used to proxy the feed through a [[Datasette]] instance. The episode shows the author using Datasette as lightweight infrastructure for small workarounds, such as getting around a platform that blocks scheduled CI requests.

Substack does not offer a public API, so the author could not automate publishing and instead built a copy-and-paste workflow from their blog into Substack. By March 2023, the author's Substack newsletter had reached 640 subscribers.
## Related Entities

- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/datasette-as-a-cheap-deployment-platform|Datasette as a cheap deployment platform]]
- Substack is the delivery channel for the 'My blog as a newsletter' initiative, where the author's blog content is republished by email.

## New Information (2023-03-22-weeknotes)

- When text is pasted into the Substack editor, it is converted into Substack's own subset of HTML, which the author can then edit by hand before sending. (This describes a defining trait of Substack's editor that the page does not yet mention.)

## Mentions in Source

- "I built this one because I ran into a bug with Substack where Substack were denying requests to my newsletter’s RSS feed from code running in GitHub Actions!" — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "Frustrating, since the whole *point* of RSS is to be retrieved by bots." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "Substack doesn’t have an API, but I wanted to automate as much of the process of copying in data from my blog as possible." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "When I hit “paste” in the Substack editor interface it converts that representation into Substack’s chosen subset of HTML. Then I can edit it by hand in the Substack editor." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]