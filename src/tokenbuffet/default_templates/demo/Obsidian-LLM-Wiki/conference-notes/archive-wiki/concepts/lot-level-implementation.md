---
created: 2026-10-12
updated: 2026-10-12
generation_complete: true
sources:
  - "[[sources/at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary-1_b17566]]"
tags:
  - "action_playbook"
aliases:
  - "Tax-Lot-Level Implementation"
  - "Tax Lot Level Implementation"
  - "Tax-Lot Implementation"
  - "Individual Tax-Lot Implementation"
  - "Lot-Level Portfolio Implementation"
  - "Implementation at the Tax-Lot Level"
  - "Tax-Lot Customization"
---
## Description
Lot-level implementation is the execution of investment and rebalancing decisions at the granularity of individual tax lots rather than aggregate accounts, funds, or model portfolios. This micro-level execution serves as the primary technical foundation for [[Direct Indexing]] and tax-aware transition management, empowering algorithmic portfolio engines to selectively identify and harvest losses, prevent short-term capital gain realization, and selectively trim legacy positions according to gain budgets. By shifting wealth management from pre-tax product selection to an after-tax implementation platform within the [[Tax Stack]], it enables advisors to systematically manage complex family balance sheets, customize portfolios around client-specific exclusions and restrictions, and minimize tax drag across diverse accounts and structures.
## Related Concepts
- [[tax-stack|Tax Stack]]
- [[transitions-are-roadmaps|Transitions Are Roadmaps]]
- [[direct-indexing|Direct Indexing]]
- [[tax-loss-harvesting|Tax-Loss Harvesting]]
- [[own-securities-where-control-matters|Own Securities Where Control Matters]]
- [[losses-are-inventory|Losses as Inventory]]
## Related Entities
- [[aaron|Aaron]]
## Related Pages
- Lot-level implementation is the layer that applies [[client-specific-restrictions|Client-Imposed Restrictions]], encoding each account's exclusions and security limits on individual tax lots. [[client-specific-restrictions]]
- Lot-level implementation chooses which tax lots to sell, the control that a simple staged or phased liquidation does not provide. [[stage-sales]]
## Mentions in Source
- "implement client-specific portfolios at the tax-lot level." — [[wiki/sources/at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary-1_b17566|at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary]]
- "Lot-level implementation means making decisions at the individual tax-lot level rather than at the fund or model level." — [[wiki/sources/at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary-1_b17566|at this tax conference-keynote_-after-tax-wealth-management-and-tax-stack-design-summary]]
- "This allows advisors to harvest losses, avoid unnecessary gains, manage transitions, and customize portfolios around client-specific needs." — [[_Inbox/at this tax conference Keynote_ After-Tax Wealth Management and Tax Stack Design-Summary (1)|at this tax conference Keynote_ After-Tax Wealth Management and Tax Stack Design-Summary (1)]]