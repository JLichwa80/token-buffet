# Token Buffet Demo Projects

Every demo ships pre-configured to talk to the local router (`http://127.0.0.1:8090`).
There is nothing to register. Run `tbuffet start` in this folder, then open or launch a demo.

- **[Obsidian LLM Wiki](Obsidian-LLM-Wiki/)**: two sample Obsidian vaults (conference notes, daily notes) with AI-powered note synthesis.
- **[Chatbots](chatbots/)**: Claude Code, Codex, Grok Build and Gemini Antigravity as router clients.
- **[Claudia](claudia/)**: a sample Claudia AI chief-of-staff setup.
- **[Abject](abject/My-Tech-Friend-Demo/)**: My Tech Friend, an Abject workspace that builds apps, websites and games from plain English.

Their registrations live in `registered_apps/`, so `tbuffet list-apps` shows them.
`tbuffet reconfigure-app <type> <name>` re-applies a demo's settings if you changed them.
