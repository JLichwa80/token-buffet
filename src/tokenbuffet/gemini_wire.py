"""Text-only Gemini GenerateContent wire conversion for the CLI bridge."""

import json
import re
from urllib.parse import urlsplit


_GENERATE_PATH = re.compile(
    r"^/(?:v1|v1beta)/models/([^/:]+):(generateContent|streamGenerateContent)$"
)


def parse_generate_path(path):
    match = _GENERATE_PATH.fullmatch(urlsplit(path).path)
    if match is None:
        return None
    return match.group(1), match.group(2) == "streamGenerateContent"


def _text_parts(value, field):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field}.parts must be a nonempty array")
    parts = []
    for part in value:
        if not isinstance(part, dict):
            raise ValueError(f"{field}.parts must contain objects")
        content_keys = set(part) - {"thoughtSignature"}
        if content_keys == {"text"} and isinstance(part["text"], str):
            parts.append(part["text"])
        elif content_keys == {"functionCall"} and isinstance(part["functionCall"], dict):
            parts.append("[PRIOR FUNCTION CALL]: " + json.dumps(part["functionCall"]))
        elif content_keys == {"functionResponse"} and isinstance(part["functionResponse"], dict):
            parts.append("[FUNCTION RESULT]: " + json.dumps(part["functionResponse"]))
        else:
            raise ValueError(f"{field}.parts supports text and function calls/results only")
    return "\n".join(parts)


def to_bridge_request(payload, model, stream):
    if not isinstance(payload, dict):
        raise ValueError("GenerateContent request must be an object")
    unsupported = set(payload) - {"contents", "systemInstruction", "generationConfig",
                                  "tools", "toolConfig", "model"}
    if unsupported:
        raise ValueError("Unsupported GenerateContent fields: " + ", ".join(sorted(unsupported)))
    config = payload.get("generationConfig", {})
    if not isinstance(config, dict):
        raise ValueError("generationConfig must be an object")
    unsupported_config = set(config) - {"maxOutputTokens"}
    if unsupported_config:
        raise ValueError("Unsupported generationConfig fields: " + ", ".join(sorted(unsupported_config)))
    messages = []
    tools = []
    tool_groups = payload.get("tools", [])
    if not isinstance(tool_groups, list):
        raise ValueError("tools must be an array")
    for group in tool_groups:
        if not isinstance(group, dict) or set(group) != {"functionDeclarations"}:
            raise ValueError("Only functionDeclarations tools are supported")
        declarations = group["functionDeclarations"]
        if not isinstance(declarations, list):
            raise ValueError("functionDeclarations must be an array")
        for function in declarations:
            if not isinstance(function, dict) or not isinstance(function.get("name"), str):
                raise ValueError("Each function declaration needs a name")
            tools.append({"name": function["name"],
                          "description": function.get("description", ""),
                          "parameters": function.get("parametersJsonSchema",
                                                     function.get("parameters", {"type": "object"}))})
    tool_config = payload.get("toolConfig", {})
    if not isinstance(tool_config, dict) or set(tool_config) - {"functionCallingConfig"}:
        raise ValueError("toolConfig supports functionCallingConfig only")
    if "systemInstruction" in payload:
        system = payload["systemInstruction"]
        if not isinstance(system, dict) or set(system) != {"parts"}:
            raise ValueError("systemInstruction supports text parts only")
        messages.append({"role": "system", "content": _text_parts(system["parts"], "systemInstruction")})
    contents = payload.get("contents")
    if not isinstance(contents, list) or not contents:
        raise ValueError("contents must be a nonempty array")
    for index, item in enumerate(contents):
        if not isinstance(item, dict) or set(item) - {"role", "parts"}:
            raise ValueError(f"contents[{index}] supports role and parts only")
        role = item.get("role", "user")
        if role not in ("user", "model", "function"):
            raise ValueError(f"Unsupported contents[{index}].role: {role}")
        messages.append({"role": "assistant" if role == "model" else "user",
                         "content": _text_parts(item.get("parts"), f"contents[{index}]")})
    result = {"model": model, "stream": stream, "messages": messages}
    if tools:
        calling = tool_config.get("functionCallingConfig") or {}
        if not isinstance(calling, dict) or set(calling) - {"mode", "allowedFunctionNames"}:
            raise ValueError("Unsupported functionCallingConfig fields")
        mode = calling.get("mode", "AUTO")
        if mode not in ("AUTO", "ANY", "NONE", "VALIDATED"):
            raise ValueError("Unsupported function calling mode")
        allowed = calling.get("allowedFunctionNames")
        if allowed is not None:
            if not isinstance(allowed, list) or any(not isinstance(name, str) for name in allowed):
                raise ValueError("allowedFunctionNames must be an array of names")
            unknown = set(allowed) - {tool["name"] for tool in tools}
            if unknown:
                raise ValueError("Unknown allowed function: " + ", ".join(sorted(unknown)))
            tools = [tool for tool in tools if tool["name"] in allowed]
        if mode == "ANY" and not tools:
            raise ValueError("ANY function calling needs at least one allowed function")
        result["tools"] = tools
        result["tool_choice"] = {"NONE": "none", "ANY": "required"}.get(mode, "auto")
    elif tool_config:
        raise ValueError("toolConfig requires functionDeclarations tools")
    return result


def response(model, text, finished=True):
    candidate = {"content": {"role": "model", "parts": [{"text": text}]}, "index": 0}
    if finished:
        candidate["finishReason"] = "STOP"
    return {"candidates": [candidate], "modelVersion": model}


def stream_chunk(model, text, finished=False):
    return "data: " + json.dumps(response(model, text, finished)) + "\n\n"


def tool_response(model, chosen):
    if chosen["kind"] != "tool_calls":
        return response(model, chosen["text"])
    parts = [{"functionCall": {"id": call["id"],
                               "name": call["function"]["name"],
                               "args": json.loads(call["function"]["arguments"])}}
             for call in chosen["calls"]]
    # Google documents this validator bypass for function calls transferred
    # from a different model, where no genuine Gemini thought signature exists.
    parts[0]["thoughtSignature"] = "skip_thought_signature_validator"
    return {"candidates": [{"content": {"role": "model", "parts": parts},
                             "finishReason": "STOP", "index": 0}],
            "modelVersion": model}


def error(message):
    return {"error": {"code": 400, "message": str(message), "status": "INVALID_ARGUMENT"}}
