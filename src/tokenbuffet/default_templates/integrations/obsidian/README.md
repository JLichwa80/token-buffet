# Obsidian LLM Wiki integration

This integration connects an Obsidian vault running the **LLM Wiki** (`karpathywiki`) plugin to the Token Buffet router.
The plugin then runs its note synthesis on your CLI subscriptions.

For the concept, see the **[Karpathy LLM Wiki Overview](https://www.youtube.com/watch?v=iXd0t60YmMw)**.

## Demo vaults

The two vaults in `demo/Obsidian-LLM-Wiki/` are already configured. Open them after `tbuffet start`.

Before opening a vault, Token Buffet checks that its folder exists and that Obsidian lists it.
If Obsidian cannot find the vault, close Obsidian completely and retry the command.
If the problem persists, add the existing vault folder in Obsidian before opening it with Token Buffet.

## Register your own vault

```bash
tbuffet add-app obsidian <name> --path "/path/to/vault" --vault-type <type>
```

- `--path` (required) is the vault folder. The settings are written to `<vault>/.obsidian/plugins/karpathywiki/data.json`.
- `--vault-type` picks a tag and prompt preset from `vault_types.json`: `default`, `finance-conference`, `research-papers` or `daily-notes`.

`tbuffet reconfigure-app obsidian <name>` re-applies the settings.

## Settings written to the plugin

They come from `app_config.json → client_settings`, merged over `app_settings.json` and the vault-type preset:

| Plugin key | Value |
|---|---|
| `provider` | `custom-responses` (calls the router's `/v1/responses`) |
| `baseUrl` | `http://127.0.0.1:8090/v1/` |
| `model` | `single_model_tier` (default `fast`) |
| `usePerTaskModels` | `model_mode` |
| `ingestModel` / `lintModel` / `queryModel` | `task_model_tiers` (`fast` / `reasoning` / `reasoning`) |

```
Obsidian vault -> LLM Wiki plugin -> Token Buffet router (8090) -> provider proxies -> Claude / Codex / Grok / agy
```
