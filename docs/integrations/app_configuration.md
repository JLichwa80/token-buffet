# App configuration

`integrations/<type>/app_config.json` defines the initial fields for an integration type. Registration copies it into `registered_apps/<type>/<name>/app_config.json` and writes instance values.

- `name` and `type`: instance name and integration type.
- `path`: app root. Defaults to `.` (the folder containing the instance's `app_config.json`). Relative paths resolve from that instance folder.
- `bridge_configuration`: settings file written by the bridge. Relative paths resolve from `path`; absolute paths are accepted. Defaults are `.obsidian/plugins/karpathywiki/data.json` for Obsidian and `.claude/settings.local.json` for Claudia.
- `client_settings`: `active_endpoint`, `single_model_tier`, `model_mode` (`"false"` or `"true"`), and `task_model_tiers`.

`tbuffet add-app TYPE NAME --path APP_PATH [--preset CLIENT] [--vault-type PRESET] [--label L]`
(which wraps `integrations/register.py`) copies the integration into `registered_apps/TYPE/NAME`.
Obsidian, Claudia, and chatbot clients require `--path`. Chatbot clients also require `--preset`
with a choice from `integrations/chatbot/presets/`. Unknown presets are rejected before files are
created. Existing target settings and launchers are overwritten without backups. `tbuffet reconfigure-app TYPE NAME` reapplies an existing instance.
Relative stored `path` values resolve against the instance folder.

For example:

```powershell
tbuffet add-chatbot grok --path C:\mygrok
tbuffet open chatbot mygrok
```

An integration type can declare `presets_directory` in its base `app_config.json`. Registration
copies the type's shared files, then overlays the selected preset's files. The selected preset's
`app_config.json` supplies its client-specific fields. The Hub discovers the same preset folders.

The four chatbot demos are registered in `registered_apps/chatbot/` as
`Gemini`, `Claude`, `OpenAI`, and `Grok`. Their configuration targets are
under `demo/chatbots/`. Reapplying an instance copies its saved
`app_settings.json` into that target, merging JSON settings and replacing
text config files. Its `files` object supplies the launcher and
additional workspace files. `{active_endpoint}` and `{single_model_tier}` are rendered from the
instance's `client_settings`; source templates remain unchanged. The agy backend
uses a separate home at `data/provider_homes/agy`.
