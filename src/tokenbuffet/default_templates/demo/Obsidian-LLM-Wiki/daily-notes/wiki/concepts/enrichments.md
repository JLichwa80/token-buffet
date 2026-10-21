---
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-11-22-weeknotes_49168f]]"

generation_complete: true
---

type: concept
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2023-11-22-weeknotes_49168f]]"]
tags: [idea]
aliases: ["Datasette enrichments", "datasette-enrichments"]
---

# enrichments

## Definition

Enrichments are a [[Datasette]] feature for applying enrichment operations, such as geocoding, language model prompt evaluation, and OCR, to rows stored in Datasette. The feature is developed alongside the datasette-enrichments plugin, which was released as version 0.1a4 on 20 November 2023.

## Key Characteristics

- Operates on rows of data already stored in Datasette.
- Enrichment operations named in the source include geocoding, evaluating prompts with a language model (see [[GPTs]]), and OCR.
- Implemented as the datasette-enrichments plugin; version 0.1a4 was released on 20 November 2023.
- Long-anticipated feature: the author states they have wanted to build it for a couple of years and began implementing it in the post's period.
- Described in the source as the main new Datasette feature introduced in the post, with more detail promised in a later update.

## Applications

- Geocoding location data stored in Datasette tables.
- Running language model prompts over rows, using [[GPTs]] as the model family referenced in the source.
- Running OCR over rows that reference scanned or image content.

## Related Concepts

- [[concepts/gpts|GPTs]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/alex-garcia|Alex Garcia]]

## Mentions in Source

- "Meanwhile I’ve been putting together the first working version of *enrichments*—a feature I’ve been threatening to build for a couple of years now." — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]
- "The key idea here is to make it easy to apply enrichment operations—geocoding, language model prompt evaluation, OCR etc—to rows stored in Datasette." — [[_Inbox/2023-11-22-weeknotes|2023-11-22-weeknotes]]