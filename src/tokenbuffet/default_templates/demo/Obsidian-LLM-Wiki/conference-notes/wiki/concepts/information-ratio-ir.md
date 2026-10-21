---
type: concept
created: 2026-10-18
updated: 2026-10-19
generation_complete: true
sources:
  - "[[sources/10-09-keynote_-tax-aware-long-short-investing-pretax-alpha-and-after-tax-_8ca74c]]"
tags:
  - "terminology"
aliases:
  - "IR"
  - "Information Ratio"
---

# Information Ratio (IR)

## Definition

The Information Ratio (IR) is a risk-adjusted performance measure defined as [[Pretax Alpha]] divided by [[Tracking Error]], quantifying an active manager's skill and efficiency in generating excess returns relative to a specified benchmark.

## Key Characteristics

- **Formula**: Calculated as active return (pretax alpha) divided by active risk (volatility of active returns or tracking error).
- **Skill Quantification**: Standardizes active performance to measure manager competence independently of overall portfolio leverage or absolute market volatility.
- **Sensitivity Metric in Simulations**: Serves as a primary independent variable across multi-year horizon simulations (e.g., varied from -1.0 to +1.0 across rolling 15-year periods) to assess sensitivity of after-tax wealth and tax alpha.
- **Cost Cushion**: High IR accelerates position turnover and loss harvesting in long-short frameworks, whereas zero or negative IR leaves the portfolio vulnerable to severe drag from borrowing and transaction costs.

## Applications

- **Manager Selection and Evaluation**: Benchmarking active investment managers on their capacity to deliver consistent excess return per unit of active risk.
- **Tax-Aware Strategy Modeling**: In [[concepts/tax-aware-long-short|Tax-Aware Long-Short Investing]], varying the assumed IR allows investors to determine whether gross alpha offsets financing spreads and friction while compounding tax-loss harvesting benefits.
- **Portfolio Construction**: Calibrating sizing and target tracking error allocations to optimize the trade-off between alpha potential and risk budget.

## Related Concepts

- [[concepts/pretax-alpha|Pretax Alpha]]
- [[concepts/tracking-error|Tracking Error]]
- [[concepts/tax-aware-long-short-overlay|Tax-Aware Long-Short Investing]]

## Related Entities

## Mentions in Source

- "Information Ratio (IR) - Definition: Pretax alpha divided by target tracking error; a risk-adjusted measure of manager skill." — [[_Inbox/10-09 Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary|10-09 Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary]]
- "Information ratio (IR) varied from -1 to +1 to reflect manager skill." — [[_Inbox/10-09 Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary|10-09 Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary]]