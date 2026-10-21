---
created: 2026-10-20
updated: 2026-10-20
sources:
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"

generation_complete: true
---

type: concept
created: 2026-10-20
updated: 2026-10-20
sources: ["[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"]
tags: [terminology]
aliases: ["Datasette plugin hooks", "Datasette hooks"]
---

# plugin hook

## Definition

A plugin hook is an extension point in [[Datasette]] that lets plugins register additional behavior, such as extra menu items. Before version 1.0a12, Datasette exposed hooks only for the database and table action menus. Later hooks added support for other page types, extending the [[action buttons]] to more parts of the interface.

## Key Characteristics

- Lets plugins add behavior to Datasette without modifying its core code.
- Commonly used to register extra menu items, such as action buttons.
- Each hook targets a specific page type:
  - `query_actions()`: query pages. Added specifically to support the datasette-create-view plugin.
  - `view_actions()`: view pages.
  - `row_actions()`: row pages.
  - `homepage_actions()`: the homepage.
- Before 1.0a12, only the database and table action menus had hooks.

## Applications

- Adding action buttons to query results, for example a plugin that creates a view from a query.
- Adding action buttons to views, rows, or the homepage, so plugins can offer shortcuts on the page where they are most useful.
- Building extraction or transformation plugins, such as [[datasette-extract]], that surface their actions in the interface.

## Related Concepts

- [[concepts/action-buttons|action buttons]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-extract|datasette-extract]]

## Mentions in Source

- "Prior to 1.0a12 Datasette had plugin hooks for just the database and table actions menus. I’ve added four more:" — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]