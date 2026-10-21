# Grok Build client demo

After starting the bridge, run `tbuffet open chatbot Grok` or use **Open** in the Hub.
The script sets `GROK_HOME` to this demo's `.grok/` folder for the current session so your usual Grok
config is not changed. Its `.grok/config.toml` selects the router as the default and sends the `medium` model to the
router's `/v1` endpoint over OpenAI chat completions.

Grok restricts provider settings in ordinary project config; the session-local home makes this
workspace's provider configuration apply. See [Grok settings](https://docs.x.ai/build/settings).

The bridge supports buffered OpenAI chat function-call handoff. The demo home does not copy your Grok auth file into the repository.
