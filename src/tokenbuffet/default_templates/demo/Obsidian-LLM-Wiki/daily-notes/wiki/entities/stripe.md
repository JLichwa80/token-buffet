---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [organization]
aliases:
  - "Stripe billing"
sources:
  - "[[sources/2024-07-02-weeknotes_55c009]]"

generation_complete: true
---

# Stripe

## Description

Stripe is the payments company that [[Datasette Cloud]] uses for billing. In the 2024-07-02 weeknotes, [[Simon Willison]] reports that he is integrating Stripe with Datasette Cloud and targets starting billing via Stripe at the end of July 2024. He is outsourcing as much of the subscription-management UI as possible to Stripe's customer portal. The integration produced a TIL on mocking Stripe signature checks in a pytest fixture. Stripe is a supporting dependency rather than a subject of analysis, but it is a concrete step toward billing for Datasette Cloud.

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/simon-willison|Simon Willison]]

## Related Concepts

## Mentions in Source

- "I’m using [Stripe](https://stripe.com/) for billing, and attempting to outsource as much of the UI complexity of managing subscriptions to their [customer portal](https://docs.stripe.com/customer-management) product as possible." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]