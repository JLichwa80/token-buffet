# Outreach Draft — video presentation & blog post

Status: draft. Amplify the `demo/` set into a recorded walkthrough and a written post. Each
section lists options with a **Recommended** pick and the reasoning, so nothing is left open.

---

## 1. Video presentation

**Goal:** 5–7 min screen-recorded walkthrough proving "one engine, many clients/vaults."

### Recommended tools
| Job | Recommended | Alternatives | Why |
|-----|-------------|--------------|-----|
| Screen capture | **OBS Studio** (free, open source) | ScreenToGif (short silent clips), Windows Game Bar (quick, no setup) | OBS does scene switching (dashboard ↔ terminal ↔ Obsidian) + webcam overlay + system audio, all free |
| Editing | **DaVinci Resolve** (free) | CapCut (fast/simple), Clipchamp (built into Win11) | Resolve handles trims, zoom-to-cursor, captions; free tier is enough |
| Zoom/highlight cursor | **Mouseposé-style**: OBS "zoom on cursor" or Resolve keyframe zoom | PowerToys (cursor crosshair) | logs/JSON are small text — zooming is essential on screen |
| Voiceover | record live in OBS | ElevenLabs (scripted narration) | live is faster; scripted if you want polish |

### Structure / shot list (map to `demo/README.md`)
1. **Hook (0:00–0:30)** — "Your Claude/GPT/Gemini subscriptions, behind one OpenAI-compatible
   API — no API keys." One line of what it is.
2. **Start the fleet (0:30–1:15)** — `tbuffet start`; cut to dashboard (8080), all
   providers 🟢. Narrate: proxy per provider, router on 11434, dashboard on 8080.
3. **Register two vaults (1:15–2:30)** — run the two `register.py … vault_type=…` commands;
   show the created `registered_apps/obsidian/<name>/`. Emphasize: *only `vault_type` differs.*
4. **Ingest (2:30–3:30)** — drop/seed `_Inbox/`; show pages appear in Obsidian; call out
   the shared Entity pages (Lena Ortiz / Project Atlas) and the **dedup** on the near-duplicate
   paper.
5. **Query + routing (3:30–4:45)** — ask each vault a question; split-screen the live
   `router/router.log` line `tier 'reasoning' -> claude (Opus) [custom order]`.
6. **Monitor + stop (4:45–6:00)** — dashboard usage/limits, recent requests, logs tree; then
   `Ctrl+C` / Kill. Close on the payoff: two unrelated knowledge bases, one untouched engine.

### Distribution
**Recommended:** YouTube (unlisted first for review → public) + an embed in the blog post.
Alternatives: Loom (fastest, link-only), X/LinkedIn native upload (better reach, worse SEO).

---

## 2. Blog post

**Goal:** the written version of the same story — skimmable, with the architecture diagram and
copy-pasteable commands.

### Recommended platform
| Recommended | Alternatives | Why |
|-------------|--------------|-----|
| **dev.to** | Hashnode (own domain, good dev SEO), Medium (reach, paywall-ish), personal site + static gen | dev.to is free, markdown-native, dev audience, canonical-URL friendly so you can cross-post |

If you have a personal site: write in markdown, publish there as canonical, cross-post to
dev.to/Hashnode with `canonical_url`. Static-site recommendation: **Astro** or **Hugo**.

### Outline
1. **The problem** — you pay for Claude/GPT/Gemini *subscriptions*, but apps want *API keys*.
   Subscriptions have no API. (Hook on the pain.)
2. **The idea** — wrap each vendor's interactive CLI as an OpenAI/Ollama-compatible HTTP
   endpoint; a router maps semantic tiers (fast/medium/reasoning) to whichever subscription has
   quota (or a fixed preference).
3. **Architecture** — the three processes (proxy / router / dashboard) + the extractor
   subsystem that scrapes `/usage` and `/model` from the TUIs. One diagram.
4. **Config-driven, no per-provider code** — adding a provider is a JSON file. Show a provider
   `config.json` snippet (tiers regex, stream extractors).
5. **Demo: one engine, two vaults** — the `demo/` walkthrough; stress that only `vault_type`
   changes. Embed the video here.
6. **Clients** — Obsidian (karpathywiki) today; **claudia** (Claude Code GUI via LiteLLM →
   our router) as a second client. (See [Claudia integration](../integrations/claudia_integration.md).)
7. **Where it goes** — multimodal ingestion (link the proposal). The separate [Graphify project](../../graphify/) tracks the second-brain design.
8. **Caveats / honesty** — TUI scraping is brittle; this rides subscription ToS; not for
   production SLAs. (Credibility.)

### Draft opening (seed — rewrite freely)
> I pay for Claude, ChatGPT, and Gemini every month. All three ship slick CLIs. None of them
> give me an API key I can point my own tools at — that's a separate bill. So I wrote a small
> pure-Python proxy that turns each vendor's *interactive CLI* into a standard
> OpenAI/Ollama-compatible endpoint, and a router that picks the right model for each task from
> whatever subscription still has quota. My Obsidian wiki and my Claude Code GUI now both run
> on it, no API keys involved. Here's how it works — and where it gets sketchy.

### Assets to prepare
- One architecture diagram. **Recommended tool:** Excalidraw (hand-drawn feel, free, exports
  SVG/PNG). Alternatives: Mermaid (inline in markdown, version-controllable), draw.io.
- The provider `config.json` snippet + the two `register.py` commands.
- The embedded video.

---

