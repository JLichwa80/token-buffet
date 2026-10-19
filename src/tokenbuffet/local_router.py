from tokenbuffet.log_paths import LOG_DIR
from tokenbuffet.log_config import console_handler
from tokenbuffet import loopback
import argparse
import http.server
import http.client
import json
import urllib.request
import urllib.error
import logging
import sys
import os
import re
import select
import socket
import glob
import time
import threading
import uuid
import tempfile
from collections import OrderedDict
from urllib.parse import urlsplit

from .gemini_wire import parse_generate_path

sys.stdout.reconfigure(encoding='utf-8')

ROUTER_CONFIG_PATH = os.path.join("config", "router_config.json")


_WARNED = set()


def _build_tiers(skip=()):
    """Resolve each not-yet-snapshotted provider's tier regex to a concrete CLI model id.

    Reads the family regexes from registered_providers/*/config.json and
    resolves each against that provider's /models endpoint (newest-first)
    to an exact --model id. A provider whose models can't be read yet is
    skipped silently (its proxy is still reading them in the background); one
    whose regex matches nothing is skipped for that tier and logged once.
    """
    tiers = {}
    for config_file in sorted(glob.glob("registered_providers/*/config.json")):
        provider = os.path.basename(os.path.dirname(config_file))
        if provider in skip:
            continue
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            logging.error(f"Error parsing {config_file}: {e}")
            continue
        try:
            available = fetch_export(provider, "models")["models"]["available"]
        except (OSError, ValueError, KeyError, TypeError, urllib.error.URLError):
            continue
        ids = [m["id"] if isinstance(m, dict) else m for m in available]
        for tier_name, pattern in config.get("tiers", {}).items():
            model_id = next((mid for mid in ids if re.search(pattern, mid, re.IGNORECASE)), None)
            if model_id is None:
                if (provider, tier_name) not in _WARNED:
                    _WARNED.add((provider, tier_name))
                    logging.warning(f"Populate: {provider} tier '{tier_name}' regex "
                                    f"'{pattern}' matched no model id; skipping.")
                continue
            effort = DEFAULT_TIER_EFFORTS.get(tier_name)
            backend = {"provider": provider, "model": model_id}
            if effort:
                backend["effort"] = effort
            tiers.setdefault(tier_name, []).append(backend)
    return tiers


DEFAULT_TIER_EFFORTS = {
    "fast": "low",
    "medium": "medium",
    "reasoning": "high",
}


def providers_from_tiers(tiers):
    providers = {}
    for tier, backends in tiers.items():
        for backend in backends:
            prov = backend["provider"]
            providers.setdefault(prov, {"tiers": {}})["tiers"][tier] = backend["model"]
            if "effort" in backend:
                providers[prov].setdefault("effort", {})[tier] = backend["effort"]
    return providers


def tiers_from_providers(providers, global_effort=None):
    tiers = {}
    for provider, config in providers.items():
        prov_effort = config.get("effort")
        for tier, model_entry in config.get("tiers", {}).items():
            if isinstance(model_entry, dict):
                model = model_entry.get("model")
                effort = model_entry.get("effort")
            else:
                model = model_entry
                effort = None
            if effort is None and isinstance(prov_effort, dict):
                effort = prov_effort.get(tier) or prov_effort.get(model)
            elif effort is None and isinstance(prov_effort, str):
                effort = prov_effort
            if effort is None and isinstance(global_effort, dict):
                effort = global_effort.get(tier) or global_effort.get(model)
            elif effort is None and isinstance(global_effort, str):
                effort = global_effort
            if effort is None:
                effort = DEFAULT_TIER_EFFORTS.get(tier)

            backend = {"provider": provider, "model": model}
            if effort:
                backend["effort"] = effort
            tiers.setdefault(tier, []).append(backend)
    return tiers


def load_router_config():
    """Load provider-first exact model mappings; migrate the legacy tier map."""
    config = {}
    if os.path.exists(ROUTER_CONFIG_PATH):
        with open(ROUTER_CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
    config.setdefault("mode", "usage")
    config.setdefault("custom_order", [])
    changed = False
    if "providers" not in config and config.get("tiers"):
        config["providers"] = providers_from_tiers(config.pop("tiers"))
        changed = True
    config.setdefault("providers", {})
    if changed:
        save_router_config(config)
    return config


def save_router_config(config):
    os.makedirs(os.path.dirname(ROUTER_CONFIG_PATH), exist_ok=True)
    with open(ROUTER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def populate_providers(config):
    """Freeze exact tier ids for each provider that has none yet; True when any were added.

    Providers read their models in the background, so the refresher calls this
    until every provider has been resolved once. Existing entries (including
    hand-edits) are never touched.
    """
    added = providers_from_tiers(_build_tiers(skip=set(config["providers"])))
    if not added:
        return False
    config["providers"].update(added)
    save_router_config(config)
    logging.info("Populate: froze tiers for %s", ", ".join(sorted(added)))
    return True


def resolve_model(provider, pattern):
    """Resolve a tier's regex to a concrete CLI model id, newest-first.

    Tiers declare a family regex (e.g. 'flash-low$') instead of a pinned
    version, matched against the model ids from that proxy's /models endpoint.
    Returns the FIRST match in
    file order -- the CLIs list newest-first, so that's the newest model in the
    family. None if the endpoint is unavailable or nothing matches.
    """
    try:
        models = fetch_export(provider, "models")["models"]["available"]
    except (OSError, ValueError, KeyError, TypeError, urllib.error.URLError):
        return None
    for m in models:
        mid = m["id"] if isinstance(m, dict) else m
        if re.search(pattern, mid, re.IGNORECASE):
            return mid
    return None


def load_all_models():
    """Every provider's full model catalog as {model_id: provider}, cached once.

    Read from each running proxy's /models endpoint so a
    request naming an exact vendor id (e.g. "claude-opus-4-8") resolves straight
    to its provider, and /v1/models can advertise the full catalog -- not just
    the three tiers. Later ids win on collision (providers don't share ids).
    """
    catalog = {}
    for path in glob.glob("registered_providers/*/config.json"):
        provider = os.path.basename(os.path.dirname(path))
        try:
            available = fetch_export(provider, "models")["models"]["available"]
        except (OSError, ValueError, KeyError, TypeError, urllib.error.URLError):
            continue
        for m in available:
            catalog[m["id"] if isinstance(m, dict) else m] = provider
    return catalog


def running_port(provider):
    """Return a provider port only when status says running and it is listening."""
    try:
        with open(f"data/providers_status/{provider}_run_status.json", encoding="utf-8") as f:
            state = json.load(f)
        if state.get("status") != "running":
            return None
        port = int(state["port"])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return port if loopback.listening(port) else None


def fetch_export(provider, op):
    """Ask one running proxy to own and return its extractor export."""
    port = running_port(provider)
    if port is None:
        raise OSError(f"{provider} proxy is not running")
    with urllib.request.urlopen(loopback.url(port, f"/{op}"), timeout=190) as response:
        data = json.load(response)
    if data.get("provider") != provider or not isinstance(data.get(op), dict):
        raise ValueError(f"invalid {op} export from {provider}")
    return data

os.makedirs(os.path.join(LOG_DIR, "router"), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [ROUTER] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        console_handler(sys.stdout, "%(asctime)s [ROUTER] %(message)s"),
        logging.FileHandler(os.path.join(LOG_DIR, "router", "router.log"), encoding="utf-8", mode="a")
    ]
)

CONFIG = load_router_config()
TIERS = tiers_from_providers(CONFIG.get("providers", {}), CONFIG.get("effort"))
MODE = CONFIG.get("mode", "usage")
CUSTOM_ORDER = CONFIG.get("custom_order", [])
ALL_MODELS = {}
MODELS = list(TIERS.keys())
ADVERTISED = MODELS + [m for m in ALL_MODELS if m not in MODELS]
RESPONSE_CONTEXT = OrderedDict()
RESPONSE_CONTEXT_LOCK = threading.Lock()
RESPONSE_CONTEXT_LIMIT = 100


def _response_input_items(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    if isinstance(value, str):
        return [{"role": "user", "content": value}]
    return []


def remember_response(response, request_input, requested_model):
    if not isinstance(response, dict) or response.get("status") != "completed":
        return
    response_id = response.get("id")
    output = response.get("output")
    if not isinstance(response_id, str) or not isinstance(output, list):
        return
    history = _response_input_items(request_input) + output
    # A process-local cache avoids writing client prompts or tool results to disk.
    if len(json.dumps(history, ensure_ascii=False)) > 500000:
        return
    with RESPONSE_CONTEXT_LOCK:
        RESPONSE_CONTEXT[response_id] = {"history": history,
                                         "requested_model": requested_model}
        RESPONSE_CONTEXT.move_to_end(response_id)
        while len(RESPONSE_CONTEXT) > RESPONSE_CONTEXT_LIMIT:
            RESPONSE_CONTEXT.popitem(last=False)

def load_usage():
    """Each provider's tightest remaining quota, cached in memory (USAGE).

    Routing never scrapes inline; it requests each proxy's /usage endpoint,
    which owns the cached extractor envelope:
        {"provider": ..., "usage": {"limits": {"<period>": {"remaining_pct": N}}}}
    reduced to one number: the MIN remaining_pct across periods (the tightest
    limit). Loaded once at startup and refreshed by start_refresher. Value is:
        None  -- unknown (proxy unavailable/no usable period); never skipped
        <= 0  -- known depleted; skipped in ANY routing mode
        > 0   -- remaining headroom; also orders the usage mode
    """
    usage = {}
    for config_file in glob.glob("registered_providers/*/config.json"):
        prov = os.path.basename(os.path.dirname(config_file))
        remaining = None
        try:
            data = fetch_export(prov, "usage")
            periods = (data.get("usage") or {}).get("limits") or {}
            vals = [p["remaining_pct"] for p in periods.values()
                    if isinstance(p, dict) and p.get("remaining_pct") is not None]
            if vals:
                remaining = min(vals)
        except Exception:
            remaining = None
        usage[prov] = remaining
    return usage


def format_usage(usage_dict):
    parts = []
    for prov in sorted(usage_dict):
        rem = usage_dict[prov]
        parts.append(f"{prov}={rem}%" if rem is not None else f"{prov}=unknown")
    return ", ".join(parts) if parts else "none"


USAGE = {}


def start_refresher(interval):
    """Poll each running proxy's cached usage and models endpoints.

    Proxies read usage and models in the background, so early polls find them
    unavailable; poll quickly until every provider has both, then every `interval`.
    """

    def loop():
        global USAGE, ALL_MODELS, ADVERTISED, CONFIG, TIERS, MODELS
        first_pass = True
        while True:
            try:
                catalog = load_all_models()
                usage = load_usage()
                prev_usage = USAGE
                ALL_MODELS = catalog
                USAGE = usage
                if populate_providers(CONFIG):
                    TIERS = tiers_from_providers(CONFIG["providers"], CONFIG.get("effort"))
                    MODELS = list(TIERS)
                ADVERTISED = MODELS + [m for m in catalog if m not in MODELS]
                if first_pass or usage != prev_usage:
                    logging.info("USAGE provider quotas: %s", format_usage(usage))
                first_pass = False
            except Exception as e:
                logging.error("proxy metadata refresh failed: %s", e)
            if interval <= 0:
                return
            providers = {os.path.basename(os.path.dirname(f)) for f in glob.glob("registered_providers/*/config.json")}
            complete = all(USAGE.get(p) is not None for p in providers) and providers <= set(ALL_MODELS.values())
            time.sleep(interval if complete else min(interval, 10))

    threading.Thread(target=loop, daemon=True).start()

class RouterHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _client_origin(self):
        """Remove a client-scoped prefix and return its provider name."""
        if not self.path.startswith("/client/"):
            return None
        parts = self.path.split("/", 3)
        if (len(parts) != 4 or not parts[3] or
                not os.path.isfile(os.path.join("registered_providers", parts[2], "config.json"))):
            raise ValueError("Unknown client route")
        self.path = "/" + parts[3]
        return parts[2]

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Api-Key, Anthropic-Version, Anthropic-Beta, Anthropic-Dangerous-Direct-Browser-Access")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        try:
            origin = self._client_origin()
        except ValueError:
            self.send_error(404, "Unknown client route")
            return
        advertised = ([m for m in ADVERTISED
                       if (any(b["provider"] != origin for b in TIERS[m]) if m in TIERS
                           else ALL_MODELS.get(m) != origin)]
                      if origin else ADVERTISED)
        clean_path = urlsplit(self.path).path
        gemini_models = clean_path == "/v1beta/models" or (
            origin == "agy" and clean_path == "/v1/models")
        gemini_detail = (clean_path.startswith("/v1beta/models/") or
                         (origin == "agy" and clean_path.startswith("/v1/models/")))
        if gemini_models:
            response_obj = {"models": [{"name": "models/" + m,
                                        "baseModelId": m,
                                        "displayName": m,
                                        "supportedGenerationMethods": ["generateContent", "streamGenerateContent"]}
                                       for m in advertised]}
            resp_bytes = json.dumps(response_obj).encode("utf-8")
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        elif origin == "claude" and clean_path == "/v1/models":
            response_obj = {
                "data": [{"type": "model", "id": m, "display_name": m,
                          "created_at": "1970-01-01T00:00:00Z"} for m in advertised],
                "first_id": advertised[0] if advertised else None,
                "last_id": advertised[-1] if advertised else None,
                "has_more": False,
            }
            resp_bytes = json.dumps(response_obj).encode("utf-8")
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        elif gemini_detail:
            model_id = clean_path.rsplit("/", 1)[-1]
            if model_id not in advertised:
                self.send_error(404, "Unknown model")
                return
            response_obj = {"name": "models/" + model_id,
                            "baseModelId": model_id,
                            "displayName": model_id,
                            "supportedGenerationMethods": ["generateContent", "streamGenerateContent"]}
            resp_bytes = json.dumps(response_obj).encode("utf-8")
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        elif clean_path.endswith("/v1/models") or clean_path.endswith("/models"):
            response_obj = {
                "object": "list",
                "data": [{"id": m, "object": "model", "owned_by": "local"} for m in advertised]
            }
            resp_bytes = json.dumps(response_obj, indent=2).encode("utf-8")
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        elif clean_path.endswith("/api/tags"):
            response_obj = {
                "models": [{
                    "name": m,
                    "model": m,
                    "modified_at": "2024-01-01T00:00:00Z",
                    "size": 1000000000,
                    "digest": "sha256:dummy",
                    "details": {"family": "llama", "parameter_size": "7B", "quantization_level": "Q4_0"}
                } for m in advertised]
            }
            resp_bytes = json.dumps(response_obj).encode("utf-8")
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        elif clean_path == "/":
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "Router is running"}')
        else:
            self.send_response(404)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def do_POST(self):
        try:
            origin = self._client_origin()
        except ValueError:
            self.send_error(404, "Unknown client route")
            return
        request_path = urlsplit(self.path).path
        request_id = uuid.uuid4().hex[:8]
        started = time.monotonic()
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        
        try:
            payload = json.loads(raw_body.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Request body must be a JSON object")
            gemini_route = parse_generate_path(self.path)
            if request_path in ("/v1/responses", "/v1/chat/responses"):
                previous_id = payload.get("previous_response_id")
                if previous_id:
                    with RESPONSE_CONTEXT_LOCK:
                        previous = RESPONSE_CONTEXT.get(previous_id)
                    if previous is None:
                        raise ValueError("Unknown previous_response_id; send full input history")
                    payload["input"] = (previous["history"] +
                                        _response_input_items(payload.get("input")))
                    payload.setdefault("model", previous["requested_model"])
                    payload.pop("previous_response_id", None)
            if request_path == "/v1/messages":
                from .anthropic_sse import validate_request
                validate_request(payload)
            requested_model = gemini_route[0] if gemini_route else payload.get("model", "fast")
        except Exception as e:
            self.send_response(400)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if request_path == "/v1/messages":
                error = {"type": "error", "error": {"type": "invalid_request_error", "message": str(e)}}
            else:
                error = {"error": {"message": "Invalid JSON or missing model", "details": str(e)}}
            self.wfile.write(json.dumps(error).encode("utf-8"))
            return
            
        logging.info("REQUEST id=%s model=%s path=%s", request_id, str(requested_model).replace("\n", " "), self.path)

        # Best-effort resolution of the requested model to a backend list.
        # tier -> exact id -> provider name -> fuzzy family match -> medium.
        tier = requested_model
        specific = None  # a single pinned {provider, model} (exact id or fuzzy match)
        backends = TIERS.get(tier)

        if backends is None and tier in ALL_MODELS:
            # Exact vendor id -> straight to that provider with that id.
            prov = ALL_MODELS[tier]
            effort = (CONFIG.get("providers", {}).get(prov, {}).get("effort", {}).get(tier)
                      if isinstance(CONFIG.get("providers", {}).get(prov, {}).get("effort"), dict)
                      else CONFIG.get("providers", {}).get(prov, {}).get("effort"))
            specific = {"provider": prov, "model": tier}
            if effort:
                specific["effort"] = effort

        if backends is None and specific is None:
            # Provider name (e.g. "claude") -> that provider's first tier.
            for t, b in TIERS.items():
                if any(x["provider"] == tier for x in b):
                    tier, backends = t, b
                    break

        if backends is None and specific is None:
            # Fuzzy family match against the cached catalog (e.g. "opus" -> claude-opus-...).
            match = next((mid for mid in ALL_MODELS
                          if tier.lower() in mid.lower() or mid.lower() in tier.lower()), None)
            if match:
                logging.info(f"Fuzzy-matched '{requested_model}' -> {match} ({ALL_MODELS[match]}).")
                prov = ALL_MODELS[match]
                effort = (CONFIG.get("providers", {}).get(prov, {}).get("effort", {}).get(match)
                          if isinstance(CONFIG.get("providers", {}).get(prov, {}).get("effort"), dict)
                          else CONFIG.get("providers", {}).get(prov, {}).get("effort"))
                specific = {"provider": prov, "model": match}
                if effort:
                    specific["effort"] = effort

        if backends is None and specific is None:
            # Nothing matched -> default to the medium tier.
            logging.info(f"Unmapped model '{requested_model}' -> defaulting to medium tier.")
            tier, backends = "medium", TIERS.get("medium")
            if not backends:
                logging.error("FAIL id=%s status=503 reason=no_medium_fallback", request_id)
                self.send_response(503)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": {
                    "message": "No medium fallback tier is configured",
                    "model": requested_model
                }}).encode("utf-8"))
                return

        # A pinned (exact id / fuzzy) model is tried first; if it's out of tokens or
        # down, try the other providers in the SAME tier as that model.
        if specific is not None:
            prov = specific["provider"]
            tier = next((t for t, bs in TIERS.items()
                         if any(x["provider"] == prov and x["model"] == specific["model"] for x in bs)), None)
            if tier is None:
                tier = next((t for t, bs in TIERS.items() if any(x["provider"] == prov for x in bs)), "medium")
            retry = [b for b in TIERS.get(tier, []) if b["provider"] != prov]
        else:
            retry = []

        # Order per the configured mode. usage: most remaining first. custom: global
        # provider preference (unlisted last). Depleted/down are skipped in the loop.
        if MODE == "custom":
            order = lambda lst: sorted(lst, key=lambda b: CUSTOM_ORDER.index(b.get("provider", ""))
                                       if b.get("provider", "") in CUSTOM_ORDER else len(CUSTOM_ORDER))
        else:
            order = lambda lst: sorted(lst, key=lambda b: USAGE.get(b.get("provider", "")) or 0, reverse=True)

        if specific is not None:
            primary = [specific]                 # requested model stays first
            sorted_backends = primary + order(retry)   # try every eligible same-tier alternate
        else:
            primary = order(backends)
            sorted_backends = primary

        order_summary = " -> ".join(
            f"{b['provider']}:{b['model']}{'(' + b['effort'] + ')' if b.get('effort') else ''}({USAGE.get(b['provider']) if USAGE.get(b['provider']) is not None else '?'})"
            for b in sorted_backends
        )
        logging.info("ORDER id=%s mode=%s tier=%s candidates=[%s]", request_id, MODE, tier, order_summary)

        headers = {"X-Request-ID": request_id}
        for k, v in self.headers.items():
            if k.lower() not in ("host", "content-length", "x-request-id"):
                headers[k] = v

        stream_requested = gemini_route[1] if gemini_route else payload.get("stream") is True
        response_request_input = payload.get("input")
        # Lock one effort for the whole request so a retry to another backend
        # keeps the same effort: the client's if given, else the first
        # candidate's resolved effort.
        locked_effort = (payload.get("effort") or payload.get("reasoning_effort") or
                         next((b.get("effort") for b in sorted_backends if b.get("effort")), None))
        client_started = False

        # Log-only: the router buffers non-stream replies, so without this a
        # client that gave up only shows up at the final write.
        responding = threading.Event()
        send_response = self.send_response
        def mark_responding(*args, **kwargs):
            responding.set()
            return send_response(*args, **kwargs)
        self.send_response = mark_responding
        client_sock = self.connection
        def watch_client():
            while not responding.wait(1):
                try:
                    readable, _, _ = select.select([client_sock], [], [], 0)
                    if readable and client_sock.recv(1, socket.MSG_PEEK) == b"":
                        logging.warning("CLIENT_GONE id=%s after=%.2fs (client closed before any reply)",
                                        request_id, time.monotonic() - started)
                        return
                except (OSError, ValueError):
                    return
        threading.Thread(target=watch_client, daemon=True).start()

        def send_stream_error(reason):
            message = " ".join(str(reason).split())[:500]
            if gemini_route:
                wire = f"data: {json.dumps({'error': {'code': 502, 'message': message, 'status': 'UNAVAILABLE'}})}\n\n"
            elif request_path.startswith("/v1/"):
                if request_path == "/v1/messages":
                    wire = f"event: error\ndata: {json.dumps({'type': 'error', 'error': {'type': 'api_error', 'message': message}})}\n\n"
                elif request_path in ("/v1/responses", "/v1/chat/responses"):
                    event = {"type": "response.failed", "response": {
                        "status": "failed", "error": {"code": "server_error", "message": message}}}
                    wire = f"event: response.failed\ndata: {json.dumps(event)}\n\n"
                else:
                    wire = f"data: {json.dumps({'error': {'message': message}})}\n\n"
            else:
                wire = json.dumps({"error": message}) + "\n"
            try:
                self.wfile.write(wire.encode("utf-8"))
                self.wfile.flush()
            except OSError:
                pass

        for i, backend in enumerate(sorted_backends):
            if i == len(primary) and len(sorted_backends) > len(primary):
                logging.info("RETRY id=%s tier=%s", request_id, tier)
            prov = backend["provider"]
            if prov == origin:
                logging.info("Skipping %s: request originated from that CLI client.", prov)
                continue
            remaining = USAGE.get(prov)
            if remaining is not None and remaining <= 0:
                logging.info(f"Skipping {prov}: out of tokens (0 remaining).")
                continue

            port = running_port(prov)
            if port is None:
                logging.info(f"Skipping {prov}: proxy not running or not listening.")
                continue

            backend_model = backend["model"]  # exact id frozen in router_config.json
            target_url = loopback.url(port, self.path)

            payload["model"] = backend_model
            effective_effort = locked_effort
            if effective_effort:
                payload["effort"] = effective_effort

            raw_body_modified = json.dumps(payload).encode("utf-8")
            headers["Content-Length"] = str(len(raw_body_modified))

            note = f"[remaining: {remaining}]" if remaining is not None else "[unknown]"
            effort_note = f" effort={effective_effort}" if effective_effort else ""
            logging.info("ROUTE id=%s provider=%s model=%s%s %s", request_id, prov, backend_model, effort_note, note)

            try:
                req = urllib.request.Request(target_url, data=raw_body_modified, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=600) as response, tempfile.SpooledTemporaryFile(max_size=1024 * 1024) as attempt:
                    # Hold each attempt until validated, so retries never mix partial outputs.
                    stream_error = None
                    completed_response = [None]
                    pending = b""
                    def inspect_line(line):
                        if line.startswith(b"data: "):
                            line = line[6:]
                        try:
                            event = json.loads(line)
                            if event.get("type") == "response.completed":
                                completed_response[0] = event.get("response")
                            if event.get("type") in ("error", "response.failed", "response.incomplete") or event.get("error"):
                                return event.get("error") or event.get("response", {}).get("error") or event.get("type")
                        except (ValueError, AttributeError):
                            pass
                        return None
                    if stream_requested:
                        def has_text(line):
                            if line.startswith(b"data: "):
                                line = line[6:]
                            try:
                                event = json.loads(line)
                            except (ValueError, UnicodeDecodeError):
                                return False
                            if not isinstance(event, dict):
                                return False
                            if request_path == "/v1/messages" and event.get("type") == "ping":
                                return True
                            if event.get("type") in ("response.output_text.delta",
                                                     "response.function_call_arguments.delta",
                                                     "response.custom_tool_call_input.delta",
                                                     "text-delta"):
                                return bool(event.get("delta"))
                            if event.get("type") == "content_block_delta":
                                return bool((event.get("delta") or {}).get("text"))
                            if event.get("choices"):
                                return any(bool((choice.get("delta") or {}).get("content") or
                                                (request_path == "/v1/chat/completions" and
                                                 (choice.get("delta") or {}).get("role") == "assistant") or
                                                (choice.get("delta") or {}).get("tool_calls") or choice.get("text"))
                                           for choice in event["choices"] if isinstance(choice, dict))
                            if event.get("candidates"):
                                return any(bool(part.get("text"))
                                           for candidate in event["candidates"] if isinstance(candidate, dict)
                                           for part in (candidate.get("content") or {}).get("parts", [])
                                           if isinstance(part, dict))
                            message = event.get("message")
                            return bool((isinstance(message, dict) and message.get("content")) or
                                        (isinstance(event.get("response"), str) and event["response"]))

                        while line := response.readline():
                            stream_error = inspect_line(line) or stream_error
                            if client_started:
                                self.wfile.write(line)
                                self.wfile.flush()
                                if stream_error:
                                    logging.error("FAIL id=%s provider=%s reason=%s partial=true", request_id, prov,
                                                  " ".join(str(stream_error).split())[:500])
                                    return
                                continue
                            attempt.write(line)
                            if stream_error:
                                break
                            if has_text(line):
                                self.send_response(response.status)
                                for k, v in response.headers.items():
                                    if k.lower() not in ("transfer-encoding", "connection", "content-length"):
                                        self.send_header(k, v)
                                self.send_header("Connection", "close")
                                self._send_cors_headers()
                                self.end_headers()
                                client_started = True
                                attempt.seek(0)
                                while chunk := attempt.read(65536):
                                    self.wfile.write(chunk)
                                self.wfile.flush()
                        if stream_error:
                            logging.error("FAIL id=%s provider=%s reason=%s retry=next", request_id, prov,
                                          " ".join(str(stream_error).split())[:500])
                            continue
                        if not client_started:
                            if attempt.tell() == 0:
                                logging.error("FAIL id=%s provider=%s reason=empty_stream retry=next", request_id, prov)
                                continue
                            self.send_response(response.status)
                            for k, v in response.headers.items():
                                if k.lower() not in ("transfer-encoding", "connection", "content-length"):
                                    self.send_header(k, v)
                            self.send_header("Connection", "close")
                            self._send_cors_headers()
                            self.end_headers()
                            client_started = True
                            attempt.seek(0)
                            while chunk := attempt.read(65536):
                                self.wfile.write(chunk)
                            self.wfile.flush()
                        logging.info("DONE id=%s provider=%s elapsed=%.2fs streamed=true", request_id, prov,
                                     time.monotonic() - started)
                        if completed_response[0] is not None:
                            remember_response(completed_response[0], response_request_input,
                                              requested_model)
                        return
                    while True:
                        chunk = response.read1(4096)
                        if not chunk:
                            break
                        attempt.write(chunk)
                        pending += chunk
                        while b"\n" in pending:
                            line, pending = pending.split(b"\n", 1)
                            stream_error = inspect_line(line) or stream_error
                        if len(pending) > 1024 * 1024:
                            pending = b""
                    stream_error = inspect_line(pending) or stream_error
                    if attempt.tell() == 0:
                        stream_error = "Empty provider response"
                    if stream_error:
                        logging.error("FAIL id=%s provider=%s reason=%s retry=next", request_id, prov, " ".join(str(stream_error).split())[:500])
                        continue
                    if request_path in ("/v1/responses", "/v1/chat/responses"):
                        attempt.seek(0)
                        try:
                            remember_response(json.load(attempt), response_request_input,
                                              requested_model)
                        except (ValueError, UnicodeError):
                            pass
                    self.send_response(response.status)
                    for k, v in response.headers.items():
                        if k.lower() not in ("transfer-encoding", "connection"):
                            self.send_header(k, v)
                    self.send_header("Connection", "close")
                    self._send_cors_headers()
                    self.end_headers()
                    attempt.seek(0)
                    try:
                        while chunk := attempt.read(65536):
                            self.wfile.write(chunk)
                        self.wfile.flush()
                    except OSError as e:
                        logging.error("FAIL id=%s reason=client_disconnected elapsed=%.2fs detail=%s", request_id,
                                      time.monotonic() - started, " ".join(str(e).split()))
                        return
                    logging.info("DONE id=%s provider=%s elapsed=%.2fs", request_id, prov, time.monotonic() - started)
                    return
            except urllib.error.HTTPError as e:
                error_body = e.read(4096)
                reason = " ".join(error_body.decode("utf-8", errors="replace").split())[:500]
                logging.error("FAIL id=%s provider=%s status=%s reason=%s", request_id, prov, e.code, reason)
                if client_started:
                    send_stream_error(reason)
                    return
                if 400 <= e.code < 500 and e.code != 429:
                    self.send_response(e.code)
                    self._send_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(error_body)))
                    self.send_header("Connection", "close")
                    self.end_headers()
                    self.wfile.write(error_body)
                    return
            except urllib.error.URLError as e:
                logging.error("FAIL id=%s provider=%s reason=%s", request_id, prov, " ".join(str(e).split()))
                if client_started:
                    send_stream_error(e)
                    return
            except (OSError, TimeoutError, http.client.HTTPException) as e:
                logging.error("FAIL id=%s provider=%s reason=%s retry=next", request_id, prov, " ".join(str(e).split()))
                if client_started:
                    send_stream_error(e)
                    return
                continue
                
        logging.error("FAIL id=%s status=503 reason=all_backends_unavailable", request_id)
        if gemini_route:
            err_json = {"error": {"code": 503, "message": "All proxy backends failed or have depleted limits.", "status": "UNAVAILABLE"}}
        elif request_path == "/v1/messages":
            err_json = {"type": "error", "error": {"type": "api_error", "message": "All proxy backends failed or have depleted limits."}}
        else:
            err_json = {"error": {"message": "All proxy backends failed or have depleted limits.", "type": "router_error"}}
        resp_bytes = json.dumps(err_json).encode("utf-8")
        self.send_response(503)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            self.wfile.write(resp_bytes)
        except OSError:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Provider Router")
    parser.add_argument("--port", type=int, default=8090, help="Port to bind the router to")
    parser.add_argument("--refresh-interval", type=int, default=1800,
                        help="Seconds between proxy metadata polls (0 means startup only)")
    args = parser.parse_args()

    logging.info(f"Starting Multi-Provider Router on port {args.port}...")
    logging.info(f"Routing mode: {MODE}" + (f" (order: {', '.join(CUSTOM_ORDER)})" if MODE == "custom" and CUSTOM_ORDER else ""))
    logging.info(f"Reading usage and models from provider proxies every {args.refresh_interval}s.")
    start_refresher(args.refresh_interval)
    existing_router_port = loopback.already_running(os.path.join("data", "providers_status", "router_run_status.json"))
    if existing_router_port:
        logging.error(f"Cannot start router: one is already running on port {existing_router_port}.")
        sys.exit(1)
    try:
        server = loopback.serve_next(args.port, RouterHandler)
    except OSError as e:
        logging.error(f"Cannot start router: {e}")
        sys.exit(1)
    port = server.server_address[1]
    if port != args.port:
        logging.warning(f"Port {args.port} is taken by another process; router is using {port}.")
    # Publish router PID so `tbuffet stop` can find and kill this process.
    _status_dir = os.path.join("data", "providers_status")
    os.makedirs(_status_dir, exist_ok=True)
    _status_path = os.path.join(_status_dir, "router_run_status.json")
    _tmp = _status_path + f".{os.getpid()}.tmp"
    with open(_tmp, "w", encoding="utf-8") as _f:
        json.dump({"status": "running", "port": port, "pid": os.getpid()}, _f)
    os.replace(_tmp, _status_path)
    server.serve_forever()
