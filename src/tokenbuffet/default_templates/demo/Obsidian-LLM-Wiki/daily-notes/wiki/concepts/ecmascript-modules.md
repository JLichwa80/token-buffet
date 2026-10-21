---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "ES modules"
  - "ESM"
sources:
  - "[[sources/2023-05-10-weeknotes_35d224]]"

generation_complete: true
---

# ECMAScript modules

## Definition

ECMAScript modules (ES modules, ESM) are the standard module format for JavaScript. They are the ECMAScript-standardized way to organize and share JavaScript code across files and packages. In the source, the ECMAScript module versions of npm packages are the target output of the [[download-esm]] tool.

## Key Characteristics

- The standard module format for JavaScript, defined by ECMAScript.
- A package is available in ECMAScript module form, distinct from other module formats.
- A package's ECMAScript module version depends on other modules, so the dependencies must be fetched along with it.
- Using them directly in the browser or runtime avoids the need for a bundler or other [[JavaScript build tools]].

## Applications

- Writing modern JavaScript without relying on build tools. The source describes this as the author's central goal, and ECMAScript modules are central to it.
- Downloading npm packages in ECMAScript module form, with all of their module dependencies, using [[download-esm]].

## Related Concepts

## Related Entities

- [[entities/download-esm|download-esm]]

## Mentions in Source

- "I wrote more about my justification for building that tool in [download-esm: a tool for downloading ECMAScript modules](https://simonwillison.net/2023/May/2/download-esm/)." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]