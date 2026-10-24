# Roadmap
- Evaluate multiple-account per LLM provider options
- Graphify with Obisidian Docs
- Ideas Board (Wordpress)
- Portal for sharing knowledge

---


# Pending engineering (bigger items)
- Multimodal ingestion — see proposal below. NOT STARTED: no `execution.attachments` in the proxy or any provider config; `analyzeEmbeddedImages` is still `false` in the demo `data.json`.

---

# Router — known concerns (see [router.md](../infrastructure/router.md) for current behavior)
- **`USAGE` quota cache is only as fresh as the refresh interval.** Remaining-quota is cached in
  memory, loaded at startup and refreshed on the `--refresh-interval` timer (default 30 min). A
  provider that hits 0 tokens *mid-interval* won't be skipped until the next refresh, so a request
  can still be routed to an already-depleted backend (the proxy/CLI then fails and the loop falls
  through). Matches the "cached, not inline-scraped" design; tighten the interval, or refresh
  `USAGE` on a quota-exhaustion response, if this becomes a problem.

---

# Proposal (future): multimodal ingestion — let models process images & PDFs

## Problem
The models themselves (Sonnet/Opus, GPT, Gemini) are natively multimodal — they read
images and PDFs. The ONLY thing blocking it is our invocation layer: the proxy flattens
every request to text and drops non-text parts before shelling to the CLI
(`src/tokenbuffet/cli_proxy_server.py`, the content-list flatten ~L234-237). So the
plugin's `analyzeEmbeddedImages` and native-PDF features send image/PDF content that the
proxy silently discards — the model never sees it. This is a quality ceiling for
chart/slide/table-heavy conference decks.

Key fact: the plugin sends local images/PDFs as **base64 content parts inline** (remote
URLs are never downloaded). So the proxy receives *bytes*, not a path — "forwarding a
path" means decode the bytes to a temp file, then pass that path to the CLI.

## What each CLI accepts (researched)
| CLI            | Images | PDFs | Mechanism                              |
|----------------|--------|------|----------------------------------------|
| claude         | yes    | no   | `--image <path>` (repeatable), works in headless/print |
| agy / gemini   | yes    | yes  | `@<path>` injected into the prompt text |
| codex          | buggy  | no   | `codex exec --image` **hangs with `--json`** (openai/codex #5773) — skip |
| grok           | no     | no   | no documented file input — skip        |

Native Claude/GPT *PDF* only exists via their HTTP APIs (document block), not the CLIs —
and using the API defeats the subscription-CLI design. So PDF-through-subscription =
Gemini `@file`, or convert first with MinerU (self-hosted for confidential docs).

## Ideal design (config-driven, engine stays generic)
Add an OPTIONAL per-provider `execution.attachments` block. Absent = today's behavior
exactly (non-text dropped), so every existing provider is unchanged.

```jsonc
// claude/config.json  — argv-flag delivery
"execution": { "attachments": { "mode": "arg",    "arg": ["--image", "{file}"], "accept": ["image"] } }
// agy/config.json     — prompt-injection delivery (@path)
"execution": { "attachments": { "mode": "prompt", "inject": "@{file}",          "accept": ["image","pdf"] } }
```

Proxy change (~30 lines, all gated on `attachments` being present):
1. While flattening `content`, keep text parts as today; for image/pdf parts, base64-decode
   to a temp file (suffix from the MIME type) and collect the path.
2. Deliver by mode:
   - `arg`: append `arg` (with `{file}` substituted) to argv, once per file.
   - `prompt`: append `inject` (`@{file}`) to the prompt text — must happen BEFORE the
     `{prompt}`/prompt-file is materialized.
3. Add the temp files to the existing `cleanup()`.
Supported wire shapes to parse: OpenAI chat `image_url`, OpenAI Responses `input_image`,
Anthropic `image` + `source.data`.

## Routing caveat (don't forget)
Image requests ride the **ingest tier (`fast`)**. In `usage` mode they can land on grok
(no vision) and be wasted. Fixes:
- Prefer a vision backend: the router `mode: custom`, claude-first change already routes
  `fast` -> claude Haiku (vision-capable). OR
- Teach the router to restrict to vision-capable providers when the payload has image parts.

## Rollout
1. Implement `attachments` in the proxy (config-gated, default no-op).
2. Add the block to `claude` (images); probe whether the `agy` binary honors `@file`
   (google gemini-cli does; antigravity fork unverified) before adding it there (images+PDF).
3. Ensure routing sends image requests to a vision backend (custom-mode claude-first).
4. Only then flip `analyzeEmbeddedImages` + `saveEmbeddedImageEvidence` back to `true` in
   the Obsidian `data.json`. (Kept OFF until this lands — otherwise images are stripped.)

## Open questions
- Does the `agy`/antigravity CLI accept `@file` like upstream gemini-cli? (probe)
- PDF strategy: native via Gemini `@file` vs MinerU conversion (tables->HTML, formulas->
  LaTeX may be higher-fidelity for data-dense decks than vision-by-eye). Possibly both.
- Size limits: claude piped stdin caps ~10MB; attachments via file path avoid that, but
  confirm per-CLI image size ceilings.

Sources: Claude Code `--image`/headless (code.claude.com/docs/en/headless);
codex `--image`+`--json` hang (github.com/openai/codex/issues/5773); gemini-cli `@file`
multimodal (til.simonwillison.net/llms/prompt-gemini); MinerU (github.com/opendatalab/mineru).
