# Provider Proxies

**One local API for the AI subscriptions you already pay for.**

Token Buffet's provider proxies turn Claude Code, Codex, Grok Build and Gemini Antigravity into standard HTTP endpoints on your own machine. Your apps talk to a familiar API. The proxy runs your logged-in CLI behind it. No API keys, no third-party gateway, no extra bill.

## Live request processing

- **Speaks every major API.** OpenAI Chat, Completions and Responses, Ollama, Anthropic Messages and Google Gemini GenerateContent, all from the same proxy. Point an existing app at it and it just works.
- **Real-time streaming.** Answers stream to your app as the CLI writes them, in each API's native format.
- **Tools stay with your app.** When a request carries tools, the CLI returns one structured tool-call decision and your app runs the tool and sends back the result.
- **Your subscription, your login.** Each request runs the vendor's own CLI with your account. Inherited API keys and base URLs are stripped so the CLI always uses your plan.
- **Clean separation.** Agy runs in a private home folder with its own tools denied, and Grok gets a fresh sandbox for every request.
- **Honest errors.** If a provider fails, you get the provider's error. No hidden retries, no silent fallbacks.

## Usage and model awareness

- **Know what's left.** Each proxy reads its CLI's own usage screen and reports remaining session and weekly quota, the plan, and reset times. The router uses this to send work to the provider with the most headroom.
- **Always the right model id.** Model lists are read straight from each CLI, so the id you send is exactly the id the CLI accepts. Models can be requested directly or through the `fast`, `medium` and `reasoning` tiers.
- **Never blocks.** Usage and models are read in the background and cached, so the proxy is ready the moment it starts.
- **Adjustable effort.** Reasoning effort is passed to CLIs that support it.

## One proxy per provider

| Proxy | Port | Runs |
|---|---|---|
| Grok | 8000 | Grok Build |
| Claude | 8001 | Claude Code |
| Codex | 8002 | Codex CLI |
| Agy | 8003 | Gemini Antigravity |

Every proxy binds to `127.0.0.1` only. Nothing is exposed to your network.

## Built to extend

Providers are defined by a single JSON file: the command to run, how to read its output, and how to read its usage and models. Adding a new CLI means writing a config, not changing the engine.
