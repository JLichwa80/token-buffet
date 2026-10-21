---
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"

generation_complete: true
---

type: concept
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2023-08-05-weeknotes-plugins_fc2660]]"]
tags: [terminology]
aliases: ["API key", "API key mechanism"]
---

# API tokens

## Definition

API tokens are credentials that authenticate access to Datasette instances. They can be created and revoked interactively, and they gate access to the [[write API]].

## Key Characteristics

- Authenticate requests to a Datasette instance.
- Can be created and revoked interactively by the user.
- Gate write access to the [[write API]].
- Were added through the [[Plugins|plugin]] datasette-auth-tokens, released in preview.

## Applications

- Datasette Cloud users create API tokens so that automatic data imports can authenticate and write data.
- Revoking a token cuts off the import access that uses it.

## Related Concepts

- [[concepts/write-api|write API]]
- [[concepts/plugins|Plugins]]

## Related Entities

- [[entities/datasette-auth-tokens|datasette-auth-tokens]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "This meant I needed an API key mechanism that allowed tokens to be both created and revoked interactively." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "Datasette plugin for authenticating access using API tokens" — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]