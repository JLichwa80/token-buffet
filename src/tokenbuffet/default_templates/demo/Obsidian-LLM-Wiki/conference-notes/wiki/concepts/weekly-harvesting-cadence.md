---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags: [action_playbook]
aliases:
  - "weekly tax loss harvesting"
  - "weekly harvesting frequency"
sources:
  - "[[sources/10-09-keynote_-tax-alpha-fixed-income-and-smart-rebalancing-summary_bf9109]]"

generation_complete: true
---

# weekly harvesting cadence

## Definition

A weekly harvesting cadence is an execution schedule for systematic equity direct indexing tax loss harvesting. It represents the optimal rebalancing frequency to maximize tax alpha while minimizing incremental tracking error and avoiding short-term market noise.

## Key Characteristics

- **Alpha Capture**: Captures approximately 200 basis points of tax alpha compared to roughly 100 basis points generated under a monthly harvesting schedule.
- **Noise Avoidance**: Prevents the alpha degradation associated with daily harvesting, which tends to capture short-term mean reversions and market noise.
- **Risk-Return Trade-Off**: Establishes an optimal balance between after-tax alpha generation and tracking error relative to the target index.
- **Systematic Implementation**: Designed for automated, rule-based execution within direct indexing strategies.

## Applications

- **Direct Indexing Portfolios**: Deployed as the standard loss-harvesting rebalancing cycle in separately managed accounts (SMAs) holding individual equities.
- **Tax-Aware Wealth Management**: Utilized by systematic wealth management platforms to optimize after-tax returns for taxable investors without taking on unintended factor or benchmark tracking risk.

## Related Concepts

- [[concepts/tax-loss-harvesting|tax loss harvesting]]
- [[concepts/direct-indexing|direct indexing]]
- [[concepts/tax-alpha|tax alpha]]

## Related Entities

- [[entities/equities|equities]]

## Mentions in Source

- "Optimizing Equity Harvesting: Before moving to bonds, the speaker shared a key tactical tip for direct indexing: harvest weekly, not monthly or daily." — [[_Inbox/10-09 Keynote_ Tax Alpha, Fixed Income, and Smart Rebalancing-Summary|10-09 Keynote_ Tax Alpha, Fixed Income, and Smart Rebalancing-Summary]]