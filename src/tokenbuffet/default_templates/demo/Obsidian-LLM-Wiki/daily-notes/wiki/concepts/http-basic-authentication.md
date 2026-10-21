---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "HTTP Basic auth"
  - "Basic auth"
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"

generation_complete: true
---

# HTTP Basic authentication

## Definition

HTTP Basic authentication is a standard HTTP access-control scheme in which a client sends a username and password with each request, in an `Authorization` header encoded in Base64. It is defined in RFC 7617. In the source, the scheme is a feature added to [[shot-scraper]] in version 1.4, where each command can take a username and password.

## Key Characteristics

- Credentials are sent with every request in the `Authorization` header, so it needs no session or login form.
- Credentials are Base64-encoded, not encrypted; it should be used over HTTPS.
- It is supported by most HTTP clients and servers with little code, which makes it a common choice for simple access control.
- It is a per-request scheme: the server checks the credentials on each call.

## Applications

- Adding a simple access-control option to a small command-line tool that makes web requests, as [[shot-scraper]] did in version 1.4.
- Protecting small web applications or APIs that do not need a full user-account system, such as those hosted on a low-cost platform like [[Datasette as a cheap deployment platform]].

## Related Concepts

- [[concepts/datasette-as-a-cheap-deployment-platform|Datasette as a cheap deployment platform]]

## Related Entities

- [[entities/shot-scraper|shot-scraper]]

## Mentions in Source

- "I dropped into the repo to add HTTP Basic authentication support and found several excellent PRs waiting to be merged, so I bundled those together into a new release." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "New `--auth-username x --auth-password y` options for each `shot-scraper` command, allowing a username and password to be set for HTTP Basic authentication." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]