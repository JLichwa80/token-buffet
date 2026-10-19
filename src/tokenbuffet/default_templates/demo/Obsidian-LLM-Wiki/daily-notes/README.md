# Daily Notes Vault

Sample Obsidian vault with 275 daily notes sourced from Simon Willison's blog. Demonstrates daily note templates, weekly reviews, and AI-augmented note synthesis. Content spans multiple years and topics including AI, technology, tools, and personal observations.

**Content Source:** [Simon Willison's Blog](https://simonwillison.net/) — 275 entries extracted with proper attribution.

## Configuration

The vault is pre-configured. Open it in Obsidian after `tbuffet start` (see the [parent README](../README.md)).

- **Plugin settings:** `.obsidian/plugins/karpathywiki/data.json`
- **Registration:** `registered_apps/obsidian/daily-notes/` (apply it again with `tbuffet reconfigure-app obsidian daily-notes`)
- **Router:** `http://127.0.0.1:8090/v1/`
- **Model tiers:** ingest (`fast`), lint (`reasoning`), query (`reasoning`)
- **Vault type:** `daily-notes`
