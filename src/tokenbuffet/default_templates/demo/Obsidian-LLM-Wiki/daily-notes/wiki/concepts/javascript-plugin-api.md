---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Javascript Plugin API"
  - "JS plugin API"
sources:
  - "[[sources/2023-10-22-weeknotes_1435b6]]"

generation_complete: true
---

# JavaScript plugin API

## Definition

The JavaScript plugin API is a [[Datasette]] feature, authored by [[Cameron Yick]], that lets plugins use JavaScript to modify the Datasette interface. It adds a hook for custom panels above the main table view, shares that area between plugins through an automatic tabbed interface, and adds options to the column action menu, similar to the existing table and database action menu hooks.

## Key Characteristics

- Lets plugins modify the Datasette user interface with JavaScript.
- Provides a hook for adding custom panels above the main table view.
- Groups panels from multiple plugins into an automatic tabbed interface in that area.
- Adds extra options to the column action menu, parallel to the existing table and database action menu hooks.
- Its mechanism is inspired by Python's pluggy, and it is designed so plugins can collaborate with each other.
- At the time of the source, [[Simon Willison]] hoped to add documentation and example plugins before the next Datasette alpha release.

## Applications

- Adding custom visual panels or summaries above a table view in Datasette.
- Letting several plugins contribute panels to the same table view without conflicting, through the tabbed interface.
- Adding per-column actions to the column action menu, for example to run a plugin's operation on a single column.

## Related Concepts

- [[concepts/datasette-metadata|Datasette metadata]]

## Related Entities

- [[entities/cameron-yick|Cameron Yick]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "His [Javascript Plugin API (Custom panels, column menu items with JS actions)](https://github.com/simonw/datasette/pull/2052) pull request has been brewing for months." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]
- "It introduces a hook for adding a custom panel to the Datasette interface, displayed above the main table view." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]