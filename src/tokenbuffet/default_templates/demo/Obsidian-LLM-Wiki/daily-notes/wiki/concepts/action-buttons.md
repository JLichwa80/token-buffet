---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [terminology]
aliases:
  - "Action menu"
  - "Datasette action buttons"
sources:
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"

generation_complete: true
---

# action buttons

## Definition

Action buttons are the clickable menus in [[Datasette]] that expose actions registered by plugins on database, table, query, and other pages. Before Datasette 1.0a12, these actions were hidden behind a cog icon. In 1.0a12 and 1.0a13, the cog was replaced with a clearer button.

## Key Characteristics

- Expose [[plugin hook|plugin-registered]] actions on several page types, including database, table, and query pages.
- Replaced a cog icon that the author considered not discoverable enough and similar to "mystery meat navigation."
- Menu items can include an optional description shown below the item's label.
- The redesign was the main theme of the two 1.0 alpha releases (1.0a12 and 1.0a13) covered in the source.

## Applications

- Letting users find plugin-provided actions on database, table, and query pages without guessing what an icon does.
- Plugin authors adding actions that appear in the menu, with descriptions to explain each item.
- Used in [[Datasette Cloud]] as well as the open-source Datasette project.

## Related Concepts

- [[concepts/plugin-hook|plugin hook]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "The main theme of these two releases was improvements to Datasette’s “action buttons”." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "The cog wasn’t discoverable enough, and felt too much like mystery meat navigation. I decided to turn it into a much more clear button." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]