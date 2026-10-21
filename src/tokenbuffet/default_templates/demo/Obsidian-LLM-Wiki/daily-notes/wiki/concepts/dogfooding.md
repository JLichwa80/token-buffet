---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "Eating your own dog food"
sources:
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"

generation_complete: true
---

# Dogfooding

## Definition

Dogfooding is the practice of using your own product. Teams that dogfood use the software they build in their own daily work, so they experience its strengths and weaknesses directly. In the source, the author uses [[Datasette Cloud]] to run analytics on [[Datasette Cloud]] itself, which ties the analytics tooling to the product's own development.

## Key Characteristics

- Uses the product in real work rather than only in testing.
- Turns the builder's own needs into a source of product feedback.
- Connects operational analytics to the product's development.
- Treated by the author as a guiding value across the [[Datasette]] ecosystem.

## Applications

- Running product analytics on the product's own hosted instance, as the author does with [[Datasette Cloud]].
- Building plugins for internal needs first, such as the `datasette-events-forward` plugin, which the author cites as a pleasing example of the practice. It relies on [[Datasette Events]].
- Using the same tools that customers use to monitor and improve the product.

## Related Concepts

- [[concepts/datasette-events|Datasette Events]]

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "Using Datasette Cloud for analytics for Datasette Cloud is a pleasing exercise in dogfooding." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]