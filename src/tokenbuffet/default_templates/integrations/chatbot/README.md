# Chatbot workspaces

Register a CLI and workspace folder with the standard app commands:

```powershell
tbuffet add-chatbot grok --path C:\mygrok
tbuffet open chatbot mygrok
tbuffet open chatbot      # lists your chatbot instances and asks which one to open
tbuffet open              # same, across every openable app
```

Built-in presets are `claude`, `codex`, `grok`, and `agy`. The path is required and can point to
an existing folder or a new one. Registration lists the files to write before confirmation.
No backups are made. JSON settings are merged, preserving unrelated settings and hooks.

In the Hub, open **Connect an App**, select **Chatbot**, select a **CLI**, and enter an instance ID
and workspace folder. The registered client gets an **Open** button. On Windows, Open starts a
visible terminal in that folder and starts the CLI with the environment from the workspace's `launch.json`. No script runs, so PowerShell's execution policy does not apply.

| Preset | Native configuration | Session setup |
| --- | --- | --- |
| `claude` | `.claude/settings.local.json` | Explicit `--settings` file |
| `codex` | `.codex/config.toml` | `CODEX_HOME` set to the workspace's `.codex` |
| `grok` | `.grok/config.toml` | `GROK_HOME` set to the workspace's `.grok` |
| `agy` | `.gemini/antigravity-cli/settings.json` | Workspace home and router URL set for the session |

For `codex`, `grok` and `agy` (the CLIs that do not inherit global settings the way `claude` does), registration also copies the CLI's global home (`CODEX_HOME`/`GROK_HOME`, else
`~/.codex`/`~/.grok`/`~/.gemini`, resolved from your user profile) into the workspace home, without overwriting existing
files, so the workspace behaves like the global one: settings, login and conversations. Logs, lock files and
temp folders are skipped (the `skip` globs in the preset). The home can be large (Codex's is hundreds of MB), so
the first registration may take a while. The session login is persisted, not per-process; the copy is
a snapshot, so a later re-login in either place is not shared. Codex copies `auth.json` only if it uses file
credential storage (the OS keyring is not copied). The user profile (`HOME`/`USERPROFILE`) must be defined,
and the workspace should be opened with `tbuffet open` so the `launch.json` home override applies.

Each preset selects the router's `medium` tier by default. User-wide configuration is not edited.
Run `tbuffet start` before using AI features. The client route excludes that CLI's own provider backend.

## Change an existing client

Edit `registered_apps/chatbot/NAME/app_config.json` to change `client_settings.active_endpoint` or
`client_settings.single_model_tier`, then run:

```powershell
tbuffet reconfigure-app chatbot NAME
```

Reapply rewrites the native configuration and launcher using that instance's saved templates.

## Add another CLI preset

Create `integrations/chatbot/presets/NEW/` by copying a related preset. Edit its two files:

- `app_config.json`: declared client type, required workspace path (`[app_path]`), router endpoint,
  model tier, and primary native settings path in `bridge_configuration`.
- `app_settings.json`: primary native settings (`format: json` with `data`, or `format: text` with
  `content`) and a `files` object containing `launch.json` (`command`, `env`, and `requires`, the settings file that must exist; `{workspace}` expands to the workspace folder) and any additional workspace files.
  Every additional file also declares its `format` and `data` or `content`.

`{active_endpoint}` and `{single_model_tier}` in template strings are replaced with that instance's
client settings. All generated
files must stay inside the chosen workspace. Use the CLI's documented configuration mechanism.
Keep credentials out of preset files; the existing demos use a local placeholder router key.

The preset becomes available in `--preset` and the Hub's CLI selector without changing Python or
JavaScript. Register it with `tbuffet add-app chatbot NAME --preset NEW --path FOLDER`.
