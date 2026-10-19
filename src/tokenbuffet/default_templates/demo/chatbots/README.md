# AI Clients Demo

Use your favorite AI client — Claude Code, Codex, Grok, or Gemini Antigravity — with your own context and workflows, while your prompts are served across all your subscriptions combined. When one provider runs low, the router transparently picks another. All your conversation history stays in one place, and you get access to the best available model at any moment — zero friction.

Each client is preconfigured to connect to the local router via `/client/<provider>/`, which excludes that client's own provider from routing to prevent recursion. All registrations are in `registered_apps/chatbot/`.

| Client | Registration |
|--------|-------------|
| [Claude Code](claude/README.md) | `registered_apps/chatbot/Claude/` |
| [Codex CLI](codex/README.md) | `registered_apps/chatbot/OpenAI/` |
| [Grok Build](grok/README.md) | `registered_apps/chatbot/Grok/` |
| [Gemini Antigravity](agy/README.md) | `registered_apps/chatbot/Gemini/` |

All clients route to `http://127.0.0.1:8090/client/<provider>/`, and the router picks the provider with the most quota left. Run `tbuffet start` first.

Run `tbuffet demo init` to apply the registered router settings. On Windows, click **Open** beside
a chatbot in the Hub's Client Integrations area. It opens a visible terminal in that
demo workspace and starts the CLI with the router setup from its `launch.json`. The selected CLI must be installed and available on PATH.

The same launch is available with `tbuffet open chatbot Claude`, `tbuffet open chatbot OpenAI`,
`tbuffet open chatbot Grok`, and `tbuffet open chatbot Gemini`.

To connect another folder, use a preset with the regular registration command:

```powershell
tbuffet add-app chatbot mygrok --preset grok --path C:\mygrok
tbuffet open chatbot mygrok
```

The Hub's Connect an App form offers the same CLI and folder choices. Registration creates the
native settings and launcher in your selected workspace. Available presets are `claude`, `codex`,
`grok`, and `agy`; add more under `integrations/chatbot/presets/`.
