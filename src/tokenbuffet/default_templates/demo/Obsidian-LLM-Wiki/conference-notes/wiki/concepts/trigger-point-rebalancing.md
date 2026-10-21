---
type: concept
created: 2026-10-19
updated: 2026-10-19
generation_complete: true
sources:
  - "[[sources/10-09-keynote_-tax-alpha-fixed-income-and-smart-rebalancing-summary_bf9109]]"
tags:
  - "financial_strategy"
  - "action_playbook"
aliases:
  - "math-based hard rebalancing"
  - "trigger point framework"
---

# trigger point rebalancing

## Definition

Trigger point rebalancing is a quantitative portfolio management strategy where discretionary rebalancing trades are triggered strictly when asset allocation drift reaches a mathematically determined threshold at which the marginal benefits of risk realignment equal the total costs of execution.

## Key Characteristics

- **Cost-Benefit Threshold Optimization**: Replaces calendar-based rebalancing intervals with mathematically derived boundaries where tracking error reduction outweighs capital gains taxes and transaction costs.
- **Drift Tolerance Thresholds**: In standard implementations such as a 60/40 allocation, the actionable trigger typically occurs around a 6.5% drift, preventing premature turnover.
- **Friction-Aware Sizing**: Directly accounts for OTC transaction costs and tax friction before initiating rebalancing trades.
- **Coordination with Destination Points**: Operates in conjunction with an optimal destination point to maximize net after-tax, risk-adjusted returns rather than naively trading all the way back to baseline targets.

## Applications

- Managing taxable investment portfolios seeking to generate tax alpha by minimizing unnecessary realization of capital gains.
- Managing multi-asset allocations across asset classes with high OTC bid-ask spreads or illiquid rebalancing channels.
- Transitioning institutional and wealth management portfolios from arbitrary calendar schedules (monthly/quarterly) to automated, risk-budgeted execution triggers.

## Related Concepts

- [[concepts/rebalancing-destination|rebalancing destination]]
- [[concepts/cash-flow-rebalancing|soft rebalancing]]
- [[concepts/tax-alpha|tax alpha]]

## Related Entities

- [[entities/equities|equities]]
- [[entities/municipal-bonds|municipal-bonds]]

## Mentions in Source

- "Concept 2: Math-Based 'Hard' Rebalancing: Eventually, a portfolio will drift enough to need a true rebalancing trade. Instead of using arbitrary calendar dates or simple thresholds, the speaker's firm uses a calculated 'trigger point.'" — [[_Inbox/10-09 Keynote_ Tax Alpha, Fixed Income, and Smart Rebalancing-Summary|10-09 Keynote_ Tax Alpha, Fixed Income, and Smart Rebalancing-Summary]]
- "The Trigger Point: This is 'exactly where the costs and the benefits equal one another.' For a 60/40 portfolio, this trigger is around 6.5% drift." — [[_Inbox/10-09 Keynote_ Tax Alpha, Fixed Income, and Smart Rebalancing-Summary|10-09 Keynote_ Tax Alpha, Fixed Income, and Smart Rebalancing-Summary]]