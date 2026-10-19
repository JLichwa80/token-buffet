# Claudia Demo - My Client Relationships Management

Claudia is a terminal-based AI chief of staff that remembers your relationships, tracks your commitments, surfaces patterns in your work, and helps you prioritize strategically. This demo shows a client relationship management workspace preconfigured to connect to the local router.

See the [Claudia project](https://github.com/kbanc85/claudia) for full details.

On Windows, use **Open** beside this demo in the Hub's Client Integrations area to start Claude Code
in the demo workspace. Claude Code must be installed and available on PATH.
The same launcher is available with `tbuffet open claudia "My Client Relationships Management"`.

## Configuration

**app_config.json** (`registered_apps/claudia/My Client Relationships Management/app_config.json`):
```json
{
    "name": "My Client Relationships Management",
    "type": "claudia",
    "path": "../../../demo/claudia/My-Client-Relationships-Management-Demo",
    "client_settings": {
        "active_endpoint": "http://127.0.0.1:8090/v1",
        "single_model_tier": "medium",
        "model_mode": "false",
        "task_model_tiers": {
            "taskType1": "fast",
            "taskType2": "medium",
            "taskType3": "reasoning"
        }
    },
    "bridge_configuration": ".claude/settings.local.json"
}
```

**app_settings.json** (`registered_apps/claudia/My Client Relationships Management/app_settings.json`):
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:8090/v1",
    "ANTHROPIC_API_KEY": "",
    "ANTHROPIC_AUTH_TOKEN": "local-bridge"
  }
}
```


