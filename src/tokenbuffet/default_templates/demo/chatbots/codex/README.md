# Codex CLI client demo

After starting the bridge, run `tbuffet open chatbot OpenAI` or use **Open** in the Hub.
The launcher sets `CODEX_HOME` to this workspace's `.codex/` folder for the current session.
Its `.codex/config.toml` selects the router's `medium` tier and custom Responses provider.
The local placeholder bearer key is supplied only to the launched session.

Codex ignores custom provider definitions in ordinary project config. Setting `CODEX_HOME`
makes this folder the session's configuration home instead, so those definitions apply without
editing your normal Codex configuration. Session state also stays under the local `.codex/` folder.
See [Codex configuration locations](https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations).
The bridge's Responses path
supports buffered function and custom freeform tool handoff, including
`apply_patch`, and router-local continuation history.
