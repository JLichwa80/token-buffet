---
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-11-22-weeknotes_49168f]]"
tags:
  - "terminology"
---

# text-to-speech

## Definition

Text-to-speech (TTS) is the conversion of written text into spoken audio. In the December 2023 weeknotes, it is the function of the [[entities/ospeak|ospeak]] command-line tool, which sends text to a text-to-speech service and returns audio.

## Key Characteristics

- Takes written text as input and produces spoken audio as output.
- Delivered as a remote service call: the CLI tool runs the text through a text-to-speech service.
- Model choice affects output quality. The `tts-1-hd` model option produces higher-quality audio than the default.
- Presented in the source as a practical command-line capability, not as a topic in its own right.
- Exposed through OpenAI's text-to-speech API, which was new at the time; Simon Willison built ospeak, a CLI tool for working with it, announced at OpenAI DevDay in November 2023.
- In the 2023-11-22 weeknotes, Willison describes OpenAI's text-to-speech API as excellent. He built ospeak that same evening, on the day of DevDay (7 November 2023), as a CLI for working with the API.

## Applications

- Reading text aloud from a terminal, via command-line tools such as [[entities/ospeak|ospeak]].
- Selecting a higher-quality model (`tts-1-hd`) when audio quality matters more than speed or cost. Support for this option was added in ospeak 0.3 (December 2023).
- Part of a wider set of AI-backed command-line tools. The author maintained several such tools that month, alongside the [[concepts/llm-plugin-system|LLM plugin system]] work.
- ospeak 0.2 was released on 2023-11-07 as a CLI tool for running text through OpenAI Text to speech, before the 0.3 release that added the `tts-1-hd` option in December 2023.

## Related Concepts

- [[concepts/llm-plugin-system|LLM plugin system]]

## Related Entities

- [[entities/ospeak|ospeak]]
- [[entities/openai|OpenAI]]
- [[entities/openai-devday|OpenAI DevDay]]

## Mentions in Source

- "My [ospeak](https://github.com/simonw/ospeak) tool for running text-to-speech on the command-line now supports `-m tts-1-hd` for higher quality output, thanks to a [PR](https://github.com/simonw/ospeak/pull/5) from Mikolaj Holysz." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "**[ospeak 0.3](https://github.com/simonw/ospeak/releases/tag/0.3)**—2023-12-13  
  CLI tool for running text through OpenAI Text to speech" — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]