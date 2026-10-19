# Dashboard

The live AI Subscription Hub is served at `http://127.0.0.1:8080/` by
`python -m tokenbuffet.dashboard` or the fleet launcher. It reads the
registered providers, exported status, quotas, models, app instances, router
configuration, and request logs from this workspace.

Home shows remaining quota percentages for the current CLI login under each
provider, sorted by each provider's tightest reported remaining quota, as the
router's usage mode does. A missing quota export is
shown as unknown. My Apps lists `registered_apps/<type>/<name>/app_config.json`
instances and lets you register or reapply them through
`integrations/register.py`. Registration shows its target settings path. If the
integration's initialization or configuration fails, the UI shows the error.

LLM Providers shows the single current login, models, quota, live port, and
process status. Launch starts one configured proxy, Stop checks the process
identity before terminating it, and Log in opens the provider CLI on Windows
or macOS. Advanced mode exposes provider tools, saved router settings, and
recent request activity. Provider tool changes require a proxy restart.

Router Configuration edits `mode`, `custom_order`, and exact model IDs under
`providers.<name>.tiers`. The server validates every provider and model ID
against the current exports. Saving changes the file, while a running router
keeps its startup snapshot until restarted. The page labels this distinction.
The fleet launcher uses router port 8090, while a direct router launch without
`--port` defaults to 11434.

Activity reads per-provider session logs in root `logs/` and correlates
request IDs with router records. It shows no prompt or response text. App
attribution remains unknown when the client does not provide it. Full payloads
appear only when Debug logging is enabled, and are not shown in this page.

The dashboard listens only on loopback. Its control endpoints use JSON POSTs:
`/api/apps/register`, `/api/apps/apply`, `/api/providers/launch`,
`/api/providers/stop`, `/api/providers/login`, `/api/providers/tools`, and
`/api/router`. `GET /api/state` supplies the current UI state. Global pause,
multiple logins per provider, account removal, and in-browser app settings
editing are not implemented.

Design history is in [dashboard_design.md](dashboard_design.md) (prototype review `DPR-001`), which records the decision to use runtime data instead of the prototype's hardcoded examples.
