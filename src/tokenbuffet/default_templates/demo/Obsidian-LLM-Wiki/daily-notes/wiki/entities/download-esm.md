---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "download-esm tool"
  - "download-esm CLI"
sources:
  - "[[sources/2023-05-10-weeknotes_35d224]]"

generation_complete: true
---

# download-esm

## Description

download-esm is a Python command-line tool written by the author to download the ECMAScript module (ESM) versions of an npm package, together with all of their module dependencies. The author built it as part of an ongoing effort to write modern JavaScript without depending on JavaScript build tools. A separate post explaining the justification for the tool was published on 2023-05-02. The tool is one of the three main threads of the author's weeknotes from that week, alongside sqlite-utils and the Pyodide sandbox. It connects to the broader goal of working with [[ECMAScript modules]] directly.

## Related Entities

## Related Concepts

- [[concepts/ecmascript-modules|ECMAScript modules]]

## Mentions in Source

- "As part of my ongoing mission to figure out how to write modern JavaScript without surrendering to one of the many different JavaScript build tools, I built [download-esm](https://github.com/simonw/download-esm)—a Python CLI tool for downloading the ECMAScript module versions of an npm package along with all of their module dependencies." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]