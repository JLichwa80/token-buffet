---
type: concept
created: 2026-10-18
updated: 2026-10-18
tags: [terminology]
aliases:
  - "Beta One"
  - "Market Return"
  - "Systematic Risk"
sources:
  - "[[sources/10-09-keynote_-tax-aware-long-short-investing-pretax-alpha-and-after-tax-_8ca74c]]"

generation_complete: true
---

# Market Beta

## Definition

Market beta is a statistical measure of systematic risk reflecting the degree to which an asset or portfolio's returns co-move relative to the broad market benchmark. In long-short portfolio construction, setting beta to approximately 1.0 ensures benchmark-neutral equity risk exposure, isolating idiosyncratic manager skill from general market performance.

## Key Characteristics

- **Systematic Exposure**: Captures non-diversifiable market co-movement relative to a broad index such as the [[Russell 1000]].
- **Leverage Invariance in Long-Short Portfolios**: Broad market movements scale long and short positions proportionately in tandem, leaving net percentage leverage unchanged.
- **Inability to Induce Position Creation**: Because general market appreciation or depreciation does not alter portfolio leverage ratios, beta alone cannot trigger [[Position Creation]] or generate tax rebalancing opportunities.
- **Skill Isolation**: Constraining beta to 1.0 isolates [[Pretax Alpha]] by neutralizing systemic directional bias.

## Applications

- **Benchmark Alignment**: Calibrating long-short equity strategies to maintain an overall beta near 1.0 relative to target benchmarks.
- **Performance Attribution**: Disentangling macro-driven market returns from active manager returns.
- **Risk Management**: Monitoring and controlling portfolio sensitivity to broad market swings while minimizing unintended [[Tracking Error]].

## Related Concepts

- [[concepts/position-creation|Position Creation]]
- [[concepts/pretax-alpha|Pretax Alpha]]
- [[concepts/tracking-error|Tracking Error]]

## Related Entities

- [[entities/russell-1000|Russell 1000]]

## Mentions in Source

- "Long-short variants: 150/50, 200/100, 250/150; beta ~1; 2%, 4%, 6% informed tracking error driven by an alpha model." — [[_Inbox/10-09 Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary|10-09 Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary]]