# How Claude Code works with Token Buffet and OpenRouter

**A step by step walkthrough for readers without a technical background**

Claude Code is the assistant you interact with. Token Buffet sits behind it and chooses which connected AI service handles a request. You can keep using the same assistant interface while drawing on different AI accounts.

The main difference from OpenRouter is how you access and pay for the AI: **Token Buffet is designed to use the allowance in your existing AI subscriptions through their signed-in CLI applications. OpenRouter uses hosted model APIs with metered API billing.** API usage tokens are the units consumed by requests; an API key is the credential used to access the service.

The introductory conversation and quota examples are illustrative. Section 9 explains the implementation; section 10 contains actual recorded demo requests, process input/output, SSE responses, and a skill/MCP exchange. Section 11 compares client formats using clearly labeled explanatory examples.

For detailed configuration, see [addresses and ports](#9-2-what-the-address-and-ports-mean). For packet contents, see [observed wire examples](#10-observed-demo-and-complete-wire-examples). For the short flow, see [the complete numbered sequence](#14-the-complete-numbered-sequence).

## 1 Separate the assistant from the AI answering it

Think of Claude Code as the assistant's workspace. It holds the conversation and provides actions such as reading files, searching a folder, or editing a document. The AI model supplies the reasoning and decides what to say or which action to request.

```text
YOU
 | "Read these notes and help me write a proposal."
 v
CLAUDE CODE
Conversation, project context, and available actions
 | Asks an AI for the next answer or action
 v
AI MODEL
 | "Here is the answer..."
 |             or
 | "Please read this file first."
 v
CLAUDE CODE
Displays the answer or performs the permitted action
```

**With Token Buffet connected, using the Claude Code interface does not necessarily mean a Claude model answers every request.**

## 2 Where Token Buffet fits

```text
                    YOUR COMPUTER
+-------------------------------------------------------+
| YOU -> CLAUDE CODE                                    |
|          |                                            |
|          v                                            |
|     TOKEN BUFFET                                      |
|     Chooses a connected service                       |
|          |                                            |
|    +-----+-----------+---------------+                |
|    v                 v               v                |
| Claude connector  Codex connector  Grok connector      |
+----|-----------------|---------------|----------------+
     v                 v               v
 Claude online AI  OpenAI online AI  xAI online AI
```

Each connector is a translator. It takes the request from Token Buffet, passes it to the service's installed command-line application, and translates the answer back into a form Claude Code understands.

**The router and connectors run locally. The AI processing still happens at the selected online service.**

Token Buffet uses those installed applications and their signed-in accounts. Whether a request uses subscription allowance or incurs another charge depends on that account and application's billing setup.

## 3 What happens before the conversation starts

Token Buffet needs to know which models each connected service offers and how much of each account's allowance remains. It reads the application's model and usage screens. Each connector reports that information to the router.

| Level | Intended purpose |
| --- | --- |
| fast | Quick, lighter requests |
| medium | Everyday work |
| reasoning | Work intended for stronger reasoning |

These are configured groupings, not guarantees that different companies' models have identical abilities. Each provider defines all three tiers. The Claude provider configuration assigns Haiku to fast, Sonnet to medium, and Opus to reasoning. The router accepts either a tier name or a model name, but handles them differently: a tier request uses normal provider ordering immediately; a recognized model request tries that specific model first and uses same-tier alternatives as backups. An unrecognized name, such as nemotron when it matches nothing in the available model catalog, defaults to medium. Token Buffet does not read the question and estimate its difficulty.

Model assignments are saved as specific model names. They are not automatically replaced with a newer model on every request. Usage information refreshes periodically, so routing uses the latest information Token Buffet has collected.

## 4 Walkthrough of the first request

**You open Claude Code in your project folder and type:**

"Read meeting-notes.txt and draft a short proposal based on what we discussed."

Assume the request explicitly uses `model: medium` and Token Buffet is in usage mode. This is the built-in Claude preset's default setting. For a tier request, usage mode prefers the eligible service with the highest remaining percentage. Medium is a preset choice, not the only level the router supports.

| Connected service | Remaining allowance | Available now |
| --- | --- | --- |
| Codex | 75% | Yes |
| Grok | 45% | Yes |
| Claude | 20% | Yes |

These percentages describe each account's own limits. They are not equal quantities of tokens or equal amounts of money.

```text
YOU
 | "Read the notes and draft a proposal."
 v
CLAUDE CODE
 | Sends your instruction, relevant context,
 | available actions, and selected level: medium
 v
TOKEN BUFFET
 | Candidate order: Codex 75% -> Grok 45% -> Claude 20%
 | Chooses Codex
 v
CODEX CONNECTOR -> CODEX AI
 | "I need to read meeting-notes.txt."
 v
TOKEN BUFFET -> CLAUDE CODE
```

1. Claude Code prepares the request. It includes the instruction and context it sends to the model, plus descriptions of available actions.

2. Token Buffet identifies the selected level and its configured candidates. It checks whether their connectors are running and skips accounts known to have no allowance left.

3. Token Buffet chooses Codex because it has the highest remaining percentage in this example.

4. The connector turns the conversation and action descriptions into a text prompt for the backend application.

5. The AI asks to read the notes. Token Buffet translates that decision into a file-reading request Claude Code recognizes.

**The file has not been read by Token Buffet. The AI has asked Claude Code to read it.**

## 5 Reading the file creates another request

Claude Code performs the action, subject to its permissions, then sends the result back for the next decision.

```text
CLAUDE CODE
 | Reads meeting-notes.txt
 v
FILE CONTENTS
 | Added to the conversation as an action result
 v
NEW REQUEST TO TOKEN BUFFET
 | "Here are the notes. Continue the task."
 v
SELECTED AI SERVICE
 | Uses the supplied notes to draft the proposal
 v
TOKEN BUFFET -> CLAUDE CODE -> YOU
```

**One instruction from you can produce several AI requests.**

```text
One user instruction
        |
        +--> Request 1: Decide what information is needed
        |
        +--> Local action: Read the notes
        |
        +--> Request 2: Use the notes to draft the proposal
        |
        +--> Possible further actions and requests
        |
        +--> Final answer
```

For requests carrying action definitions, Token Buffet asks the backend for one structured decision at a time. That decision can contain an answer or requests for client actions.

Claude Code remains responsible for carrying out those client actions. Token Buffet coordinates the AI request and translates the result.

This matters because reading a file and asking an AI to interpret the file are separate operations. Claude Code accesses the local file. The selected online service receives the content Claude Code includes in its next request.

## 6 Switching services and handling failures

You continue: "Make the proposal shorter and friendlier." Token Buffet makes a routing decision for this new request. Suppose a later usage refresh reports Codex at 30%, Grok at 45%, and Claude at 20%.

```text
Earlier request
Claude Code -> Token Buffet -> Codex -> Answer

Later request
Claude Code -> Token Buffet -> Grok -> Revised answer
```

The new service receives the conversation context included in the new request. It does not inherit another service's private internal session. The conversation can continue using supplied history, but writing style and judgment can vary when the model changes.

A switch is possible, not something that necessarily happens after every message. This example uses a tier request. A recognized model request keeps its requested model first, using other providers as backups. If routing information remains unchanged, Token Buffet may keep choosing the same service. It does not subtract an exact measured cost from its allowance estimate after every response.

For work you want handled at the reasoning level, that level must be selected or requested. Typing a harder question alone does not trigger an automatic upgrade.

### If the chosen service cannot answer

```text
REQUEST -> Try Codex
                |
                +--> Temporary rate limit before client stream starts
                             |
                             v
                       Try Grok at the same level
                             |
                             v
                       Return answer to Claude Code
```

Token Buffet can try another eligible backend for connection problems, rate limits, and certain service errors. It generally tries alternatives within the same level. Some request errors are returned immediately.

Once the response stream has started reaching the client, Token Buffet reports a failure instead of silently continuing with another service. An Anthropic keepalive ping can start that stream before any answer text exists. If every candidate is unavailable or depleted, the request fails.

### Choosing your own service order

For tier requests, usage mode means "Prefer the eligible account with the most allowance left." Custom mode means "Follow my preferred service order," for example Grok, then Codex, then Claude. A recognized model request keeps its specific model first and applies this ordering to its backups. Both modes skip services known to be depleted or not running.

## 7 The same conversation through OpenRouter

OpenRouter offers a direct Claude Code connection using an Anthropic-compatible interface. An API is a standard way for applications to exchange requests and answers.

```text
YOUR COMPUTER
YOU -> CLAUDE CODE
             |
             v
        OPENROUTER
        Hosted gateway
             | Selects an API provider
             v
        MODEL PROVIDER
             | Answer or request for a local action
             v
        OPENROUTER -> CLAUDE CODE
                          |
                          +--> Displays answer
                          |
                          +--> Performs permitted action
                               and sends another request
```

This connection uses OpenRouter credentials and billing rather than drawing on a Claude Code subscription allowance. OpenRouter's Claude Code guide guarantees compatibility only with Anthropic's first-party provider and cautions that other models may not work correctly. [2]

The file-reading sequence stays familiar: you ask for a proposal; Claude Code asks through OpenRouter; the model requests the notes; Claude Code reads the file and sends its contents through OpenRouter; the model drafts the proposal; Claude Code displays it.

OpenRouter's provider routing considers measured factors such as price, speed, latency, and reliability. It supports preferences and backup providers. This differs from Token Buffet's remaining-allowance ranking. [3]

```text
Provider fallback
Same model -> another company hosting that model

Model fallback
Requested model -> a different configured backup model
```

OpenRouter supports configured model fallbacks, including through its Anthropic Messages endpoint. This does not mean Claude Code automatically configures a backup list for you. [4]

## 8 Comparison and practical limits

| Question | Token Buffet | OpenRouter |
| --- | --- | --- |
| What do I interact with? | Claude Code | Claude Code |
| Where does routing run? | On your computer | Hosted by OpenRouter |
| How does it reach the AI? | Installed provider applications | Provider APIs |
| What accounts does it use? | Accounts signed into those applications | OpenRouter credentials with API billing options |
| What guides the choice? | Tier requests use allowance or preferred order; recognized models are tried first with same-tier backups | Model selection and provider routing preferences |
| Can different models answer? | Yes, through configured levels and alternatives | Yes, when selected or configured |
| Who reads or edits local files? | Claude Code performs client actions | Claude Code performs client actions |
| Is the AI processing offline? | No | No |

**Token Buffet focuses on using the AI subscription allowance you already pay for. OpenRouter provides metered API access through a common hosted gateway.**

The current Token Buffet bridge supports text conversations and client action handoff, but it is not a complete reproduction of every native Claude capability. Its Claude Code preset disables thinking, and its reported response token counts are placeholders.

### Sources

[1] Claude Code documentation, How Claude Code works
https://code.claude.com/docs/en/how-claude-code-works

[2] OpenRouter documentation, Claude Code integration
https://openrouter.ai/docs/guides/coding-agents/claude-code-integration

[3] OpenRouter documentation, Provider routing
https://openrouter.ai/docs/guides/routing/provider-selection

[4] OpenRouter documentation, Model fallbacks
https://openrouter.ai/docs/guides/routing/model-fallbacks

Token Buffet source reviewed on October 29 2026: local_router.py, cli_proxy_server.py, tool_wire.py, anthropic_sse.py, the Claude chatbot preset, and docs/integrations/chatbots.md.

## 9 Detailed request lifecycle

This section follows Claude Code as the client and Codex as the selected backend. The code and templates were inspected on October 30 2026. This describes the existing implementation, not a live request trace. Addresses below are the configured defaults; runtime proxy ports can differ if a port is occupied.

### 9 1 Claude Code starts with workspace settings

The workspace launcher starts the client with:

```text
claude --settings <workspace>/.claude/settings.local.json
```

The local settings point its model traffic at Token Buffet:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:8090",
    "ANTHROPIC_MODEL": "medium",
    "CLAUDE_CODE_DISABLE_THINKING": "1",
    "CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY": "1"
  }
}
```

The launcher also sets `CLAUDE_CONFIG_DIR` to the workspace's `.claude-home`. Registration copies selected files from the normal Claude home, skipping configured logs, histories, and temporary files. This creates workspace settings and a snapshot of selected account configuration. It is not a new security sandbox for every request.

The preset renders `ANTHROPIC_MODEL` from the instance's `single_model_tier`, which defaults to `medium`. Therefore this particular configuration sends a tier name. The router also accepts requests that contain a specific model name; those take the separate model-resolution path described below. Inspect the actual request's `model` field to tell which path is being used. A default in a client preset does not mean the router forces every request to medium.

### 9 2 What the address and ports mean

```text
http://127.0.0.1:8090/v1/messages?beta=true
       |         |    |            |
       |         |    |            +-- Optional client query flag
       |         |    +--------------- Messages operation
       |         +-------------------- Router's listening port
       +------------------------------ This same computer
```

Claude Code makes an outgoing HTTP connection to the router. It is not given a permanent listening port of its own for this conversation. The operating system chooses the temporary source port for its connection.

| Component | Default destination | Purpose |
| --- | --- | --- |
| Router | `127.0.0.1:8090` | Receives model requests and selects a provider |
| Claude proxy | `127.0.0.1:8001` | Runs the Claude backend application |
| Codex proxy | `127.0.0.1:8002` | Runs the Codex backend application |
| Dashboard | `127.0.0.1:8080` | Displays status and configuration |

The dashboard is outside the request path. The router finds each proxy's actual port from its run-status file and verifies that the port is listening. A proxy can bind the next free port when its default is occupied.

#### Where the client destination is configured

There are three representations of the same setting. They serve different purposes and are not automatically synchronized with a running server.

```text
Shipped Claude preset
src/tokenbuffet/default_templates/integrations/chatbot/presets/claude/
    app_config.json
          |
          | Workspace initialization copies templates
          v
Runtime integration preset
<Token Buffet workspace>/integrations/chatbot/presets/claude/
          |
          | Registration copies the chosen preset into an instance
          v
Registered instance
<Token Buffet workspace>/registered_apps/chatbot/<instance>/app_config.json
          |
          | init.py reads client_settings.active_endpoint
          | and replaces {active_endpoint} in app_settings.json
          v
Actual Claude workspace
<Claude workspace>/.claude/settings.local.json
          |
          | launch.json passes that file with --settings
          v
Claude Code's ANTHROPIC_BASE_URL
```

The instance configuration contains:

```json
{
  "client_settings": {
    "active_endpoint": "http://127.0.0.1:8090",
    "single_model_tier": "medium"
  },
  "bridge_configuration": ".claude/settings.local.json"
}
```

Its settings template contains `"ANTHROPIC_BASE_URL": "{active_endpoint}"`. The chatbot initializer recursively substitutes the endpoint and model tier, merges the generated JSON into the workspace settings, and writes `launch.json`. The launcher reads that file, sets its declared environment values, sets the process working directory to the Claude workspace, and starts Claude Code with the explicit settings file.

Thus `active_endpoint` is the saved integration input; `ANTHROPIC_BASE_URL` is the value consumed by Claude Code. The IP address and port are both inside that URL. The `/v1/messages` operation is appended by the client's API behavior, not stored as a per-chatbot route in Token Buffet.

Changing the shipped preset does not change an already generated workspace. Reapplying an instance uses its saved instance configuration and templates. Reading the actual `.claude/settings.local.json` and launcher is necessary to establish which destination an existing client uses.

#### Where the servers listen

The receiving side is configured independently:

| Receiving component | Setting used at startup | Source location |
| --- | --- | --- |
| IP address for local services | `HOST = "127.0.0.1"` | `src/tokenbuffet/loopback.py` |
| Router launched directly | `--port`, default 8090 | `local_router.py` argument parser |
| Router launched by the fleet | Explicit `--port 8090` | `cli.py`, fleet startup |
| Router launched through dashboard control | Explicit port 8090 | `dashboard/server.py`, `start_router()` |
| Provider proxy | Explicit `--port`, otherwise provider `server.port` | `cli_proxy_server.py` |
| Codex provider preferred port | `server.port: 8002` | Runtime `registered_providers/codex/config.json` |
| Claude provider preferred port | `server.port: 8001` | Runtime `registered_providers/claude/config.json` |
| Dashboard | `TOKENBUFFET_DASHBOARD_PORT`, default 8080 | `dashboard/server.py` |

`config/router_config.json` stores routing choices, not the router's listening port. Editing an app's `active_endpoint` changes where that app connects. It does not restart a service, allocate that port, or move a listening socket.

```text
Client says: connect to 127.0.0.1:9090
Server says: listen on 127.0.0.1:8090
                         |
                         v
They do not connect merely because both belong to Token Buffet.
The destination and listening port must agree.
```

The local IP is a shared source constant, not a per-client server-IP setting. Supplying another address in the client's URL does not make the local router bind to that address.

#### Requested ports versus actual ports

`loopback.serve_next()` probes up to 50 ports, starting at the requested port. It skips ports that are already listening and tries to bind the first free candidate. The actual bound port is obtained from the server socket, not assumed from the requested number.

A proxy publishes a run-status record such as:

```json
{"status":"running","port":8002,"pid":33404,"usage":{"state":"ready"}}
```

This is an example shape, not a permanent PID. The router's `running_port()` reads that provider's status file, requires `status=running`, and probes the published port before forwarding. This lets the router follow a provider that moved to another port.

The router publishes its own actual port in `data/providers_status/router_run_status.json`. The Claude client preset, however, stores a URL; it does not read that status file to discover a new router port. If direct or fleet router startup moves from its requested port, the client's saved URL does not automatically follow. Dashboard `start_router()` differs: it checks port 8090 first and refuses to launch when that port is already occupied.

The live trace later in this document deliberately uses different local ports without changing these product defaults. A recording relay is explicitly included in that diagram so it is not confused with a normal Token Buffet component.

### 9 3 Skills tools and MCP remain client responsibilities

These are different pieces of the client environment:

| Component | What it supplies | Who manages it |
| --- | --- | --- |
| Skill | Instructions and a reusable procedure | Claude Code |
| Built-in tool | An action such as reading a file or running a command | Claude Code |
| MCP connection | Access to tools or information exposed by another program or service | Claude Code and the MCP server |

Claude Code loads a skill's body when that skill is used. Relevant instructions become part of the context it supplies to the model. Token Buffet does not install that Claude skill into Codex or convert it into a Codex skill package. It carries the text that arrives in the request. Skills can also involve local processing or supporting scripts handled by the client. [5]

Claude Code maintains its MCP connections. The model is shown descriptions of the tools made available in the current request. For a supported MCP tool call, Token Buffet carries the tool name, description, input definition, and later the result. It does not take over the client's MCP connection or authenticate to the MCP server on the client's behalf. [6]

```text
Instructions and skills ----------> Claude Code context
Built-in tools -------------------> Claude Code action list
MCP servers <---------------------> Claude Code MCP connections
                                          |
                                          | Model request containing context
                                          | and available tool definitions
                                          v
                                    Token Buffet
                                          |
                                          v
                                    Selected backend
```

MCP traffic and model traffic are separate connections. Changing `ANTHROPIC_BASE_URL` redirects model requests; it does not redirect MCP servers to port 8090.

### 9 4 Claude Code sends an Anthropic Messages request

The main model endpoint for this client is `POST /v1/messages`, sometimes with `?beta=true`. The router parses the path separately from the query string.

The following abbreviated JSON illustrates a request explicitly selecting `reasoning`, rather than the preset's default medium. It is not a complete captured request:

```json
{
  "model": "reasoning",
  "stream": true,
  "max_tokens": 4096,
  "system": "Project instructions and relevant skill instructions",
  "messages": [
    {"role": "user", "content": "Read my notes and draft a proposal."}
  ],
  "tools": [
    {
      "name": "Read",
      "description": "Read a text file",
      "input_schema": {
        "type": "object",
        "properties": {"file_path": {"type": "string"}},
        "required": ["file_path"]
      }
    }
  ]
}
```

The router reads the HTTP body using `Content-Length`, decodes JSON, and creates a request ID. For this endpoint, it validates the supported Anthropic request structure. The current bridge requires `stream: true`, a model string, a positive `max_tokens`, and supported message and tool blocks.

### 9 5 The router resolves a tier or a specific model

The router reads `payload.model`. A variable called `tier` initially holds that incoming string; its variable name does not mean classification has already happened. The code then tries the following lookups in order.

The provider configuration supplies the model families used when building the saved tier assignments:

```json
{
  "tiers": {
    "fast": "^Haiku$",
    "medium": "^Sonnet$",
    "reasoning": "^Opus$"
  }
}
```

Those regular expressions are used during model discovery to choose exact backend model IDs for the saved tier configuration. They are not run against incoming requests to split versioned names into family tokens. No model versions are hard-coded in this request-resolution path.

```text
Incoming request             Resolution
--------------------------------------------------------------
reasoning                 -> Get reasoning tier backends
Exact model in catalog    -> Try that specific provider/model first
Provider name             -> Use its first configured tier
Partial model name        -> Try first matching catalog model first
No match                  -> Use medium tier backends
```

The resolution order is:

1. An explicit tier name, such as `reasoning`, is used directly.
2. An exact model ID in `ALL_MODELS`, the cached available-model catalog, creates a specific provider/model candidate. That candidate is first, rather than being reordered by usage.
3. A provider name alone, such as `claude`, selects that provider's first configured tier. The resulting tier's backends use normal usage/custom ordering. A bare provider name does not itself pin that provider.
4. A partial name is compared with catalog model IDs, ignoring case. A match occurs if either string contains the other. The first catalog match becomes a specific provider/model candidate.
5. Only a name that survives all those checks without a match defaults to `medium`.

For a specific candidate, the router separately finds its tier by looking for the same provider and model in the saved tier assignments. That tier supplies the alternate providers. If the model has no exact tier assignment, the current code uses that provider's first tier, or medium if it cannot find a provider tier. If the same model appears in several tiers, the first match wins.

For example, `opus` can resolve to a catalog model containing `opus`, or a full versioned name can match a shorter catalog alias such as `Opus`. This is a catalog substring lookup, not a promise to recognize every future model ID. If `nemotron` matches no explicit tier, catalog model, provider name, or partial catalog name, it defaults to medium.

There is no prompt analysis, model download, or live model-list refresh during these lookups. A wholly unrecognized name needs a configured medium fallback; without one, the router returns HTTP 503.

### 9 6 The router selects a provider and its model for that tier

Every provider has mappings for all three tiers. For an explicit `reasoning` request, the router orders the reasoning backends by usage or custom order. Assume those rules select Codex:

```text
Claude Code sends model=reasoning
          |
          v
Get configured reasoning backends
          |
          v
Router compares reasoning backends
          |
          v
Codex selected by usage or custom order
          |
          v
Read providers.codex.tiers.reasoning
          |
          v
Invoke Codex with THAT configured Codex model
```

Codex does not receive `reasoning` or `Opus` as its model argument. The router replaces `payload.model` with the exact Codex model ID saved for `reasoning` in `config/router_config.json`.

A specific-model request takes a different route. Assuming the catalog recognizes Opus and its saved tier is reasoning:

```text
Claude Code sends an Opus model name
          |
          v
Resolve the catalog entry and keep that Claude model first
          |
          +--> Success: return its answer
          |
          +--> Unavailable or retryable failure before streaming
                         |
                         v
                  Try reasoning-tier alternatives
                         |
                         v
                  Codex chosen as an alternate
                         |
                         v
                  Call Codex's configured reasoning model
```

Usage/custom ordering applies immediately to explicit tier requests and to the alternate list for specific-model requests. It does not move an available requested model behind another provider just because another account has more quota.

Usage mode ranks by the tightest known remaining percentage. For example, an account with 80% remaining in its short window but 15% remaining in its weekly window is ranked at 15%. Unknown usage is not the same as known exhaustion: it sorts as zero in usage mode but remains eligible. Known depleted and stopped providers are skipped in both modes.

Tier backends carry effort resolved from their model entry, provider setting, global setting, or tier default. The normal reasoning default is `high`. A specific model candidate instead starts with its per-model or provider effort lookup. For the whole request, explicit `effort` or `reasoning_effort` wins; otherwise the router takes the first candidate with an effort value. It locks that value across retries. If no effort is resolved, the proxy receives no injected effort argument and the backend application uses its own behavior.

### 9 7 The router forwards to the Codex proxy

The HTTP format remains the client's format:

```text
Claude Code
 POST http://127.0.0.1:8090/v1/messages?beta=true
 model = reasoning
                   |
                   v
Router
 Reads reasoning tier and selects Codex
 Replaces model with Codex's configured reasoning model
 Adds resolved effort and X-Request-ID
 Recalculates Content-Length
                   |
                   v
Codex proxy
 POST http://127.0.0.1:8002/v1/messages?beta=true
 model = <configured Codex reasoning model>
```

The router forwards the path, including its query string. It forwards incoming headers except the host, old body length, and old request ID, which it handles for the local hop. It does not convert this request to `/v1/responses` merely because Codex was selected.

The proxy chooses the response protocol from the request path. Its provider configuration chooses which backend application to launch. These are independent choices.

### 9 8 The proxy converts the conversation into a text prompt

The Codex proxy recognizes `/v1/messages` as Anthropic input. It extracts the conversation, system text, tool definitions, and previous tool results, then builds a text prompt:

```text
You are supplying one model response to an API client.
The client owns these tools and executes returned calls.
Do not execute the client tools yourself.
Return one JSON decision: an answer or tool calls.
Available tools: [names, descriptions, input definitions]

[SYSTEM]:
Project instructions and relevant skill instructions

[USER]:
Read my notes and draft a proposal.

[ASSISTANT TOOL CALL]:
...previous call if supplied...

[TOOL RESULT toolu_...]:
...previous result if supplied...
```

Anthropic's `input_schema` becomes the bridge's common `parameters` field in the tool description. Conversation roles become text labels. The original system instructions are included as text; this is not a lossless conversion to a native OpenAI system message.

When tools are available, the bridge asks the backend to return a structured decision:

```json
{"kind":"tool_calls","calls":[{"name":"Read","arguments":{"file_path":"meeting-notes.txt"}}]}
```

Or an answer:

```json
{"kind":"text","text":"Here is the proposal..."}
```

### 9 9 The proxy launches one backend process

For Codex, the configured invocation has this form:

```text
codex exec --json --skip-git-repo-check
  --model <configured Codex reasoning model>
  -c model_reasoning_effort="high"
```

The proxy builds an argument list and launches a subprocess. It prepares a temporary prompt file, although this preset sends the actual prompt through the process's standard input. It captures standard output and standard error through separate pipes.

```text
HTTP body
    |
    v
Translated prompt -> subprocess standard input
                         |
                         v
                    codex exec
                         |
                         v
                    OpenAI service
                         |
                         v
JSON lines on standard output -> proxy parser
Errors on standard error ------> error capture
```

The Codex application handles its own remote authentication and service communication. Token Buffet is not building a direct OpenAI API request in this path. Consequently, an Anthropic-to-OpenAI HTTP envelope conversion is not needed here: the intermediate representation is a text prompt passed to the CLI.

The provider's configuration tells the proxy which JSON output events contain answer text. For example, the Codex configuration recognizes an `item.completed` event with `item.type` equal to `agent_message` and reads `item.text`. It also recognizes configured text delta events.

### 9 10 The proxy returns the client's protocol

For an ordinary text response without tool mode, the proxy can extract text as the backend emits it and wrap it as Anthropic streaming events.

For a tool-enabled request, it buffers the extracted output until it can interpret the complete structured decision. It checks the returned tool name against the offered tools, checks argument object shape, and enforces required-call or parallel-call restrictions. It does not perform full JSON Schema validation of every argument value.

The bridge creates an Anthropic call ID and produces events such as:

```text
event: message_start
event: content_block_start     type=tool_use, name=Read
event: content_block_delta     type=input_json_delta
event: content_block_stop
event: message_delta           stop_reason=tool_use
event: message_stop
```

An answer uses a text content block and `stop_reason=end_turn` instead. Claude Code receives Anthropic events even when Codex generated the underlying decision.

### 9 11 Streaming does not always mean incremental answer text

There are three different layers:

| Layer | What can stream |
| --- | --- |
| Backend application | JSON output events or text fragments on standard output |
| Proxy processing | Immediate text translation, or buffering a complete tool decision |
| HTTP response | Server-sent events delivered to Claude Code |

The Anthropic endpoint requires a streaming HTTP request. With tools available, the proxy sends keepalive `ping` events while it buffers the backend decision, normally every ten seconds, including an initial ping. It then emits the completed answer or tool call as events.

```text
Time --->
Backend:    [computing and producing structured output.......]
Proxy:      [collecting the complete decision................]
HTTP:       ping ... ping ... ping ... [complete decision events]
```

Therefore a response can be streaming at the HTTP level while its useful answer arrives in one batch. This also applies when a tool-enabled request ultimately returns text rather than calling a tool.

The router forwards stream lines once it sees a recognized event. Its current implementation counts an Anthropic ping as enough to start the client response. After that, a failure is reported to the client instead of trying another provider. This means automatic failover is not guaranteed merely because no answer text has appeared yet.

### 9 12 Claude Code executes the action and sends another request

For a built-in file tool:

```text
Backend asks for Read
       |
       v
Proxy returns Anthropic tool_use
       |
       v
Claude Code applies its permissions and executes Read
       |
       v
Claude Code adds tool_result to its conversation
       |
       v
New POST /v1/messages through Token Buffet
```

For an MCP tool, the execution path is:

```text
Backend requests an offered MCP tool by name
       |
       v
Proxy -> router -> Claude Code
                       |
                       | MCP tool call over its own connection
                       v
                    MCP server -> external service or local operation
                       |
                       v
                    Tool result -> Claude Code
                                      |
                                      v
                               Next model request
```

The selected backend does not need to install the client's MCP server to choose a tool from its supplied definition. Claude Code performs the actual MCP invocation. Results must fit the bridge's supported text-based message format; images or newer special blocks are not automatically supported.

Every follow-up model request is routed again. It can use another provider. Continuity comes from the conversation and tool results that Claude Code includes, rather than from a persistent backend CLI session maintained by Token Buffet.

### 9 13 What is and is not isolated

| Layer | Current separation | Important boundary |
| --- | --- | --- |
| Client workspace | Local settings and a workspace Claude home | This is configuration separation, not OS isolation |
| Individual request | New subprocess, request ID, prompt, pipes, and response handling | A fresh process can still read shared configuration or credentials |
| Backend environment | Provider-configured environment changes | It begins with inherited environment unless the configuration removes or replaces values |
| Grok backend | Fresh temporary home, copied auth file, `GROK_HOME` override, cleanup | This separates a home directory; it does not change the subprocess working directory or create a full OS sandbox |
| agy backend | Persistent provider home with configured tool-denial settings | Shared across that provider's calls; not a fresh home per request |
| Claude and Codex backends | Their current presets disable the temporary-home sandbox option | Do not describe these as fully sandboxed calls |

The proxy removes provider-specific routing environment variables before launch. For example, the Claude backend removes `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, and `ANTHROPIC_API_KEY`; Codex removes `OPENAI_BASE_URL` and `OPENAI_API_KEY`. These removals are configuration-driven, not universal isolation of every environment variable.

For client tool handoff, the prompt instructs the backend to leave execution to the client. Claude and Grok also have configured `--tools ""` handoff arguments. Codex's current preset does not contain that same tool-disabling argument. Prompt instructions alone are not a security boundary, and the proxy does not automatically remove every backend skill or MCP configuration.

### 9 14 Cleanup logs and compatibility boundaries

At the end of the request, the proxy stops a still-running child, waits for it, closes the pipes, deletes its temporary prompt and temporary home when applicable, and closes its session log. The provider proxy and router remain running for subsequent requests.

The shared request ID connects router and proxy log entries. Debug mode additionally saves request bodies, raw backend output, translated HTTP output, and extracted text. Request cleanup does not delete those retained logs.

The current implementation has these practical boundaries:

- Anthropic message usage counts are zero placeholders. They do not mean the request consumed no allowance.
- `max_tokens` must be present and positive but is not enforced by this bridge as a backend generation limit.
- The supplied Claude preset disables thinking. Native thinking blocks are not carried losslessly through the text bridge.
- The current proxy dispatcher has no `/v1/messages/count_tokens` handler.
- Anthropic validation supports text, `tool_use`, and text `tool_result` blocks, not arbitrary multimodal or newer protocol blocks.
- Current Claude Code documentation describes deferred MCP tool loading and `tool_reference` blocks. The current bridge validator does not implement those blocks or the full tool-search protocol. Ordinary tools supplied with a complete name and `input_schema` use the handoff described above; full deferred-tool compatibility has not been established. [6]

### 9 15 How this differs from the OpenRouter path

```text
TOKEN BUFFET
Claude Code Anthropic request
 -> local router resolves tier or specific model and candidate order
 -> local proxy translates to text instructions
 -> installed provider CLI contacts its service
 -> proxy extracts text or a structured decision
 -> proxy constructs Anthropic response events
 -> Claude Code executes requested client actions

OPENROUTER
Claude Code Anthropic request
 -> OpenRouter's hosted Anthropic-compatible endpoint
 -> provider API routing and protocol handling
 -> hosted model response
 -> Anthropic-compatible response to Claude Code
 -> Claude Code executes requested client actions
```

In the Token Buffet path, the installed provider application is the bridge to its online AI. In the OpenRouter path, the gateway communicates through hosted APIs. The client still owns its local actions and MCP connections in either path.

### Additional references

[5] [Claude Code skills](https://code.claude.com/docs/en/skills)

[6] [Claude Code MCP connections and tool search](https://code.claude.com/docs/en/mcp)

[7] [Claude Code gateway protocol requirements](https://code.claude.com/docs/en/llm-gateway-protocol)

Implementation: [router](src/tokenbuffet/local_router.py), [proxy](src/tokenbuffet/cli_proxy_server.py), [tool translation](src/tokenbuffet/tool_wire.py), [Anthropic response events](src/tokenbuffet/anthropic_sse.py), [process environment](src/tokenbuffet/extractors/process_env.py), and [Claude client settings template](src/tokenbuffet/default_templates/integrations/chatbot/presets/claude/app_settings.json).

## 10 Observed demo and complete wire examples

The following observations come from live runs on October 30 2026, using Claude Code 2.1.308 and Codex CLI 0.166.0. The product router, proxy, tool translator, and Anthropic formatter were used without modifying their source. A demo-only wrapper recorded subprocess arguments and standard input; a local HTTP relay recorded client requests and response lines. Captured payloads, rather than assumed API behavior, drive the examples below.

The existing fleet at `C:\Users\Jack\TokenBuffet` was left running. Separate demo services used ports 18002 and 18090, with a recording relay on 18890. The demo copied the installed Codex provider configuration, saved models and usage, and Codex's three saved tier assignments into a separate runtime directory. Only Codex was registered in this demo runtime, so this validates the cross-vendor translation path, not a competition among several live backends. It does not validate automatic failover.

The client used an empty demo configuration home, a placeholder gateway credential, and explicitly selected tools. The backend Codex application used its normal provider login. No private user document was read. The file and MCP data were fixtures created for this trace.

```text
Claude Code client
  destination configured as http://127.0.0.1:18890
          |
          | HTTP JSON request; Anthropic Messages format
          v
Recording relay on 18890              [demo instrumentation]
          |
          | Same JSON body forwarded to router
          v
Original Token Buffet router on 18090
          |
          | /v1/messages?beta=true remains unchanged
          | model rewritten from medium to gpt-6.1-sol
          | effort=medium injected
          v
Original Codex provider proxy on 18002
          |
          | Text prompt through a local stdin pipe
          v
codex exec --json --model gpt-6.1-sol
          |
          | Codex's own encrypted provider connection
          v
Online AI service
```

The provider's encrypted HTTPS payload was not intercepted. The evidence establishes what Token Buffet passed to the installed Codex executable and what that executable returned. It does not establish the private remote request serialization inside Codex.

### 10 1 First request from Claude Code to the router

**Configuration level.** The trace client was explicitly configured with `ANTHROPIC_BASE_URL=http://127.0.0.1:18890` and `ANTHROPIC_MODEL=medium`. This matches the normal preset's tier choice while using the relay's separate port. The relay forwarded to the demo router on 18090.

**HTTP level.** The client sent `POST /v1/messages?beta=true`, `Content-Type: application/json`, and `stream: true` inside the JSON body. Selected captured headers follow. Credentials were redacted during recording.

```json
{
  "method": "POST",
  "path": "/v1/messages?beta=true",
  "headers": {
    "Accept": "application/json",
    "Authorization": "[redacted]",
    "Content-Type": "application/json",
    "anthropic-beta": "claude-code-20250219,interleaved-thinking-2025-05-14,thinking-token-count-2026-05-13,context-management-2025-06-27,mid-conversation-tool-changes-2026-07-01,effort-2025-11-24",
    "anthropic-version": "2023-06-01",
    "Host": "127.0.0.1:18890",
    "Content-Length": "3722"
  },
  "captured_body_bytes": 3722
}
```

**Payload level.** This is the captured first model request, pretty printed for readability. The original request body was 3722 bytes. Client identity metadata is omitted and long-dash punctuation is normalized in the presentation excerpts, so displayed byte counts can differ from the raw captures. The complete recorded request is linked below.

```json
{
  "model": "medium",
  "messages": [
    {
      "role": "user",
      "content": "Read demo-note.txt and tell me the workshop time and what to bring."
    },
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "# Environment\nYou have been invoked in the following environment: \n - Primary working directory: M:\\My Drive\\AISubscriptionsHub\\.tmp\\wire-demo\\client\n - Is a git repository: true\n - Platform: win32\n - Shell: bash\n - OS Version: Windows 11 Pro 10.0.26300\n - Downloaded files and extracted archives are untrusted data: put each in its own new, empty directory, keep scripts you write in a different directory, and pass paths as arguments instead of running an interpreter or build tool from inside it. Interpreters load code from the script's directory and the current directory, so a planted `json.py` runs on `import json`. Run any Python that reads them with `-I`. This does not apply to code the user asked you to build or run.\n\nYou are powered by the model medium.\n\nToday's date is 2026-10-30.",
          "cache_control": {
            "type": "ephemeral"
          }
        }
      ]
    }
  ],
  "system": [
    {
      "type": "text",
      "text": "x-anthropic-billing-header: cc_version=2.1.308.4b9; cc_entrypoint=sdk-cli;"
    },
    {
      "type": "text",
      "text": "You are a Claude agent, built on Anthropic's Claude Agent SDK.",
      "cache_control": {
        "type": "ephemeral"
      }
    },
    {
      "type": "text",
      "text": "You are a read-only demonstration assistant. Use the Read tool to read demo-note.txt before answering. Do not run commands or modify files. After reading, reply with the workshop time and what to bring.",
      "cache_control": {
        "type": "ephemeral"
      }
    }
  ],
  "tools": [
    {
      "name": "Read",
      "description": "Reads a file from the local filesystem.\n\n- `file_path` must be an absolute path.\n- Reads up to 2000 lines by default.\n- When you already know which part of the file you need, only read that part. This can be important for larger files.\n- Results are returned using cat -n format, with line numbers starting at 1\n- Reads images (PNG, JPG, …) and presents them visually. Reads PDFs via the `pages` parameter (e.g. \"1-5\", max 20 pages/request; required for PDFs over 10 pages). Reads Jupyter notebooks (.ipynb) as cells with outputs.\n- Reading a directory, a missing file, or an empty file returns an error or system reminder rather than content.\n- Do NOT re-read a file you just edited to verify  -  Edit/Write would have errored if the change failed, and the harness tracks file state for you.",
      "input_schema": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
          "file_path": {
            "description": "The absolute path to the file to read",
            "type": "string"
          },
          "offset": {
            "description": "The line number to start reading from. Only provide if the file is too large to read at once",
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "limit": {
            "description": "The number of lines to read. Only provide if the file is too large to read at once.",
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "pages": {
            "description": "Page range for PDF files (e.g., \"1-5\", \"3\", \"10-20\"). Only applicable to PDF files. Maximum 20 pages per request.",
            "type": "string"
          },
          "allow_large": {
            "description": "Set to true to read a text file, or a line range of one, that is over the usual size limits, up to what still fits in your context. Only use this when you genuinely need all of it or the user asked for the whole file; otherwise read it in parts with offset and limit, or search it.",
            "type": "boolean"
          }
        },
        "required": [
          "file_path"
        ],
        "additionalProperties": false
      }
    }
  ],
  "metadata": "[client identity metadata omitted from this display]",
  "max_tokens": 32000,
  "output_config": {
    "effort": "high"
  },
  "stream": true
}
```

The same observed fields can be represented as an HTTP message. This is a normalized reproduction: client identity metadata is replaced, incidental headers are omitted, and Content-Length is recalculated for the exact compact body displayed here. HTTP header lines use CRLF on the connection; this Markdown view uses readable line breaks. This example is not a byte-identical copy of the original 3722-byte body.

```http
POST /v1/messages?beta=true HTTP/1.1
Host: 127.0.0.1:18890
Content-Type: application/json
Content-Length: 3606

{"model":"medium","messages":[{"role":"user","content":"Read demo-note.txt and tell me the workshop time and what to bring."},{"role":"system","content":[{"type":"text","text":"# Environment\nYou have been invoked in the following environment: \n - Primary working directory: M:\\My Drive\\AISubscriptionsHub\\.tmp\\wire-demo\\client\n - Is a git repository: true\n - Platform: win32\n - Shell: bash\n - OS Version: Windows 11 Pro 10.0.26300\n - Downloaded files and extracted archives are untrusted data: put each in its own new, empty directory, keep scripts you write in a different directory, and pass paths as arguments instead of running an interpreter or build tool from inside it. Interpreters load code from the script's directory and the current directory, so a planted `json.py` runs on `import json`. Run any Python that reads them with `-I`. This does not apply to code the user asked you to build or run.\n\nYou are powered by the model medium.\n\nToday's date is 2026-10-30.","cache_control":{"type":"ephemeral"}}]}],"system":[{"type":"text","text":"x-anthropic-billing-header: cc_version=2.1.308.4b9; cc_entrypoint=sdk-cli;"},{"type":"text","text":"You are a Claude agent, built on Anthropic's Claude Agent SDK.","cache_control":{"type":"ephemeral"}},{"type":"text","text":"You are a read-only demonstration assistant. Use the Read tool to read demo-note.txt before answering. Do not run commands or modify files. After reading, reply with the workshop time and what to bring.","cache_control":{"type":"ephemeral"}}],"tools":[{"name":"Read","description":"Reads a file from the local filesystem.\n\n- `file_path` must be an absolute path.\n- Reads up to 2000 lines by default.\n- When you already know which part of the file you need, only read that part. This can be important for larger files.\n- Results are returned using cat -n format, with line numbers starting at 1\n- Reads images (PNG, JPG, \u2026) and presents them visually. Reads PDFs via the `pages` parameter (e.g. \"1-5\", max 20 pages/request; required for PDFs over 10 pages). Reads Jupyter notebooks (.ipynb) as cells with outputs.\n- Reading a directory, a missing file, or an empty file returns an error or system reminder rather than content.\n- Do NOT re-read a file you just edited to verify \u2014 Edit/Write would have errored if the change failed, and the harness tracks file state for you.","input_schema":{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"file_path":{"description":"The absolute path to the file to read","type":"string"},"offset":{"description":"The line number to start reading from. Only provide if the file is too large to read at once","type":"integer","minimum":0,"maximum":9007199254740991},"limit":{"description":"The number of lines to read. Only provide if the file is too large to read at once.","type":"integer","exclusiveMinimum":0,"maximum":9007199254740991},"pages":{"description":"Page range for PDF files (e.g., \"1-5\", \"3\", \"10-20\"). Only applicable to PDF files. Maximum 20 pages per request.","type":"string"},"allow_large":{"description":"Set to true to read a text file, or a line range of one, that is over the usual size limits, up to what still fits in your context. Only use this when you genuinely need all of it or the user asked for the whole file; otherwise read it in parts with offset and limit, or search it.","type":"boolean"}},"required":["file_path"],"additionalProperties":false}}],"metadata":"[client identity metadata omitted from this display]","max_tokens":32000,"output_config":{"effort":"high"},"stream":true}
```

Full evidence: [client request body](.tmp/wire-demo/trace/http-002.request.body) and [request headers and byte count](.tmp/wire-demo/trace/http-002.request.json).

The `tools` entry describes an action; it does not contain the file. `input_schema` tells the model which arguments to return for `Read`. The first request contains the user's instruction but no file contents. The top-level `system` and the system-role message are separate parts of the client envelope; the proxy later turns both into labeled text.

The client also made `HEAD /api/hello` before the first model request. The router returned HTTP 501 for that unsupported method. The client continued and both model requests succeeded. This trace therefore distinguishes a nonfatal startup probe from the model operation itself. The relay added no successful model response of its own.

### 10 2 The router changes the provider model and effort

**Lookup level.** `medium` directly matched the router's configured tier. The copied Codex mapping assigned that tier to `gpt-6.1-sol`. The routing log recorded `mode=usage`, `tier=medium`, and Codex as the candidate.

**Mutation level.** The router modified its parsed JSON dictionary, then serialized it as UTF-8 for the proxy hop. The observed changed top-level fields were:

```json
{
  "model": {
    "client": "medium",
    "proxy": "gpt-6.1-sol"
  },
  "effort": {
    "client": "[absent]",
    "proxy": "medium"
  }
}
```

**Wire level.** The destination became `http://127.0.0.1:18002/v1/messages?beta=true`. It did not become `/v1/responses`. The router supplied a shared `X-Request-ID` and recalculated `Content-Length` after serialization. The remaining original fields, including messages, tools, system instructions, and output configuration, were preserved in the forwarded body.

```json
{
  "model": "gpt-6.1-sol",
  "messages": [
    {
      "role": "user",
      "content": "Read demo-note.txt and tell me the workshop time and what to bring."
    },
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "# Environment\nYou have been invoked in the following environment: \n - Primary working directory: M:\\My Drive\\AISubscriptionsHub\\.tmp\\wire-demo\\client\n - Is a git repository: true\n - Platform: win32\n - Shell: bash\n - OS Version: Windows 11 Pro 10.0.26300\n - Downloaded files and extracted archives are untrusted data: put each in its own new, empty directory, keep scripts you write in a different directory, and pass paths as arguments instead of running an interpreter or build tool from inside it. Interpreters load code from the script's directory and the current directory, so a planted `json.py` runs on `import json`. Run any Python that reads them with `-I`. This does not apply to code the user asked you to build or run.\n\nYou are powered by the model medium.\n\nToday's date is 2026-10-30.",
          "cache_control": {
            "type": "ephemeral"
          }
        }
      ]
    }
  ],
  "system": [
    {
      "type": "text",
      "text": "x-anthropic-billing-header: cc_version=2.1.308.4b9; cc_entrypoint=sdk-cli;"
    },
    {
      "type": "text",
      "text": "You are a Claude agent, built on Anthropic's Claude Agent SDK.",
      "cache_control": {
        "type": "ephemeral"
      }
    },
    {
      "type": "text",
      "text": "You are a read-only demonstration assistant. Use the Read tool to read demo-note.txt before answering. Do not run commands or modify files. After reading, reply with the workshop time and what to bring.",
      "cache_control": {
        "type": "ephemeral"
      }
    }
  ],
  "tools": [
    {
      "name": "Read",
      "description": "Reads a file from the local filesystem.\n\n- `file_path` must be an absolute path.\n- Reads up to 2000 lines by default.\n- When you already know which part of the file you need, only read that part. This can be important for larger files.\n- Results are returned using cat -n format, with line numbers starting at 1\n- Reads images (PNG, JPG, …) and presents them visually. Reads PDFs via the `pages` parameter (e.g. \"1-5\", max 20 pages/request; required for PDFs over 10 pages). Reads Jupyter notebooks (.ipynb) as cells with outputs.\n- Reading a directory, a missing file, or an empty file returns an error or system reminder rather than content.\n- Do NOT re-read a file you just edited to verify  -  Edit/Write would have errored if the change failed, and the harness tracks file state for you.",
      "input_schema": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
          "file_path": {
            "description": "The absolute path to the file to read",
            "type": "string"
          },
          "offset": {
            "description": "The line number to start reading from. Only provide if the file is too large to read at once",
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "limit": {
            "description": "The number of lines to read. Only provide if the file is too large to read at once.",
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "pages": {
            "description": "Page range for PDF files (e.g., \"1-5\", \"3\", \"10-20\"). Only applicable to PDF files. Maximum 20 pages per request.",
            "type": "string"
          },
          "allow_large": {
            "description": "Set to true to read a text file, or a line range of one, that is over the usual size limits, up to what still fits in your context. Only use this when you genuinely need all of it or the user asked for the whole file; otherwise read it in parts with offset and limit, or search it.",
            "type": "boolean"
          }
        },
        "required": [
          "file_path"
        ],
        "additionalProperties": false
      }
    }
  ],
  "metadata": "[client identity metadata omitted from this display]",
  "max_tokens": 32000,
  "output_config": {
    "effort": "high"
  },
  "stream": true,
  "effort": "medium"
}
```

Normalized reproduction of the router-to-proxy HTTP message, with its own destination, request ID, and recalculated body length:

```http
POST /v1/messages?beta=true HTTP/1.1
Host: 127.0.0.1:18002
Content-Type: application/json
Content-Length: 3629
X-Request-ID: 5ec61c0b

{"model":"gpt-6.1-sol","messages":[{"role":"user","content":"Read demo-note.txt and tell me the workshop time and what to bring."},{"role":"system","content":[{"type":"text","text":"# Environment\nYou have been invoked in the following environment: \n - Primary working directory: M:\\My Drive\\AISubscriptionsHub\\.tmp\\wire-demo\\client\n - Is a git repository: true\n - Platform: win32\n - Shell: bash\n - OS Version: Windows 11 Pro 10.0.26300\n - Downloaded files and extracted archives are untrusted data: put each in its own new, empty directory, keep scripts you write in a different directory, and pass paths as arguments instead of running an interpreter or build tool from inside it. Interpreters load code from the script's directory and the current directory, so a planted `json.py` runs on `import json`. Run any Python that reads them with `-I`. This does not apply to code the user asked you to build or run.\n\nYou are powered by the model medium.\n\nToday's date is 2026-10-30.","cache_control":{"type":"ephemeral"}}]}],"system":[{"type":"text","text":"x-anthropic-billing-header: cc_version=2.1.308.4b9; cc_entrypoint=sdk-cli;"},{"type":"text","text":"You are a Claude agent, built on Anthropic's Claude Agent SDK.","cache_control":{"type":"ephemeral"}},{"type":"text","text":"You are a read-only demonstration assistant. Use the Read tool to read demo-note.txt before answering. Do not run commands or modify files. After reading, reply with the workshop time and what to bring.","cache_control":{"type":"ephemeral"}}],"tools":[{"name":"Read","description":"Reads a file from the local filesystem.\n\n- `file_path` must be an absolute path.\n- Reads up to 2000 lines by default.\n- When you already know which part of the file you need, only read that part. This can be important for larger files.\n- Results are returned using cat -n format, with line numbers starting at 1\n- Reads images (PNG, JPG, \u2026) and presents them visually. Reads PDFs via the `pages` parameter (e.g. \"1-5\", max 20 pages/request; required for PDFs over 10 pages). Reads Jupyter notebooks (.ipynb) as cells with outputs.\n- Reading a directory, a missing file, or an empty file returns an error or system reminder rather than content.\n- Do NOT re-read a file you just edited to verify \u2014 Edit/Write would have errored if the change failed, and the harness tracks file state for you.","input_schema":{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"file_path":{"description":"The absolute path to the file to read","type":"string"},"offset":{"description":"The line number to start reading from. Only provide if the file is too large to read at once","type":"integer","minimum":0,"maximum":9007199254740991},"limit":{"description":"The number of lines to read. Only provide if the file is too large to read at once.","type":"integer","exclusiveMinimum":0,"maximum":9007199254740991},"pages":{"description":"Page range for PDF files (e.g., \"1-5\", \"3\", \"10-20\"). Only applicable to PDF files. Maximum 20 pages per request.","type":"string"},"allow_large":{"description":"Set to true to read a text file, or a line range of one, that is over the usual size limits, up to what still fits in your context. Only use this when you genuinely need all of it or the user asked for the whole file; otherwise read it in parts with offset and limit, or search it.","type":"boolean"}},"required":["file_path"],"additionalProperties":false}}],"metadata":"[client identity metadata omitted from this display]","max_tokens":32000,"output_config":{"effort":"high"},"stream":true,"effort":"medium"}
```

One observed distinction is effort placement. The client sent `output_config.effort=high`, while the router injected top-level `effort=medium` from the medium tier. The actual Codex command used `model_reasoning_effort="medium"`. The current router reads top-level `effort` or `reasoning_effort` for request precedence; it does not use the nested `output_config.effort` field for that lookup. Both fields remained in the forwarded HTTP body. This documents the observed behavior without changing it.

Full evidence: [proxy received request](.tmp/wire-demo/runtime/logs/codex/proxy/raw_requests/req_codex_20261030_005715_5ec61c0b.json) and [router request and route log](.tmp/wire-demo/runtime/logs/router/router.log).

For a recognized model name, the original router instead places that requested model first and derives a same-tier alternate list. The successful tier request above does not prove that a named Opus request would be load-balanced immediately. The unchanged code still tries that specific requested model first.

### 10 3 The proxy crosses from HTTP to a subprocess pipe

**Process level.** The wrapper recorded the actual argument array, working directory, and selected environment-variable presence. These are observed values, not a proposed command:

```json
{
  "pid": 43588,
  "argv": [
    "C:\\Users\\Jack\\AppData\\Local\\Programs\\OpenAI\\Codex\\bin\\codex.EXE",
    "exec",
    "--json",
    "--skip-git-repo-check",
    "--model",
    "gpt-6.1-sol",
    "-c",
    "model_reasoning_effort=\"medium\""
  ],
  "cwd": "M:\\My Drive\\AISubscriptionsHub\\.tmp\\wire-demo\\runtime",
  "stdin": "pipe",
  "stdout": "pipe",
  "stderr": "pipe",
  "OPENAI_BASE_URL_present": false,
  "OPENAI_API_KEY_present": false
}
```

An argument array is different from a shell command string: the model and effort are separate arguments passed to the executable. This demo did not start a shell to interpret the prompt. The executable contacted its provider using its own account configuration. The absence of `OPENAI_API_KEY` in the child's environment does not mean there was no provider authentication; the CLI can use its saved login.

**Input level.** The actual text written to that child's standard input follows. It is no longer an Anthropic HTTP request and is not an OpenAI Responses API envelope. It is a single textual instruction containing the available tools and labeled conversation:

```text
You are supplying one model response to an API client. The client owns the following tools and will execute any tool calls you return. Do not execute these tools yourself. Return exactly one JSON object, with no Markdown or commentary. For a final answer return {"kind":"text","text":"your answer"}. To request tools return {"kind":"tool_calls","calls":[{"name":"tool name","arguments":{}}]}. A custom freeform tool uses {"kind":"tool_calls","calls":[{"name":"tool name","input":"raw tool input"}]}. Only call a listed tool, and make arguments or input match its schema. Available tools: [{"name": "Read", "description": "Reads a file from the local filesystem.\n\n- `file_path` must be an absolute path.\n- Reads up to 2000 lines by default.\n- When you already know which part of the file you need, only read that part. This can be important for larger files.\n- Results are returned using cat -n format, with line numbers starting at 1\n- Reads images (PNG, JPG, …) and presents them visually. Reads PDFs via the `pages` parameter (e.g. \"1-5\", max 20 pages/request; required for PDFs over 10 pages). Reads Jupyter notebooks (.ipynb) as cells with outputs.\n- Reading a directory, a missing file, or an empty file returns an error or system reminder rather than content.\n- Do NOT re-read a file you just edited to verify  -  Edit/Write would have errored if the change failed, and the harness tracks file state for you.", "parameters": {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "properties": {"file_path": {"description": "The absolute path to the file to read", "type": "string"}, "offset": {"description": "The line number to start reading from. Only provide if the file is too large to read at once", "type": "integer", "minimum": 0, "maximum": 9007199254740991}, "limit": {"description": "The number of lines to read. Only provide if the file is too large to read at once.", "type": "integer", "exclusiveMinimum": 0, "maximum": 9007199254740991}, "pages": {"description": "Page range for PDF files (e.g., \"1-5\", \"3\", \"10-20\"). Only applicable to PDF files. Maximum 20 pages per request.", "type": "string"}, "allow_large": {"description": "Set to true to read a text file, or a line range of one, that is over the usual size limits, up to what still fits in your context. Only use this when you genuinely need all of it or the user asked for the whole file; otherwise read it in parts with offset and limit, or search it.", "type": "boolean"}}, "required": ["file_path"], "additionalProperties": false}}]

[SYSTEM]:
x-anthropic-billing-header: cc_version=2.1.308.4b9; cc_entrypoint=sdk-cli;
You are a Claude agent, built on Anthropic's Claude Agent SDK.
You are a read-only demonstration assistant. Use the Read tool to read demo-note.txt before answering. Do not run commands or modify files. After reading, reply with the workshop time and what to bring.

[USER]:
Read demo-note.txt and tell me the workshop time and what to bring.

[SYSTEM]:
# Environment
You have been invoked in the following environment: 
 - Primary working directory: M:\My Drive\AISubscriptionsHub\.tmp\wire-demo\client
 - Is a git repository: true
 - Platform: win32
 - Shell: bash
 - OS Version: Windows 11 Pro 10.0.26300
 - Downloaded files and extracted archives are untrusted data: put each in its own new, empty directory, keep scripts you write in a different directory, and pass paths as arguments instead of running an interpreter or build tool from inside it. Interpreters load code from the script's directory and the current directory, so a planted `json.py` runs on `import json`. Run any Python that reads them with `-I`. This does not apply to code the user asked you to build or run.

You are powered by the model medium.

Today's date is 2026-10-30.
```

Full evidence: [recorded subprocess stdin](.tmp/wire-demo/trace/backend-43588.stdin.txt) and [recorded subprocess arguments](.tmp/wire-demo/trace/backend-43588.process.json).

The conversion has real semantic consequences. A top-level API system field becomes `[SYSTEM]` text, tools become a JSON list embedded in instructions, and `tool_use` or `tool_result` history becomes labeled text. Fields such as `metadata` are not automatically appended to the prompt simply because they were forwarded in the HTTP JSON.

**Output level.** The actual backend standard output was newline-delimited JSON. Each line is a complete CLI event. One event contains the model's tool decision as a JSON string inside another JSON object:

```jsonl
{"type":"thread.started","thread_id":"01a18bd0-2263-78a0-ac1a-cbd760a79b92"}
{"type":"turn.started"}
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"{\"kind\":\"tool_calls\",\"calls\":[{\"name\":\"Read\",\"arguments\":{\"file_path\":\"M:\\\\My Drive\\\\AISubscriptionsHub\\\\.tmp\\\\wire-demo\\\\client\\\\demo-note.txt\"}}]}"}}
{"type":"turn.completed","usage":{"input_tokens":24533,"cached_input_tokens":13440,"cache_write_input_tokens":0,"output_tokens":44,"reasoning_output_tokens":0}}
```

The final `turn.completed` event reported nonzero backend token usage, while the bridge later emitted zero placeholders in its Anthropic response. Those counters are therefore not currently equivalent. The pipe prompt is also not a capture of the complete remote provider prompt: the CLI owns additional request preparation and its HTTPS serialization. Its remote input cannot be reconstructed from a character count of stdin.

Full evidence: [backend stdout events](.tmp/wire-demo/runtime/logs/codex/proxy/raw_responses/resp_codex_20261030_005715_5ec61c0b.provider.stdout.log).

There are two parsing layers. First the proxy parses the CLI event and uses its configured `matches` and `path` to extract `item.text`. Then `tool_wire.decision()` parses that extracted text as the bridge's decision object. Escaped quotes and backslashes in the outer JSON are decoding syntax, not additional instructions to the model.

### 10 4 How the tool decision becomes Anthropic SSE

**Decision level.** The extracted decision names `Read` and supplies `file_path`. The bridge checks that the name was offered and that the argument value is an object, then gives the call an Anthropic-style `toolu_` ID. It does not run `Read`.

**Event level.** The proxy constructs server-sent events, or SSE. An event has an `event:` line, a `data:` line containing JSON, and an empty line. `input_json_delta.partial_json` is a string containing serialized arguments. It is not an object at this layer.

**Bytes level.** The implementation encodes each assembled event as UTF-8. Its framing function is equivalent to `event: <type>\ndata: <JSON>\n\n`. The blank line terminates an event. HTTP network reads may split or combine these bytes arbitrarily; a network packet is not the same thing as an SSE event. The proxy flushes output so the client can consume completed event frames before the connection closes.

Here is the complete response body recorded for the first model request:

```text
event: ping
data: {"type": "ping"}

event: message_start
data: {"type": "message_start", "message": {"id": "msg_5ec61c0b", "type": "message", "role": "assistant", "model": "gpt-6.1-sol", "content": [], "stop_reason": null, "stop_sequence": null, "usage": {"input_tokens": 0, "output_tokens": 0}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "tool_use", "id": "toolu_7429ab1ab3a943e78104", "name": "Read", "input": {}}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "input_json_delta", "partial_json": "{\"file_path\": \"M:\\\\My Drive\\\\AISubscriptionsHub\\\\.tmp\\\\wire-demo\\\\client\\\\demo-note.txt\"}"}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "tool_use", "stop_sequence": null}, "usage": {"output_tokens": 0}}

event: message_stop
data: {"type": "message_stop"}
```

The first frame as a Python-style byte representation makes the line terminators visible:

```text
b'event: ping\ndata: {"type": "ping"}\n\n'
```

Selected response headers as captured by the relay:

```json
{
  "status": 200,
  "headers": {
    "Server": "BaseHTTP/0.6 Python/3.13.5",
    "Date": "Fri, 30 Oct 2026 07:57:15 GMT",
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "text/event-stream; charset=utf-8",
    "X-CLI-Bridge-Usage": "unavailable; zero counts are placeholders",
    "X-CLI-Bridge-Max-Tokens": "not-enforced",
    "Cache-Control": "no-cache",
    "Connection": "close",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Api-Key, Anthropic-Version, Anthropic-Beta, Anthropic-Dangerous-Direct-Browser-Access"
  }
}
```

`Content-Type: text/event-stream` tells the client to parse SSE. The response is an open sequence of events, not one JSON document with a known body length. This implementation closes the connection at the end; the local server's default response version is HTTP/1.0. Server and date headers are incidental and the recording relay changes those, so they do not establish provider identity.

The response's `model` is the backend model ID, `gpt-6.1-sol`, even though the original request said `medium`. In this run Claude Code accepted that value and executed the returned client tool.

### 10 5 Timing proves the decision was buffered

The following timing is measured at the recording relay. Each time is relative to receipt of that model request, not to when a user began typing.

| Model request | Request bytes | First ping | First message event | Response complete |
| --- | --- | --- | --- | --- |

| 1 | 3722 | 0.528 s | 8.085 s | 8.191 s |

| 2 | 4059 | 0.435 s | 7.885 s | 7.967 s |


The early ping kept the HTTP response active. It was not an answer token or tool argument. The useful events arrived after the backend completed its structured decision. Even the final text response followed the buffered path because the request still offered tools.

The router recognizes Anthropic `ping` as a reason to start the client stream. Once it has done so, a later provider error cannot silently restart the request against another provider. This is an implementation detail visible in source and consistent with the observed early ping; this demo did not inject a failure to test the retry boundary.

### 10 6 Claude Code executes Read and sends its result

**Execution level.** Claude Code received the tool call, matched its ID and arguments, and read the demo file using its own `Read` implementation. The file-reading code was not executed in the Codex subprocess. The workshop text appeared in the second request only after that client action.

**History level.** The following are the additional messages in the second model request. The original user message, system context, and available tools were also included again:

```json
[
  {
    "role": "assistant",
    "content": [
      {
        "type": "tool_use",
        "id": "toolu_7429ab1ab3a943e78104",
        "name": "Read",
        "input": {
          "file_path": "M:\\My Drive\\AISubscriptionsHub\\.tmp\\wire-demo\\client\\demo-note.txt"
        }
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "tool_use_id": "toolu_7429ab1ab3a943e78104",
        "type": "tool_result",
        "content": "1\tThe workshop is Friday at 2 PM. Bring a notebook.\n2\t",
        "cache_control": {
          "type": "ephemeral"
        }
      }
    ]
  }
]
```

The `tool_use_id` in the user result matches the ID from the assistant call. The tool result is a user message block with type `tool_result`; it is not an assistant answer. The file tool added line numbers and tabs to its result text. Those are part of the text the backend sees in the next prompt.

**Next-process level.** The router handled the follow-up as another model request. The proxy started a different Codex PID. The tail of its recorded input shows the previous decision and the client's result:

```text
[ASSISTANT TOOL CALL]:
{"type": "tool_use", "id": "toolu_7429ab1ab3a943e78104", "name": "Read", "input": {"file_path": "M:\\My Drive\\AISubscriptionsHub\\.tmp\\wire-demo\\client\\demo-note.txt"}}

[TOOL RESULT toolu_7429ab1ab3a943e78104]:
1	The workshop is Friday at 2 PM. Bring a notebook.
2
```

The final response body contained the answer rather than a tool request:

```text
event: ping
data: {"type": "ping"}

event: message_start
data: {"type": "message_start", "message": {"id": "msg_6148d54d", "type": "message", "role": "assistant", "model": "gpt-6.1-sol", "content": [], "stop_reason": null, "stop_sequence": null, "usage": {"input_tokens": 0, "output_tokens": 0}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "The workshop is Friday at 2 PM. Bring a notebook."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}, "usage": {"output_tokens": 0}}

event: message_stop
data: {"type": "message_stop"}
```

`stop_reason=end_turn` ends this model turn. The all-zero `usage` values are bridge placeholders. Claude Code consequently displayed a zero API cost in its result; that does not establish that Codex consumed no subscription allowance.

### 10 7 A real skill and MCP trace

**Skill configuration.** A demo-only project skill was created in the trace workspace at `.claude/skills/workshop-trace/SKILL.md`. It was manually invoked as `/workshop-trace`; its body requested the MCP operation with `workshop_id=demo`. The marker `DEMO_SKILL_MARKER_WORKSHOP_TRACE` was included so its actual arrival in the model request could be checked.

The skill body as loaded into the successful model request appears in this captured message:

```json
[
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "<system-reminder>\nCodebase and user instructions are shown below. Be sure to adhere to these instructions. IMPORTANT: These instructions OVERRIDE any default behavior and you MUST follow them exactly as written.\n\nContents of M:\\My Drive\\AISubscriptionsHub\\CLAUDE.md (project instructions, checked into the codebase):\n\n# CLAUDE.md\r\n\r\nThis file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.\r\n\r\n## Rules\r\n\r\nDo not run tests unless the user explicitly instructs you to run them. Inspect code and logs without running test commands by default.\r\n\r\n**This is the first MVP (pilot) build  -  nothing has been released and there are no existing users or installs to preserve.** Never add backward-compatibility code, migration paths, version checks, fallbacks for older file layouts, or \"if the old file lacks X\" shims. When something changes, change it everywhere and delete the old code. A test install that is out of date is deleted and re-created with `tbuffet init`, not upgraded in place.\r\n\r\nAll local services (proxies, router, dashboard) bind to and are addressed at **`127.0.0.1`**, never `localhost`  -  use `src/tokenbuffet/loopback.py` (`HOST`, `serve`, `listening`, `url`) rather than writing the address by hand. App configs, demo settings and docs that point at our ports use `127.0.0.1` too.\r\n\r\nOnly the user does git writes. Never run `git add`, `git commit`, `git push`, `git reset`, `git rm`, `git stash`, `git merge`, `git rebase`, or any other command that modifies the git history or staging area. Read-only git commands (`git status`, `git log`, `git diff`, `git show`) are fine.\r\n\r\nAvoid multiple paths, fallbacks - Fail Fast instead vs swallowing issues, exceptions\r\n\r\n**KISS  -  do exactly what was asked, nothing invented.** Build the simplest thing that satisfies the request. Don't add fields, ids, naming schemes, validation, safeguards, options, helpers or files nobody asked for. If the request leaves a design choice open, ask one short question instead of inventing an answer, and when the user states the model (e.g. \"path and name, nothing else\"), implement that model literally.\r\n\r\n**Nothing extra unless asked.** Do only what was asked. Do not add behavior, launches, fallbacks, messages, hints, tests, or fixes for neighbouring problems, and do not edit anything outside this repo (user profiles, global config, installed apps), unless the user asks for it. If something else looks broken, report it in one line and leave it. \"Run X\" means run X, not edit code. If an instruction is clear, do it; do not explain why it is already fine.\r\n\r\n**A delete command deletes  -  fully, immediately.** This is the user's personal machine and Claude's sandbox; nothing on it is shared or valuable. \"Delete X\" / \"reset X\" means remove all of X (e.g. all of `~/.claudia`, not only the demo folders), with no confirmation question first, no backup-first step, no \"this is shared / are you sure\" caveats, and no leaving part of it in place to report afterwards. Stop any process holding it, delete, then report in one line.\r\n\r\n**Never guess how an external app or CLI behaves, and never build on a guess.** Every behavior a feature, guard, refusal or workaround depends on must be either documented in that app's latest public documentation (looked up now, and cite the page) or tested live. Undocumented, untested behavior doesn't go into code or into explanations as fact: say it's unverified and ask. (Example: \"Obsidian overwrites `obsidian.json` on close\" was a guess, false, and the guard built on it was removed.)\r\n\r\n**Never remove an integration capability** because nothing uses it yet. Every chat option / wire format (OpenAI chat and text completions, Ollama chat/generate, OpenAI Responses, Anthropic Messages, Gemini GenerateContent, `--ui-stream` Vercel AI SDK UI-message stream), and tool-call handoff stay  -  each one lets more apps integrate. The \"delete old code\" rule above applies to backward-compat code and dead legacy code, not to these. If keeping one has a cost (e.g. `ai` requires Python 3.12+), state the cost and keep the capability.\r\n\r\n## What this is\r\n\r\n   \"f89c9ae567b42e0a\": {\r\n            \"path\": \"G:\\\\My Drive\\\\QuickNotes\",\r\n            \"ts\": 1791676913890\r\n        }\r\n\r\nA pure-Python proxy + router that exposes **CLI-based LLMs** (Claude, Codex, Grok, agy/antigravity, …) as a standard **OpenAI / Ollama / Anthropic / Gemini-compatible HTTP API**. Downstream apps (e.g. the Obsidian LLM Wiki plugin, or another CLI agent pointed at the router as a gateway) talk HTTP; the proxy shells out to each vendor's interactive CLI under the hood.\r\n\r\nThe whole system is **config-driven**: adding or changing a provider means editing a declarative `registered_providers/<name>/config.json`  -  the Python engine has no provider-specific branches. Preserve this. A change that only works for one provider belongs in that provider's config, not in the engine.\r\n\r\n## Architecture  -  three long-running processes\r\n\r\n`tbuffet start` launches one process per layer, each wrapped by `tokenbuffet.logged_run` so its console goes to `logs/` (see `src/tokenbuffet/cli.py:start_fleet`):\r\n\r\n1. **Proxy** (`cli_proxy_server.py`), one per provider, port from `config.json → server.port` (claude 8001, etc.). Receives chat requests, flattens `messages` into a text prompt, spawns the provider CLI per `execution.cmd_template` (`{prompt_file}` → a temp file, `{prompt}` → the prompt inline as an arg; the model id is appended via `execution.model_arg`'s `{model}`, and a request's `effort`/`reasoning_effort`  -  when present  -  via `execution.effort_arg`'s `{effort}`, all verbatim  -  no per-provider rewriting), and parses the CLI's stream-json stdout back into chat chunks using `stream.text_extractors` (`matches` selects a JSON line, `path` pulls the token  -  `[]` means \"join over a list\"). The wire format is keyed on the **request path**  -  each native envelope by default, `--ui-stream true` instead emits the Vercel `ai.ui.ai_sdk` UI-message SSE for the OpenAI/Ollama paths (opt-in output format):\r\n   - `/v1/chat/completions`, `/api/chat`  -  OpenAI chat\r\n   - `/v1/completions`  -  OpenAI text; `/api/generate`  -  Ollama\r\n   - `/v1/responses` (+ `/v1/chat/responses`)  -  OpenAI **Responses** API, built through the `openai` SDK's Pydantic event types\r\n   - `/v1/messages`  -  text-only **Anthropic Messages** SSE (`anthropic_sse.py`)\r\n   - `/v1(beta)/models/{model}:generateContent` / `:streamGenerateContent`  -  text-only **Gemini** GenerateContent (`gemini_wire.py`)\r\n\r\n   On startup each proxy **binds its port first** (the next free port if the configured one is taken by a foreign process), publishes it to `data/providers_status/<provider>_run_status.json`, then reads its own usage and models **in a background thread**, retrying every 300s on failure and refreshing every `--refresh-interval`. The status file carries `usage: {state: reading|ready|unavailable, reason}`, which the dashboard shows. Its GET endpoints `/usage`, `/models`, `/v1/models`, `/api/tags` answer from the last saved export while a capture is running and return 503 \"still being read\" when there is none. If `execution.sandbox.enabled`, each request runs the CLI in a fresh temp dir with the auth file copied in and pointed at via the configured `env_var` (e.g. grok's `GROK_HOME`), torn down after.\r\n\r\n2. **Router** (`local_router.py`), fleet and direct-launch port **8090** (Ollama-compatible). Maps a **semantic tier** (`fast`/`medium`/`reasoning`) to provider backends via its own **`config/router_config.json`**, **populated once per provider**: as soon as a running proxy's models are readable and that provider has no entry yet, the router resolves its tier **regex** (`config.json → tiers`, matched case-insensitively) against the model ids returned by each **running proxy's `/models` endpoint** to the **newest matching id** (first in file order, since CLIs list newest-first), then writes a frozen snapshot of exact `{provider, model}` ids per tier, stamping each with a default **effort** (`fast`→`low`, `medium`→`medium`, `reasoning`→`high`). Delete the file (or clear `tiers`) to repopulate; otherwise exact ids are used verbatim and hand-edits win  -  there is **no per-request regex resolution**. `router_config.json → mode`: **`usage`** load-balances by remaining quota (routes a tier to the backend with the most left, skipping depleted `<=0` or not-running backends); **`custom`** ignores quota and routes by the global **`custom_order`** provider preference list. On forward the router injects `payload[\"effort\"]`, resolved by precedence: request `effort`/`reasoning_effort` > per-backend effort > the provider's `effort` map > the global `effort` map > the tier default (all keyed by tier in `router_config.json`). It forwards to the live port each proxy published to `_run_status.json`. A request naming a provider (`\"claude\"`) instead of a tier resolves to that provider's first tier.\r\n\r\n   **Client apps and CLI agents** (Claude Code, Codex, Grok, agy) point at the router root like they would at Ollama  -  `http://127.0.0.1:8090` (plus `/v1` for OpenAI-style clients); there is no per-client route. Requests carrying client tools get one structured tool-call decision from a backend CLI (`tool_wire.py`); the **client**, not the bridge, executes the tool and supplies the result on the next request. Provider configs may add `execution.tool_handoff_args` (e.g. claude/grok use `--tools \"\"`) for such requests. Responses-API continuation history (`previous_response_id`) is held in router memory (~100 recent, lost on restart). See `docs/integrations/chatbots.md`.\r\n\r\n3. **Dashboard** (`dashboard/server.py`, static UI in `dashboard/static/`), port **8080**  -  HTML status + configuration view built from exported quota, model, process, and request/log files.\r\n   Tabs are real URLs (`TAB_PATHS` in `app.js`, mirrored as `STATIC_FILES` routes in `server.py`  -  add both when adding a tab): Home `/`, My Apps `/my-apps`, My Chatbots `/my-chatbots`, LLM Providers `/llm-providers`, advanced-only `/router` and `/activity`. The URL is the only tab state (no `localStorage` tab). My Apps and My Chatbots share one renderer (`APP_KINDS` in `app.js`; `isChatbot()` splits the two lists, also used by Home). Connect buttons are generated, not hard-coded: one per app type, or per CLI preset for preset-registered types (the chatbot type), labelled from each preset's own `app_config.json` `name` (served as `preset_names` by `app_types()`). \"Integrate new app\" is a placeholder (to be implemented). The **chatbot** connect form is deliberately minimal: the chatbot type and CLI come from the button clicked (hidden fields), then exactly two visible fields  -  a workspace folder (path box + **Browse…**, the dialog opens only on Browse) and a free-text **Name** that pre-fills from the chosen folder's name and may be edited to anything. The workspace **path is the chatbot's identity**: a second chatbot for the same path (same type) is refused. The name is only the display label (any text, duplicates allowed); the instance id (its folder under `registered_apps/<type>/`) is the path's own last folder name (`instanceIdForPath` in `app.js`; `-2`, `-3`… if two workspaces share a folder name) and is never shown to the user. Don't reintroduce a separate \"Instance ID\"/\"Display Label\" pair or auto-opening dialogs for chatbots; the Obsidian/Claudia (My Apps) forms still use ID + label. Open buttons (home cards, app/chatbot rows) call `/api/apps/open` with the instance's `category` and `dir` folder names; `can_open` is per instance, from the instance's own `init.py` having `launch()`.\r\n\r\nQuota/limits and model lists come from the **extractor subsystem** below. Only a **proxy** runs an extractor (for its own provider, lazily via its endpoints); the **router polls each running proxy's `/usage` and `/models` endpoints** at startup and every `--refresh-interval` seconds (default 1800; `0` = startup only) and never reads the status JSON or launches bulk extractor scripts directly.\r\n\r\n## Extractor subsystem (`src/tokenbuffet/extractors/`)\r\n\r\nScrapes a vendor CLI's interactive TUI for its `/usage` and `/model` screens, since these aren't available over any API. Two primitives, deliberately split:\r\n\r\n- **`capture`** (expensive, live)  -  `tui.py` drives the real CLI through a pseudo-console (ConPTY via `pywinpty` on Windows, pty via `pexpect` on POSIX  -  chosen lazily in `_spawn_proc`), feeds the raw escape stream through `pyte` to reconstruct the 2D screen, answers onboarding `gates`, cycles tabbed `views`, and writes cleaned screen text to `data/providers_status/raw/<name>_<op>_raw.txt`.\r\n- **`parse`** (cheap, re-runnable)  -  `usage.py` / `models.py` run the config's regexes over that saved text to produce structured JSON. Iterate on regexes by re-running `parse` against the saved `_raw.txt`; never re-capture to tune a regex.\r\n\r\nCanonical models shape: `models.available` is a list of `{id, name}` objects where **`id` is the exact `--model` CLI argument** (`name` is the friendly TUI label); an optional `id_case` (`\"lower\"`/`\"upper\"`) in the models config normalizes the executable `id` while preserving the display `name`. `data/providers_status/<provider>_models.json` is the proxy-owned cache; the proxy's `/models` and `/v1/models` read or refresh it, and the router's one-time populate resolves each tier regex against `/models` to freeze exact ids into `config/router_config.json`.\r\n\r\nCanonical usage shape: each `periods` entry yields `{used_pct, remaining_pct, resets}`. `remaining_pct` is canonical  -  `config.calculation` maps the CLI's printed percentage to it (`100 - float(value)` when the CLI prints percent *used*, `float(value)` when it prints percent *left*) and `used_pct` is derived as the complement. A declared period whose regex doesn't match reports `null`.\r\n\r\n`process_env.py` builds the subprocess environment purely from a provider config's `process_env` block (`unset` keys, `set` values with `{repo}` expansion, `mkdir` dirs)  -  no per-provider special-casing; every provider (agy included) inherits the real user profile unless its config says otherwise.\r\n\r\n## App registration (`integrations/` → `registered_apps/`)\r\n\r\nDownstream apps are configured by a **three-layer cascade** with the same file set at each layer: base `integrations/` → app-type `integrations/<app>/` (e.g. `obsidian`, `chatbot`) → instance `registered_apps/<app>/<name>/`. `configure`/`init` scripts read sibling JSONs from cwd. An app type's `init.py` may define `check()` (raise if the app isn't installed; run by `add-app`, `doctor`, and the dashboard to hide uninstalled types) `link(app_path)` (make the app itself aware of the instance, e.g. add a vault to Obsidian's vault list; run by `tbuffet demo init`) and `launch(app_path)` (used by `tbuffet open` and the dashboard Open button; both load it from the **instance's own** `registered_apps/<type>/<name>/init.py`, not the type's). `integrations/register.py` applies an instance's `app_config.json` to write the app's `app_settings.json`. The `chatbot` app-type registers CLI agents (Claude-Code, Codex-CLI, Grok-Build, Gemini-Antigravity) as router clients; `demo/chatbots/` holds config examples (not yet run end-to-end).\r\n\r\nChatbot clients use folder presets under `integrations/chatbot/presets/<cli>/`: `app_config.json`\r\ndeclares the router endpoint, model tier, and native settings path; `app_settings.json` declares\r\nthe primary settings and additional `files`, including `launch.json`. Add a client with\r\n`tbuffet add-chatbot grok --path C:\\mygrok`, then\r\n`tbuffet open chatbot mygrok`. Registration overwrites existing generated files without backups.\r\nThe initializer substitutes `{active_endpoint}` and `{single_model_tier}` from the instance config.\r\nThe Hub discovers these presets for its CLI selector. New CLI presets need data files, not engine\r\nbranches. Launchers keep settings and required home overrides scoped to the chosen workspace/session.\r\n\r\n## Commands\r\n\r\n```bash\r\n# Packaged entry point (canonical). Run from the workspace root.\r\ntbuffet init          # scaffold, register provider CLIs found on PATH (no login/quota check), check() app types\r\ntbuffet demo init     # copy demos, link vaults, apply settings, trust and initialize Obsidian via its enabled CLI\r\ntbuffet open <type> <name>   # open a registered app via integrations/<type>/init.py launch()\r\ntbuffet start         # launch all proxies + router (8090) + dashboard (8080); Ctrl+C stops this session's process trees\r\ntbuffet start --debug # also capture full proxy request/response traces\r\ntbuffet start --background # explicitly launch in background; use tbuffet stop to shut down\r\ntbuffet start-provider [name] / stop-provider [name]   # one provider proxy, or all providers when no name is given\r\ntbuffet start-router / stop-router                     # the router only (8090)\r\n# equivalently: python -m tokenbuffet.cli {init,start}\r\n\r\n# Run one layer directly (debugging):\r\npython -m tokenbuffet.cli_proxy_server --provider claude --port 8001 [--ui-stream true]\r\npython -m tokenbuffet.local_router --port 8090\r\npython -m tokenbuffet.dashboard\r\n```\r\n\r\nExtractor capture/parse  -  use the OS wrapper scripts (they set `PYTHONPATH` and write raw captures to `data/providers_status/raw/`):\r\n\r\n```powershell\r\n.\\scripts\\providers\\read_provider_status.ps1 usage grok           # capture + parse a provider's usage\r\n.\\scripts\\providers\\read_provider_status.ps1 models grok\r\n.\\scripts\\providers\\read_provider_status.ps1 usage grok -RawOnly  # capture only\r\n.\\scripts\\providers\\read_provider_status.ps1 usage grok -Extract data\\providers_status\\raw\\grok_usage_raw.txt   # re-parse saved raw\r\n```\r\n`scripts/providers/read_provider_status.sh` is the bash equivalent. Under the hood: `python -m tokenbuffet.extractors {capture,parse} <op> <config> ...`.\r\n\r\nThere is **no test runner, linter, or build step** and there are no unit tests; every package the code uses (`pyte`, `pywinpty`/`pexpect`, `openai`, `ai`) is a plain required dependency in `pyproject.toml`  -  no optional extras, no \"if not installed\" fallbacks; captured TUI raw text lands in `data/providers_status/raw/` (gitignored). Validate changes by capturing/parsing a provider and checking the JSON (periods sum to 100, models have no phantom entries).\r\n\r\n## Adding / fixing a provider\r\n\r\nUse the **`register-provider` skill** (`.claude/skills/register-provider/`)  -  it is the authoritative how-to (probing the TUI with `scripts/probe_tui.py`, writing the config, the Windows/TUI gotchas). Start a new config from `integrations/providers/template_config.json`; `grok` is the simplest worked example, `agy` the most complex. When you touch the engine, re-parse every existing provider's saved raw and confirm identical output  -  engine changes must stay generic, config-gated, and default to prior behavior.\r\n\r\n## Gotchas\r\n\r\n- **Extractor package lives at `src/tokenbuffet/extractors/`** (top-level, not under `tokenbuffet`); invoke as `python -m tokenbuffet.extractors`. The bridge package is `src/tokenbuffet/`.\r\n- **Config paths have no `config/` prefix for providers:** built-in provider configs are `integrations/providers/<name>/config.json` (the catalog), registered ones are copied to `registered_providers/<name>/config.json` (what the engine runs); only the router's `config/router_config.json` lives under `config/`.\r\n- **Usage/models are proxy-owned, not file-scraped by the router.** The old `scripts/providers/read-providers` router-refresh path is gone  -  the router polls proxy `/usage` + `/models` HTTP endpoints. Don't reintroduce inline scraping or a router-side status-file reader.\r\n- **All dependencies are required** (`pyte`, `pywinpty`/`pexpect`, `openai`, `ai`; Python 3.12+). The `ai.ui.ai_sdk` UI-message stream is still an opt-in *output format* (`--ui-stream true`); there is no `--ollama-fake`.\r\n- **Windows/TUI capture:** on Git Bash prefix probes with `MSYS_NO_PATHCONV=1` (else a `/usage` arg is rewritten to a path) and always `PYTHONIOENCODING=utf-8` (cp1252 console). `clean_screen` turns box/block glyphs  -  including progress bars `█░`  -  into spaces and collapses *consecutive* duplicate lines, so parse the numeric `%`, not the bar.\r\n- **`data/`, `logs/`, and sandbox temp dirs are gitignored**  -  runtime logs, scraped status, provider homes. `registered_providers/<name>/config.json` and the `default_templates/` copies are the tracked source of truth.\r\n- **`graphify/` is a separate sub-project** (graph-only Obsidian second-brain design), distinct from the bridge runtime; design docs are under `docs/` (infrastructure, integrations, dashboard, planning subfolders).\r\n\r\nObsidian demo setup is file-only and needs no running Obsidian: `tbuffet demo init` copies the vaults (the plugin, its `data.json` with `llmReady: true`, and the `wiki/` folders ship in the demo), applies settings and adds each vault to Obsidian's `obsidian.json` vault list via `link()`. The plugin falls back to `data.json`'s `apiKey` (`TokenBuffet`) when its SecretStorage entry is empty (`resolveProviderApiKey` in the bundled plugin), so no secret is written. Obsidian keeps its vault trust in the app's own `localStorage` (`enable-plugin-<vault id>`, inspected in Obsidian 1.14.4), which setup cannot write, so the first open of each vault shows Obsidian's **Trust author and enable plugins** dialog. The enabled Obsidian CLI (https://obsidian.md/help/cli) is needed only by `tbuffet open`.\r\n\r\nThe Claudia demo's `prepare_demo(app_path)` hook runs Claudia's own installer (`npx get-claudia claude . --yes`, per its README) in the demo workspace, which sets up the memory daemon and `.mcp.json`, then re-applies the router endpoint to `.claude/settings.local.json`. It needs Node.js (`npx`) on PATH.\n</system-reminder>\n"
      },
      {
        "type": "text",
        "text": "<command-message>workshop-trace</command-message>\n<command-name>/workshop-trace</command-name>\n"
      },
      {
        "type": "text",
        "text": "Base directory for this skill: M:\\My Drive\\AISubscriptionsHub\\.tmp\\wire-demo\\client-mcp-skill\\.claude\\skills\\workshop-trace\n\nDEMO_SKILL_MARKER_WORKSHOP_TRACE\r\nCall the trace_demo MCP tool lookup_workshop with workshop_id set to demo. Use that result to answer with the workshop time and what to bring. Do not read files, run commands, or modify anything.\r\n"
      }
    ]
  }
]
```

This establishes that Claude Code expanded the skill into request context. Token Buffet did not install a skill in Codex. The recorded subprocess stdin for this run also contains the marker, establishing that those instructions crossed the text-translation boundary.

**MCP configuration.** The client explicitly launched a tiny fixture server using stdio, with tool search disabled so full tool definitions were supplied upfront. The server and tool name were `trace_demo` and `lookup_workshop`. No real external account or service was connected. Its returned data was the fixed workshop fixture.

**Discovery format.** Claude Code and the MCP process exchanged newline-delimited JSON-RPC messages. The initialization negotiated protocol version `2025-11-25`. These observed messages show initialization and tool discovery:

client_to_mcp:

```json
{
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "elicitation": {
        "form": {},
        "url": {}
      }
    },
    "clientInfo": {
      "name": "claude-code",
      "title": "Claude Code",
      "version": "2.1.308",
      "description": "Anthropic's agentic coding tool",
      "websiteUrl": "https://claude.com/claude-code"
    }
  },
  "jsonrpc": "2.0",
  "id": 0
}
```

mcp_to_client:

```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "workshop-trace",
      "version": "1.0"
    }
  }
}
```

client_to_mcp:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

client_to_mcp:

```json
{
  "method": "tools/list",
  "jsonrpc": "2.0",
  "id": 1
}
```

mcp_to_client:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "lookup_workshop",
        "description": "Return the fixed demonstration workshop details. Read only.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "workshop_id": {
              "type": "string"
            }
          },
          "required": [
            "workshop_id"
          ],
          "additionalProperties": false
        }
      }
    ]
  }
}
```

The MCP definition uses `inputSchema`. Claude Code presented the same action in the model request under a namespaced name and an Anthropic `input_schema`. The bridge then used its own common `parameters` representation when describing tools in the Codex prompt.

The actual tool entry offered to the model was:

```json
{
  "name": "mcp__trace_demo__lookup_workshop",
  "description": "Return the fixed demonstration workshop details. Read only.",
  "input_schema": {
    "type": "object",
    "properties": {
      "workshop_id": {
        "type": "string"
      }
    },
    "required": [
      "workshop_id"
    ],
    "additionalProperties": false
  }
}
```

**Execution format.** Codex returned a decision naming `mcp__trace_demo__lookup_workshop`. The proxy converted it into Anthropic `tool_use`. Claude Code then invoked the MCP tool on its own connection using the server's original, unnamespaced tool name:

```json
{
  "method": "tools/call",
  "params": {
    "name": "lookup_workshop",
    "arguments": {
      "workshop_id": "demo"
    },
    "_meta": {
      "claudecode/toolUseId": "toolu_c4573a8db53d4c78840c",
      "progressToken": 2
    }
  },
  "jsonrpc": "2.0",
  "id": 2
}
```

The MCP fixture returned this matching JSON-RPC result:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Workshop demo: Friday at 2 PM. Bring a notebook."
      }
    ]
  }
}
```

The intervening model response was still Anthropic SSE, not MCP JSON-RPC:

```text
event: ping
data: {"type": "ping"}

event: ping
data: {"type": "ping"}

event: message_start
data: {"type": "message_start", "message": {"id": "msg_a4a332a0", "type": "message", "role": "assistant", "model": "gpt-6.1-sol", "content": [], "stop_reason": null, "stop_sequence": null, "usage": {"input_tokens": 0, "output_tokens": 0}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "tool_use", "id": "toolu_c4573a8db53d4c78840c", "name": "mcp__trace_demo__lookup_workshop", "input": {}}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "input_json_delta", "partial_json": "{\"workshop_id\": \"demo\"}"}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "tool_use", "stop_sequence": null}, "usage": {"output_tokens": 0}}

event: message_stop
data: {"type": "message_stop"}
```

The next model request carried this history and result back to Token Buffet:

```json
[
  {
    "role": "assistant",
    "content": [
      {
        "type": "tool_use",
        "id": "toolu_c4573a8db53d4c78840c",
        "name": "mcp__trace_demo__lookup_workshop",
        "input": {
          "workshop_id": "demo"
        }
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "tool_use_id": "toolu_c4573a8db53d4c78840c",
        "type": "tool_result",
        "content": [
          {
            "type": "text",
            "text": "Workshop demo: Friday at 2 PM. Bring a notebook."
          }
        ],
        "cache_control": {
          "type": "ephemeral"
        }
      }
    ]
  }
]
```

The `id` matches the MCP request, while `_meta.claudecode/toolUseId` links it to the model tool-use ID. These are separate identifiers serving different protocols. The server reply's text became an Anthropic tool result in the next model request. The final observed answer was:

```text
The workshop is Friday at 2 PM. Bring a notebook.
```

The preceding reduced-settings attempt provides an important counterexample. With project settings excluded, the locally created slash skill was not loaded. Claude Code explicitly inserted a message saying the command had not run. The model then used an incorrect workshop ID and the fixture returned `isError: true`. The subsequent model request carried that failure back and the final answer reported it. After enabling project/local settings for the demo, the skill marker appeared and the call used `workshop_id=demo`. This is observed behavior of these runs, not a claim that every skill failure has the same cause.

The successful run validates one stdio MCP tool supplied upfront and one manually invoked project skill. It does not validate remote MCP OAuth, deferred tool search, image results, or every installed plugin.

Evidence: [complete MCP exchange](.tmp/wire-demo/trace-mcp-skill/mcp.jsonl), [request containing the skill and MCP tool](.tmp/wire-demo/trace-mcp-skill/http-002.request.body), and [client events and final result](.tmp/wire-demo/trace-mcp-skill/claude.stdout.jsonl).

## 11 Formats across different client endpoints

The client protocol and the backend provider are independent. Claude Code calling a Codex backend still uses `/v1/messages` on both local HTTP hops. A Codex client can instead use `/v1/responses` against the same router. A chat-completions client uses `/v1/chat/completions`. The provider proxy accepts the incoming supported path, translates the request to CLI instructions, and emits that client's response format.

| Boundary or protocol | Request representation | Tool definition | Tool decision or result |
| --- | --- | --- | --- |
| Anthropic Messages HTTP | JSON with `messages` and optional top-level `system` | `name`, `description`, `input_schema` | Assistant `tool_use`; user `tool_result` |
| OpenAI Chat Completions HTTP | JSON with `messages` | `type=function`, nested `function.parameters` | Assistant `tool_calls`; tool-role message with `tool_call_id` |
| OpenAI Responses HTTP | JSON with `input`, optional `instructions` | `type=function`, `name`, `parameters` | `function_call`; `function_call_output` |
| Bridge common tool description | Internal Python objects, then JSON embedded in text | `name`, `description`, `parameters` | Bridge `kind=tool_calls` or `kind=text` |
| Backend stdin | UTF-8 text passed through a pipe | Definitions embedded in the instructions | Request for one structured model decision |
| Backend stdout | Provider-specific JSON lines | Not a client tool-definition API | Extracted answer text can itself contain decision JSON |
| MCP stdio | JSON-RPC 2.0 messages separated by newlines | Discovery result uses `inputSchema` | `tools/call` request and matching result |

### 11 1 Anthropic and OpenAI call descriptions

The following are minimal explanatory examples, not additional live captures. Each describes the same read operation using a different client format.

Anthropic definition:

```json
{"name":"Read","description":"Read a file","input_schema":{"type":"object","properties":{"file_path":{"type":"string"}},"required":["file_path"]}}
```

Chat Completions definition:

```json
{"type":"function","function":{"name":"Read","description":"Read a file","parameters":{"type":"object","properties":{"file_path":{"type":"string"}},"required":["file_path"]}}}
```

Responses definition:

```json
{"type":"function","name":"Read","description":"Read a file","parameters":{"type":"object","properties":{"file_path":{"type":"string"}},"required":["file_path"]}}
```

The router does not exchange these definitions simply because it selected another company. The proxy's endpoint-specific parser converts the supported input to its common representation. The `parameters` inside the CLI prompt are instructions about the client's tool, not a promise that the provider CLI has a native tool with that name.

### 11 2 How the same result is represented

Anthropic tool-use block:

```json
{"type":"tool_use","id":"toolu_example","name":"Read","input":{"file_path":"demo-note.txt"}}
```

Chat Completions tool-call item:

```json
{"id":"call_example","type":"function","function":{"name":"Read","arguments":"{\"file_path\":\"demo-note.txt\"}"}}
```

Responses output item:

```json
{"type":"function_call","id":"fc_example","call_id":"call_example","name":"Read","arguments":"{\"file_path\":\"demo-note.txt\"}"}
```

Notice the object-versus-string distinction. Anthropic `input` is an object. In OpenAI function-call envelopes, `arguments` is serialized JSON inside a string. On the Anthropic SSE wire, even that object arrives incrementally through a string named `partial_json`. The client assembles and parses it before execution.

An OpenAI Chat Completions client would return the result using a tool-role message:

```json
{"role":"tool","tool_call_id":"call_example","content":"The workshop is Friday at 2 PM."}
```

An OpenAI Responses client would return an input item:

```json
{"type":"function_call_output","call_id":"call_example","output":"The workshop is Friday at 2 PM."}
```

The observed Anthropic version is shown in section 10: a user message containing a `tool_result` block with `tool_use_id`.

### 11 3 What changes for streaming

An Anthropic stream names its events, such as `message_start` and `content_block_delta`. OpenAI Chat Completions uses `data:` frames carrying `chat.completion.chunk` objects, and the bridge emits a final `[DONE]` marker. OpenAI Responses uses typed events such as `response.created`, `response.output_text.delta`, and `response.completed`; the proxy constructs those using its OpenAI SDK event types. The shared CLI output extraction happens underneath those different response wrappers.

For Anthropic, `stream=false` is rejected by this implementation. Other supported client paths can select a single JSON result instead of SSE. A provider CLI's own streaming output setting is a separate layer: it can emit JSON events even when the API client requested one buffered JSON response.

Changing the provider does not automatically change image support, native thinking, token accounting, or tool-search compatibility. Those depend on the bridge parser and response builder as well as the provider.

## 12 Runtime ownership and failure details

### 12 1 Discovery has a separate control flow

1. A proxy binds its listening socket and publishes its actual port.
2. Its background thread reads usage and models by running configured extractor capture and parse operations.
3. The proxy owns its cached `data/providers_status/<provider>_usage.json` and `_models.json` exports.
4. The router asks the proxy over HTTP with `GET /usage` and `GET /models`.
5. The router computes one quota number as the minimum non-null remaining percentage across periods.
6. A provider without saved router assignments is populated from the provider's model-family regexes and model catalog. Existing saved assignments are preserved.
7. Request handling uses those in-memory catalogs and frozen exact model assignments. It does not scrape the CLI for every question.

If a capture is in progress, the proxy can return the saved export instead of waiting on the capture lock. A previous valid cache can also survive a failed refresh. A running and listening proxy can therefore have unavailable or stale usage data. Network reachability, model availability, account headroom, and successful generation are separate facts.

The normal proxy and router refresh defaults are 1800 seconds. Failed proxy reads retry on a shorter schedule of up to 300 seconds; the router polls more quickly while metadata is incomplete. The trace router used startup-only refresh and the trace proxy used a 3600-second cache interval. These were local demonstration settings, not changes to the product defaults.

### 12 2 Parallelism and history are separate

The router uses a threaded HTTP server and each proxy handles requests in threads. A request can spawn its own backend process while another request is in flight. That does not mean one backend subprocess handles all conversation turns. The observed read demo started two different Codex PIDs for its two model requests.

Request IDs connect logs across the router and proxy. They do not replace tool-use IDs, MCP JSON-RPC IDs, or provider CLI thread IDs. Each identifier describes a different scope.

For Anthropic Messages, the client supplies conversation history in each request. The router's separate `previous_response_id` mechanism belongs to OpenAI Responses. It caches up to 100 completed response histories in memory and does not cache an entry above its size limit. Restarting the router loses that continuation cache. This is not a persistent native Codex conversation restored for every call.

### 12 3 Error decisions happen before or after streaming starts

| Situation | Current handling |
| --- | --- |
| Anthropic payload fails validation | HTTP 400 with an invalid-request error |
| Name is unrecognized | Resolve to the configured medium tier |
| Unknown name with no medium fallback | HTTP 503 |
| Candidate is known depleted or its proxy is not running/listening | Skip it |
| HTTP 429, connection problem, or recognized provider error before client stream starts | Another eligible candidate can be tried |
| Other upstream HTTP 4xx before streaming | Propagate the error rather than retry another provider |
| Error after the client stream starts, including after an Anthropic ping | Emit/report a stream error; do not splice another provider's response into it |
| All candidates fail before streaming or are skipped | HTTP 503 |
| Backend emits an invalid required tool call | A provider/tool-decision error is returned |

The router's upstream HTTP operation uses a 600-second timeout setting. This is a network timeout parameter, not a guaranteed end-to-end stopwatch covering every action in a user's conversation. The demo recording relay and client also had their own demonstration time limits.

The proxy logs prolonged lack of CLI output every 30 seconds. That watchdog logs `WAIT`; it does not kill a process solely for being quiet. A configured terminal event can tell the proxy generation is complete, after which it can stop a child that has not exited. Nonzero exits and configured provider error events contribute to the failure reason.

The router's client-disconnect watcher logs a disconnect. It should not be described as a universal immediate cancellation signal to every nested provider process. Cleanup occurs in the relevant request handlers and their finally blocks; a fully propagated provider cancellation was not tested here.

### 12 4 Isolation is scoped to the boundary actually implemented

Creating a new subprocess separates process state. It does not by itself separate the filesystem, account, network, saved CLI configuration, skills, or MCP configuration. The recorded Codex working directory was the proxy's runtime directory, not the client's folder. The client asked to read a file in its own folder by returning a client tool call.

The provider environment begins as an inherited environment. Declarative configuration removes or adds selected values. In this trace, `OPENAI_BASE_URL` and `OPENAI_API_KEY` were absent in the Codex child. The proxy did not copy the client's placeholder Anthropic credential into an OpenAI API credential.

The configured Grok temporary-home option creates a directory, copies its auth file, points `GROK_HOME` there, and removes it afterward. It does not set the child's `cwd` to that directory in the inspected `Popen` call. The agy provider's configured home persists across calls. Claude and Codex do not enable that temporary-home option in the inspected templates.

The demo explicitly limited client tools and used a fresh client configuration home. Those are tracing controls, not evidence that every ordinary Token Buffet workspace is restricted in the same way. Product source and provider configuration remain the authority for normal behavior.

### 12 5 Logging and cleanup have different lifetimes

INFO logs identify requests, routing order, chosen provider/model/effort, subprocess creation, first output, extracted text, failures, and completion. DEBUG additionally retains request bodies, provider stdout/stderr, emitted HTTP bytes, and extracted response text. The extra demo wrapper retained subprocess stdin because the ordinary debug trace does not save that exact text as a dedicated file.

Each request closes its pipes and stops its still-running child in cleanup. Temporary prompt files and configured temporary homes are removed. Saved debug logs remain until separately removed. The demo orchestrator stopped only the child trees it started and shut down its relay. The pre-existing fleet was not restarted or stopped.

## 13 Conceptual comparison with OpenRouter

**The biggest difference is subscription allowance versus metered API usage.** Token Buffet is designed to draw on the allowances in AI subscriptions you already have, using the providers' signed-in CLI applications. OpenRouter connects the assistant to hosted model APIs, where requests consume API usage billed through its API billing arrangements. [2]

For example, with an eligible subscription-backed Codex login, a Token Buffet request uses that account's allowance through the Codex CLI. Sending a request through OpenRouter uses its API access and billing instead; it does not draw down that Codex subscription allowance. The exact billing behavior of a Token Buffet backend still depends on the account and billing mode configured in that provider application.

```text
TOKEN BUFFET
Claude Code -> your local router -> installed provider CLI -> online AI

OPENROUTER
Claude Code -> OpenRouter's hosted gateway -> provider API -> online AI
```

| Concept | Token Buffet | OpenRouter |
| --- | --- | --- |
| Main payment model | Use existing subscription allowances through signed-in provider applications | Pay for metered API usage |
| Account access | The subscription account signed into each provider application | OpenRouter API credentials and API billing options |
| Routing | Tier requests use remaining allowance or preferred order; recognized models are tried first with same-tier backups | Selected models and provider routing preferences, with configured fallbacks |
| Where the gateway runs | Your computer | OpenRouter's hosted service |
| Translation | Converts supported requests into CLI prompts and reconstructs API responses | Provides an API gateway to model providers |
| Skills tools and MCP | Claude Code manages its skills and executes client actions | Claude Code still manages its skills and executes client actions |

For example, Token Buffet can route a `reasoning` request to the model assigned to that tier in one of your connected provider accounts. OpenRouter normally routes access to the selected API model, choosing among eligible providers; changing to a different model requires a corresponding selection or routing configuration. [3] [4]

Token Buffet's routing helps coordinate the remaining allowances across those subscriptions. OpenRouter's routing coordinates API access to models and providers. The local-versus-hosted gateway distinction explains the implementation, but the subscription-versus-API distinction explains the main difference for the user. Neither makes the online model run locally. [2]

This comparison is conceptual and documentation-based. OpenRouter was not run or tested. Its Claude Code guide guarantees compatibility only with Anthropic's first-party provider. [2]

## 14 The complete numbered sequence

1. Register a Claude Code workspace. Saved app configuration supplies the router URL and default tier.
2. Generate `.claude/settings.local.json` and `launch.json`. The launcher passes the settings and chooses the client configuration home.
3. Start the provider proxies, router, and optional dashboard. Each listener binds its own socket; client destination settings do not bind server sockets.
4. Proxies collect/cache their model and usage information. The router reads those exports over the proxies' HTTP endpoints.
5. Claude Code loads the instructions and skills enabled in that session and discovers tools through its own MCP connections.
6. Claude Code sends JSON to the configured base URL's `/v1/messages` operation, including the chosen tier or model, context, tools, and `stream=true`.
7. The router validates the supported request structure and resolves a tier, specific model, provider-name route, partial model match, or medium fallback.
8. For a tier request it orders candidates by usage/custom mode. For a recognized model request it keeps that model first and orders same-tier backups.
9. The router skips known depleted or stopped candidates, finds the selected proxy's live port, replaces the model with the backend's exact ID, and forwards the supported request path and JSON with resolved effort.
10. The proxy converts the API conversation and tools into text instructions and starts the configured provider executable with model/effort arguments and a pipe for the prompt.
11. The provider CLI communicates with its online AI using its own authentication and returns provider-specific JSON output events.
12. The proxy extracts text. With tools enabled it buffers and parses a complete decision, while HTTP keepalive pings can already be flowing.
13. The proxy constructs the client's response protocol, such as Anthropic SSE text or tool-use events. The router forwards the stream.
14. Claude Code executes a permitted built-in action or sends a separate MCP JSON-RPC tool call. Token Buffet does not execute that client action.
15. Claude Code adds the tool-use history and result to another model request. A new routing attempt and backend subprocess can follow.
16. The backend eventually returns an answer; the proxy emits end-turn events and the client displays it.
17. Request resources are cleaned up, while long-running services and retained logs have separate lifetimes.

### Trace references and source map

[8] [OpenRouter Claude Code integration](https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration)

[9] [MCP tool protocol specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/tools.mdx)

| Question | Source to inspect |
| --- | --- |
| Where does the app URL come from | `default_templates/integrations/chatbot/presets/claude/app_config.json` and instance `app_config.json` |
| How does it become native settings | Chatbot `init.py`: `_render()`, `_write()`, and `init()` |
| How does a server bind and choose a port | `loopback.py`: `HOST`, `serve_next()`, and `listening()` |
| How are provider models and usage cached | `cli_proxy_server.py`: `provider_export()`, `cached_export()`, and background `refresh_loop()` |
| How is a request resolved and forwarded | `local_router.py`: `RouterHandler.do_POST()`, `running_port()`, and `tiers_from_providers()` |
| How are client tools represented | `tool_wire.py`: `anthropic_tools()`, `instruction()`, `anthropic_history()`, and `decision()` |
| How does the CLI run and get parsed | `cli_proxy_server.py`: `handle_chat()`, configured execution arguments, and text/error extractors |
| How are Anthropic events serialized | `anthropic_sse.py`: `event_bytes()` and `buffered_events()` |
| How are environments and homes selected | `extractors/process_env.py`: `build_process_env()` and `isolated_home()` |

The retained demo helpers live under `.tmp/wire-demo`. They record only their own demo processes and do not alter the router's selection algorithm or provider mappings. The ordinary fleet and generated user workspaces were not reconfigured for these runs.
