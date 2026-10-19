# Logging

Active bridge processes and launch scripts write to `logs/` at the repository root. The directory is created automatically and ignored by Git.

- `router/router.log`: router decisions and service messages.
- `router/console.log`: router launcher output, errors, and exit status.
- `<provider>/proxy/proxy.log`: one-line proxy request, completion, and failure summaries.
- `<provider>/proxy/console.log`: per-provider launcher output and full startup tracebacks.
- `dashboard/console.log`: dashboard launcher output and errors.
- `extractors/console.log`: individual capture/parse output and errors.
- `extractors/refresh-*.log`: bulk refresh script output.
- `<provider>/proxy/sessions/`: per-request trace (`.log`). At `INFO`, it records the route, model, request size, output size, timing, and errors. At `DEBUG`, it also records the full payload, CLI chunks, stderr, and HTTP chunks.
- `<provider>/proxy/raw_requests/`: captured incoming request JSON at `DEBUG`.
- `<provider>/proxy/raw_responses/`: provider stdout, provider stderr, and exact HTTP response body (`.raw`) at `DEBUG`.
- `<provider>/llm_provider/raw_responses/`: extracted assistant text (`.txt`) at `DEBUG`.

The default is `INFO`, set in `config/logging.json`. Set its `level` to `DEBUG` for persistent full traces. For one run, use `tbuffet start --debug`. The proxy also accepts `--debug` directly. `--log-level` is available as an explicit override, with `--debug` taking priority. Filenames share the request ID across directories. Restart proxies after changing the config.

The Python launcher appends output as it arrives, preserving the command exit code. Restart already-running services to pick up the new paths. Historical files in `data/logs/` remain in place.

The dashboard session list reads the per-provider session traces. Response capture starts when proxies load this version of the code; historical responses cannot be recovered from earlier empty directories. Recovered older logs under `data/logs/` remain in place.

The PowerShell fleet supervisor relays new proxy summary lines into its own console. The Bash fleet leaves child console output attached. Router launch scripts print their summaries directly. Requests share an ID across router and proxy. Raw CLI stdout/stderr dumps no longer flood the console; failures retain a bounded one-line reason. Historical shared proxy logs are preserved, but new processes use per-provider files to avoid concurrent writers on Google Drive.

The dashboard reads per-provider session traces and correlates their request IDs with router log records. It does not display raw prompts or responses.
