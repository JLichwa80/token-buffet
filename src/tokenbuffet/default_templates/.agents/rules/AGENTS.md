---
description: Global project rules and context for the Knowlege Base - Obsidian
---

# Project Overview & Guidelines

This project focuses on automatically transforming raw financial conference transcripts and summaries into a highly structured, interconnected knowledge base (a "Wiki") within an Obsidian vault. It bridges local Obsidian plugins with a local CLI LLM agent to accomplish this without relying on cloud-based web endpoints.

## 1. Directory Structure & Key Files

### The Proxy Bridge (cli_proxy_server.py & local_router.py)
- **Role:** Acts as a localhost OpenAI-compatible API. It listens for standard HTTP POST requests and pipes the prompt payload to local CLI tools (grok.exe, claude, codex) using subprocess.Popen. 
- **Features:** Supports SSE streaming, model endpoints, and transparent error handling (injecting stderr directly into the Obsidian chat).

### The Obsidian Vault (LLM Wiki Play\)
- **
aw\**: Contains the raw input files (Markdown transcripts and summaries from financial conferences).
- **wiki\**: Contains the LLM generated output organized into concepts/, ntities/, and sources/.
- **karpathywiki plugin**: Automatically reads 
aw/ files and queries the proxy server to construct the wiki/ folder.

## 2. Agent Behavior & Execution Workflow
- **Validate Before Execution**: Do NOT execute steps based on your own ideas or assumptions without getting validation and explicit permission from the user first.
- **Smart Routing based on Limits**: The router NO LONGER fails fast when a provider fails. Instead, local_router.py actively checks limits.json and automatically routes the request to the backend proxy with the highest tokens remaining. If the chosen proxy fails, it falls back to the next proxy.
- **No Failsafe Defaults**: When gathering provider limits, the router MUST physically query each provider (using API or TTY, parsing their specific `usage` config) to get real usage. It must never use fallback values or defaults (e.g., 500,000 tokens) if the limits are missing or outdated.
- **Report & Shutdown**: After completing a requested code change or task, simply report what was changed and end your turn immediately. Do NOT run idle "Waiting for go-ahead" loops or ping status messages.
- **Do Not Autostart Servers**: Do NOT automatically launch or restart background servers (like the proxy or router) during or after code changes unless explicitly asked.

## 3. Architecture & Code Philosophy (Maintainability First)
- **Least Code to Maintain (OVERRIDING RULE)**: Maintainability is the top priority — above minimizing dependencies. Prefer adding a well-maintained dependency over writing our own logic; our code should be thin glue between libraries. "100 dependencies with less of our own code" is the goal. If a library can save a line of our code, use it. This supersedes the repo's older "stdlib-only / zero-dependency / extreme minimalism" ethos wherever they conflict.
- **Use Official SDKs, never hand-roll schemas**: Build protocol payloads through the owning SDK's models, never by constructing JSON/schemas by hand. Example: the OpenAI Responses wire is built with the `openai` Python SDK (`openai.types.responses`), so spec drift is absorbed by `pip install -U openai` rather than code edits.
- **Serving frameworks are allowed**: The old "no FastAPI/Flask, stdlib `http.server` only" rule is retired under the rule above — a serving/proxy library that removes our code (e.g. LiteLLM, which natively serves `/v1/responses`, `/v1/chat/completions`, and `/api/chat`) is preferred over hand-rolled handlers.
- **No Repo Clutter (Scratch Scripts)**: Under NO circumstances should temporary/scratchpad scripts (like proxy test scripts, one-off patching or migration scripts) be saved into the project repository. Always use the hidden agent scratch/ directory.
- **No Prompt Assumptions**: Pass the prompt exactly as it is received. Do NOT inject fallbacks or modify the user's prompt.

## 4. Throughput & Concurrency (The GROK_HOME Trick)
- **The SQLite Locking Problem**: By default, grok.exe writes every chat session to a local SQLite database. Spawning multiple processes simultaneously forces them to execute sequentially due to file locks.
- **The Sandbox Solution**: To achieve true parallelism, the proxy creates a unique temporary directory for every request, copies uth.json into it, and sets GROK_HOME. This tricks each thread into using an isolated sandbox database, eliminating lock collisions.

## 5. Multi-Provider Routing & Semantic Tiers
- **TUI Constraints**: The CLIs for codex and claude are built as Text User Interfaces and their interactive model lists cannot be fetched programmatically in the background. 
- **The Router Tiers (local_router.py)**: To abstract provider-specific models from the Obsidian plugin, the router employs a strict semantic tier system. The plugin requests a tier, and the router maps it to the appropriate model.
  - ast: Smaller, faster models.
  - medium: Balanced models.
  - 
easoning: Large, complex reasoning models.

## 6. Obsidian Plugin Settings & Proxy Implementation (CRITICAL)
- **Provider Setting**: Must be set to **"Custom OpenAI-Compatible (Responses)"**.
- **API Spec Details (CORRECTED — this previously pointed at the wrong wire)**:
  - The Obsidian plugin uses the JavaScript Vercel AI SDK via `createOpenAICompatible(...).responses(...)`, which speaks the **OpenAI Responses API** wire to the proxy: `POST /v1/responses`, streaming `response.created` → `response.output_text.delta` → `response.completed`. This is OpenAI's spec, not a Vercel-proprietary protocol — the Vercel client merely conforms to it.
  - **Build via the `openai` SDK, no hand-rolled JSON**: Construct those events through the `openai` Python SDK's `openai.types.responses` Pydantic models (building through them validates the shape before it reaches Obsidian), then serialize with `.model_dump_json()`. Do NOT hand-write event JSON/schemas like `{"type": "output_text"}`.
  - **`ai.ui.ai_sdk` is a SEPARATE, opt-in format — NOT what Obsidian's Responses preset consumes**: the Vercel Python `ai` package emits the AI-SDK UI-message stream (`text-delta`…), a different wire. It is opt-in via `--ui-stream true` (for a future Vercel `useChat`-style frontend). The default emits native per-path formats (OpenAI chat / Ollama ndjson / Responses SSE), selected by the request path.
- **Base URL**: http://127.0.0.1:11434/v1 (The Router port, masquerading as Ollama)
- **Connection Handling (CRITICAL HANG FIX)**: Because Python's `http.server` lacks automatic chunked transfer encoding, streaming SSE endpoints omit `Content-Length`. To prevent clients from hanging indefinitely waiting for EOF:
  - You MUST explicitly send `self.send_header("Connection", "close")` for all streaming responses.
  - Proxy routers bridging the stream must also send `Connection: close` to the client.
  - For non-streaming endpoints, you MUST compute the byte length of the encoded JSON payload and explicitly send `self.send_header("Content-Length", str(len(resp_bytes)))` along with `Connection: close`.

## 7. Obsidian Wiki File Structure Constraints
If generating or summarizing notes:
- **Read from:** LLM Wiki Play/raw/
- **Write to:** LLM Wiki Play/wiki/concepts/, LLM Wiki Play/wiki/entities/, or LLM Wiki Play/wiki/sources/.
- **Never** dump markdown files in the project root.
