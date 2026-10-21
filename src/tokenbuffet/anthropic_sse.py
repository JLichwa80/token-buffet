"""Text-only Anthropic Messages request and SSE helpers.

The bridge cannot measure provider token usage, so usage values are placeholders.
"""

import json


def text_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list) and all(
        isinstance(block, dict)
        and block.get("type") == "text"
        and isinstance(block.get("text"), str)
        and set(block) <= {"type", "text", "cache_control"}
        for block in content
    ):
        return "\n".join(block["text"] for block in content)
    raise ValueError("Only strings and plain text blocks are supported")


def validate_request(payload):
    if not isinstance(payload, dict):
        raise ValueError("Request must be a JSON object")
    if payload.get("stream") is not True:
        raise ValueError("This endpoint requires stream: true")
    if not isinstance(payload.get("model"), str) or not payload["model"]:
        raise ValueError("model is required")
    limit = payload.get("max_tokens")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
        raise ValueError("max_tokens must be a positive integer")
    allowed = {"model", "messages", "system", "stream", "max_tokens", "metadata",
               "tools", "tool_choice", "thinking", "context_management", "output_config", "effort"}
    extra = set(payload) - allowed
    if extra:
        raise ValueError("Unsupported parameters: " + ", ".join(sorted(extra)))
    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("messages must be a nonempty list")
    for message in messages:
        if not isinstance(message, dict) or message.get("role") not in ("user", "assistant", "system"):
            raise ValueError("Only user, assistant and system messages are supported")
        content = message.get("content")
        if isinstance(content, str):
            continue
        if not isinstance(content, list) or not content:
            raise ValueError("Message content must be text or a nonempty block list")
        for block in content:
            if not isinstance(block, dict):
                raise ValueError("Content blocks must be objects")
            kind = block.get("type")
            if kind == "text":
                text_content([block])
            elif kind == "tool_use" and message["role"] == "assistant":
                if not all(key in block for key in ("id", "name", "input")):
                    raise ValueError("tool_use needs id, name, and input")
            elif kind == "tool_result" and message["role"] == "user":
                if not all(key in block for key in ("tool_use_id", "content")):
                    raise ValueError("tool_result needs tool_use_id and content")
                text_content(block["content"])
                if "is_error" in block and not isinstance(block["is_error"], bool):
                    raise ValueError("tool_result.is_error must be a boolean")
            else:
                raise ValueError("Unsupported content block: " + str(kind))
    if "system" in payload:
        text_content(payload["system"])
    if "tools" in payload:
        from .tool_wire import anthropic_tools
        anthropic_tools(payload)
    if "tool_choice" in payload:
        choice = payload["tool_choice"]
        if not isinstance(choice, dict) or choice.get("type") not in ("auto", "any", "none", "tool"):
            raise ValueError("Unsupported tool_choice")
        if "disable_parallel_tool_use" in choice and not isinstance(
                choice["disable_parallel_tool_use"], bool):
            raise ValueError("tool_choice.disable_parallel_tool_use must be a boolean")
        if choice["type"] == "tool" and not isinstance(choice.get("name"), str):
            raise ValueError("tool_choice.name is required for a forced tool")


def event_bytes(event):
    return ("event: " + event["type"] + "\ndata: " + json.dumps(event) + "\n\n").encode("utf-8")


def start_events(message_id, model):
    return (
        {"type": "message_start", "message": {
            "id": message_id, "type": "message", "role": "assistant", "model": model,
            "content": [], "stop_reason": None, "stop_sequence": None,
            "usage": {"input_tokens": 0, "output_tokens": 0}}},
        {"type": "content_block_start", "index": 0,
         "content_block": {"type": "text", "text": ""}},
    )


def text_delta(value):
    return {"type": "content_block_delta", "index": 0,
            "delta": {"type": "text_delta", "text": value}}


def stop_events():
    return (
        {"type": "content_block_stop", "index": 0},
        {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": None},
         "usage": {"output_tokens": 0}},
        {"type": "message_stop"},
    )


def error_event(reason):
    return {"type": "error", "error": {"type": "api_error", "message": reason}}


def buffered_events(message_id, model, chosen):
    """Produce a complete stream after the provider's structured decision."""
    yield {"type": "message_start", "message": {
        "id": message_id, "type": "message", "role": "assistant", "model": model,
        "content": [], "stop_reason": None, "stop_sequence": None,
        "usage": {"input_tokens": 0, "output_tokens": 0}}}
    if chosen["kind"] == "tool_calls":
        for index, call in enumerate(chosen["calls"]):
            yield {"type": "content_block_start", "index": index, "content_block": {
                "type": "tool_use", "id": call["id"], "name": call["function"]["name"],
                "input": {}}}
            yield {"type": "content_block_delta", "index": index, "delta": {
                "type": "input_json_delta", "partial_json": call["function"]["arguments"]}}
            yield {"type": "content_block_stop", "index": index}
        stop_reason = "tool_use"
    else:
        yield {"type": "content_block_start", "index": 0,
               "content_block": {"type": "text", "text": ""}}
        yield text_delta(chosen["text"])
        yield {"type": "content_block_stop", "index": 0}
        stop_reason = "end_turn"
    yield {"type": "message_delta", "delta": {"stop_reason": stop_reason,
                                              "stop_sequence": None},
           "usage": {"output_tokens": 0}}
    yield {"type": "message_stop"}
