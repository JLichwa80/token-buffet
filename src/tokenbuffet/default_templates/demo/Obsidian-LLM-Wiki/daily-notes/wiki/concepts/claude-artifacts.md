---
type: concept
created: 2026-10-20
updated: 2026-10-20
generation_complete: true
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"
  - "[[sources/2024-07-02-weeknotes_55c009]]"
tags:
  - "reference"
  - "terminology"
aliases:
  - "Artifacts"
  - "artifacts feature"
---

# Claude Artifacts

## Definition

Claude Artifacts is an [[Anthropic]] feature that presents generated code or documents as an interactive artifact the user can run and modify, rather than as plain chat text.

## Key Characteristics

- Renders generated output as a runnable, editable artifact inside the Claude interface.
- Works well with single-file vanilla HTML and JavaScript apps, where all code sits in one file that can be pasted back into the model for changes.
- Avoids a build step: the author has to instruct the model "no React" to get an artifact that can be edited without configuring a React build toolchain.
- Makes LLM-generated front-end code directly usable and iterable by the user.
Artifacts is a capability of Claude 3.5 Sonnet, which writes HTML, CSS and JavaScript and displays the result directly. The existing section doesn't name the model, so this is new.
## Applications

- Prototyping small single-file HTML/JavaScript tools by generating them with an LLM and then iterating on them in the artifact view.
- Producing runnable front-end demos or utilities without setting up a local project or bundler.
- Steering the model's output format (for example, requesting plain HTML/JS instead of React) so the result is easy to modify by hand.
- Simon Willison used artifacts to build "quite a sophisticated animated visualization" that he showed in his AI Engineer World's Fair keynote.
## Related Concepts

## Related Entities

- [[entities/anthropic|Anthropic]]

## Mentions in Source

- "This approach also works really well with [Claude Artifacts](https://simonwillison.net/tags/claude-artifacts/), though I have to tell it “no React” to make sure I get an artifact I can hack on without needing to configure a React build step." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]
- "I’ve also been thoroughly enjoying the new artifacts feature where it can write and then display HTML/CSS/JavaScript—I’ve used that for several prototyping projects as well as quite a sophisticated animated visualization I used in my keynote last week." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]