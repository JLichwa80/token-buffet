# Chatbots using the router

Claude Code, Codex CLI, Grok Build, and Gemini Antigravity are configured as client apps of the router.
Each demo workspace owns its settings and points at the router, `http://127.0.0.1:8090`.
Launchers apply these defaults for their own sessions. They do not edit the user's normal CLI configuration.

Add any number of workspaces using the same preset:

```powershell
tbuffet add-chatbot grok --path C:\mygrok   # omit --path to pick the folder in a dialog; --name defaults to the folder name
tbuffet open chatbot mygrok
```

In the Hub, **My Chatbots** has one button per CLI preset ("Connect Claude-Code instance", "Connect
Codex instance", and so on; the names come from each preset's `app_config.json`). The button picks the
CLI, so the form has only two visible fields:

1. **Workspace folder** — a path box with **Browse…** (the folder dialog opens only when you click Browse).
2. **Name** — free text that pre-fills from the chosen folder's name; leave it or edit it to anything.

Then submit. The workspace path identifies the chatbot: registering the same folder twice for one CLI is refused.
The name is only the display label (any text, duplicates allowed). The instance folder under
`registered_apps/chatbot/` is the workspace folder's own name (`-2`, `-3`... if two workspaces share one) and is
never shown to the user.

Registration creates native settings and a local `launch.json`, then makes the workspace available through Open.
Built-in presets are `claude`, `codex`, `grok`, and `agy`. New presets are data files under
`integrations/chatbot/presets/`; see that integration's README for the format.

| Client | Config mechanism | Bridge endpoint |
| --- | --- | --- |
| Claude Code | `.claude/settings.local.json`, explicitly passed with `--settings` | `/v1/messages` |
| Codex CLI | `.codex/config.toml`, with session `CODEX_HOME` set to this workspace's `.codex` | `/v1/responses` |
| Grok Build | `.grok/config.toml`, with session `GROK_HOME` set to this workspace's `.grok` | `/v1/chat/completions` |
| Gemini Antigravity | `.gemini/antigravity-cli/settings.json`, session home set to the workspace, and session `GOOGLE_GEMINI_BASE_URL` | `/v1beta/models/{model}:generateContent` |

Codex and Grok restrict provider definitions in ordinary project config. Their launchers select
the workspace folder as the session's configuration home so the local router provider is loaded.
Antigravity documents the custom endpoint as an environment variable; its launcher sets that
variable only for the session. The router excludes each originating CLI's own backend.

## Wire format details

**Claude Code** — Sends Anthropic Messages (`/v1/messages?beta=true`). May also probe `HEAD /api/hello`. Demo disables thinking (`CLAUDE_CODE_DISABLE_THINKING=1`) and enables gateway model discovery so `/model` lists available tiers.

**Codex CLI** — Uses the OpenAI Responses API (`/v1/responses`). Requires the `openai` Python SDK in the proxy environment; returns HTTP 503 if absent. Supports buffered function, custom freeform, and `apply_patch` tool handoff. Router holds continuation history for up to 100 recent responses (lost on restart).

**Grok Build** — Uses OpenAI chat completions (`/v1/chat/completions`). Supports buffered function-call handoff with periodic empty chunks during backend work.

**Gemini Antigravity** — Uses Gemini GenerateContent. Supports buffered function-call handoff. The agy backend home (`data/provider_homes/agy`) needs its own sign-in independently of the client demo.

## Tool handoff

For requests carrying client tools, the router asks a backend CLI for one structured tool-call decision, then returns it to the client for execution. Provider configs may add `execution.tool_handoff_args` (claude/grok use `--tools ""`) to signal the backend to leave tool execution with the client.

## Official references

- [Claude Code gateway configuration](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Grok Build settings](https://docs.x.ai/build/settings)
- [Antigravity CLI custom endpoint](https://www.antigravity.google/docs/cli/install/)
