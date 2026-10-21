---
type: concept
created: 2026-10-18
updated: 2026-10-19
generation_complete: true
sources:
  - "[[sources/10-09-keynote_-tax-alpha-fundamental-indexing-rafi-and-rebalancing-alpha-_1d585c]]"
tags:
  - "portfolio_archetype"
aliases:
  - "equal-weight indexing"
  - "Equal Weighting"
  - "EWI"
---

# Equal weight

## Definition

Equal weight is a portfolio construction archetype that assigns an identical weighting to every constituent security in an index or portfolio, contrasting with traditional market-capitalization weighting. It operates as a rebalancing mechanism where outperforming assets are systematically trimmed and underperforming assets are bought to restore parity.

## Key Characteristics

- **Constituent Parity**: Every asset receives an equal target allocation regardless of company size, market capitalization, or fundamental metrics.
- **Systematic Rebalancing Mechanism**: Generates its return profile through periodic rebalancing back to target weights, effectively buying low and selling high.
- **Gross Rebalancing Premium**: Can deliver gross rebalancing alpha (approximately 1.1% gross over cap weighting), but with higher turnover.
- **Vulnerability to Cost and Tax Drag**: The gross rebalancing edge decays significantly once fees, transaction costs, and taxes are accounted for (shrinking to ~0.4% net of fees, ~0.1% after tax, and turning negative at approximately −0.7% after liquidation).
- **Factor Exposures**: Inherently tilts toward smaller-capitalization stocks and value factors relative to broad cap-weighted benchmarks.

## Applications

- **Smart Beta Strategy Implementation**: Utilized under the smart-beta umbrella to capture non-cap-weighted diversification and contrarian rebalancing returns.
- **Decomposition of Rebalancing Alpha**: Used in empirical portfolio research to isolate and differentiate the edge generated purely by rebalancing from fundamental accounting metrics.
- **After-Tax Benchmark Evaluation**: Evaluated against after-tax performance hurdles to determine whether the mechanical rebalancing premium survives implementation costs and liquidation taxes in taxable accounts.

## Related Concepts

- [[concepts/rebalancing-alpha|Rebalancing alpha]]
- [[concepts/smart-beta|Smart beta]]
- [[concepts/after-tax-benchmarking|After-tax benchmarking]]

## Related Entities

- [[concepts/fundamental-indexing|RAFI]]

## Mentions in Source

- "Equal weight: Adds ~1.1%, ~0.4% net of fees, ~+0.1% after tax, ~-0.7% post liquidation (as read from the table)." — [[_Inbox/10-09 Keynote_ Tax Alpha, Fundamental Indexing (RAFI), and Rebalancing Alpha After Fees & Taxes-Summary (2)|10-09 Keynote_ Tax Alpha, Fundamental Indexing (RAFI), and Rebalancing Alpha After Fees & Taxes-Summary (2)]]