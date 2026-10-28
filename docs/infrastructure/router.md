# Router configuration and behavior

The fleet launcher and direct `python -m tokenbuffet.local_router` both default to port 8090. Pass `--port` to choose explicitly.

## Provider-first configuration

`config/router_config.json` stores exact model IDs under providers:

```json
{
  "mode": "usage",
  "custom_order": ["claude", "codex", "agy", "grok"],
  "providers": {
    "grok": {
      "tiers": {
        "fast": "grok-4.7-build-fast",
        "medium": "grok-4.6",
        "reasoning": "grok-4.7"
      }
    }
  }
}
```

The router derives its internal tier lookup from this structure. Exact model IDs and hand edits are preserved. Existing tier-first files migrate at load time. Missing or empty `providers` is populated once from provider tier regexes and each running proxy's `/models` endpoint. Restart after config changes.

## Routing and retries

Requests resolve by tier, exact model ID, provider name, fuzzy model match, then the medium tier. If no medium fallback is configured, an unmapped request returns a structured HTTP 503.

Usage mode sorts providers by remaining quota. Custom mode follows `custom_order`. Both skip known depleted or stopped providers. Exact-model requests try their provider first and then every alternate in the same tier. Tier requests try all eligible backends in order.

Provider failures, connection failures, HTTP 429, and explicit error events advance to the next candidate. Before a stream starts, other HTTP 4xx responses from a proxy are returned to the client with their error body, since retrying another provider cannot fix the request. The proxy returns HTTP 502 for failed nonstreaming CLI executions and emits an error event for failed streams. Nonstreaming attempts are buffered, spilling to disk above 1 MiB, so failed attempts can be retried without sending partial output. For `"stream": true`, the router holds only the stream prelude until the first text arrives, then forwards and flushes each line as it arrives. Failures before text can be retried; failures after text are passed to the client as stream errors because the partial answer is already visible. If every candidate fails or is unavailable, the router returns HTTP 503.

The client selects the response format. A request with `"stream": true` receives streamed events; an omitted or false `stream` field receives one JSON response. The saved Obsidian ingestion request omitted `stream`, so its response remains nonstreaming unless that client changes its request.

Each proxy binds its port first, then reads its own usage and models in a background thread and retries every 300 s on failure. If the CLI shows an updater or another screen without quota values, the read fails, the proxy logs the captured reason, and its run status records `usage: {state: unavailable, reason}`; while a read is running the state is `reading`, and after success it is `ready`. Failed reads preserve the last valid usage JSON. Run status also records `starting`, `running`, and `stopped`. The router only uses a provider marked `running` whose port is listening, so a failed startup or a stale file after a forced stop is skipped. `GET /usage` and `GET /models` return that proxy's cached extractor JSON while fresh and refresh it when missing or stale. The default cache lifetime is 1800 seconds and can be set with the proxy's `--refresh-interval` option. The router polls each running proxy's endpoints at startup and on its own `--refresh-interval` schedule; zero means startup only. It never reads provider usage or model files or launches bulk extractor scripts. The fleet launcher waits for proxy startup before launching the router so its first model snapshot can include the running providers.

## Console and files

Both router and proxy consoles emit one-line `REQUEST`, `FAIL`, and `DONE` summaries with a shared request ID. Router `ROUTE` lines identify each attempted backend. Provider errors are whitespace-normalized and bounded to 500 characters. See [logging.md](logging.md) for file locations.
