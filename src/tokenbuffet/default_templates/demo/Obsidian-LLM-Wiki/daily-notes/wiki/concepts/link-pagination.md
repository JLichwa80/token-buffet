---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "HTTP link header pagination"
  - "Link header pagination"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# link pagination

## Definition

Link pagination is a pattern in JSON APIs where the HTTP `Link` header indicates the URLs of the next and last pages of results. A client follows the `next` URL repeatedly until no further pages remain.

## Key Characteristics

- Pagination links are delivered in the HTTP `Link` response header rather than in the response body.
- The header identifies the next page and the last page of results.
- Clients iterate by requesting the `next` URL until it is absent.
- The [[Datasette]] JSON API supports this pattern.
- The GitHub API uses this pattern.

## Applications

- Retrieving every record from a paginated JSON API by following `next` links until the result set is exhausted.
- Automating full-collection exports with [[paginate-json]], which fetches every page and combines the results into a single JSON array or a newline-delimited stream.

## Related Concepts

## Related Entities

- [[entities/paginate-json|paginate-json]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "There’s a neat pattern in some JSON APIs where the [HTTP link header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link) is used to indicate subsequent pages of results." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]