# agy client demo

After starting the bridge, run `tbuffet open chatbot Gemini` or use **Open** in the Hub.
The workspace contains `.gemini/antigravity-cli/settings.json` with
`modelProvider: "gemini"`. The launcher uses this workspace as HOME and USERPROFILE for the
current session, sets a local placeholder `GEMINI_API_KEY`, points
`GOOGLE_GEMINI_BASE_URL` at `http://127.0.0.1:8090/client/agy`, and starts
`agy --model medium`. It restores the shell's environment when agy exits.
The registered `Gemini-Antigravity` app writes the isolated settings file.
Your normal agy settings are not changed.

Antigravity requires the endpoint through `GOOGLE_GEMINI_BASE_URL`; the launcher sets it for the
session rather than adding an unsupported URL key to settings.json.
See [Antigravity custom endpoints](https://www.antigravity.google/docs/install?tab=cli#point-the-cli-to-a-custom-endpoint).

The bridge's agy provider backend uses a different home at
`data/provider_homes/agy`; sign in there independently. The router excludes the
agy backend for requests from this client. The Gemini route has buffered
function-call handoff.
