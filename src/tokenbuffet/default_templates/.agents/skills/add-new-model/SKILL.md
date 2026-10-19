---
name: add-new-model
description: Use this skill when the user asks to add a new model (e.g., GPT-7, a new Claude variant, etc.) to the proxy router and dashboard UI.
---

# Add New Model

Since Codex and Claude cannot fetch their model lists dynamically via the TUI, adding a new model requires manual updates in multiple places.

## Workflow Steps

### 1. Update the UI Layer (`dashboard/server.py`, `dashboard/static/app.js`)
Add the exact model string to the hardcoded model arrays (e.g., `CODEX_MODELS` or `CLAUDE_MODELS`) so it appears in the dropdown menus for the user.

### 2. Update the Routing Layer (`local_router.py`)
Add the model to the semantic tier dictionary (`fast`, `medium`, `reasoning`) so the Obsidian plugin can request it abstractly.

### 3. Restart the Stack
After modifying the Python files, use the `start-local-proxy` skill to restart the dashboard and router on their respective ports so the changes take effect.
