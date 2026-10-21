---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "--get option"
  - "Datasette --get"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# datasette --get

## Definition

`datasette --get` is a command-line option of [[Datasette]] that simulates an HTTP request against a Datasette instance and prints the response, without starting a web server on a port. Version 1.0a5 added an `--actor` option that runs the simulated request as a specific actor.

## Key Characteristics

- Simulates an HTTP GET request through a Datasette instance from the command line.
- Does not start a server or bind to a port.
- Supports an `--actor` option (added in 1.0a5) so the simulated request runs as a named actor, allowing authentication and permission behavior to be tested.
- Originated as a debugging helper during work on restricted API tokens.

## Applications

- Generating social media card images for Simon Willison's TILs website.
- Testing how a Datasette instance responds to requests made as a specific actor, to verify authentication and permissions without running a server.

## Related Concepts

## Related Entities

- [[entities/datasette|Datasette]]

## Mentions in Source

- "The `datasette --get /...` option is a neat trick that can be used to simulate an HTTP request through the Datasette instance, without even starting a server running on a port." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]