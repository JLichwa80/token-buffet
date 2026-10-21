---
type: concept
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-10-22-weeknotes_1435b6]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "terminology"
aliases:
  - "Datasette plugin ecosystem"
---

# Datasette plugins

## Definition

Datasette plugins are extensions that add features to [[Datasette]]. In the 2023-10-22 weeknotes, they include Python plugins and, for the first time, JavaScript plugins that modify the Datasette interface. The goal described in the post is to let plugins work together rather than in isolation, and the [[JavaScript plugin API]] was added to support this.

## Key Characteristics

- Extend Datasette with new features, and come in Python and JavaScript forms.
- JavaScript plugins can modify the Datasette interface through hooks for custom panels and column menu actions.
- Plugins can share the same interface area; Datasette shows them in a tabbed view when several plugins use the same panel.
- Designed to interact with one another, not only to run in isolation.

## Applications

- Adding custom panels above the table view, with tabbed switching between plugins that share the area.
- Adding extra actions to the column action menu.
- Building an ecosystem of extensions that build on each other within the Datasette interface.

## Related Concepts

- [[concepts/javascript-plugin-api|JavaScript plugin API]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/cameron-yick|Cameron Yick]]

## Mentions in Source

- "The key idea here is to provide much richer support for Datasette plugins that use JavaScript to modify the Datasette interface." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]
- "In particular, we want plugins to be able to collaborate with each other." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]