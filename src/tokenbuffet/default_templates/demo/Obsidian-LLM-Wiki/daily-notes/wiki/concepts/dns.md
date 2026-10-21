---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [terminology]
aliases:
  - "Domain Name System"
  - "DNS issue"
sources:
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"

generation_complete: true
---

# DNS

## Definition

DNS, the Domain Name System, translates domain names into the addresses that browsers and apps use to reach servers. When it fails, services under the affected domains become unreachable even when the servers themselves are running.

## Key Characteristics

- Maps human-readable domain names to the network addresses used to reach servers
- Sits in front of every service that is reached by domain name, so a failure affects all of them at once
- Depends on the domain registration being kept current; a lapsed renewal can lead to the domain being parked and its DNS failing
- Can take down unrelated self-hosted services that share the same domain, such as [[Mastodon]]
- Failures are often treated as a frequent and far-reaching cause of outages, as reflected in the section title "It's always DNS" in the source

## Applications

- Pointing a website or API domain at its hosting provider
- Setting up redirects and recovery configuration during an outage, such as with [[Cloudflare]]
- Diagnosing outages: checking DNS and domain registration status early when a site becomes unreachable
- Domain management practice: tracking renewal dates and the account and email tied to a registrar

## Related Concepts

## Related Entities

- [[entities/mastodon|Mastodon]]
- [[entities/cloudflare|Cloudflare]]

## Mentions in Source

- "This site was offline for 24 hours this week due to a DNS issue." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]