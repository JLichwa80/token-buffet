---
created: 2026-10-19
updated: 2026-10-19
generation_complete: true
sources:
  - "[[sources/10-09-keynote_-tax-alpha-fixed-income-and-smart-rebalancing-summary_bf9109]]"
  - "[[sources/10-09-keynote_-tax-aware-long-short-investing-pretax-alpha-and-after-tax-_8ca74c]]"
tags:
  - "terminology"
aliases:
  - "Model Drift"
  - "Active Risk"
  - "Tracking Risk"
  - "Portfolio Drift"
  - "TE"
---

---

# Tracking Error

## Definition

Tracking error measures the divergence between the price behavior or returns of a customized client portfolio and the target investment benchmark model. In after-tax portfolio design, tracking error is treated as a deliberate budgetary parameter rather than an accidental defect. Advisors define explicit risk budgets that permit acceptable degrees of model drift to harvest tax losses or avoid triggering large capital gains.

## Key Characteristics

- It quantifies how far a customized portfolio may depart from its target investment model.
- In after-tax design it is set in advance as part of a [[concepts/use-budgets-not-gaps|risk budget]], alongside gain, time, and liquidity budgets.
- Acceptable tracking error, also called model drift, is the room used to harvest losses or defer gains without abandoning the destination model.
- It is one input to a transition roadmap, weighed with taxes, risk, time, liquidity, available losses, and client psychology.
- Disciplined rebalancing frameworks establish math-based trigger points to weigh tracking error reduction directly against transaction costs and tax friction.
- Tracking error can be categorized into uninformed tracking error (budgeted solely for tax-loss harvesting in direct indexing, typically ~1%) and informed tracking error (driven by an active alpha model in long-short portfolios, typically 2%, 4%, or 6%).
## Applications

- Advisors set how much tracking error or model drift is acceptable when a portfolio must stay near a target model while remaining tax-aware.
- Transition plans use that budget to move gradually from the current portfolio to the destination, harvesting at the tax-lot level and pairing losses against gains instead of selling everything at once.
- The same budget lets implementation bend around client needs: realize losses, avoid large capital gains, and still control exposure to the investment model.
- In equity direct indexing, weekly loss harvesting optimizes the trade-off between tracking error and tax alpha, producing roughly double the tax alpha of monthly harvesting (~200 bps vs. ~100 bps) at lower tracking error while avoiding the mean-reversion noise associated with daily rebalancing.
- In tax-aware long-short portfolios (e.g., 150/50, 200/100, and 250/150 archetypes with beta ~1 to the Russell 1000), expanding the informed tracking error budget (from 2% to 6%) alongside leverage enhances alpha-driven position turnover and scales subsequent tax-loss harvesting capacity.
## Related Concepts

- [[concepts/risk-budgets|Risk Budgets]]
- [[concepts/tax-design|Tax Design]]
- [[concepts/tax-neutral-transition|Transition Management]]
- [[concepts/long-only-direct-indexing|Direct Indexing]]
- [[concepts/weekly-harvesting-cadence|Weekly Harvesting Cadence]]
- [[concepts/trigger-point-rebalancing|Trigger Point Rebalancing]]
- [[concepts/tax-aware-long-short-overlay|Tax-Aware Long-Short Overlay]]
- [[concepts/information-ratio-ir|Information Ratio (IR)]]
- [[concepts/long-only-direct-indexing|Long-Only Direct Indexing]]

## Related Entities

## Mentions in Source

- "How much tracking error or model drift is acceptable?" — [[_Inbox/10-09 Keynote_ After-Tax Wealth Management and Tax Stack Design-Summary (1)|10-09 Keynote_ After-Tax Wealth Management and Tax Stack Design-Summary (1)]]
- "The roadmap considers taxes, risk, time, liquidity, available losses, tracking error, and client psychology." — [[_Inbox/10-09 Keynote_ After-Tax Wealth Management and Tax Stack Design-Summary (1)|10-09 Keynote_ After-Tax Wealth Management and Tax Stack Design-Summary (1)]]
- "He presented data showing that weekly harvesting generated double the tax alpha (200 bps) of monthly harvesting (100 bps) for slightly less tracking error." — [[_Inbox/10-09 Keynote_ Tax Alpha, Fixed Income, and Smart Rebalancing-Summary|10-09 Keynote_ Tax Alpha, Fixed Income, and Smart Rebalancing-Summary]]
- "Long-short variants: 150/50, 200/100, 250/150; beta ~1; 2%, 4%, 6% informed tracking error driven by an alpha model." — [[_Inbox/10-09 Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary|10-09 Keynote_ Tax-Aware Long-Short Investing, Pretax Alpha, and After-Tax Wealth-Summary]]