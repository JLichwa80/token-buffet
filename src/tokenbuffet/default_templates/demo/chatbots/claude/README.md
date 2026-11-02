# Claude Code client demo

The `.claude/settings.local.json` in this folder sends Claude Code requests to
`http://127.0.0.1:8090/v1/messages` through its
`ANTHROPIC_BASE_URL` setting. It sets no model.
After starting the bridge, run `tbuffet open chatbot Claude` or use **Open** beside Claude Code
in the Hub. Both start Claude Code in this workspace with its router settings.
The launch explicitly passes this folder's settings file using `--settings` for the session.

The client-scoped path prevents a Claude Code request from selecting the
Claude provider proxy. The endpoint supports buffered tool-use handoff.
