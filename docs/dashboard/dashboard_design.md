# Dashboard Design — Control Center, App Registration & Configuration

Status: proposal (now largely implemented). Target is a single-page operator console for the
whole bridge: watch the fleet, register apps against the new `integrations/` flow, and edit an
app's settings/meta in place.

> **Consolidated history.** This file now carries the full dashboard design lineage. Appended
> below are: **Amendment A1** (the LLM-Provider/Account model, which *supersedes* the "Accounts"
> terminology used in the body), the **prototype review** (`DPR-001`), and the original
> **control plan** (the earliest restart-via-web sketch, fully superseded). Read the body for the
> design rationale, the amendment for current vocabulary, and the appendices as dated record. The
> live operating guide is [dashboard.md](dashboard.md).

## Purpose

One page (`dashboard.py`, port 8080) to:
1. **Control the fleet** — see every proxy + router + dashboard, their ports, PIDs, quota;
   launch / kill / restart / login per provider.
2. **Register apps** — pick an app type, give a name + path + per-type extras, and run the
   real `integrations/register.py` pipeline (copy → substitute → init → configure).
3. **Configure apps** — edit a registered instance's `app_meta.json` / `app_settings.json` /
   `vault_types.json`, then re-run `configure` to push into the app's own config file.
4. **See providers & router** — per-provider tiers/tools/usage/models, and the router's
   `mode` / `custom_order` / frozen `tiers`.

## Constraints (carry the project ethos)

- **Stdlib only**, single `dashboard.py`, `http.server` — no framework, no build step.
- **Config-driven, no per-provider / per-app branches** in the dashboard. It renders whatever
  it discovers on disk. Adding a provider or app type is a filesystem change, never a
  dashboard edit.
- **Read from the sources of truth, don't re-derive.** No inline CLI scraping (today it runs
  `grok models` at import and pulls `/v1/usage` text blobs). Everything is already exported
  to `data/providers_status/` and the config trees.
- **The dashboard orchestrates existing ops, it doesn't reimplement them.** Registration =
  shell out to `integrations/register.py`. Configuration = re-run the instance's `configure`.

## Current state → gaps to close

| Area | Today | Target |
|------|-------|--------|
| Branding | hardcoded "🚀 Grok Proxy Dashboard" | provider-agnostic |
| Providers | `PROVIDERS` fixed to grok/claude/codex via `shutil.which`; agy missing | discovered from `registered_providers/*/config.json` |
| Models | inline `grok models` scrape at import, grok-only | read `data/providers_status/<p>_models.json` |
| Usage | pulls `/v1/usage` text from each proxy | read `data/providers_status/<p>_usage.json` (structured periods) |
| Ports | hardcoded `{grok:8000, claude:8001, codex:8002}` | `config.server.port` + live port from `<p>_run_status.json` |
| App list | reads dead `config/registered_apps/*/config.json` | walk `registered_apps/<app>/<name>/app_meta.json` |
| App register | old `template_<type>.json` + `mapping` writer | shell `integrations/register.py <app> <name> <path> [k=v…]` |
| App config | none | edit instance JSONs + re-run `configure` |
| Router | not shown | view/edit `config/router_config.json` |
| Dialogs | blocking `alert()` | inline status lines |

## Sources of truth (what the dashboard reads/writes)

- `registered_providers/<p>/config.json` — provider def: `server.port`, `tiers` (regex),
  `tools.available/enabled`, execution. **Read**; `tools.enabled` is the only field the
  dashboard writes.
- `data/providers_status/<p>_run_status.json` — live port the proxy published. **Read** (is it
  up, on what port).
- `data/providers_status/<p>_models.json` — `models.available[{id,name}]`. **Read**.
- `data/providers_status/<p>_usage.json` — `periods[{used_pct,remaining_pct,resets}]`. **Read**.
- `config/router_config.json` — `mode`, `custom_order`, `tiers`. **Read/write**.
- `integrations/<app>/` — the app *types* available to register (each folder = one type) and
  its `vault_types.json` presets + `app_settings.json` baseline. **Read** (to populate the
  register form: which types, which vault_types, which extras).
- `registered_apps/<app>/<name>/` — registered instances: `app_meta.json`,
  `app_settings.json`, `vault_types.json`, `configure.py`. **Read/write** (configuration).
- `integrations/register.py` — invoked as a subprocess to register. **Execute**.

## Information architecture (panels)

### 1. Control Center (fleet)
Per discovered provider: name, configured port (`config.server.port`), live state from
`<p>_run_status.json` (🟢 up on port N / ⚪ down), PID, quota summary from `<p>_usage.json`
(e.g. `session 41% left · week 68%`). Actions: **Launch** (default port from config),
**Kill** (PID), **Login** (open the CLI in a terminal). Separate rows for **Router** (11434)
and **Dashboard** (8080). "Start all" = the `tbuffet start` fleet.

### 2. Providers
Per provider card: resolved tier → model table (from `router_config.tiers` + `<p>_models.json`
names), full `models.available` list, and `tools.available` checkboxes writing
`tools.enabled`. No provider-specific markup — purely data-driven.

### 3. Router
Show `mode` (`usage` / `custom`), the `custom_order` list, and the frozen `tiers` map
(tier → [{provider, model}]). Edit: toggle `mode`, reorder `custom_order` (drag/up-down).
Writing back is a plain rewrite of `router_config.json`. Note it's read once at router start —
changes need a router restart (surface that).

### 4. App Registration
Form driven entirely by `integrations/`:
- **App type** — one option per folder in `integrations/` (minus `_base`): `obsidian`,
  `claudia`, `outlook`, …
- **Name** — instance name → `registered_apps/<app>/<name>/`.
- **Path** — the app's root (vault folder for obsidian).
- **Extras** — key/value rows. For obsidian, `vault_type` is offered as a dropdown populated
  from that type's `vault_types.json` keys (`default`, `finance-conference`, …). Generic: any
  `[placeholder]` the type's `app_meta.json` declares can be surfaced as a field.

Submit → `POST /api/apps/register` → dashboard shells:
```
python register.py <app> <name> "<path>" vault_type=<vt> [extra=val …]
```
(run with cwd = `integrations/`). register copies the type's files into the instance,
substitutes `[app_path]`/`[extra]` in `app_meta.json`, runs `init` (scaffold, e.g.
`_Inbox/`) and `configure` (apply settings into the app's own config file).

### 5. App Configuration
For each registered instance, an editor over its three JSONs:
- `app_meta.json` — concrete `location`, `vault_type` (read-mostly; vault_type editable).
- `app_settings.json` — the instance overrides (free JSON edit, or known-key form).
- `vault_types.json` — the preset map (editable).
Action: **Apply** → `POST /api/apps/<app>/<name>/configure` → re-run that instance's
`configure()` (import from the instance dir with cwd set there, as register does). This
re-pushes settings + the vault_type preset into the target `location` file, preserving its
other keys. Re-runnable any number of times.

### 6. Requests & logs
Keep the recent-requests table (parse `data/logs/sessions/req_*.log`), made provider-generic
(it already keys off the filename's provider segment).

## Usability & UX ideation (tabs, basic/advanced, personas, use cases)

The 6 panels above are the technical information architecture. This section reframes them into a
persona- and task-driven layout: **tabs ordered simplest → most advanced**, each with a *basic*
surface and an *advanced* disclosure, so a non-technical user never meets routing internals unless
they ask for them. A single header **Advanced mode** switch (off by default, remembered) reveals the
advanced tabs and the advanced controls inside every tab.

### Who uses it (personas)

| Persona | Goal | Lives in |
|---------|------|----------|
| **Everyday user** (non-technical) | "Make my apps smart with my AI subscriptions, and tell me it's working." | Home, My Apps |
| **Setter-upper** (semi-technical helper/consultant) | Install once, connect accounts + a few apps, hand it over. | + Accounts |
| **Operator / tinkerer** (you) | Tune routing, watch logs, add providers/app types. | all tabs + Advanced |

### Everything controllable (inventory)

| Area | Control | Basic / Adv | Who |
|------|---------|-------------|-----|
| Fleet | **Start everything / Stop everything** | Basic | Everyday |
| Fleet | Restart one component | Basic | Everyday |
| Fleet | Launch / Kill a specific proxy | Adv | Operator |
| Fleet | Router start / stop / restart | Adv | Operator |
| Fleet | Refresh usage now | Basic | Everyday |
| Fleet | Usage refresh interval | Adv | Operator |
| Accounts | **Log in** to a provider CLI | Basic | Everyday / Setter |
| Accounts | Enable / disable a provider in routing | Basic | Setter |
| Accounts | See quota / limits (gauges) | Basic | Everyday |
| Accounts | Re-scrape models / usage | Adv | Operator |
| Accounts | Enable / disable tools per provider | Adv | Operator |
| Accounts | Sandbox on/off per provider | Adv | Operator |
| Apps | **Add (register) an app** | Basic | Everyday / Setter |
| Apps | Choose a preset (vault_type / template) | Basic | Everyday |
| Apps | Re-apply (configure) | Basic | Setter |
| Apps | Remove an app | Basic | Everyday |
| Apps | Edit an app's settings (JSON / known-key form) | Adv | Setter / Operator |
| Apps | Per-task "smart level" (ingest/lint/query → tier) | Adv | Setter |
| Routing | Mode: balance vs preference | Adv | Operator |
| Routing | Preferred account order (`custom_order`) | Adv | Operator |
| Routing | Tier → model pinning (`tiers`) | Adv | Operator |
| Routing | Repopulate tiers (rebuild from regex) | Adv | Operator |
| Activity | View recent requests | Basic (view) | all |
| Activity | Live routing log / open log files | Adv | Operator |

### Tab breakdown (basic surface → advanced disclosure)

- **Home** *(maps: Control Center + usage summary)* — one hero status line ("All systems go" /
  "2 of 4 accounts need login"), a big **Start everything** button, quota gauges per account, and a
  list of connected apps with green/red dots. *Advanced:* per-component rows (router, dashboard, each
  proxy) with port/PID and launch/kill/restart, plus the refresh interval.
- **My Apps** *(maps: App Registration + Configuration)* — cards of connected apps (icon, name,
  "Obsidian · finance-conference", green dot) with **Re-apply** and **Remove**. **＋ Add an app** opens
  a wizard: pick the app (icons), pick the folder/path, pick a preset (plain descriptions), Finish.
  *Advanced:* raw editors for `app_meta` / `app_settings` / `vault_types`, and per-task smart-level
  dropdowns.
- **Accounts** *(maps: Providers)* — one card per AI subscription: logo, "Logged in ✓ / Log in", a
  quota gauge, an Enable/Disable switch. *Advanced:* tools checkboxes, sandbox toggle, model list,
  re-scrape.
- **Routing** *(advanced-only; maps: Router)* — reduced on its (optional) basic surface to a single
  choice: *"Spread work across accounts (save quota)"* vs *"Always use my best account first"* →
  `usage` vs `custom`. *Advanced:* provider-order drag list, tier→model table, repopulate, and a
  restart-required banner.
- **Activity** *(advanced; maps: Requests & logs)* — basic: recent requests in plain English
  ("Obsidian asked Claude · 2m ago · ok"). *Advanced:* live router-log tail, open log files, filter.

### Most common use cases → shortest path

| I want to… | Path | Tab(s) |
|------------|------|--------|
| Turn it all on | Home → **Start everything** | Home |
| Log into my AI accounts | Accounts → **Log in** on each red one | Accounts |
| Make my notes app smart | My Apps → **Add an app** → Obsidian → pick vault → pick preset → Finish | My Apps |
| Check I'm not out of quota | Home gauges (or Accounts) | Home |
| Fix "it stopped working" | Home → restart the red component | Home |
| Always prefer Claude | Routing → "Use my best account first" (+ order) | Routing (adv) |
| Change what a vault extracts | My Apps → app → preset (or Advanced → tags) | My Apps |
| See what just happened | Activity → recent requests | Activity |

### Non-technical intuitiveness

**Principles**
- **Plain words over jargon** (mapping below); internals (tiers, regex, ports) never appear on a
  basic surface.
- **Status is visual** — green/amber/red dots and quota gauges, never raw JSON.
- **One primary action per screen** (Start everything; Add an app; Log in).
- **Wizards for anything multi-step** (registration), with presets carrying plain descriptions, not
  tag strings.
- **Advanced is opt-in and remembered** — basic users never meet routing/providers internals.
- **Safe by default** — confirm Remove/Kill, inline status lines (never blocking `alert()`), back up
  a target file before Apply overwrites it.
- **Explain consequences in situ** — e.g. "Routing changes need a restart to take effect" shown next
  to the control.

**Jargon → plain language**

| Internal | Shown to the everyday user |
|----------|----------------------------|
| Provider | **Account** (your Claude / ChatGPT / Gemini / Grok) |
| Proxy up on port 8001 | 🟢 **Claude connected** |
| Tier `fast` / `medium` / `reasoning` | **Quick / Balanced / Best** |
| Router mode `usage` / `custom` | **Spread work** / **Use best first** |
| `custom_order` | **Preferred account order** |
| Integration / app type | **App** |
| `vault_type` preset | **Template** (e.g. "Research papers", "Journal") |
| `register` / `configure` | **Connect** / **Re-apply** |
| `remaining_pct` | **Quota gauge** (% left, resets in …) |

**Per-tab rating + the one friction to fix**

| Tab | Non-tech rating | Main friction to fix |
|-----|-----------------|----------------------|
| Home | ★★★★★ | none |
| My Apps | ★★★★☆ | folder/path entry — needs a picker, not typed paths |
| Accounts | ★★★★☆ | Login opens a terminal TUI — must be wrapped/guided |
| Routing | ★★☆☆☆ (hidden) | internals; expose only the single plain toggle on basic |
| Activity | ★★★☆☆ | keep the basic view plain-English; raw logs stay advanced |

**Biggest non-technical risks (call out early)**
1. **CLI login** — provider auth happens in an interactive terminal TUI; a non-technical user can't be
   dropped into that. Needs a guided/wrapped login flow, or a one-time setter-upper step.
2. **Path entry** — typing a vault/app path is error-prone; needs a folder picker (or drag-a-folder).
3. **Restart-to-apply** — routing/provider edits only take effect on restart; must be surfaced and
   ideally automated (offer a one-click restart of the affected component).

## UI direction: Progressive Hub (chosen)

A single page that is **friendly by default and morphs dense on demand**. One header
**Advanced** switch (off by default, remembered in `localStorage`) toggles a `body.adv` class;
CSS then reveals the advanced blocks (ports, PIDs, logs, routing internals, raw JSON) and
tightens spacing. Everyday users see cards + one hero action; the operator flips one switch and
gets the control-room density — same page, no separate "pro mode" build.

### Design philosophy
- **Calm, not busy.** Whitespace, few colors, one primary action per screen.
- **Status is the hero.** The first thing you see is "is it working?" in one line + colored dots.
- **Plain words** (per the jargon table above): Accounts, Apps, Quick/Balanced/Best, Templates.
- **Nothing blocks.** Inline toasts and status lines, never `alert()`; destructive actions confirm.
- **Progressive disclosure** does the heavy lifting — complexity exists, it's just folded away.

### Visual language (stdlib-achievable: one hand-written CSS block, CSS variables)
- **Theme:** light default, dark via `prefers-color-scheme` + a manual override; all colors are
  CSS vars (`--bg`, `--card`, `--accent`, `--ok`, `--warn`, `--down`, `--muted`).
- **Accent:** one calm indigo/blue. **Status palette:** green = up/ready, amber = needs you
  (login / low quota), red = down/error, grey = disabled/unknown.
- **Status vocabulary (consistent everywhere):** `●` up · `●` (amber) attention · `○` down ·
  `✓` ready · `⚠` action needed.
- **Cards:** rounded, soft shadow, generous padding. **Gauge:** horizontal bar + `%` + "resets in…".
- **Type:** system font stack; one display size for the hero line, one body size, one small/meta.
- **Motion:** tiny (dot pulse on "up", 150ms toggle); nothing that distracts.

### Tab bar
`Home · My Apps · Accounts` always visible. **`Routing · Activity` appear only when Advanced is
on** (they're operator surfaces). The Advanced switch lives top-right, always.

### Screen mockups

**Home — basic**
```
 tbuffet                                   [ Advanced ◯ ]
 ──────────────────────────────────────────────────────────────
  ● All systems go

  ┌─ Claude ──┐ ┌─ Codex ───┐ ┌─ Grok ────┐ ┌─ Agy ─────┐
  │  ✓ ready  │ │  ✓ ready  │ │  ⚠ log in │ │  ✓ ready  │
  │ ▓▓▓░ 41%  │ │ ▓▓▓▓ 68%  │ │   ----    │ │ ▓░░░ 12%  │
  │ resets 3h │ │ resets 1d │ │           │ │ resets 5h │
  └───────────┘ └───────────┘ └───────────┘ └───────────┘

               [  ▶  Start everything  ]

  Connected apps
  📓 LLM Wiki Play · finance-conference · ●                [open]
  ＋ Add an app
```

**Home — Advanced on** (same screen, morphed)
```
 tbuffet                                   [ Advanced ● ]
 ──────────────────────────────────────────────────────────────
  ● All systems go              refresh every 30m   [⟳ now]

  COMPONENT   STATE     PORT   PID    QUOTA
  router      ● up      11434  4290   —
  dashboard   ● up       8080  4120   —
  claude      ● up       8001  4312   41% ▓▓▓░   [kill][login]
  codex       ● up       8002  4410   68% ▓▓▓▓   [kill][login]
  grok        ○ down      ---   ---   ---         [launch][login]
  agy         ● up       8003  4502   12% ▓░░░   [kill][login]
  [Start all]  [Stop all]
```

**My Apps — basic** (cards + add tile; Advanced adds raw JSON + per-task smart-level)
```
  ┌──────────────────────────────────────────────┐
  │ 📓 LLM Wiki Play                             ●│
  │    Obsidian · finance-conference              │
  │    [ Re-apply ]   [ Remove ]          [ open ]│
  └──────────────────────────────────────────────┘
  ┌──────────────────────────────────────────────┐
  │ ＋  Add an app                                │
  └──────────────────────────────────────────────┘
```

**Add-an-app wizard** (modal; 3 steps → runs `register.py`, streams result inline)
```
  Add an app                                           (1 / 3)
  ───────────────────────────────────────────────────────────
  Pick the app
    ◉ 📓 Obsidian        ○ 🧠 Claudia
    ○ 🦁 Brave Leo       ○ 🏠 Home Assistant
                                              [ Next → ]
  step 2: choose folder (picker)   step 3: pick a Template
  (vault_type, shown with plain descriptions) → [ Finish ]
```

**Accounts — basic** (Advanced adds tools checkboxes, sandbox, model list, re-scrape)
```
  ┌─ Claude ───────────────┐ ┌─ Codex ────────────────┐
  │ ✓ Logged in            │ │ ✓ Logged in            │
  │ ▓▓▓░ 41%  · resets 3h  │ │ ▓▓▓▓ 68%  · resets 1d  │
  │ Enabled  ●———          │ │ Enabled  ●———          │
  └────────────────────────┘ └────────────────────────┘
  ┌─ Grok ─────────────────┐ ┌─ Agy ──────────────────┐
  │ ⚠ Not logged in        │ │ ✓ Logged in            │
  │ [ Log in ]             │ │ ▓░░░ 12%  · resets 5h  │
  │ Enabled  ◯———          │ │ Enabled  ●———          │
  └────────────────────────┘ └────────────────────────┘
```

**Routing — Advanced only** (basic surface is just the one plain choice at top)
```
  How should requests pick an account?
    ◉ Spread work across accounts   (save quota)   ← usage
    ○ Always use my best account first             ← custom
  ────────────────────────────────────────────────────────
  Preferred order          Tiers → models
    1. claude  ⬍            Quick     → claude Haiku
    2. codex   ⬍            Balanced  → claude Sonnet
    3. agy     ⬍            Best      → claude Opus
    4. grok    ⬍
  ⚠ Changes apply after a router restart   [ Restart router ]
```

**Activity — Advanced** (basic = plain recent list; advanced = live log tail)
```
  2m   Obsidian → Claude (Opus)    query    ok
  5m   Obsidian → Claude (Haiku)   ingest   ok
  1h   Brave    → Codex            chat     ok
  [ Live log ▾ ]   router.log tailing…
```

### Component kit (what we actually build once, reuse everywhere)
`statusDot`, `quotaGauge`, `card`, `toggleSwitch`, `heroButton`, `wizardModal`, `toast`,
`kvEditor` (JSON/known-key form), `dragList` (custom_order). All plain DOM + the one CSS block.

### Key interactions
- **Polling:** one `GET /api/fleet` on a short interval repaints status dots/gauges; no sockets.
- **Start everything / Launch / Kill / Login:** `POST /api/fleet/*`, result as a toast; the row
  updates on the next poll. Login explains it opens a terminal (the known non-tech friction).
- **Add an app:** wizard collects `{app, path, template}`, `POST /api/apps/register`, streams
  `register.py` stdout into the modal, then shows the new card.
- **Re-apply / Remove:** `POST …/configure` / delete instance (confirm).
- **Routing edits:** write `router_config.json`, show the restart banner + one-click restart.

### Implementation notes (keep the project ethos)
- **Still one `dashboard.py`, stdlib `http.server`.** It serves a single self-contained HTML page
  (inline CSS + vanilla JS) and the JSON/exec endpoints below. No framework, no build.
- **Data-driven:** cards/rows are rendered from `/api/fleet`, `/api/providers`, `/api/apps`,
  `/api/apps/types` — adding a provider or app type never touches the dashboard.
- **Advanced is pure CSS:** `body.adv` reveals `.adv` blocks; the switch only toggles the class +
  `localStorage`. No duplicate markup, no second page.

### Accounts screen — layout explorations

The Accounts tab carries both the highest-frequency actions (glance at status+quota) and the
highest-friction one (CLI login). Jobs ranked by how often users do them:

| Action | Frequency | Urgency | Who |
|--------|-----------|---------|-----|
| Glance at status + quota | **every visit** | low | everyone |
| Log in / re-auth (expired) | occasional | **high/blocking** | everyone |
| Enable/disable in routing | rare | low | setter/operator |
| Tools / sandbox / models / re-scrape | very rare | low | operator |

→ The layout must make **status+quota instantly scannable** and **login unmissable when needed**.

**A — Card grid** (friendly, equal-weight). Pros: approachable, self-contained cards, demo-ready.
Cons: wraps past ~6 accounts, the broken card doesn't stand out, space-hungry. Best for everyday
users with few accounts. Tradeoff: calm uniformity over triage.

**B — Compact table** (`account | status | quota | resets | routing | actions`). Pros: densest
scan, quotas align for comparison, scales, sortable. Cons: spreadsheet feel (intimidating),
cramped actions. Best for the operator (Advanced). Tradeoff: density over approachability.

**C — Quota-first gauges** (sorted by headroom). Pros: answers "which account has room / am I about
to run out" instantly. Cons: login/enable buried under bars. Best for usage-mode quota watchers.
Tradeoff: serves monitoring, under-serves fix-it.

**D — Attention-first triage** ("Needs you (N)" band up top; healthy accounts collapse to a strip).
Pros: the must-do action is huge and first, zero hunting, scales. Cons: hides per-account quota
behind "expand" when healthy — the every-visit glance costs a click; layout shifts with health.
Best for "just tell me if anything needs me." Tradeoff: fix-it/calm over always-visible quota.

**E — Hero "up next" + slim list** (highlights the account routing will hit next). Pros: shows the
consequence of routing. Cons: "up next" is ambiguous across tiers; novel pattern. Tradeoff:
editorializes one account; weaker for even-handed management.

**Chosen: D's triage logic folded into A's cards**, morphing to B under Advanced:
- A **"Needs you"** band appears above the grid *only when* an account needs login / is depleted —
  so login is unmissable when it matters, absent when it doesn't.
- Healthy cards are **not collapsed** (fixes D's weakness) → quota stays always-visible.
- **Advanced ON** swaps the grid for table **B** with tools/sandbox/models/re-scrape.
- Net: **basic = triage-band + card grid; advanced = table** — serves the #1 (glance) and #2
  (fix login) jobs directly, stays friendly, reuses the one Progressive-Hub mechanic.

### Add-an-app wizard — layout explorations

The wizard is the highest-stakes surface: first-run success here is what makes or breaks adoption,
and it carries the two frictions flagged earlier — **path entry** and **restart-to-apply**. Unlike
Accounts it's a *flow*, so the ranking axis is steps by friction / failure-risk, grounded in what
`register.py` actually consumes (`{app, name, path, extras}` → copy type files → substitute
`[app_path]`/`[vault_type]` → `init` + `configure`):

| Step | Collects | Friction | Failure if wrong |
|------|----------|----------|------------------|
| Pick app type | a folder under `integrations/` (minus `_base`) | low | — |
| Name the instance | `registered_apps/<app>/<name>/` | medium — easy to skip | **silent overwrite** of an existing app (`mkdir exist_ok` + copy) |
| Pick folder / path | app root → `[app_path]` | **high** | `configure` writes into a bad `location`; half-registered instance |
| Pick a Template (preset) | `vault_type` key → plain description | medium | wrong extraction behavior — but fixable later via Re-apply |
| Run & watch | streams `register.py` stdout | medium | `init`/`configure` error leaves a silent half-registered instance |

→ The flow must **make the path unmissable and hard to get wrong**, **never silently clobber** an
existing instance, and **show the register run** so failures surface instead of hiding.

**A — Linear stepper** (one decision per screen, Next/Back; the current mockup above). Pros: lowest
cognitive load, each step explained, demo-ready. Cons: 4–5 clicks for a repeat adder, name+path
buried mid-flow, no at-a-glance overview. Best for first-timers. Tradeoff: hand-holding over speed.

**B — Single scrolling form** (all fields on one panel, inline validation, one Finish). Pros:
fastest for a setter-upper adding several, whole thing visible, no step state. Cons: a wall of
fields intimidates a novice; path picker and template dropdown compete for attention. Best for the
repeat installer. Tradeoff: speed/overview over gentleness.

**C — Pick-app-first branching** (choose the app, then the form morphs to only *that* type's fields).
Pros: shows only relevant extras (obsidian → Template; claudia → none), honors the config-driven
ethos, no dead fields. Cons: layout shifts after step 1; two-stage feel. Best when app types have
very different extras. Tradeoff: relevance over a stable layout.

**D — Folder-first** (drag-a-folder / pick a folder, infer the app type from its contents, e.g.
`.obsidian/` present → Obsidian). Pros: kills the #1 friction by making the folder *the* entry point
and auto-selecting the app. Cons: detection is heuristic and per-app — fights the no-per-app-branch
rule unless the detection signature itself lives in each type's config; ambiguous folders need a
fallback. Best for the "just point at my vault" user. Tradeoff: magic over explicitness.

**E — Template-first gallery** (lead with the outcome — "Research papers", "Finance conference",
"Journal" — then app + folder). Pros: sells the value, leads with intent not mechanism, reuses the
presets' plain descriptions. Cons: Template is obsidian-specific (`vault_type`); other app types
have no presets, so the lead step is empty for them; inverts the natural "which app?" question. Best
for outcome-driven note users. Tradeoff: markets the value but doesn't generalize across types.

**Chosen: A's linear stepper as the spine, with C's per-app morphing and a Review-&-run close:**
- **Step 1 pick app** (icons) → the remaining steps are driven by that type's declared
  `[placeholders]` + `vault_types.json` keys (C), so claudia (no extras) skips the Template step —
  no dead fields, stays config-driven.
- **Step 2 name + folder on one screen**, with the **folder picker** (fixes the #1 path friction)
  and the **name defaulted from the folder name** — closing the current mockup's missing-name gap —
  plus a **collision warning** when `registered_apps/<app>/<name>/` already exists (register
  overwrites silently otherwise).
- **Step 3 Template** shows `vault_type` keys with plain descriptions; D's heuristic app-detection is
  *avoided* — the folder picker makes the app explicit, no per-app sniffing branch.
- **Final Review & run** streams `register.py` stdout inline and surfaces an `init`/`configure`
  failure instead of leaving a silent half-registered instance.
- Net: a first-timer gets a guided 3–4 step flow; the per-app morph keeps it honest to the configs;
  the run step makes failures visible. Reuses `wizardModal` + one new folder-picker component.

## Files & data surface (implementation reference)

Concrete map of every file/call the dashboard touches **now** vs **after the revamp**. The dashboard
is a single source file — `src/tokenbuffet/dashboard.py` (inline HTML/CSS/JS + handlers, no separate
assets). Everything below is data it renders, mutates, or shells out to; line numbers are the current
code. The ⚠️ rows are exactly what the revamp removes (inline scrapes, hardcoded ports, dead paths).

**Reads**

| Path | Now | After revamp |
|------|-----|--------------|
| `registered_providers/<p>/config.json` | ✅ (511, 730) | keep — port, tiers, tools, execution |
| `data/providers_status/<p>_usage.json` | ✅ (582) + inline `/v1/usage` scrape | sole usage source (drop the scrape) |
| `data/providers_status/<p>_run_status.json` | — | 🆕 live port + up/down (replaces hardcoded ports) |
| `data/providers_status/<p>_models.json` | — (uses `grok models`) | 🆕 model lists (replaces the scrape) |
| `config/router_config.json` | — | 🆕 mode / custom_order / tiers (new Router panel) |
| `registered_apps/<app>/<name>/app_meta.json` | — | 🆕 walk for the app list |
| `registered_apps/<app>/<name>/app_settings.json` | — | 🆕 instance settings editor |
| `registered_apps/<app>/<name>/vault_types.json` | — | 🆕 preset editor |
| `integrations/<app>/` (`vault_types.json`, `app_settings.json`, `[placeholders]`) | — | 🆕 drives the Add-an-app form |
| `data/logs/sessions/req_*.log` | ✅ (454) | keep — made provider-generic |
| `data/logs/proxy.log` | ✅ (9, 783) | keep |
| `config/registered_apps/*/config.json` | ⚠️ dead path (743) | ❌ removed |
| `registered_apps/template_{app_type}.json` | ⚠️ stale (656, 658) | ❌ removed |

**Writes**

| Path | Now | After revamp |
|------|-----|--------------|
| `registered_providers/<p>/config.json` (`tools.enabled` only) | ✅ (536) | keep |
| `config/router_config.json` (`mode`, `custom_order`) | — | 🆕 Router panel edits |
| `registered_apps/<app>/<name>/*.json` (instance JSONs) | — | 🆕 config editor |
| `registered_apps/<name>/config.json` + app target file | ⚠️ stale register (675, 706) | ❌ replaced by `register.py` / `configure` |

**Executes / calls**

| Call | Now | After revamp |
|------|-----|--------------|
| `integrations/register.py <app> <name> <path> [k=v…]` | — | 🆕 the register pipeline |
| instance `registered_apps/<app>/<name>/configure.py` → `configure()` | — | 🆕 re-apply settings |
| launch proxy (`cli_proxy_server`), kill PID, login (open CLI) | ✅ (558, 594, 622–629) | keep — PIDs from `_run_status.json`, process scan only as fallback |
| router start / stop / restart | — | 🆕 fleet control + restart-to-apply |
| `grok models` scrape · inline `/v1/usage` · `wmic`/`tasklist`/`ps` for state | ✅ (436, 764, 799, 808, 843) | ❌ removed — read the status JSONs instead |

Endpoints the revamp serves are listed in the **HTTP API** section below (all handled inside
`dashboard.py`).

## Appendix: config schemas & sample data

Real samples (trimmed) of every file the dashboard reads, so the UI can be built against concrete
shapes without touching the live tree. Paths are relative to the workspace root.

### Provider definition — `registered_providers/<p>/config.json`

The dashboard reads `server.port`, `tiers` (regex), `tools.available`/`tools.enabled`, and
`execution.sandbox`. It writes **only** `tools.enabled`. (Sample = `grok`, the simplest provider; the
`usage`/`models`/`stream` blocks drive the extractor subsystem, not the dashboard — shown abbreviated.)

```jsonc
{
  "server": { "port": 8000, "protocol": "responses" },
  "tiers": {                       // regex per semantic tier (resolved once into router_config)
    "fast":      "build-fast$",
    "medium":    "grok-4\\.6",
    "reasoning": "grok-4\\.7$"
  },
  "tools": {
    "available": ["Bash", "Edit", "Read", "WebSearch"],
    "enabled":   ["Bash"],         // <-- the ONLY field the dashboard writes
    "arg_format": "comma_separated",
    "arg_flag":   "--tools"
  },
  "execution": {
    "cmd_template": ["…grok.exe", "--output-format", "streaming-messages-json", "--prompt-file", "{prompt_file}"],
    "model_arg": ["--model", "{model}"],
    "input_method": "file",
    "sandbox": { "enabled": true, "env_var": "GROK_HOME", "copy_auth": "~\\.grok\\auth.json" }
  },
  "usage":  { "type": "tui", "command": "/usage", "periods": { "daily": {…}, "weekly": {…} } },
  "models": { "type": "subcmd", "list_cmd": ["grok", "models"] },
  "stream": { "text_extractors": [ { "matches": {…}, "path": "event.delta.text" } ] }
}
```

### Provider live port — `data/providers_status/<p>_run_status.json`

Published by each proxy at startup; the dashboard reads it for up/down + the actual bound port.

```json
{ "port": 8000 }
```

### Provider usage — `data/providers_status/<p>_usage.json`

Note the **real shape** is `usage.limits.<named-period>` (not a flat `periods[]` list). A period the
CLI didn't report is `null`. `remaining_pct` is canonical; `used_pct` is its complement.

```json
{
  "provider": "grok",
  "usage": {
    "plan": "SuperGrok",
    "limits": {
      "daily": null,
      "weekly": { "used_pct": 12.0, "remaining_pct": 88.0, "resets": "October 15, 18:30" }
    },
    "gathered_at": "2026-10-09T17:39:01-07:00"
  }
}
```

### Provider models — `data/providers_status/<p>_models.json`

`available[].id` is the exact `--model` argument; `name` is the friendly TUI label. Single source of
truth for `/v1/models` and for the router's one-time tier resolution.

```json
{
  "provider": "grok",
  "models": {
    "available": [
      { "id": "grok-4.7", "name": "grok-4.7" },
      { "id": "grok-4.7-build-fast", "name": "grok-4.7-build-fast" },
      { "id": "grok-4.6", "name": "grok-4.6" }
    ],
    "default": "grok-4.7"
  }
}
```

### Router — `config/router_config.json`

`mode` is `usage` (load-balance by most remaining quota) or `custom` (follow `custom_order`). `tiers`
is the frozen snapshot of exact `{provider, model}` per tier (one tier shown; `fast`/`medium`/
`reasoning` all follow the same shape).

```json
{
  "mode": "usage",
  "custom_order": ["claude", "codex", "agy", "grok"],
  "tiers": {
    "reasoning": [
      { "provider": "agy",    "model": "gemini-3.1-pro-high" },
      { "provider": "claude", "model": "Opus" },
      { "provider": "codex",  "model": "GPT-6-Astra" },
      { "provider": "grok",   "model": "grok-4.7" }
    ]
  }
}
```

### App type (register form source) — `integrations/<app>/`

`app_meta.json` carries `[placeholders]` substituted at register time; `vault_types.json` is the preset
map offered as "Templates"; `app_settings.json` is the baseline pushed into the app.

```json
// integrations/obsidian/app_meta.json
{ "app": "obsidian", "location": "[app_path]/.obsidian/plugins/karpathywiki/data.json", "vault_type": "[vault_type]" }
```
```json
// integrations/obsidian/vault_types.json  (keys become the "Template" dropdown)
{
  "default": {},
  "finance-conference": {
    "tagVocabularyMode": "custom",
    "customEntityTags": "person, organization, fund, asset_class, instrument, index, other",
    "customConceptTags": "financial_strategy, portfolio_archetype, action_playbook, theory, terminology",
    "customQueryInstructions": "This is a financial conference transcript. Focus on …"
  },
  "research-papers": { "…": "…" },
  "daily-notes":     { "…": "…" }
}
```

### Registered app instance — `registered_apps/<app>/<name>/`

After register, `[placeholders]` are concrete. `app_meta.json` is read-mostly (the dashboard walks it
for the app list); `app_settings.json` is the instance editor target; `configure.py` is re-run on Apply.

```json
// registered_apps/obsidian/llm-wiki-play/app_meta.json
{ "app": "obsidian", "location": "M:/My Drive/basisconf/LLM Wiki Play/.obsidian/plugins/karpathywiki/data.json", "vault_type": "finance-conference" }
```
```jsonc
// registered_apps/obsidian/llm-wiki-play/app_settings.json  (abbreviated)
{
  "provider": "custom-responses",
  "baseUrl": "http://127.0.0.1:8090/v1/",      // points at the router
  "model": "fast",
  "availableModels": ["fast", "medium", "reasoning"],
  "usePerTaskModels": true,
  "ingestModel": "fast", "lintModel": "reasoning", "queryModel": "reasoning",
  "tagVocabularyMode": "default",
  "periodicLint": "weekly", "autoSmartFix": true,
  "maxTokensPerCall": 65536
  // …plus lint thresholds, temperatures, watched folders
}
```

### Logs

**`data/logs/proxy.log`** — fleet start lines:
```
Starting http.server Proxy for agy on port 8003
Starting http.server Proxy for claude on port 8001
Starting http.server Proxy for grok on port 8000
Starting http.server Proxy for codex on port 8002
```

**`data/logs/sessions/req_*.log`** — the recent-requests table. Filename encodes everything the table
needs: `req_<provider>_<YYYYMMDD>_<HHMMSS>_<reqid>.log` (e.g. `req_claude_20261011_204213_6b959df8.log`).
Status is inferred from body markers: `"Output received:"` → **Completed**, `"Proxy Error"` → **Error**,
else **In Progress**. (None present in the current tree — proxies write them per request.)

**`data/logs/<p>/proxy/raw_requests/req_<p>_<ts>_<id>.json`** — the raw Responses-API payload the proxy
received (the `/v1/responses` wire). Useful for debugging what an app actually sent:
```jsonc
{
  "model": "Opus",
  "input": [
    { "role": "system", "content": "…schema + tag vocabulary system prompt…" },
    { "role": "user",   "content": [ { "type": "input_text", "text": "…the task prompt…" } ] }
  ],
  "temperature": 0.2,
  "max_output_tokens": 8000
}
```

## HTTP API

Read:
- `GET /api/fleet` — providers (config port, live port/up, pid, usage summary) + router +
  dashboard state. Replaces the grok-centric `/api/stats` process scan; prefer
  `<p>_run_status.json` over `wmic`/`tasklist`/`ps`, fall back to a scan only to find PIDs.
- `GET /api/providers` — each `registered_providers/*/config.json` + merged `_models.json`.
- `GET /api/router` — `router_config.json`.
- `GET /api/apps/types` — folders under `integrations/` (minus `_base`), each with its
  `vault_types.json` keys and declared `[placeholders]`.
- `GET /api/apps` — walk `registered_apps/<app>/<name>/app_meta.json`.
- `GET /api/apps/<app>/<name>` — that instance's three JSONs.

Write / execute:
- `POST /api/providers/<p>/tools` — toggle `tools.enabled` (exists today, keep).
- `POST /api/router` — rewrite `mode` / `custom_order`.
- `POST /api/apps/register` — `{app, name, path, extras{}}` → shell `register.py`.
- `POST /api/apps/<app>/<name>` — save edited instance JSON(s).
- `POST /api/apps/<app>/<name>/configure` — re-run `configure`.
- `POST /api/fleet/{launch,kill,login}` — lifecycle (launch reads the port from config, not a
  hardcoded map).

## Non-goals

- No auth / multi-user (localhost operator tool).
- No live config hot-reload of running processes beyond what a restart gives.
- No reimplementing register/configure/init logic in the dashboard — it only invokes them.

## Rollout

1. **De-grok the read path**: discover providers from `registered_providers/`, read
   models/usage/ports from `data/providers_status/` and config. Fix the `/api/apps` path and
   drop the inline `grok models` import scrape. (Pure cleanup, no new UI.)
2. **Registration v2**: `/api/apps/types` + rewrite `/api/apps/register` to shell
   `integrations/register.py`; form driven by discovered types + their `vault_types`.
3. **Configuration**: instance JSON editor + `/configure` re-run.
4. **Router panel**: view + `mode`/`custom_order` edit (flag restart requirement).
5. **Control-center polish**: run_status-based state, inline status lines instead of `alert()`.
```

---

# Appendix A1 — "LLM Providers" & the provider-type / account model

Status: amendment to the design above. **Supersedes** the "Accounts" terminology and the jargon-table
row `Provider → Account` in that body. Where the two conflict, this amendment wins.

## What changes

The earlier spec renamed *provider* to **"Account"** for everyday users. That was wrong — it collapses two
distinct concepts into one. The correct model has **two levels**:

- **LLM Provider (type)** — the vendor/service and *how to talk to it*: Claude, Codex, Grok, Agy. This is the
  thing you **register** (its CLI command, tiers, tools, execution, sandbox). One provider type per
  `registered_providers/<name>/config.json`.
- **Account** — an individual authenticated login/subscription **under** a provider type. A provider type can
  have one or many accounts (e.g. a personal + a work Claude). Each account has its own auth and its own
  **quota**.

So: **provider types contain accounts.** The primary UI term is **"LLM Providers"** (not "Accounts"); accounts
are a layer *inside* each provider.

> **Current state:** exactly **one account per provider type** (the single CLI auth present on the machine).
> The account layer is therefore mostly latent today — but the model, data shapes, and UI should be built so
> adding a second account later is additive, not a rewrite.

## Corrected jargon

| Internal | Shown to the user |
|----------|-------------------|
| `registered_providers/<name>/` (the def) | **LLM Provider** (its *type*: Claude, Grok, …) |
| the CLI's logged-in auth | **Account** (a login under that provider) |
| `remaining_pct` for that auth | the **account's** quota gauge |
| Router `{provider, model}` | picks a **provider** by tier, then an **account** within it |

The dashboard tab formerly called **Accounts** becomes **LLM Providers**.

## Mapping to today's architecture

| Concept | Today (1 account/provider) | With multiple accounts (future) |
|---------|----------------------------|---------------------------------|
| Provider *type* def | `registered_providers/<p>/config.json` | unchanged — still one def per type |
| Account auth | the single CLI auth (e.g. `~/.grok/auth.json`) | N auths per type (per-account auth files / sandbox homes) |
| Quota | `data/providers_status/<p>_usage.json` | per account: `…/<p>/<account>_usage.json` (or nested) |
| Live state | `data/providers_status/<p>_run_status.json` | per account |
| Routing unit | `{provider, model}` | `{provider, account, model}` — tier → type → pick account by quota |

Nothing in the current data layout has to change *now*; the single account is implicit. The amendment only
fixes the **vocabulary** and reserves the **account** level so the quota/routing/registration surfaces can grow
into it.

## Registering & controls (the "LLM Providers" surface)

Two registration actions, now clearly separated:

1. **Register a provider (type)** — add a new `registered_providers/<name>/config.json` (today via the
   `register-provider` skill; the dashboard can expose an "Add provider" entry that scaffolds from
   `template_config.json`). This defines *how* to drive that vendor's CLI.
2. **Add / log in an account** — under an existing provider type, authenticate a login. Today this is the
   single CLI login (the existing **Log in** control). With the account model it becomes "**＋ Add account**"
   per provider, each with its own Log in / Remove and its own quota gauge.

Per-provider controls (unchanged in spirit, re-homed under the provider → account tree):

- **Provider level:** enable/disable in routing, tools checkboxes, sandbox toggle, model list, re-scrape.
- **Account level:** Log in / re-auth, quota gauge, enable/disable *this account*, remove.

## Home surface — available-tokens focus

Home's hero is **how much you have left, everywhere** — a quota overview **per provider type, broken down by
account**, sorted most-remaining-first (mirrors what `usage`-mode routing picks). "Available tokens" is the
extractor's **remaining quota as a percentage + reset time** per period (e.g. `weekly 88% · resets Oct 15
18:30`), from `usage.limits.<period>.remaining_pct` / `resets`. Depleted (`<=0%`) or not-logged-in accounts
surface red/amber inline. Start/stop and per-component health move below the roster.

---

# Appendix DPR-001 — prototype review

Reviewed against the static [AI Subscription Hub.html](../../demo/dashboard/AI%20Subscription%20Hub.html),
`src/tokenbuffet/dashboard.py`, and the registration files on 2026-10-13. The HTML is a self-contained
demonstration with hardcoded providers, apps, quota, PIDs, and activity; its controls change browser state only.
It should guide the live dashboard's layout and wording, not be served as operational data.

| Ref | Finding | Recommendation |
| --- | --- | --- |
| `D01` | The prototype's Home, My Apps, LLM Providers, Router Configuration, and Activity navigation is clearer than the current single status page. | Adopt that navigation and responsive layout. Keep operational controls in Advanced mode while leaving health and quota visible on Home. |
| `D02` | The prototype uses hardcoded providers, ports, models, accounts, quotas, and PIDs. The current dashboard also hardcodes some CLIs and probes Grok at import. | Discover provider definitions from `registered_providers`, models and quota from `data/providers_status`, and live process state from the run-status files. Show unknown values plainly. |
| `D03` | The prototype has one illustrative account per provider. The runtime has one CLI login and quota file per provider, with no account-level selector. | Render the existing login as a single account row. Keep add/remove account controls disabled until the runtime supports separate authentication and quota. |
| `D04` | The current dashboard writes `registered_apps/<name>/config.json` but lists `config/registered_apps/*/config.json`; the maintained registration flow writes `registered_apps/<type>/<name>/app_config.json`. | Use the typed instance structure for both registration and listing. Call `integrations/register.py` rather than keeping a second registration implementation in the dashboard. Report initialization/configuration failure to the UI. |
| `D05` | The prototype app wizard implies a real folder picker and live apply, but only simulates them. The current registration accepts an application path and a separate `bridge_configuration` field. | Expose both fields explicitly, default the app path to the instance location, and show the exact target configuration path before applying. Back up a target file before writing it. |
| `D06` | The prototype routing page displays only illustrative model rows. The live router uses `config/router_config.json` with `mode`, `custom_order`, and `providers.<name>.tiers`. | Read and edit the current schema, validate provider names and model IDs, and distinguish saved settings from the router's active settings. |
| `D07` | The prototype activity feed is sample data. The current dashboard reads per-provider session logs, but its summary counters also depend on legacy shared-log assumptions. | Build activity from current root `logs/` session and router records, correlate by request ID, and label missing app attribution as unknown. Keep raw prompt and response content behind Debug logging. |
| `D08` | The prototype offers login, restart, pause, and remove controls without real operations. The current dashboard has separate restart and kill endpoints. | Bind each control to an existing operation with structured success/failure responses. Make the UI refresh from actual process state after each action. Defer global pause until its effect on all running services is defined. |

Suggested build order: first fix data discovery and the app registration/listing mismatch (`D02`, `D04`), then
render the prototype's read-only views (`D01`, `D03`, `D06`, `D07`). Wire operational controls (`D05`, `D08`)
after each action has an unambiguous target and failure response.

---

# Appendix — original control plan (earliest sketch, superseded)

The first idea for a "Control Center": per-provider port field + **Restart** button that shelled a
`start_proxy.ps1` via `Start-Process` to a new visible PowerShell window (so OAuth prompts / crashes stay
visible), driven by a `do_POST` handler on `/api/restart` parsing `{"provider", "port"}`. Superseded by the
fleet model (`tbuffet start`) and the design above; retained only as a record of the original intent.
