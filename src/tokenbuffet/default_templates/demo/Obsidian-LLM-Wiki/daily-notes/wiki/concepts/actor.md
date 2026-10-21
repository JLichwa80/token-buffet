---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Datasette actor"
  - "--actor option"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# actor

## Definition

In [[Datasette]], an actor is the identity on whose behalf a request is made. The actor drives authentication and permission checks, so it determines what a request is allowed to do.

## Key Characteristics

- Represents the identity behind a request, used for authentication and authorization.
- Is the input to Datasette's permission checks.
- Can be simulated from the command line with the `--actor` option when running `datasette --get`.
- Lets developers test configured authentication and permissions without starting a server.
- Is part of the permissions work in the 1.0a5 release, alongside [[finely-grained permissions]].

## Applications

- **Testing permissions:** A developer runs `datasette --get` with `--actor` to check what a given identity can access, without starting a server.
- **Testing authentication:** Developers can verify that a configured authentication setup produces the expected actor for a request.
- **Developing permission rules:** Fine-grained permission rules can be checked against different actors while the rules are being written.

## Related Concepts

- [[concepts/finely-grained-permissions|finely-grained permissions]]

## Related Entities

- [[entities/datasette|Datasette]]

## Mentions in Source

- "The new `--actor` option lets you add a simulated [actor](https://docs.datasette.io/en/latest/authentication.html#actors) to the request, which is useful for testing out things like configured authentication and permissions." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]