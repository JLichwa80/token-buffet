---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "JavaScript bundlers"
  - "JS build tools"
sources:
  - "[[sources/2023-05-10-weeknotes_35d224]]"

generation_complete: true
---

# JavaScript build tools

## Definition

JavaScript build tools are the bundlers and toolchains that developers commonly use to prepare modern JavaScript for use in the browser. They transform and combine source code and its dependencies into files a browser can load.

## Key Characteristics

- Prepare modern JavaScript for browser execution through a build step that runs before deployment.
- Include bundlers and wider toolchains, which can be numerous and complicated to set up and maintain.
- Are the default workflow for many developers writing modern JavaScript.
- Can be avoided when browser code loads [[ECMAScript modules]] directly, without a build step.

## Applications

- **Bundling application code:** Combining many source files and npm dependencies into a small number of files for the browser.
- **Avoiding build complexity:** Writing modern JavaScript without depending on a build toolchain. [[download-esm]] supports this by downloading ECMAScript module versions of npm packages along with their module dependencies, so browser code can import them directly.
- **Simplifying workflows:** Used as a reference point in the broader search for a simpler way to develop browser JavaScript.

## Related Concepts

- [[concepts/ecmascript-modules|ECMAScript modules]]

## Related Entities

- [[entities/download-esm|download-esm]]

## Mentions in Source

- "As part of my ongoing mission to figure out how to write modern JavaScript without surrendering to one of the many different JavaScript build tools, I built [download-esm](https://github.com/simonw/download-esm)—a Python CLI tool for downloading the ECMAScript module versions of an npm package along with all of their module dependencies." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]