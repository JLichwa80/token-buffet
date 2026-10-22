from tokenbuffet.log_paths import LOG_DIR
from tokenbuffet.log_config import resolve_log_level, console_handler
from tokenbuffet import loopback
import argparse
import json
import subprocess
import time
import uuid
import os
import tempfile
import sys
import shutil
import logging
import datetime
import threading
import queue
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
# OpenAI Responses API event models, used for the "custom-responses" wire served
# on /v1/responses. Building each event *through* these Pydantic models validates
# its shape before it is streamed to the client.
from openai.types.responses import (
    ResponseCreatedEvent, ResponseTextDeltaEvent, ResponseCompletedEvent,
    ResponseOutputItemAddedEvent, ResponseOutputItemDoneEvent,
    ResponseFunctionCallArgumentsDeltaEvent, ResponseFunctionCallArgumentsDoneEvent,
    ResponseCustomToolCallInputDeltaEvent, ResponseCustomToolCallInputDoneEvent,
    ResponseContentPartAddedEvent, ResponseContentPartDoneEvent,
    ResponseTextDoneEvent,
)
from openai.types.responses.response import Response as _OAResponse
from openai.types.responses.response_usage import ResponseUsage as _OAUsage
from openai.types.responses.response_output_message import ResponseOutputMessage as _OAMsg
from openai.types.responses.response_output_text import ResponseOutputText as _OAText
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall as _OAFnCall
from openai.types.responses.response_custom_tool_call import ResponseCustomToolCall as _OACustomCall
from openai.types.responses.response_tool_search_call import ResponseToolSearchCall as _OAToolSearchCall

sys.stdout.reconfigure(encoding='utf-8')

PROVIDER = None
PORT = 8000
PROTOCOL = "openai"
MODEL = None
UI_STREAM = False
REFRESH_INTERVAL = 1800
_EXTRACT_LOCKS = {"usage": threading.Lock(), "models": threading.Lock()}
_INFLIGHT = [0]
_INFLIGHT_LOCK = threading.Lock()
STALL_LOG_INTERVAL = 30
TRACE_LEVEL = resolve_log_level()

logger = logging.getLogger("ProxyServer")
logger.setLevel(logging.DEBUG)
_PROXY_FORMAT = "%(asctime)s [PROXY] %(message)s"
_console_format = logging.Formatter(_PROXY_FORMAT, datefmt="%H:%M:%S")
stdout_handler = console_handler(sys.stdout, _PROXY_FORMAT)
stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)
stderr_handler = console_handler(sys.stderr, _PROXY_FORMAT)
stderr_handler.setLevel(logging.WARNING)
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)
logger.propagate = False

def one_line(value):
    return " ".join(str(value).split())[:500]


def load_provider_config(provider):
    config_path = os.path.join("registered_providers", provider, "config.json")
    if not os.path.exists(config_path):
        return None
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def cached_export(op):
    """The last saved export for this proxy, however old; RuntimeError when there is none yet."""
    path = os.path.join("data", "providers_status", f"{PROVIDER}_{op}.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = None
    if not isinstance(data, dict) or data.get("provider") != PROVIDER or not isinstance(data.get(op), dict):
        raise RuntimeError(f"{op} is still being read from the CLI")
    return data


def provider_export(op, force=False):
    """Return this proxy's fresh extractor export, refreshing only when stale.

    On failure, returns the previous cached export if it exists (don't overwrite
    good data with failure). Only raises an error if there's no previous cache.
    """
    path = os.path.join("data", "providers_status", f"{PROVIDER}_{op}.json")
    with _EXTRACT_LOCKS[op]:
        # Try to return cached data if recent
        if not force and os.path.exists(path) and time.time() - os.path.getmtime(path) < REFRESH_INTERVAL:
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("provider") == PROVIDER and isinstance(data.get(op), dict):
                    return data
            except (OSError, ValueError, AttributeError):
                pass

        # Cache is stale or missing; try to refresh
        # Call the extractor module directly so a pip-installed workspace needs no scripts/.
        config = os.path.join("registered_providers", PROVIDER, "config.json")
        raw = os.path.join("data", "providers_status", "raw", f"{PROVIDER}_{op}_raw.txt")
        os.makedirs(os.path.dirname(raw), exist_ok=True)
        env = dict(os.environ, PYTHONIOENCODING="utf-8",
                   PYTHONPATH=os.pathsep.join(filter(None, [os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                              os.environ.get("PYTHONPATH", "")])))
        base = [sys.executable, "-m", "tokenbuffet.extractors"]
        for step in (base + ["capture", op, config, raw],
                     base + ["parse", op, config, raw, path, "--provider", PROVIDER]):
            result = subprocess.run(step, capture_output=True, text=True, encoding="utf-8",
                                    errors="replace", timeout=180, env=env)
            if result.returncode:
                break

        # If capture/parse fails, return previous cache if it exists
        if result.returncode:
            if os.path.exists(path):
                try:
                    with open(path, encoding="utf-8") as f:
                        data = json.load(f)
                    if data.get("provider") == PROVIDER and isinstance(data.get(op), dict):
                        return data
                except (OSError, ValueError, AttributeError):
                    pass
            # No previous cache; raise the original error
            raise RuntimeError(one_line(result.stderr or result.stdout or
                                        f"{op} extractor exited {result.returncode}"))

        # Capture/parse succeeded; read and return the new data
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if data.get("provider") != PROVIDER or not isinstance(data.get(op), dict):
                raise ValueError(f"invalid {op} export for {PROVIDER}")
            return data
        except (OSError, ValueError) as e:
            # Parse succeeded but file is invalid; fall back to previous cache
            if os.path.exists(path):
                try:
                    # Try to read the previous version
                    with open(path, encoding="utf-8") as f:
                        data = json.load(f)
                    if data.get("provider") == PROVIDER and isinstance(data.get(op), dict):
                        return data
                except (OSError, ValueError, AttributeError):
                    pass
            raise

def check_match(obj, condition):
    for k, v in condition.items():
        keys = k.split(".")
        curr = obj
        found = True
        for key in keys:
            if isinstance(curr, dict) and key in curr:
                curr = curr[key]
            else:
                found = False
                break
        if not found or curr != v:
            return False
    return True

def extract_path(obj, path):
    keys = path.split(".")
    curr = obj
    for i, key in enumerate(keys):
        if key == "[]" and isinstance(curr, list):
            res = []
            rest_path = ".".join(keys[i+1:])
            for item in curr:
                val = extract_path(item, rest_path)
                if val:
                    res.append(val)
            return "".join(res)
        elif isinstance(curr, dict) and key in curr:
            curr = curr[key]
        else:
            return ""
    return str(curr) if curr is not None else ""

# --- OpenAI Responses API (/v1/responses) event builders -------------------
# Each returns a ready-to-write SSE line (`data: {json}\n\n`). Constructing via
# the openai Pydantic models means a malformed event raises here rather than
# silently reaching Obsidian.

def _responses_usage():
    return _OAUsage(
        input_tokens=0, output_tokens=0, total_tokens=0,
        input_tokens_details={"cached_tokens": 0, "cache_write_tokens": 0},
        output_tokens_details={"reasoning_tokens": 0},
    )

def _responses_obj(resp_id, model, created_at, status, output, usage=None,
                   allow_parallel=False):
    kw = dict(id=resp_id, created_at=created_at, model=model, object="response",
              status=status, output=output, parallel_tool_calls=allow_parallel,
              tool_choice="auto", tools=[])
    if usage is not None:
        kw["usage"] = usage
    return _OAResponse(**kw)

def _responses_message(item_id, full_text):
    return _OAMsg(id=item_id, type="message", role="assistant", status="completed",
                  content=[_OAText(type="output_text", text=full_text, annotations=[])])

def responses_sse_created(seq, resp_id, model, created_at, allow_parallel=False):
    ev = ResponseCreatedEvent(type="response.created", sequence_number=seq,
                              response=_responses_obj(resp_id, model, created_at, "in_progress", [],
                                                      allow_parallel=allow_parallel))
    return f"data: {ev.model_dump_json(exclude_none=True)}\n\n"

def responses_sse_delta(seq, item_id, text):
    ev = ResponseTextDeltaEvent(type="response.output_text.delta", sequence_number=seq,
                                item_id=item_id, output_index=0, content_index=0,
                                delta=text, logprobs=[])
    return f"data: {ev.model_dump_json(exclude_none=True)}\n\n"

def responses_sse_completed(seq, resp_id, model, created_at, item_id, full_text,
                            allow_parallel=False):
    r = _responses_obj(resp_id, model, created_at, "completed",
                       [_responses_message(item_id, full_text)], _responses_usage(),
                       allow_parallel)
    ev = ResponseCompletedEvent(type="response.completed", sequence_number=seq, response=r)
    return f"data: {ev.model_dump_json(exclude_none=True)}\n\n"

def responses_nonstream_json(resp_id, model, created_at, item_id, full_text,
                             allow_parallel=False):
    r = _responses_obj(resp_id, model, created_at, "completed",
                       [_responses_message(item_id, full_text)], _responses_usage(),
                       allow_parallel)
    return r.model_dump_json(exclude_none=True)


def _responses_tool_items(chosen):
    items = []
    for call in chosen["calls"]:
        if call["type"] == "tool_search_call":
            items.append(_OAToolSearchCall(type="tool_search_call", id="tsc_" + call["id"],
                                           call_id=call["id"], arguments=call["arguments"],
                                           execution="client", status="completed"))
        elif call["type"] == "custom_tool_call":
            items.append(_OACustomCall(type="custom_tool_call", id="ctc_" + call["id"],
                                       call_id=call["id"], name=call["name"],
                                       input=call["input"], namespace=call.get("namespace")))
        else:
            items.append(_OAFnCall(type="function_call", id="fc_" + call["id"],
                                   call_id=call["id"], name=call["function"]["name"],
                                   arguments=call["function"]["arguments"],
                                   namespace=call.get("namespace"), status="completed"))
    return items


def responses_tool_json(resp_id, model, created_at, chosen, allow_parallel=True):
    output = (_responses_tool_items(chosen) if chosen["kind"] == "tool_calls"
              else [_responses_message("msg_" + resp_id, chosen["text"])])
    return _responses_obj(resp_id, model, created_at, "completed", output,
                          _responses_usage(), allow_parallel).model_dump_json(exclude_none=True)


def responses_tool_stream(resp_id, model, created_at, chosen, allow_parallel=True):
    events = [responses_sse_created(1, resp_id, model, created_at, allow_parallel)]
    seq = 1
    if chosen["kind"] == "tool_calls":
        items = _responses_tool_items(chosen)
        for index, item in enumerate(items):
            if item.type == "tool_search_call":
                seq += 1
                events.append(ResponseOutputItemAddedEvent(
                    type="response.output_item.added", sequence_number=seq,
                    output_index=index, item=item.model_copy(update={"status": "in_progress"})
                ).model_dump_json(exclude_none=True))
                seq += 1
                events.append(ResponseOutputItemDoneEvent(
                    type="response.output_item.done", sequence_number=seq,
                    output_index=index, item=item).model_dump_json(exclude_none=True))
                continue
            custom = item.type == "custom_tool_call"
            pending = item.model_copy(update={"input": ""} if custom else
                                      {"arguments": "", "status": "in_progress"})
            seq += 1
            events.append(ResponseOutputItemAddedEvent(
                type="response.output_item.added", sequence_number=seq,
                output_index=index, item=pending).model_dump_json(exclude_none=True))
            seq += 1
            if custom:
                events.append(ResponseCustomToolCallInputDeltaEvent(
                    type="response.custom_tool_call_input.delta", sequence_number=seq,
                    item_id=item.id, output_index=index, delta=item.input
                ).model_dump_json(exclude_none=True))
            else:
                events.append(ResponseFunctionCallArgumentsDeltaEvent(
                    type="response.function_call_arguments.delta", sequence_number=seq,
                    item_id=item.id, output_index=index, delta=item.arguments
                ).model_dump_json(exclude_none=True))
            seq += 1
            if custom:
                events.append(ResponseCustomToolCallInputDoneEvent(
                    type="response.custom_tool_call_input.done", sequence_number=seq,
                    item_id=item.id, output_index=index, input=item.input
                ).model_dump_json(exclude_none=True))
            else:
                events.append(ResponseFunctionCallArgumentsDoneEvent(
                    type="response.function_call_arguments.done", sequence_number=seq,
                    item_id=item.id, output_index=index, arguments=item.arguments
                ).model_dump_json(exclude_none=True))
            seq += 1
            events.append(ResponseOutputItemDoneEvent(
                type="response.output_item.done", sequence_number=seq,
                output_index=index, item=item).model_dump_json(exclude_none=True))
        seq += 1
        completed = ResponseCompletedEvent(
            type="response.completed", sequence_number=seq,
            response=_responses_obj(resp_id, model, created_at, "completed", items,
                                    _responses_usage(), allow_parallel))
        events.append(completed.model_dump_json(exclude_none=True))
    else:
        item_id = "msg_" + resp_id
        item = _responses_message(item_id, chosen["text"])
        empty_part = _OAText(type="output_text", text="", annotations=[])
        pending = item.model_copy(update={"content": [], "status": "in_progress"})
        seq += 1
        events.append(ResponseOutputItemAddedEvent(
            type="response.output_item.added", sequence_number=seq,
            output_index=0, item=pending).model_dump_json(exclude_none=True))
        seq += 1
        events.append(ResponseContentPartAddedEvent(
            type="response.content_part.added", sequence_number=seq,
            item_id=item_id, output_index=0, content_index=0,
            part=empty_part).model_dump_json(exclude_none=True))
        seq += 1
        events.append(responses_sse_delta(seq, item_id, chosen["text"]))
        seq += 1
        events.append(ResponseTextDoneEvent(
            type="response.output_text.done", sequence_number=seq,
            item_id=item_id, output_index=0, content_index=0,
            text=chosen["text"], logprobs=[]).model_dump_json(exclude_none=True))
        seq += 1
        events.append(ResponseContentPartDoneEvent(
            type="response.content_part.done", sequence_number=seq,
            item_id=item_id, output_index=0, content_index=0,
            part=item.content[0]).model_dump_json(exclude_none=True))
        seq += 1
        events.append(ResponseOutputItemDoneEvent(
            type="response.output_item.done", sequence_number=seq,
            output_index=0, item=item).model_dump_json(exclude_none=True))
        seq += 1
        events.append(responses_sse_completed(seq, resp_id, model, created_at,
                                              item_id, chosen["text"], allow_parallel))
    return b"".join((event if event.startswith("data: ") else "data: " + event + "\n\n").encode("utf-8")
                    for event in events) + b"data: [DONE]\n\n"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_POST(self):
        with _INFLIGHT_LOCK:
            _INFLIGHT[0] += 1
        try:
            self._dispatch_post()
        except Exception as exc:
            logger.error("FAIL provider=%s path=%s reason=%s", PROVIDER, self.path, one_line(exc))
            try:
                self.send_error(502, "Proxy request failed")
            except OSError:
                pass
        finally:
            with _INFLIGHT_LOCK:
                _INFLIGHT[0] -= 1

    def _dispatch_post(self):
        from .gemini_wire import parse_generate_path
        request_path = urllib.parse.urlsplit(self.path).path
        gemini_route = parse_generate_path(self.path)
        if request_path in ["/v1/chat/completions", "/api/chat"]:
            self.handle_chat()
        elif gemini_route:
            self.handle_chat(gemini=gemini_route)
        elif request_path == "/v1/messages":
            self.handle_chat(anthropic=True)
        elif request_path in ["/v1/responses", "/v1/chat/responses"]:
            # OpenAI Responses API endpoint (plugin's "custom-responses" preset).
            # Same CLI plumbing as chat; only the wire format differs.
            self.handle_chat(responses=True)
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        request_path = urllib.parse.urlsplit(self.path).path
        if request_path in ("/usage", "/models", "/v1/models", "/api/tags"):
            op = "usage" if request_path == "/usage" else "models"
            try:
                # A capture in progress takes minutes: answer from the last saved export
                # (or 503 when there is none) instead of queueing behind it.
                export = cached_export(op) if _EXTRACT_LOCKS[op].locked() else provider_export(op)
                if op == "usage" or request_path == "/models":
                    response_obj = export
                else:
                    available_models = [m["id"] for m in export["models"]["available"]]
                    if request_path == "/v1/models":
                        response_obj = {
                            "object": "list",
                            "data": [{"id": m, "object": "model", "owned_by": "local"} for m in available_models]
                        }
                    else:
                        response_obj = {
                            "models": [{
                                "name": m, "model": m,
                                "modified_at": "2024-01-01T00:00:00Z", "size": 1000000000,
                                "digest": "sha256:dummy",
                                "details": {"family": "llama", "parameter_size": "7B", "quantization_level": "Q4_0"}
                            } for m in available_models]
                        }
            except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, KeyError, TypeError) as exc:
                body = json.dumps({"error": one_line(exc)}).encode("utf-8")
                self.send_response(503)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            resp_bytes = json.dumps(response_obj).encode("utf-8")
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(resp_bytes)
        else:
            self.send_response(404)
            self.send_header("Connection", "close")
            self.end_headers()

    def log_message(self, format, *args):
        pass

    def handle_chat(self, responses=False, anthropic=False, gemini=None):
        request_path = urllib.parse.urlsplit(self.path).path
        if UI_STREAM and not anthropic and not gemini:
            from ai.ui.ai_sdk.ui_events import UITextDeltaEvent, UIFinishEvent
            from ai.ui.ai_sdk.outbound_stream import format_sse
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        if gemini:
            from . import gemini_wire
            try:
                payload = json.loads(post_data.decode("utf-8"))
                payload = gemini_wire.to_bridge_request(
                    payload, payload.get("model", gemini[0]), gemini[1])
            except (ValueError, UnicodeError, AttributeError) as exc:
                body = json.dumps(gemini_wire.error(exc)).encode("utf-8")
                self.send_response(400)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(body)
                return
        elif anthropic:
            from . import anthropic_sse
            try:
                payload = json.loads(post_data.decode("utf-8"))
                anthropic_sse.validate_request(payload)
            except (ValueError, UnicodeError) as exc:
                body = json.dumps({"type": "error", "error": {
                    "type": "invalid_request_error", "message": str(exc)}}).encode("utf-8")
                self.send_response(400)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(body)
                return
        else:
            payload = json.loads(post_data.decode("utf-8"))

        is_stream = payload.get("stream", False)
        # The model is the CLI `--model` id exactly as it appears in
        # data/providers_status/<provider>_models.json (the single source of
        # truth for model ids). Passed through verbatim -- no per-provider
        # rewriting lives in the engine.
        requested_model = payload.get("model", MODEL or "default")
        requested_effort = payload.get("effort") or payload.get("reasoning_effort")

        messages = payload.get("messages", [])

        if not messages and "input" in payload:
            response_input = payload["input"]
            if isinstance(response_input, str):
                messages = [{"role": "user", "content": response_input}]
            elif isinstance(response_input, list):
                messages = [{"role": "user", "content": item} if isinstance(item, str) else item
                            for item in response_input]
            elif isinstance(response_input, dict):
                messages = [response_input]
            else:
                self.send_error(400, "Invalid Responses input")
                return

        if not isinstance(messages, list) or any(not isinstance(msg, dict) for msg in messages):
            self.send_error(400, "Messages must be an array of objects")
            return

        tool_mode = False
        anthropic_history_mode = False
        responses_history_mode = False
        chat_history_mode = False
        if request_path == "/v1/chat/completions" and payload.get("tools"):
            from . import tool_wire
            try:
                client_tools = tool_wire.chat_tools(payload)
            except ValueError as exc:
                self.send_error(400, str(exc))
                return
            tool_mode = bool(client_tools)
        elif anthropic:
            from . import tool_wire
            client_tools = tool_wire.anthropic_tools(payload)
            tool_mode = bool(client_tools)
            anthropic_history_mode = tool_mode or any(
                isinstance(msg.get("content"), list) and any(
                    isinstance(block, dict) and block.get("type") in ("tool_use", "tool_result")
                    for block in msg["content"])
                for msg in messages)
        elif responses:
            from . import tool_wire
            try:
                client_tools = tool_wire.responses_available_tools(
                    payload.get("input"), tool_wire.responses_tools(payload))
            except ValueError as exc:
                self.send_error(400, str(exc))
                return
            tool_mode = bool(client_tools)
        elif gemini and payload.get("tools"):
            from . import tool_wire
            client_tools = payload["tools"]
            tool_mode = True
        if responses and isinstance(payload.get("input"), list):
            responses_history_mode = any(
                isinstance(item, dict) and item.get("type") in
                ("function_call", "function_call_output", "custom_tool_call",
                 "custom_tool_call_output", "tool_search_call", "tool_search_output")
                for item in payload["input"])
        if request_path == "/v1/chat/completions":
            chat_history_mode = any(msg.get("role") == "tool" or msg.get("tool_calls")
                                    for msg in messages)
        if responses_history_mode or chat_history_mode:
            from . import tool_wire
        tool_required = False
        allow_parallel = True
        if responses or request_path == "/v1/chat/completions":
            parallel_choice = payload.get("parallel_tool_calls", True)
            if not isinstance(parallel_choice, bool):
                self.send_error(400, "parallel_tool_calls must be a boolean")
                return
            allow_parallel = parallel_choice
        elif anthropic:
            choice = payload.get("tool_choice") or {}
            allow_parallel = not choice.get("disable_parallel_tool_use", False)
        if tool_mode:
            enabled, tool_required, forced_name = tool_wire.choice_policy(
                payload.get("tool_choice"))
            if forced_name:
                client_tools = [tool for tool in client_tools
                                if tool["name"] == forced_name]
                if not client_tools:
                    self.send_error(400, "Forced tool is not in tools")
                    return
            tool_mode = enabled

        req_id = self.headers.get("X-Request-ID") or uuid.uuid4().hex[:8]
        req_id = "".join(c for c in req_id if c.isalnum())[:32] or uuid.uuid4().hex[:8]
        started = time.monotonic()
        effort_log = f" effort={requested_effort}" if requested_effort else ""
        logger.info("REQUEST id=%s provider=%s model=%s%s path=%s stream=%s inflight=%d thread=%s", req_id, PROVIDER, one_line(requested_model), effort_log, self.path, is_stream, _INFLIGHT[0], threading.current_thread().name)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        debug = TRACE_LEVEL == "DEBUG"
        if debug:
            os.makedirs(os.path.join(LOG_DIR, PROVIDER, "proxy", "raw_requests"), exist_ok=True)
            with open(os.path.join(LOG_DIR, PROVIDER, "proxy", "raw_requests", f"req_{PROVIDER}_{timestamp}_{req_id}.json"), "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

        response_dir = LOG_DIR / PROVIDER / "proxy" / "raw_responses"
        if debug:
            response_dir.mkdir(parents=True, exist_ok=True)
        response_base = response_dir / f"resp_{PROVIDER}_{timestamp}_{req_id}"
        provider_stdout_path = response_base.with_suffix(".provider.stdout.log")
        provider_stderr_path = response_base.with_suffix(".provider.stderr.log")
        http_body_path = response_base.with_suffix(".raw")
        extracted_dir = LOG_DIR / PROVIDER / "llm_provider" / "raw_responses"
        if debug:
            extracted_dir.mkdir(parents=True, exist_ok=True)
        extracted_path = extracted_dir / f"resp_{PROVIDER}_{timestamp}_{req_id}.txt"
        session_dir = LOG_DIR / PROVIDER / "proxy" / "sessions"
        session_dir.mkdir(parents=True, exist_ok=True)
        session_path = session_dir / f"req_{PROVIDER}_{timestamp}_{req_id}.log"
        session_file = session_path.open("a", encoding="utf-8")
        session_lock = threading.Lock()

        def session_log(message):
            with session_lock:
                session_file.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S,%f} [{req_id}] {message}\n")
                session_file.flush()

        session_log(f"==================== NEW {PROVIDER.upper()} REQUEST ====================")
        session_log(f">>> POST {self.path}")
        if debug:
            session_log("Raw payload: " + post_data.decode("utf-8", errors="replace").replace("\n", ""))
        effort_sess = f", effort={requested_effort}" if requested_effort else ""
        session_log(f"Request parsed: stream={is_stream}, model={requested_model}{effort_sess}, size={len(post_data)} bytes")
        if debug:
            for path in (provider_stdout_path, provider_stderr_path, http_body_path):
                path.touch()

        def append_response(path, data):
            if not debug:
                return
            with path.open("ab") as output:
                output.write(data)

        def write_response(data):
            self.wfile.write(data)
            append_response(http_body_path, data)
            if debug:
                session_log("HTTP CHUNK: " + data.decode("utf-8", errors="replace").replace("\n", "\\n"))

        def save_extracted(text):
            if debug:
                extracted_path.write_text(text, encoding="utf-8")

        if anthropic_history_mode:
            system = ("[SYSTEM]:\n" + anthropic_sse.text_content(payload["system"]) + "\n\n"
                      if "system" in payload else "")
            full_prompt = system + tool_wire.anthropic_history(messages)
        elif responses and (tool_mode or responses_history_mode):
            try:
                full_prompt = tool_wire.responses_history(payload.get("input", messages))
            except ValueError as exc:
                self.send_error(400, str(exc))
                return
        elif tool_mode or chat_history_mode:
            full_prompt = tool_wire.chat_history(messages)
        else:
            prompt_parts = []
            if anthropic and "system" in payload:
                prompt_parts.append("[SYSTEM]:\n" + anthropic_sse.text_content(payload["system"]))
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if anthropic:
                    content = anthropic_sse.text_content(content)
                elif isinstance(content, list):
                    extracted = [item["text"] for item in content if isinstance(item, dict) and "text" in item]
                    content = "\n".join(extracted)
                prompt_parts.append(f"[{role.upper()}]:\n{content}")
            full_prompt = "\n\n".join(prompt_parts)
        if responses and isinstance(payload.get("instructions"), str):
            full_prompt = "[SYSTEM]:\n" + payload["instructions"] + "\n\n" + full_prompt
        if tool_mode:
            full_prompt = tool_wire.instruction(
                client_tools, required=tool_required,
                allow_parallel=allow_parallel) + "\n\n" + full_prompt

        provider_config = load_provider_config(PROVIDER)
        exec_conf = provider_config.get("execution", {})
        stream_conf = provider_config.get("stream", {})

        temp_prompt_path = None
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as tf:
            tf.write(full_prompt)
            temp_prompt_path = tf.name

        cmd = []
        for part in exec_conf.get("cmd_template", []):
            cmd.append(part.replace("{prompt_file}", temp_prompt_path).replace("{prompt}", full_prompt))
        if cmd:
            cmd[0] = shutil.which(cmd[0]) or cmd[0]
        if tool_mode:
            cmd.extend(exec_conf.get("tool_handoff_args", []))
        if requested_model:
            for part in exec_conf.get("model_arg", []):
                cmd.append(part.replace("{model}", requested_model))
        if requested_effort:
            for part in exec_conf.get("effort_arg", []):
                cmd.append(part.replace("{effort}", str(requested_effort)))

        from tokenbuffet.extractors.process_env import build_process_env, isolated_home
        env = build_process_env(provider_config)
        for key in exec_conf.get("env_unset", []):
            env.pop(key, None)
        home = isolated_home(provider_config)
        if home:
            for key in home[1]:
                env[key] = str(home[0])
        temp_sandbox_dir = None
        sandbox = exec_conf.get("sandbox", {})
        if sandbox.get("enabled"):
            temp_sandbox_dir = tempfile.mkdtemp(prefix=f"sandbox_{req_id}_")
            auth_src = os.path.expanduser(sandbox.get("copy_auth", ""))
            if sys.platform == "darwin":
                from tokenbuffet.platforms.macos.paths import expand_path
                auth_src = expand_path(sandbox.get("copy_auth", ""))
            if os.path.exists(auth_src):
                shutil.copy2(auth_src, os.path.join(temp_sandbox_dir, "auth.json"))
            env_var = sandbox.get("env_var")
            if env_var:
                env[env_var] = temp_sandbox_dir

        def cleanup():
            if temp_sandbox_dir:
                shutil.rmtree(temp_sandbox_dir, ignore_errors=True)
            if temp_prompt_path and os.path.exists(temp_prompt_path):
                os.remove(temp_prompt_path)

        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE if exec_conf.get("input_method") in ("stdin", "stream-json") else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env
            )
        except Exception as exc:
            cleanup()
            logger.error("FAIL id=%s provider=%s reason=%s", req_id, PROVIDER, one_line(exc))
            session_log("Proxy Error: " + one_line(exc))
            session_file.close()
            self.send_error(502, "Provider launch failed")
            return

        stderr_chunks = []
        def drain_stderr():
            for chunk in iter(lambda: process.stderr.read(4096), ""):
                stderr_chunks.append(chunk)
                append_response(provider_stderr_path, chunk.encode("utf-8", errors="replace"))
                if debug:
                    session_log("STDERR: " + chunk.replace("\n", "\\n"))
        stderr_thread = threading.Thread(target=drain_stderr, daemon=True)
        stderr_thread.start()
        spawned = time.monotonic()
        last_output = [spawned]
        first_output = [True]
        seen = {"lines": 0, "text_at": None}
        logger.info("SPAWN id=%s provider=%s pid=%s after=%.2fs inflight=%d", req_id, PROVIDER, process.pid,
                    spawned - started, _INFLIGHT[0])
        def note_output():
            now = time.monotonic()
            if first_output[0]:
                first_output[0] = False
                logger.info("FIRST_OUTPUT id=%s provider=%s pid=%s after=%.2fs", req_id, PROVIDER, process.pid,
                            now - spawned)
            last_output[0] = now
            seen["lines"] += 1
        def note_text():
            if seen["text_at"] is None:
                seen["text_at"] = time.monotonic()
                logger.info("TEXT id=%s provider=%s pid=%s first answer text after=%.2fs", req_id, PROVIDER,
                            process.pid, seen["text_at"] - spawned)
        def watch_silence():
            next_warn = STALL_LOG_INTERVAL
            while process.poll() is None:
                time.sleep(1)
                quiet = time.monotonic() - last_output[0]
                if quiet < next_warn - STALL_LOG_INTERVAL:
                    next_warn = STALL_LOG_INTERVAL
                if quiet >= next_warn and process.poll() is None:
                    logger.warning("WAIT id=%s provider=%s pid=%s no CLI output for %.0fs elapsed=%.0fs lines=%d answer_text=%s inflight=%d",
                                   req_id, PROVIDER, process.pid, quiet, time.monotonic() - started, seen["lines"],
                                   "received" if seen["text_at"] else "not_yet", _INFLIGHT[0])
                    next_warn += STALL_LOG_INTERVAL
            logger.info("EXIT id=%s provider=%s pid=%s code=%s after=%.2fs exit_lag=%.2fs (since last output) lines=%d",
                        req_id, PROVIDER, process.pid, process.returncode, time.monotonic() - spawned,
                        time.monotonic() - last_output[0], seen["lines"])
        threading.Thread(target=watch_silence, daemon=True).start()
        provider_errors = []
        def capture_error(obj):
            found = False
            for ext in stream_conf.get("error_extractors", []):
                if check_match(obj, ext.get("matches", {})):
                    value = extract_path(obj, ext.get("path", ""))
                    if value:
                        provider_errors.append(str(value))
                        found = True
            return found
        done_when = stream_conf.get("done_when")
        finished = [False]
        def failure_reason():
            if finished[0] and process.poll() is None:
                # The CLI already sent its terminal event but has not exited; stop waiting on it.
                logger.info("KILL id=%s provider=%s pid=%s terminal event received after=%.2fs, process still running",
                            req_id, PROVIDER, process.pid, time.monotonic() - spawned)
                process.kill()
            process.wait()
            stderr_thread.join()
            if finished[0]:
                return one_line("; ".join(provider_errors)) if provider_errors else None
            if process.returncode or provider_errors:
                return one_line("; ".join(provider_errors) or "".join(stderr_chunks) or f"CLI exited {process.returncode}")
            return None

        response_started = False
        try:
            if exec_conf.get("input_method") == "stdin":
                process.stdin.write(full_prompt)
                process.stdin.close()
            elif exec_conf.get("input_method") == "stream-json":
                process.stdin.write(json.dumps({"event": "user", "message": {"content": full_prompt}}) + "\n")
                process.stdin.close()
            if is_stream and not tool_mode:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                if gemini:
                    self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                elif anthropic:
                    self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                    self.send_header("X-CLI-Bridge-Usage", "unavailable; zero counts are placeholders")
                    self.send_header("X-CLI-Bridge-Max-Tokens", "not-enforced")
                elif responses:
                    self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                elif not UI_STREAM:
                    if request_path in ["/v1/chat/completions", "/v1/completions"]:
                        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                    else:
                        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
                else:
                    self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "close")
                self.end_headers()

                response_started = True
                # Responses-API stream scaffolding (used only when responses=True).
                resp_id = "resp_" + req_id
                responses_item_id = "msg_" + req_id
                responses_created_at = int(time.time())
                responses_acc = []
                extracted_parts = []
                responses_seq = 0
                text_emitted = False
                if anthropic:
                    for event in anthropic_sse.start_events("msg_" + req_id, requested_model):
                        write_response(anthropic_sse.event_bytes(event))
                    self.wfile.flush()
                elif responses:
                    responses_seq += 1
                    write_response(responses_sse_created(responses_seq, resp_id, requested_model,
                                                         responses_created_at, allow_parallel).encode("utf-8"))
                    self.wfile.flush()

                def streaming_lines():
                    if not anthropic:
                        yield from process.stdout
                        return
                    pending_lines = queue.Queue()
                    def read_stdout():
                        try:
                            for output_line in process.stdout:
                                pending_lines.put(output_line)
                        finally:
                            pending_lines.put(None)
                    threading.Thread(target=read_stdout, daemon=True).start()
                    next_ping = time.monotonic() + 10
                    timeout_marker = object()
                    while True:
                        try:
                            output_line = pending_lines.get(
                                timeout=max(0, next_ping - time.monotonic()))
                        except queue.Empty:
                            output_line = timeout_marker
                        if time.monotonic() >= next_ping:
                            write_response(anthropic_sse.event_bytes({"type": "ping"}))
                            self.wfile.flush()
                            next_ping = time.monotonic() + 10
                        if output_line is timeout_marker:
                            continue
                        if output_line is None:
                            return
                        yield output_line

                for line in streaming_lines():
                    note_output()
                    append_response(provider_stdout_path, line.encode("utf-8", errors="replace"))
                    if debug:
                        session_log("CHUNK: " + line.rstrip("\r\n"))
                    line = line.strip()
                    if not line: continue
                    try:
                        obj = json.loads(line)
                        if capture_error(obj):
                            continue
                        if done_when and check_match(obj, done_when):
                            finished[0] = True
                        char = ""
                        for ext in stream_conf.get("text_extractors", []):
                            if check_match(obj, ext.get("matches", {})):
                                extracted = extract_path(obj, ext.get("path", ""))
                                if extracted:
                                    note_text()
                                    char += extracted
                        if char:
                            text_emitted = True
                            extracted_parts.append(char)
                            if gemini:
                                write_response(gemini_wire.stream_chunk(requested_model, char).encode("utf-8"))
                            elif anthropic:
                                write_response(anthropic_sse.event_bytes(anthropic_sse.text_delta(char)))
                            elif responses:
                                responses_acc.append(char)
                                responses_seq += 1
                                write_response(responses_sse_delta(responses_seq, responses_item_id, char).encode("utf-8"))
                            elif not UI_STREAM:
                                if request_path == "/v1/chat/completions":
                                    chunk = {
                                        "id": "chatcmpl-" + req_id,
                                        "object": "chat.completion.chunk",
                                        "created": int(time.time()),
                                        "model": requested_model,
                                        "choices": [{"index": 0, "delta": {"content": char}, "finish_reason": None}]
                                    }
                                    write_response(f"data: {json.dumps(chunk)}\n\n".encode("utf-8"))
                                elif request_path == "/v1/completions":
                                    chunk = {
                                        "id": "cmpl-" + req_id,
                                        "object": "text_completion",
                                        "created": int(time.time()),
                                        "model": requested_model,
                                        "choices": [{"index": 0, "text": char, "finish_reason": None}]
                                    }
                                    write_response(f"data: {json.dumps(chunk)}\n\n".encode("utf-8"))
                                elif request_path == "/api/generate":
                                    chunk = {
                                        "model": requested_model,
                                        "response": char,
                                        "done": False
                                    }
                                    write_response((json.dumps(chunk) + "\n").encode("utf-8"))
                                else:
                                    chunk = {
                                        "model": requested_model,
                                        "message": {"role": "assistant", "content": char},
                                        "done": False
                                    }
                                    write_response((json.dumps(chunk) + "\n").encode("utf-8"))
                            else:
                                evt = UITextDeltaEvent(delta=char)
                                sse_str = format_sse(evt)
                                write_response(sse_str.encode("utf-8"))
                            self.wfile.flush()
                    except json.JSONDecodeError:
                        pass
                    if finished[0]:
                        break
                
                reason = failure_reason()
                save_extracted("".join(extracted_parts))
                if not reason and not text_emitted:
                    reason = "Provider returned no text"
                if reason:
                    logger.error("FAIL id=%s provider=%s exit=%s reason=%s", req_id, PROVIDER, process.returncode, reason)
                    session_log("Proxy Error: " + reason)
                    error = {"type": "error", "error": {"message": reason, "type": "provider_error"}}
                    if gemini:
                        wire = f"data: {json.dumps({'error': {'code': 502, 'message': reason, 'status': 'UNAVAILABLE'}})}\n\n"
                    elif anthropic:
                        wire = anthropic_sse.event_bytes(anthropic_sse.error_event(reason))
                    elif responses:
                        error = {"type": "response.failed", "sequence_number": responses_seq + 1,
                                 "response": {"id": resp_id, "object": "response", "status": "failed",
                                              "error": {"code": "server_error", "message": reason}}}
                        wire = f"event: response.failed\ndata: {json.dumps(error)}\n\n"
                    elif request_path.startswith("/v1/") or UI_STREAM:
                        wire = f"data: {json.dumps(error)}\n\n"
                    else:
                        wire = json.dumps(error) + "\n"
                    write_response(wire if isinstance(wire, bytes) else wire.encode("utf-8"))
                    self.wfile.flush()
                    return

                if gemini:
                    write_response(gemini_wire.stream_chunk(requested_model, "", finished=True).encode("utf-8"))
                elif anthropic:
                    for event in anthropic_sse.stop_events():
                        write_response(anthropic_sse.event_bytes(event))
                elif responses:
                    responses_seq += 1
                    write_response(responses_sse_completed(
                        responses_seq, resp_id, requested_model, responses_created_at,
                        responses_item_id, "".join(responses_acc), allow_parallel).encode("utf-8"))
                    write_response(b"data: [DONE]\n\n")
                elif not UI_STREAM:
                    if request_path == "/v1/chat/completions":
                        chunk = {
                            "id": "chatcmpl-" + req_id,
                            "object": "chat.completion.chunk",
                            "created": int(time.time()),
                            "model": requested_model,
                            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]
                        }
                        write_response(f"data: {json.dumps(chunk)}\n\n".encode("utf-8"))
                        write_response(b"data: [DONE]\n\n")
                    elif request_path == "/v1/completions":
                        chunk = {
                            "id": "cmpl-" + req_id,
                            "object": "text_completion",
                            "created": int(time.time()),
                            "model": requested_model,
                            "choices": [{"index": 0, "text": "", "finish_reason": "stop"}]
                        }
                        write_response(f"data: {json.dumps(chunk)}\n\n".encode("utf-8"))
                        write_response(b"data: [DONE]\n\n")
                    elif request_path == "/api/generate":
                        chunk = {
                            "model": requested_model,
                            "response": "",
                            "done": True
                        }
                        write_response((json.dumps(chunk) + "\n").encode("utf-8"))
                    else:
                        chunk = {
                            "model": requested_model,
                            "message": {"role": "assistant", "content": ""},
                            "done": True
                        }
                        write_response((json.dumps(chunk) + "\n").encode("utf-8"))
                else:
                    fin_evt = UIFinishEvent(finish_reason="stop", message_metadata=None)
                    write_response(format_sse(fin_evt).encode("utf-8"))
                    write_response(b"data: [DONE]\n\n")
                self.wfile.flush()
            else:
                cli_output = ""
                buffered_chat = request_path == "/v1/chat/completions" and is_stream and tool_mode
                if is_stream and tool_mode and (anthropic or buffered_chat):
                    self.send_response(200)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                    if anthropic:
                        self.send_header("X-CLI-Bridge-Usage", "unavailable; zero counts are placeholders")
                        self.send_header("X-CLI-Bridge-Max-Tokens", "not-enforced")
                    self.send_header("Cache-Control", "no-cache")
                    self.send_header("Connection", "close")
                    self.end_headers()
                    response_started = True

                def buffered_lines():
                    if not response_started:
                        yield from process.stdout
                        return
                    pending_lines = queue.Queue()
                    def read_stdout():
                        try:
                            for output_line in process.stdout:
                                pending_lines.put(output_line)
                        finally:
                            pending_lines.put(None)
                    threading.Thread(target=read_stdout, daemon=True).start()
                    def heartbeat(first=False):
                        if anthropic:
                            return anthropic_sse.event_bytes({"type": "ping"})
                        chunk = {"id": "chatcmpl-" + req_id,
                                 "object": "chat.completion.chunk", "created": int(time.time()),
                                 "model": requested_model,
                                 "choices": [{"index": 0,
                                              "delta": {"role": "assistant"} if first else {"content": ""},
                                              "finish_reason": None}]}
                        return ("data: " + json.dumps(chunk) + "\n\n").encode("utf-8")
                    write_response(heartbeat(first=True))
                    self.wfile.flush()
                    next_ping = time.monotonic() + 10
                    timeout_marker = object()
                    while True:
                        try:
                            output_line = pending_lines.get(
                                timeout=max(0, next_ping - time.monotonic()))
                        except queue.Empty:
                            output_line = timeout_marker
                        if time.monotonic() >= next_ping:
                            write_response(heartbeat())
                            self.wfile.flush()
                            next_ping = time.monotonic() + 10
                        if output_line is timeout_marker:
                            continue
                        if output_line is None:
                            return
                        yield output_line

                for line in buffered_lines():
                    note_output()
                    append_response(provider_stdout_path, line.encode("utf-8", errors="replace"))
                    if debug:
                        session_log("CHUNK: " + line.rstrip("\r\n"))
                    line = line.strip()
                    if not line: continue
                    try:
                        obj = json.loads(line)
                        if capture_error(obj):
                            continue
                        if done_when and check_match(obj, done_when):
                            finished[0] = True
                        for ext in stream_conf.get("text_extractors", []):
                            if check_match(obj, ext.get("matches", {})):
                                extracted = extract_path(obj, ext.get("path", ""))
                                if extracted:
                                    note_text()
                                    cli_output += extracted
                    except json.JSONDecodeError:
                        pass
                    if finished[0]:
                        break
                
                reason = failure_reason()
                save_extracted(cli_output)
                if not reason and not cli_output.strip():
                    reason = "Provider returned no text"
                if reason:
                    logger.error("FAIL id=%s provider=%s exit=%s reason=%s", req_id, PROVIDER, process.returncode, reason)
                    session_log("Proxy Error: " + reason)
                    if response_started:
                        wire = (anthropic_sse.event_bytes(anthropic_sse.error_event(reason)) if anthropic
                                else ("data: " + json.dumps({"error": {"message": reason}}) + "\n\n").encode("utf-8"))
                        write_response(wire)
                        self.wfile.flush()
                        return
                    body = json.dumps({"error": {"message": reason, "type": "provider_error", "provider": PROVIDER}}).encode("utf-8")
                    self.send_response(502)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Content-Length", str(len(body)))
                    self.send_header("Connection", "close")
                    self.end_headers()
                    write_response(body)
                    return

                if tool_mode:
                    try:
                        chosen = tool_wire.decision(
                            cli_output, client_tools,
                            id_prefix="toolu_" if anthropic else "call_",
                            required=tool_required, allow_parallel=allow_parallel)
                    except ValueError as exc:
                        if response_started:
                            wire = (anthropic_sse.event_bytes(anthropic_sse.error_event(str(exc))) if anthropic
                                    else ("data: " + json.dumps({"error": {"message": str(exc)}}) + "\n\n").encode("utf-8"))
                            write_response(wire)
                            self.wfile.flush()
                            return
                        self.send_error(502, str(exc))
                        return
                    if gemini:
                        result = gemini_wire.tool_response(requested_model, chosen)
                        wire = ("data: " + json.dumps(result) + "\n\n").encode("utf-8")
                        if is_stream:
                            self.send_response(200)
                            self.send_header("Access-Control-Allow-Origin", "*")
                            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                            self.send_header("Cache-Control", "no-cache")
                            self.send_header("Connection", "close")
                            self.end_headers()
                            write_response(wire)
                            self.wfile.flush()
                            return
                        completion = result
                    elif responses:
                        resp_id = "resp_" + req_id
                        created_at = int(time.time())
                        if is_stream:
                            wire = responses_tool_stream(resp_id, requested_model,
                                                         created_at, chosen, allow_parallel)
                            self.send_response(200)
                            self.send_header("Access-Control-Allow-Origin", "*")
                            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                            self.send_header("Cache-Control", "no-cache")
                            self.send_header("Connection", "close")
                            self.end_headers()
                            write_response(wire)
                            self.wfile.flush()
                            return
                        completion = json.loads(responses_tool_json(
                            resp_id, requested_model, created_at, chosen, allow_parallel))
                    elif anthropic:
                        wire = b"".join(anthropic_sse.event_bytes(event)
                                        for event in anthropic_sse.buffered_events(
                                            "msg_" + req_id, requested_model, chosen))
                        if not response_started:
                            self.send_response(200)
                            self.send_header("Access-Control-Allow-Origin", "*")
                            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                            self.send_header("X-CLI-Bridge-Usage", "unavailable; zero counts are placeholders")
                            self.send_header("X-CLI-Bridge-Max-Tokens", "not-enforced")
                            self.send_header("Cache-Control", "no-cache")
                            self.send_header("Connection", "close")
                            self.end_headers()
                        write_response(wire)
                        self.wfile.flush()
                        return
                    elif is_stream:
                        wire = tool_wire.chat_stream("chatcmpl-" + req_id, requested_model,
                                                     int(time.time()), chosen)
                        if not response_started:
                            self.send_response(200)
                            self.send_header("Access-Control-Allow-Origin", "*")
                            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                            self.send_header("Cache-Control", "no-cache")
                            self.send_header("Connection", "close")
                            self.end_headers()
                        write_response(wire)
                        self.wfile.flush()
                        return
                    else:
                        completion = tool_wire.chat_completion("chatcmpl-" + req_id,
                                                               requested_model, int(time.time()), chosen)
                elif gemini:
                    completion = gemini_wire.response(requested_model, cli_output)
                elif responses:
                    completion = json.loads(responses_nonstream_json(
                        "resp_" + req_id, requested_model, int(time.time()),
                        "msg_" + req_id, cli_output, allow_parallel))
                elif not UI_STREAM:
                    if request_path == "/v1/chat/completions":
                        completion = {
                            "id": "chatcmpl-" + req_id,
                            "object": "chat.completion",
                            "created": int(time.time()),
                            "model": requested_model,
                            "choices": [{
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": cli_output
                                },
                                "finish_reason": "stop"
                            }],
                            "usage": { "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0 }
                        }
                    elif request_path == "/v1/completions":
                        completion = {
                            "id": "cmpl-" + req_id,
                            "object": "text_completion",
                            "created": int(time.time()),
                            "model": requested_model,
                            "choices": [{
                                "index": 0,
                                "text": cli_output,
                                "finish_reason": "stop"
                            }],
                            "usage": { "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0 }
                        }
                    elif request_path == "/api/generate":
                        completion = {
                            "model": requested_model,
                            "response": cli_output,
                            "done": True
                        }
                    else:
                        completion = {
                            "model": requested_model,
                            "message": {"role": "assistant", "content": cli_output},
                            "done": True
                        }
                else:
                    completion = {
                        "id": "chatcmpl-" + req_id,
                        "object": "chat.completion",
                        "created": int(time.time()),
                        "model": requested_model,
                        "choices": [{
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": cli_output
                            },
                            "finish_reason": "stop"
                        }],
                        "usage": { "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0 }
                    }
                
                resp_bytes = json.dumps(completion).encode("utf-8")
                
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(resp_bytes)))
                self.send_header("Connection", "close")
                self.end_headers()
                
                write_response(resp_bytes)
            session_log(f"Output received: {len(''.join(extracted_parts)) if is_stream else len(cli_output)} chars; elapsed={time.monotonic() - started:.2f}s")
            logger.info("DONE id=%s provider=%s elapsed=%.2fs inflight=%d", req_id, PROVIDER, time.monotonic() - started, _INFLIGHT[0])
        except Exception as exc:
            reason = one_line(exc)
            logger.error("FAIL id=%s provider=%s reason=%s", req_id, PROVIDER, reason)
            session_log("Proxy Error: " + reason)
            try:
                if response_started:
                    event = {"type": "error", "error": {"message": reason}}
                    if gemini:
                        wire = f"data: {json.dumps({'error': {'code': 502, 'message': reason, 'status': 'UNAVAILABLE'}})}\n\n".encode("utf-8")
                    else:
                        wire = (anthropic_sse.event_bytes(anthropic_sse.error_event(reason)) if anthropic else
                                (f"data: {json.dumps(event)}\n\n" if request_path.startswith("/v1/") or UI_STREAM else json.dumps(event) + "\n").encode("utf-8"))
                    write_response(wire)
                    self.wfile.flush()
                else:
                    self.send_error(502, "Provider execution failed")
            except OSError:
                pass
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            stderr_thread.join(timeout=2)
            process.stdout.close()
            process.stderr.close()
            if process.stdin and not process.stdin.closed:
                process.stdin.close()
            cleanup()
            session_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", required=True)
    parser.add_argument("--port", type=int)
    parser.add_argument("--protocol")
    parser.add_argument("--model")
    parser.add_argument("--ui-stream", type=str, default="false", help="Emit the Vercel ai_sdk UI-message stream instead of native OpenAI/Ollama/Responses formats (opt-in)")
    parser.add_argument("--refresh-interval", type=int, default=1800,
                        help="Seconds an extractor export remains fresh (default: 1800)")
    parser.add_argument("--log-level", choices=["INFO", "DEBUG"])
    parser.add_argument("--debug", action="store_true", help="Capture full requests, CLI output, and responses")
    args, unknown = parser.parse_known_args()

    PROVIDER = args.provider
    TRACE_LEVEL = resolve_log_level(args.log_level, debug=args.debug)
    log_folder = LOG_DIR / PROVIDER / "proxy"
    log_folder.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_folder / "proxy.log", encoding="utf-8")
    file_handler.setFormatter(_console_format)
    logger.addHandler(file_handler)
    config = load_provider_config(PROVIDER)
    PORT = args.port or config.get("server", {}).get("port", 8000)
    MODEL = args.model
    if args.protocol:
        PROTOCOL = args.protocol
    UI_STREAM = args.ui_stream.lower() == "true"
    REFRESH_INTERVAL = max(0, args.refresh_interval)

    if TRACE_LEVEL == "DEBUG":
        os.makedirs(os.path.join(LOG_DIR, PROVIDER, "proxy", "raw_requests"), exist_ok=True)
        os.makedirs(os.path.join(LOG_DIR, PROVIDER, "proxy", "raw_responses"), exist_ok=True)
        os.makedirs(os.path.join(LOG_DIR, PROVIDER, "llm_provider", "raw_responses"), exist_ok=True)

    status_path = os.path.join("data/providers_status", f"{PROVIDER}_run_status.json")
    usage_state = {"state": "reading"}
    def publish_status(state, reason=None):
        os.makedirs("data/providers_status", exist_ok=True)
        value = {"status": state, "port": PORT, "pid": os.getpid(), "usage": dict(usage_state)}
        if reason:
            value["reason"] = one_line(reason)
        temp_path = f"{status_path}.{os.getpid()}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(value, f)
        for attempt in range(5):
            try:
                os.replace(temp_path, status_path)
                break
            except PermissionError as exc:  # a reader has the status file open
                if attempt == 4:
                    raise RuntimeError(f"Could not update {status_path}: another process kept it open for 5 attempts over 2 seconds (a dashboard, router or another proxy reading it?)") from exc
                time.sleep(0.5)

    running_port = loopback.already_running(status_path)
    if running_port:
        logger.error("FAIL startup provider=%s reason=already running on port %s", PROVIDER, running_port)
        sys.exit(1)
    publish_status("starting")

    try:
        server = loopback.serve_next(PORT, ProxyHandler, ThreadedHTTPServer)
    except OSError as exc:
        logger.error("FAIL startup provider=%s reason=port bind: %s", PROVIDER, one_line(exc))
        publish_status("failed", f"port bind: {exc}")
        sys.exit(1)
    if server.server_address[1] != PORT:
        logger.warning("PORT provider=%s port %s is taken by another process; using %s", PROVIDER, PORT, server.server_address[1])
        PORT = server.server_address[1]
    publish_status("running")

    # The slow TUI captures run in the background so the proxy is usable at once;
    # clients see usage/models as unavailable until each lands, and it refreshes later.
    def refresh_loop():
        while True:
            ok = True
            for op in ("usage", "models"):
                try:
                    provider_export(op, force=True)
                    logger.info("READ provider=%s %s available", PROVIDER, op)
                    if op == "usage":
                        usage_state.clear()
                        usage_state["state"] = "ready"
                except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
                    ok = False
                    logger.error("READ provider=%s %s unavailable: %s", PROVIDER, op, one_line(exc))
                    if op == "usage":
                        usage_state.clear()
                        usage_state.update(state="unavailable", reason=one_line(exc))
                if op == "usage":
                    publish_status("running")
            if REFRESH_INTERVAL <= 0:
                return
            time.sleep(REFRESH_INTERVAL if ok else min(REFRESH_INTERVAL, 300))

    threading.Thread(target=refresh_loop, daemon=True).start()

    logger.info(f"Starting http.server Proxy for {PROVIDER} on port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        publish_status("stopped")
