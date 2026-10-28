# Token Buffet AI Subscription Hub

Turns the AI CLIs you already pay for into one local, standard API.

## 1. Core Architecture

Three long-running processes plus a scraper for quotas and models.

### CLI Proxies & Vendor Adapters

- **API Standardization**: Exposes standard endpoints (/v1/chat/completions, /v1/messages)
- **Sandbox & Session Isolation**: Uses dedicated environment homes (e.g., GROK_HOME) to prevent SQLite locking
- **Execution & Streaming**: Runs prompts via PTY/Pexpect and streams SSE line-by-line

### Smart Router

- **Semantic Tier Mapping**: Maps abstract tiers (fast, medium, reasoning) to backend models
- **Smart Load Balancing**: Routes requests based on remaining quota percentage
- **Failover & Automatic Retries**: Bypasses offline or rate-limited providers automatically
- **Tool Handoff**: Intercepts and returns structured tool-calling decisions to clients

### Dashboard Control Center

- **Fleet Management**: Single-page console monitoring statuses, ports, PIDs, and quotas
- **Lifecycle & Auth Operations**: Controls process start, stop, and terminal logins
- **App Registration Wizard**: Configures external client applications via script pipelines

### Extractor Subsystem

- **Structured State Export**: Parses TUI outputs to discover models and track quotas

## 2. Quick Start & CLI Operations

### Initialization & Setup

- **Scaffold Workspace**: tbuffet init registers local provider CLIs on PATH
- **Demo Setup**: tbuffet demo init copies pre-configured demo workspaces
- **Start Services**: tbuffet start launches proxies, router (8090), and dashboard (8080)

### Management Commands

- **Add Provider**: tbuffet add-provider NAME --validate
- **Add Application**: tbuffet add-app TYPE NAME --path PATH
- **Status Control**: tbuffet status | stop | restart | doctor

## 3. Client Integrations

### Supported Chatbots

- **Claude Code**: Uses Anthropic Messages API (/v1/messages)
- **Codex CLI**: Uses OpenAI Responses API (/v1/responses)
- **Grok Build**: Uses OpenAI chat completions (/v1/chat/completions)
- **Gemini Antigravity**: Uses Gemini GenerateContent API

### Applications & Demos

- **Obsidian LLM Wiki**: Knowledge management and query vault integration
- **Claudia**: Terminal-based chief-of-staff assistant with a memory daemon
- **Abject**: Converts natural language prompts into custom applications

## 4. Directory Layout

- **Source Code**: src/tokenbuffet/ (proxy, router, dashboard, extractors)
- **Templates**: src/tokenbuffet/default_templates/ (configurations and demos)
- **Runtime Data**: data/ (provider status, homes, temporary files)
- **Logs**: logs/ (proxy, router, and session log files)
