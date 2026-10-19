# Consumer routing roadmap — everyday apps on the local router

Status: research + roadmap (live). Consolidates the earlier `consumer_use_cases.md` and
`ollama_routable_apps.md` archive notes. Target audience: **regular, non-technical people** — not
developers. Which mainstream AI apps can run on our bridge instead of a vendor cloud, and in what order
to wire them up.

## The one fact that makes this possible

Our router answers both the **Ollama** API (`/api/chat`, `/api/generate`) and the
**OpenAI-compatible** API (`/v1/chat/completions`) on **port 8090**. Any app that exposes a
"custom base URL + API key" or "Ollama host" field points at us with a two-line change — the same way
apps target Ollama / LM Studio today — and gets *subscription-backed* Claude / GPT / Gemini / Grok
instead of a small local model.

**Value proposition for a regular person:** private, **subscription-powered** AI across the apps they
already use — no API keys to buy, no per-token bill, and (uniquely) *best-model-per-task* because our
router can send each request to Claude / GPT / Gemini / Grok depending on the tier.

### Universal config rule for every routable app

- **Endpoint:** `http://127.0.0.1:8090` (Ollama host) or `http://127.0.0.1:8090/v1/chat/completions`
  (OpenAI-compat).
- **Model name:** set it to one of our tiers — `fast` / `medium` / `reasoning` (the router routes by
  that, not by a real model id). Unknown names default to a tier, and the model-list endpoints
  (`/v1/models`, Ollama `/api/tags`) advertise the tiers, so a dropdown populates cleanly.
- **API key:** none needed — use any dummy (e.g. `ollama`).

## The hard constraint — set expectations honestly

The **biggest** consumer AI apps are **cloud-locked**: they do not let you change the endpoint, so they
**cannot** be routed to our bridge. The routable universe is (1) apps built around a bring-your-own-endpoint
model, and (2) thin apps we build ourselves.

| Top consumer AI app (2026) | Category | Routable to us? |
|----------------------------|----------|-----------------|
| ChatGPT | chatbot | ✗ cloud-locked |
| Gemini | chatbot | ✗ |
| Claude (claude.ai) | chatbot | ✗ (but the *CLI* is our backend) |
| Perplexity | search | ✗ |
| Canva (Magic) | design | ✗ |
| CapCut | video | ✗ |
| Grammarly | writing | ✗ |
| Notion AI | notes | ✗ |
| Otter.ai | transcription | ✗ |
| ElevenLabs / Suno | voice / music | ✗ (not text LLMs) |
| **Opera** | browser | ✗ ships built-in local LLMs but exposes **no** custom-endpoint field |

So the play is **not** "redirect ChatGPT." It's "give regular people the same everyday capabilities through
apps that *can* point at our bridge." (Sources: a16z Top 100, backlinko.)

## Routable targets — the Top 10 (consumer-facing)

Apps worth making `integrations/` app types, because they have **built-in AI that can be pointed at an
Ollama/OpenAI endpoint**:

| # | App | Built-in AI feature | How to point it at us | Fit |
|---|-----|---------------------|----------------------|-----|
| 1 | **Obsidian** | notes Q&A, wiki, autocomplete (our karpathywiki, Copilot, Ollama Assistant, AI Providers) | plugin's Ollama/base-URL field → `:8090`; model = tier | ★★★ our flagship, done |
| 2 | **Brave browser (Leo)** | BYOM assistant: summarize pages, chat, ask-the-web | Leo → Bring Your Own Model → `http://127.0.0.1:8090/v1/chat/completions`, model = `reasoning` | ★★★ one field, huge reach |
| 3 | **Raycast** | system-wide AI commands (Mac + Windows) | AI → Local Models / Custom Provider → Ollama host `:8090`; model = tier | ★★★ |
| 4 | **Home Assistant** | voice assistant / conversation agent (native Ollama integration, 2025.6+) | add Ollama integration → URL `:8090`, model = tier | ★★★ "talk to your house," demo-friendly |
| 5 | **Joplin** | note chat, summaries (Jarvis, NoteLLM, Joplin AI Agent) | plugin → `:8090/v1`; model = tier | ★★ open-source notes |
| 6 | **Logseq** | writing assistant (logseq-copilot / AI plugin) | plugin → Ollama `:8090/v1`; model = tier | ★★ |
| 7 | **Thunderbird** | draft/summarize email (Ollama Compose extension) | extension → Ollama `:8090`; model = tier | ★★ everyday email |
| 8 | **AnythingLLM** | private "chat with my documents" + agents | LLM provider → Ollama/Generic OpenAI `:8090`; model = tier | ★★ school-papers use-case |
| 9 | **Enchanted / Msty** | friendly native desktop/iOS assistant over an Ollama host | set Ollama server `:8090`; model = tier | ★★ non-tech-friendly front-ends |
| 10 | **claudia (Claude Code)** | the local "second brain" | `settings.local.json` base-URL → us; see [Claudia integration](claudia_integration.md) | ★★ our 2nd app type |

## Delivery model for non-tech people

They will never edit YAML or a `base_url`. Our `integrations/` framework + a one-click dashboard action does
the wiring (exactly like the obsidian / claudia app types). Three delivery tiers:

- **A — Configure an existing routable app** (lowest effort): flip its endpoint to our router.
- **B — Build a thin friendly integration** (our own small app) where no consumer app routes.
- **C — Can't route** (cloud-locked): document it so nobody expects it.

## Use-case proposals (prioritized by value ÷ effort)

1. **Unified cross-provider chat** — *Tier A, build-effort: tiny, value: highest.* One ChatGPT-style window
   that quietly uses *all* their subscriptions, picking the best model per task via our tiers. Zero new
   code, just a configured frontend. **Recommended:** **Open WebUI** (self-hostable, OpenAI-compatible, RAG,
   voice, multi-user) or **Jan** / **ChatBox** / **Msty** for a pure desktop app. Point its OpenAI endpoint
   at `http://127.0.0.1:8090/v1`; models become `fast`/`medium`/`reasoning`.
2. **Journals & notes** — *Tier A, value: high (engine already exists).* Our **Obsidian + karpathywiki**
   vault (the `demo/` set), plus **Plume** (Mac journaling, any OpenAI-compatible endpoint). Alternatives:
   **JournalLM**, **Memex**, **Logseq**.
3. **Documents / school papers** — *Tier A/B.* **AnythingLLM** (private chat over a folder of documents) for
   "ask my papers"; our Obsidian wiki for the organized, linked view.
4. **Email assistant** — *Tier A, build-effort: small.* **Thunderbird + "Ollama Compose"** (free; right-click
   an email → draft a reply). Tier-B fallback: a thin IMAP script (fetch unread → router → save draft).
5. **Social posts (FB / IG / X)** — *Tier B, build-effort: medium.* No mainstream routable app — supply the
   endpoint to an open tool: **OpenClaw** (self-hosted, 29 channels, scheduled posting) or **SamurAIGPT/
   social-post**.
6. **Messaging (WhatsApp / Telegram / Signal)** — *Tier B, build-effort: medium.* A **Telegram bot** bridging
   to our router first (official bot API); WhatsApp/Signal via their bridges later.
7. **Website builder & other AI tools** — *mostly Tier C.* Framer AI, Wix ADI, Webflow AI are cloud-locked.
   The only routable "builder" surface is dev "vibe coding" tools (Cursor, Cline, Aider) that accept a custom
   `base_url` — out of scope for non-tech users.

## Recommended integration order (as `integrations/` app types)

1. **Obsidian** — done (karpathywiki + the `demo/` vaults).
2. **Brave Leo** — single settings field, massive install base, instant "my browser AI runs on my
   subscriptions" wow. Best next target.
3. **Home Assistant** — the voice demo is the most impressive for non-tech audiences.
4. **Joplin / Logseq** — rounds out the notes story for non-Obsidian users.
5. **Thunderbird** — everyday email.

Brave and Home Assistant are both *one-field* configs — ideal for the non-tech delivery model (our dashboard
flips the field for them). The three flagship ships to prove the story: **Unified chat (Open WebUI)**,
**Journaling (Plume + our Obsidian wiki)**, **Email (Thunderbird + Ollama Compose)**.

## Sources
- [a16z — Top 100 Gen AI Consumer Apps (7th Edition)](https://a16z.com/100-gen-ai-apps-7/)
- [Most Popular AI Apps 2026 — Backlinko](https://backlinko.com/most-popular-ai-apps)
- [Ollama OpenAI-compatible API / integrations (Open WebUI, LiteLLM)](https://cohorte.co/blog/ollama-advanced-use-cases-and-integrations)
- [Giving your local LLM an OpenAI-compatible endpoint](https://inventivehq.com/blog/openai-compatible-endpoint-for-local-llm)
- [Brave — Bring Your Own Model (BYOM)](https://brave.com/blog/byom-nightly/) · [BYOM support doc](https://support.brave.app/hc/en-us/articles/34070140231821-How-do-I-use-the-Bring-Your-Own-Model-BYOM-with-Brave-Leo)
- [Raycast — Local Models / BYOM](https://manual.raycast.com/ai/local-models)
- [Home Assistant — Ollama integration](https://www.home-assistant.io/voice_control/assist_create_open_ai_personality/)
- [Obsidian local AI with Ollama (plugins)](https://localaimaster.com/blog/local-ai-obsidian-integration)
- [Joplin Jarvis plugin (Ollama)](https://github.com/alondmnt/joplin-plugin-jarvis) · [Logseq + Joplin local LLM](https://www.promptquorum.com/power-local-llm/local-llm-with-logseq-and-joplin)
- [Journaling apps that work with local AI (Plume, JournalLM, Memex)](https://getplumeapp.com/blog/journaling-apps-local-ai)
- [Local AI email (Thunderbird Ollama Compose, AI Emaily)](https://aiemaily.com/blog/local-ai-model-for-private-email)
- [AI agents for social media / OpenClaw / SamurAIGPT social-post](https://github.com/SamurAIGPT/social-post)
- [Opera built-in local LLMs (no custom endpoint)](https://techcrunch.com/2024/04/03/opera-will-now-allow-users-download-and-use-llms-locally/)
