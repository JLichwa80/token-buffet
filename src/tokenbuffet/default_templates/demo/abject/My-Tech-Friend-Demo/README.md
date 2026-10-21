# My Tech Friend Demo

The tech genius friend who supercharges your productivity. Just describe what you need in plain English, and it instantly builds custom apps, fully functional websites, and even playable games tailored to your exact workflow.

This is an [Abject](https://abject.world) workspace preconfigured to use the local router (`http://127.0.0.1:8090`) through Abject's Ollama provider.
This folder is the instance's Abject data directory (`--data-dir`), so your other Abject settings are untouched.

## Setup

Run `tbuffet demo init`. It installs Abject with its own install script if `abject` is not on PATH (`irm https://abject.world/install.ps1 | iex` on Windows, `curl -fsSL https://abject.world/install.sh | sh` on Linux/macOS).
It sets, with `abject settings set`:

- `ai.credentials.ollama` = `http://127.0.0.1:8090`
- `ai.tiers.smart` and `ai.tiers.code` = router tier `reasoning`
- `ai.tiers.balanced` = router tier `medium`
- `ai.tiers.fast` = router tier `fast`

Run `tbuffet start`, then `tbuffet open abject "My Tech Friend Demo"`.
Registration: `registered_apps/abject/My-Tech-Friend-Demo/` (apply it again with `tbuffet reconfigure-app abject My-Tech-Friend-Demo`).
