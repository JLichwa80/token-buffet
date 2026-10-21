---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "database-backed access tokens"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

generation_complete: true
---

# database-backed access tokens

## Definition

Database-backed access tokens are API tokens that are stored in a database and checked against it, rather than being self-contained signed tokens. Because the server holds the token record, it can revoke a token on demand and record when the token was last used.

## Key Characteristics

- Stored server-side in a database, so each token has a record that can be looked up and updated.
- Can be revoked individually when access needs to end.
- Can record the time of most recent use.
- Requires a database lookup on each request, which trades away the statelessness of signed tokens.

## Applications

- Datasette Cloud issues these tokens so that users can revoke a token when needed.
- The datasette-auth-tokens plugin implements this design, adding revocation and last-used tracking to token authentication.

## Related Concepts

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "Datasette Cloud’s API works using database-backed access tokens, to ensure users can revoke tokens if they need to (something that’s not easily done with purely signed tokens) and that each token can record when it was most recently used." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]