---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [terminology]
aliases:
  - "Stripe customer portal"
sources:
  - "[[sources/2024-07-02-weeknotes_55c009]]"

generation_complete: true
---

# customer portal

## Definition

The customer portal is a [[Stripe]] product that hosts a self-service interface where customers manage their own subscriptions. Using it lets a service move most of its subscription-management UI off its own codebase.

## Key Characteristics

- Hosted by [[Stripe]], not built by the application developer
- Provides self-service subscription management for end customers
- Reduces the amount of custom interface code an application must maintain
- Used as an alternative to building bespoke billing-management screens

## Applications

- **[[Datasette Cloud]] billing:** [[Simon Willison]] planned to start billing users through [[Stripe]] around the end of July 2024 and to outsource subscription management to the customer portal, minimizing the custom UI Datasette Cloud needs to build.
- **Design decision:** Adopting the customer portal was one of the design decisions behind the Stripe integration work described in the 2024-07-02 weeknotes.

## Related Concepts

## Related Entities

- [[entities/stripe|Stripe]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "I’m using Stripe for billing, and attempting to outsource as much of the UI complexity of managing subscriptions to their customer portal product as possible." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]