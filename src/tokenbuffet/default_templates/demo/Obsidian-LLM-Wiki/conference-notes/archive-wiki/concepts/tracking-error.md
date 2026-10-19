---
created: 2026-10-06
updated: 2026-10-13
generation_complete: true
sources:
  - "[[sources/at this tax conference-keynote_-tax-aware-long-short-investing-pretax-alpha-and-after-tax-_108d27]]"
  - "[[sources/at this tax conference-keynote_-tax-alpha-fixed-income-and-smart-rebalancing-summary_58815e]]"
  - "[[sources/at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary-1_b17566]]"
tags:
  - "terminology"
aliases:
  - "Active Risk"
  - "TE"
  - "Tracking Error"
  - "Tracking Error Volatility"
  - "TEV"
  - "Ex-Ante Tracking Error"
  - "Predicted Tracking Error"
  - "Standard Deviation of Active Returns"
---
## Description
Tracking error is the active-risk budget that sets how sensitive a portfolio may be to its target investment model and how much model drift is acceptable. It is the dimension that separates the tested archetypes, and it scales the information ratio: pretax alpha divided by target tracking error, so the same skill score implies more alpha dollars when the tracking-error target is wider. Long-only direct indexing is 100 long / 0 short, with beta near 1 to the Russell 1000 and 1% uninformed tracking error aimed at tax-loss harvesting inside a tight benchmark hug. Its objective is to defer gains and realize losses within that budget. The long-short variants—150/50, 200/100, and 250/150—also target beta near 1, and they use 2%, 4%, and 6% informed tracking error driven by an alpha model. Their objective is to maximize pretax alpha while still deferring gains and realizing losses under constraints. Implementation guidance is to require informed tracking error and a documented alpha model together with any loss-harvesting mandate.
In equity tax-loss harvesting, weekly harvesting generated double the tax alpha (200 bps) of monthly harvesting (100 bps) for slightly less tracking error. Daily harvesting is too frequent and degrades the amount of tax alpha by getting caught in short-term mean reversions, adding noise without a matching gain in alpha. In rebalancing, reducing tracking error is the benefit side of the trigger equation, set against taxes and trading costs, and tax decisions are allowed to increase tracking error only when the after-tax benefit is larger. The rebalancing destination rule exists because further steps toward the target buy progressively smaller tracking-error reductions.
At a fundamental level, tracking error quantifies the divergence between portfolio returns and the benchmark target. In after-tax wealth management, it functions as a deliberate risk budget, allowing the portfolio to drift away from the model when necessary to avoid triggering taxable capital gains or to navigate around concentrated legacy stock positions.
Statistically, tracking error quantifies the volatility of excess returns relative to a designated benchmark index. In long-short strategies, informed tracking error provides the dedicated active risk budget required to express positive and negative manager views, directly driving the under-leverage and position creation cycles necessary for execution.
## Related Concepts
- [[budgets-not-gaps|Budgets, Not Gaps]]
- [[portfolio-risk|Portfolio Risk]]
- [[transitions-are-roadmaps|Transitions Are Roadmaps]]
- [[tax-loss-harvesting|Tax-Loss Harvesting]]
- [[client-psychology|Client Psychology]]
- [[information-ratio|Information Ratio]]
- [[long-only-direct-indexing|Long-Only Direct Indexing]]
- [[15050-long-short|150/50 Long-Short]]
- [[pretax-alpha|Pretax Alpha]]
- [[tax-aware-long-short-equity|Tax-Aware Long-Short]]
- [[weekly-tax-loss-harvesting|Weekly Tax Loss Harvesting]]
- [[trigger-point-rebalancing|Trigger Point Rebalancing]]
- [[rebalancing-destination|Rebalancing Destination]]
- [[tax-alpha|Tax Alpha]]
## Related Entities
- [[aaron|Aaron]]
- [[russell-1000|Russell 1000]]
## Related Pages
- Daily harvesting degrades tax alpha per unit of tracking error because the portfolio gets caught in [[short-term-mean-reversion|short-term mean reversion]]. [[short-term-mean-reversion]]
- The 150/50, 200/100, and 250/150 books take 2%, 4%, and 6% informed tracking error driven by a documented [[alpha-model|alpha model]], which is the active-risk budget that separates those variants from uninformed tax-loss harvesting. [[alpha-model]]
## Mentions in Source
- "How sensitive should the portfolio be to the target investment model? How much tracking error or model drift is acceptable?" — [[_Inbox/at this tax conference Keynote_ After-Tax Wealth Management and Tax Stack Design-Summary (1)|at this tax conference Keynote_ After-Tax Wealth Management and Tax Stack Design-Summary (1)]]
- "Long-short variants: 150/50, 200/100, 250/150; beta ~1; 2%, 4%, 6% informed tracking error driven by an alpha model." — [[_Inbox/at this tax conference Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary|at this tax conference Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary]]
- "How sensitive should the portfolio be to the target investment model?" — [[wiki/sources/at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary-1_b17566|at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary]]
- "How much tracking error or model drift is acceptable?" — [[wiki/sources/at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary-1_b17566|at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary]]
- "He presented data showing that weekly harvesting generated double the tax alpha (200 bps) of monthly harvesting (100 bps) for slightly less tracking error." — [[wiki/sources/at this tax conference-keynote_-tax-alpha-fixed-income-and-smart-rebalancing-summary_58815e|at this tax conference-keynote_-tax-alpha-fixed-income-and-smart-rebalancing-summary]]
- "Long-only direct indexing: 100 long / 0 short; beta ~1 to Russell 1000; 1% uninformed tracking error focused on tax-loss harvesting." — [[wiki/sources/at this tax conference-keynote_-tax-aware-long-short-investing-pretax-alpha-and-after-tax-_108d27|at this tax conference-keynote_-tax-aware-long-short-investing-pretax-alpha-and-after-tax-wealth-summary]]
- "1% uninformed tracking error focused on tax-loss harvesting." — [[_Inbox/at this tax conference Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary|at this tax conference Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary]]