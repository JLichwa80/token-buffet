---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags: [action_playbook]
aliases:
  - "Fundamental Selection Cap Weight Trap"
  - "Cap-Weighted Screening Trap"
sources:
  - "[[sources/10-09-keynote_-tax-alpha-fundamental-indexing-rafi-and-rebalancing-alpha-_1d585c]]"

generation_complete: true
---

# Correlation Trap

## Definition

The Correlation Trap is an index design pitfall that occurs when an investment strategy uses non-price metrics (such as fundamental or factor screening) to select constituents, but weights them by market capitalization. Retaining market-cap weighting ties the portfolio's performance directly back to market pricing, resulting in a nearly complete (~99.9%) correlation to standard broad cap-weighted benchmarks and nullifying the potential benefits of active constituent selection.

## Key Characteristics

- **Benchmark Lock-in**: Maintaining market-capitalization weighting drives high co-movement (~99.9% correlation) with standard cap-weighted indices, regardless of how selective the fundamental screens are.
- **Nullified Selection Alpha**: The prospective active return from choosing fundamentally sound companies is largely offset by market-cap weighting dynamics.
- **Price-Linked Sizing**: Position sizing remains tied to constituent price rather than economic scale or fundamental size, causing overexposure to overvalued assets and underexposure to undervalued ones.
- **Suppressed Rebalancing Alpha**: By remaining anchored to market prices, the strategy fails to systematically capture contra-trading and rebalancing returns.

## Applications

- **Index Construction**: Designing indices and passive strategies that sever the link between constituent size and share price (e.g., weighting by revenues, cash flow, or dividends) to avoid market sentiment bubbles.
- **Smart Beta and Factor Product Due Diligence**: Evaluating factor and thematic ETFs to identify whether market-cap weighting schemes negate the intended factor tilts.
- **Systematic Portfolio Design**: Ensuring that portfolio weighting architectures complement the selection mechanism to reliably harvest rebalancing alpha.

## Related Concepts

- [[concepts/cap-weighted-indexing|Cap-Weighted Indexing]]
- [[concepts/fundamental-indexing|Fundamental Indexing]]

## Related Entities

## Mentions in Source

- "Correlation trap in 'fundamental selection + cap weight': If you keep cap-weighting, you can end up with ~99.9% correlation to the standard cap-weighted index (i.e., you didn’t change the engine much)." — [[_Inbox/10-09 Keynote_ Tax Alpha, Fundamental Indexing (RAFI), and Rebalancing Alpha After Fees & Taxes-Summary (2)|10-09 Keynote_ Tax Alpha, Fundamental Indexing (RAFI), and Rebalancing Alpha After Fees & Taxes-Summary (2)]]