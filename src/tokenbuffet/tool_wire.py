"""Generic tool handoff through text-only provider CLIs.

The provider is asked for one structured decision. The client, not the bridge,
executes any returned tool call and supplies its result in the next request.
"""

import json
import uuid


def chat_tools(payload):
    tools = payload.get("tools") or []
    if not isinstance(tools, list):
        raise ValueError("tools must be an array")
    result = []
    for index, item in enumerate(tools):
        if not isinstance(item, dict) or item.get("type") != "function":
            raise ValueError(f"tools[{index}] must be a function tool")
        function = item.get("function")
        if not isinstance(function, dict) or not isinstance(function.get("name"), str):
            raise ValueError(f"tools[{index}].function.name is required")
        if not function["name"]:
            raise ValueError(f"tools[{index}].function.name is required")
        result.append({"name": function["name"],
                       "description": function.get("description", ""),
                       "parameters": function.get("parameters", {"type": "object"})})
    return result


def chat_history(messages):
    parts = []
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content")
        if role != "tool" and isinstance(content, str) and content:
            parts.append(f"[{role.upper()}]:\n{content}")
        elif role != "tool" and isinstance(content, list):
            text = "\n".join(item.get("text", "") for item in content
                             if isinstance(item, dict) and isinstance(item.get("text"), str))
            if text:
                parts.append(f"[{role.upper()}]:\n{text}")
        if role == "assistant":
            for call in message.get("tool_calls") or []:
                if isinstance(call, dict):
                    parts.append("[ASSISTANT TOOL CALL]:\n" + json.dumps(call))
        if role == "tool":
            parts.append("[TOOL RESULT " + str(message.get("tool_call_id", "")) + "]:\n" +
                         (content if isinstance(content, str) else json.dumps(content)))
    return "\n\n".join(parts)


def instruction(tools, required=False, allow_parallel=True):
    result = (
        "You are supplying one model response to an API client. The client owns "
        "the following tools and will execute any tool calls you return. Do not "
        "execute these tools yourself. Return exactly one JSON object, with no "
        "Markdown or commentary. For a final answer return "
        '{"kind":"text","text":"your answer"}. To request tools return '
        '{"kind":"tool_calls","calls":[{"name":"tool name",'
        '"arguments":{}}]}. A custom freeform tool uses '
        '{"kind":"tool_calls","calls":[{"name":"tool name",'
        '"input":"raw tool input"}]}. Only call a listed tool, and make '
        "arguments or input match its schema. Available tools: " +
        json.dumps(tools, ensure_ascii=False)
    )
    if required:
        result += " You must return a tool_calls decision with at least one listed tool."
    if not allow_parallel:
        result += " Return at most one tool call in calls."
    return result


def choice_policy(value):
    """Return (enabled, required, forced_name) for common client tool choices."""
    if isinstance(value, dict):
        kind = value.get("type", "auto")
        function = value.get("function")
        forced = value.get("name") or (function.get("name") if isinstance(function, dict) else None)
        namespace = value.get("namespace") or (function.get("namespace") if isinstance(function, dict) else None)
        if forced and namespace:
            forced = namespace + "." + forced
        if kind in ("tool", "function"):
            return True, True, forced
    elif isinstance(value, str):
        kind, forced = value, None
    else:
        kind, forced = "auto", None
    if kind == "none":
        return False, False, None
    return True, kind in ("required", "any"), forced


def anthropic_tools(payload):
    tools = payload.get("tools") or []
    if not isinstance(tools, list):
        raise ValueError("tools must be an array")
    result = []
    for index, item in enumerate(tools):
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise ValueError(f"tools[{index}].name is required")
        if not isinstance(item.get("input_schema"), dict):
            raise ValueError(f"tools[{index}].input_schema must be an object")
        result.append({"name": item["name"], "description": item.get("description", ""),
                       "parameters": item["input_schema"]})
    return result


def anthropic_history(messages):
    parts = []
    for message in messages:
        role = message["role"].upper()
        content = message["content"]
        if isinstance(content, str):
            parts.append(f"[{role}]:\n{content}")
            continue
        for block in content:
            kind = block["type"]
            if kind == "text":
                parts.append(f"[{role}]:\n{block['text']}")
            elif kind == "tool_use":
                parts.append("[ASSISTANT TOOL CALL]:\n" + json.dumps(block))
            elif kind == "tool_result":
                status = " ERROR" if block.get("is_error") else ""
                parts.append("[TOOL RESULT " + block["tool_use_id"] + status + "]:\n" +
                             (block["content"] if isinstance(block["content"], str)
                              else json.dumps(block["content"])))
    return "\n\n".join(parts)


def responses_tools(payload):
    tools = payload.get("tools") or []
    if not isinstance(tools, list):
        raise ValueError("tools must be an array")
    result = []
    for index, item in enumerate(tools):
        if not isinstance(item, dict):
            raise ValueError(f"tools[{index}] must be an object")
        if item.get("type") == "namespace":
            namespace = item.get("name")
            nested = item.get("tools")
            if not isinstance(namespace, str) or not namespace or not isinstance(nested, list) or not nested:
                raise ValueError(f"tools[{index}] needs a namespace name and nonempty tools array")
            entries = nested
        else:
            namespace = None
            entries = [item]
        for nested_index, entry in enumerate(entries):
            location = f"tools[{index}]" + (f".tools[{nested_index}]" if namespace else "")
            if not isinstance(entry, dict) or entry.get("type") not in ("function", "custom", "tool_search"):
                raise ValueError(f"{location} must be a function, custom, or tool_search tool")
            if entry["type"] == "tool_search":
                if namespace:
                    raise ValueError(f"{location} cannot be nested in a namespace")
                if entry.get("execution") != "client":
                    raise ValueError(f"{location}.execution must be client")
                wire_name = "tool_search"
            else:
                wire_name = entry.get("name")
            if not isinstance(wire_name, str) or not wire_name:
                raise ValueError(f"{location}.name is required")
            name = namespace + "." + wire_name if namespace else wire_name
            if any(tool["name"] == name for tool in result):
                raise ValueError(f"Duplicate tool name: {name}")
            tool = {"name": name, "wire_name": wire_name,
                    "type": entry["type"], "description": entry.get("description", ""),
                    "defer_loading": entry.get("defer_loading") is True}
            if namespace:
                tool["namespace"] = namespace
            if entry["type"] == "function":
                tool["parameters"] = entry.get("parameters", {"type": "object"})
            elif entry["type"] == "tool_search":
                tool["parameters"] = entry.get("parameters", {"type": "object"})
            else:
                tool["format"] = entry.get("format", {})
            result.append(tool)
    return result


def responses_available_tools(response_input, declared_tools):
    """Expose deferred client tools only after a tool_search_output reveals them."""
    if isinstance(response_input, dict):
        response_input = [response_input]
    discovered = {}
    if isinstance(response_input, list):
        for item in response_input:
            if isinstance(item, dict) and item.get("type") == "tool_search_output":
                for tool in responses_tools({"tools": item.get("tools", [])}):
                    discovered[tool["name"]] = tool
    declared_names = {tool["name"] for tool in declared_tools}
    available = [tool for tool in declared_tools
                 if not tool["defer_loading"] or tool["name"] in discovered]
    available.extend(tool for name, tool in discovered.items()
                     if name not in declared_names)
    return available


def responses_history(response_input):
    if isinstance(response_input, str):
        return "[USER]:\n" + response_input
    if isinstance(response_input, dict):
        response_input = [response_input]
    if not isinstance(response_input, list):
        raise ValueError("Responses input must be a string or array")
    parts = []
    for item in response_input:
        if isinstance(item, str):
            parts.append("[USER]:\n" + item)
        elif isinstance(item, dict):
            kind = item.get("type", "message")
            if kind in ("function_call_output", "custom_tool_call_output"):
                output = item.get("output", "")
                if not isinstance(output, str):
                    output = json.dumps(output, ensure_ascii=False)
                parts.append("[TOOL RESULT " + str(item.get("call_id", "")) + "]:\n" +
                             output)
            elif kind == "tool_search_output":
                parts.append("[TOOL SEARCH RESULT " + str(item.get("call_id", "")) + "]:\n" +
                             json.dumps(item.get("tools", []), ensure_ascii=False))
            elif kind in ("function_call", "custom_tool_call", "tool_search_call"):
                parts.append("[ASSISTANT TOOL CALL]:\n" + json.dumps(item))
            elif kind == "message":
                content = item.get("content", "")
                if isinstance(content, list):
                    content = "\n".join(str(part.get("text", "")) for part in content
                                        if isinstance(part, dict))
                parts.append("[" + str(item.get("role", "user")).upper() + "]:\n" +
                             str(content))
            else:
                parts.append("[PRIOR RESPONSE ITEM " + str(kind) + "]:\n" +
                             json.dumps(item))
        else:
            raise ValueError("Unsupported Responses input item")
    return "\n\n".join(parts)


def decision(output, tools, id_prefix="call_", required=False, allow_parallel=True):
    raw = output.strip()
    if raw.startswith("```") and raw.endswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        value = json.loads(raw)
    except ValueError:
        # Some CLI streams contain both incremental deltas and a final full
        # assistant item. Accept that exact duplication without guessing at
        # arbitrary prose around a JSON object.
        try:
            value, end = json.JSONDecoder().raw_decode(raw)
            if raw[end:].strip() != raw[:end].strip():
                if required:
                    raise ValueError("Provider did not return a required tool call")
                return {"kind": "text", "text": output}
        except ValueError:
            if required:
                raise ValueError("Provider did not return a required tool call")
            return {"kind": "text", "text": output}
    if not isinstance(value, dict):
        if required:
            raise ValueError("Provider did not return a required tool call")
        return {"kind": "text", "text": output}
    if value.get("kind") == "text" and isinstance(value.get("text"), str):
        if required:
            raise ValueError("Provider did not return a required tool call")
        return value
    if value.get("kind") != "tool_calls" or not isinstance(value.get("calls"), list):
        if required:
            raise ValueError("Provider did not return a required tool call")
        return {"kind": "text", "text": output}
    allowed = {tool["name"]: tool for tool in tools}
    calls = []
    for call in value["calls"]:
        if not isinstance(call, dict) or call.get("name") not in allowed:
            raise ValueError("Provider returned an invalid tool call")
        tool = allowed[call["name"]]
        call_id = id_prefix + uuid.uuid4().hex[:20]
        if tool.get("type") == "tool_search":
            if not isinstance(call.get("arguments"), dict):
                raise ValueError("Provider returned invalid tool search arguments")
            output_call = {"id": call_id, "type": "tool_search_call",
                           "execution": "client", "arguments": call["arguments"]}
        elif tool.get("type") == "custom":
            if not isinstance(call.get("input"), str):
                raise ValueError("Provider returned invalid custom tool input")
            output_call = {"id": call_id, "type": "custom_tool_call",
                           "name": tool.get("wire_name", call["name"]), "input": call["input"]}
        else:
            if not isinstance(call.get("arguments"), dict):
                raise ValueError("Provider returned invalid function arguments")
            output_call = {"id": call_id, "type": "function",
                           "function": {"name": tool.get("wire_name", call["name"]),
                                        "arguments": json.dumps(call["arguments"], ensure_ascii=False)}}
        if tool.get("namespace"):
            output_call["namespace"] = tool["namespace"]
        calls.append(output_call)
    if not calls:
        raise ValueError("Provider returned an empty tool call list")
    if not allow_parallel and len(calls) > 1:
        raise ValueError("Provider returned parallel tool calls when disabled")
    return {"kind": "tool_calls", "calls": calls}


def chat_completion(response_id, model, created, chosen):
    message = {"role": "assistant", "content": None if chosen["kind"] == "tool_calls" else chosen["text"]}
    finish_reason = "stop"
    if chosen["kind"] == "tool_calls":
        message["tool_calls"] = chosen["calls"]
        finish_reason = "tool_calls"
    return {"id": response_id, "object": "chat.completion", "created": created,
            "model": model, "choices": [{"index": 0, "message": message,
                                    "finish_reason": finish_reason}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}}


def chat_stream(response_id, model, created, chosen):
    base = {"id": response_id, "object": "chat.completion.chunk",
            "created": created, "model": model}
    events = []
    if chosen["kind"] == "tool_calls":
        for index, call in enumerate(chosen["calls"]):
            delta = {"tool_calls": [{"index": index, **call}]}
            events.append({**base, "choices": [{"index": 0, "delta": delta,
                                                "finish_reason": None}]})
        finish_reason = "tool_calls"
    else:
        events.append({**base, "choices": [{"index": 0,
                                            "delta": {"content": chosen["text"]},
                                            "finish_reason": None}]})
        finish_reason = "stop"
    events.append({**base, "choices": [{"index": 0, "delta": {},
                                        "finish_reason": finish_reason}]})
    return b"".join(("data: " + json.dumps(event) + "\n\n").encode("utf-8")
                    for event in events) + b"data: [DONE]\n\n"
