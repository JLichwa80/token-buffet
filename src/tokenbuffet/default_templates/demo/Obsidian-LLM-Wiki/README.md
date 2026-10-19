# Obsidian LLM Wiki

The LLM Wiki pattern turns Obsidian into an AI-powered second brain.
Notes dropped into `_Inbox/` are ingested, synthesized, cross-linked and added to a growing knowledge graph.
The work is done by your local CLI subscriptions rather than a paid API.

See the **[Karpathy LLM Wiki Overview](https://www.youtube.com/watch?v=iXd0t60YmMw)** for the concept.

## Try a demo vault

1. Enable **Settings > General > Command line interface** in Obsidian (requires the current Obsidian installer and its CLI on PATH).
2. In your Token Buffet folder, run `tbuffet demo init`. It applies the demo settings, opens the demo vaults through Obsidian's CLI, turns off Restricted Mode, enables LLM Wiki, and creates each wiki's folders and schema using the plugin.
3. Demo initialization sets `llmReady: true` directly, without connection tests or a running router. Run `tbuffet start` when you are ready to use the AI features.
4. Open either demo with `tbuffet open obsidian conference-notes` or `tbuffet open obsidian daily-notes`. Drop a note into `_Inbox/`, or use the plugin's commands to ingest, lint or query.

The API key is `TokenBuffet`. The demo uses the dedicated Obsidian SecretStorage ID `tokenbuffet-provider-api-key`, shared by Token Buffet vaults. It does not replace the plugin's default provider-key secret. Running `tbuffet demo init` again reapplies the demo settings.

Automatic trust uses [Obsidian CLI](https://obsidian.md/help/cli) `eval` to call the same trust method as Obsidian's **Trust author and enable plugins** button, then enables LLM Wiki. Setup waits for the vault layout, saves its settings, and reloads the vault so an initial trust dialog is cleared. If setup fails, the command reports the error and exits with an error.

If Obsidian cannot find a demo vault, close Obsidian completely and retry `tbuffet demo init`.
If the problem persists, add the existing demo folder as a vault in Obsidian before running `tbuffet open`.
Token Buffet checks that the folder exists and that Obsidian lists the vault before opening it.

The plugin is pre-configured with these settings:

- endpoint `http://127.0.0.1:8090/v1/` (OpenAI Responses API)
- models: the router tiers `fast` / `medium` / `reasoning`
- tasks: ingest uses `fast`, while lint and query use `reasoning`

The router sends each request to whichever subscription has the most quota left.

## Demo vaults

- **[conference-notes/](conference-notes/README.md)**: 427 masked notes from a tax and wealth-management conference (vault type `finance-conference`).
- **[daily-notes/](daily-notes/README.md)**: 275 daily notes sourced from Simon Willison's blog (vault type `daily-notes`).

## Your own vault

```bash
tbuffet add-app obsidian my-vault --path "/path/to/vault" --vault-type daily-notes
```
The vault types are `default`, `finance-conference`, `research-papers` and `daily-notes`.
