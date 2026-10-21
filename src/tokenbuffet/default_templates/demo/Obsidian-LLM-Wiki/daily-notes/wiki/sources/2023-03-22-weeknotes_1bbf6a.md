---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "2023-03-22-weeknotes"
  - "Simon Willison Weeknotes"
  - "22 March 2023"
contentHash: 2d8e-035f9ef7
source_file: "[[_Inbox/2023-03-22-weeknotes.md]]"
generation_complete: true
---

# 2023-03-22-weeknotes - Summary

## Source

- Original file: [[_Inbox/2023-03-22-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

Simon Willison's weeknotes for 22 March 2023 cover three threads. First, AI announcements keep arriving fast, with many launches landing on Tuesdays, and he lists six AI posts from the month. Second, he launched a [[concepts/my-blog-as-a-newsletter|blog-as-a-newsletter]] on [[entities/substack|Substack]], which had reached 640 subscribers. He started it when [[entities/twitter|Twitter]] looked unstable. Because Substack has no API, he assembles each issue with the [[entities/blog-to-newsletter|blog-to-newsletter]] notebook on [[entities/observable|Observable]], which queries his [[entities/datasette|Datasette]] instance and is then pasted into Substack. Third, he describes a large Datasette branch that redesigns the default JSON format into a simpler object with `ok`, `next` and `rows` keys, with extras requested through `_extra`. He asks for feedback before [[entities/datasette-1-0|Datasette 1.0]]. The post closes with recent Datasette plugin releases, including [[entities/datasette-atom|datasette-atom]], which adds Atom output, and recent TIL articles. It also links his [[concepts/atom-feed|Atom feed]] as a subscription option.

## Key Entities

- [[entities/datasette|Datasette]]: the open source data tool at the center of the JSON redesign
- [[entities/datasette-1-0|Datasette 1.0]]: the planned release that the JSON redesign must precede
- [[entities/datasette-atom|datasette-atom]]: a Datasette plugin that adds an Atom output format
- [[entities/blog-to-newsletter|blog-to-newsletter]]: the Observable notebook that assembles the newsletter
- [[entities/observable|Observable]]: the notebook platform hosting the newsletter tool
- [[entities/substack|Substack]]: the newsletter platform, which has no API
- [[entities/twitter|Twitter]]: cited as the motivation for starting the newsletter
- [[entities/google-bard|Google Bard]]: one of the AI launches mentioned that week

## Key Concepts

- [[concepts/weeknotes|Weeknotes]]: the recurring blog format this post belongs to
- [[concepts/my-blog-as-a-newsletter|My blog as a newsletter]]: the idea of delivering blog posts by email
- [[concepts/large-language-models|Large language models]]: the AI systems behind most of the month's launches
- [[concepts/atom-feed|Atom feed]]: the syndication format offered as a subscription option
- [[concepts/stable-diffusion-moment|Stable Diffusion moment]]: the framing of the LLM acceleration in his earlier posts
- [[concepts/react-pattern|ReAct pattern]]: a Python implementation of the pattern for LLMs, covered in a linked TIL

## Main Points

- **AI announcements are accelerating.** Many launches land on Tuesdays, and the author expects them to continue for years.
- **A new email newsletter delivers the blog.** It reached 640 subscribers and is sent roughly weekly when there is material.
- **The newsletter is built by copy and paste.** The blog-to-newsletter notebook queries Datasette and produces HTML that is pasted into Substack, where it is edited and given extra commentary.
- **The Datasette JSON format is redesigned.** The old default had dozens of keys and array-based rows. The new default returns `ok`, `next` and `rows`, with extras requested via `_extra`.
- **The redesign is a prerequisite for Datasette 1.0.** Documentation and the effect on the arbitrary SQL query endpoint remain unfinished, and the author asks for feedback.

## Mentions in Source

- "I’m a few weeks behind on my [weeknotes](https://simonwillison.net/tags/weeknotes/), but it’s not through lack of attention to my blog." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "Apparently this blog is now partly focused on AI!" — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "I started it a few months ago when it looked like Twitter was about to collapse under the weight of its new mismanagement." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "I finally landed [a GIANT branch](https://github.com/simonw/datasette/pull/1999) I’ve been working on for several months now: a complete redesign of Datasette’s default JSON format, one of the largest changes I need to land prior to releasing Datasette 1.0." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "I always found myself adding `?_shape=array` to that URL to get a smalle format, which strongly indicated that the default I had picked was the wrong one." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "**[datasette](https://github.com/simonw/datasette)**: [0.64.2](https://github.com/simonw/datasette/releases/tag/0.64.2)—([125 releases total](https://github.com/simonw/datasette/releases))—2023-03-08" — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "[observablehq.com/@simonw/blog-to-newsletter](https://observablehq.com/@simonw/blog-to-newsletter) is an Observable notebook I wrote which assembles most of the newsletter for me." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "I built myself an automation around copy and paste!" — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]
- "This is working *really well* so far—it’s really easy to tweak the generated HTML in the Observable notebook, and once I’ve transferred it to Substack I can re-arrange things and add my own extra commentary to the top of the newsletter before hitting send." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]