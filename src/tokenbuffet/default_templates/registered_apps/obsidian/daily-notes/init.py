#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _settings_dir():
    # Global settings folder per https://obsidian.md/help/data-storage; Obsidian creates it on first run.
    home = Path.home()
    if sys.platform == "win32":
        base = Path(os.environ["APPDATA"])
    elif sys.platform == "darwin":
        base = home / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config")
    return base / "obsidian"


def check():
    if not _settings_dir().is_dir():
        raise FileNotFoundError("Obsidian must be installed and opened once: get it from https://obsidian.md/download, then run this again")


def _vault_list():
    return _settings_dir() / "obsidian.json"


def link(app_path):
    """Add the vault to Obsidian's vault list (if missing); returns its vault id."""
    vault = os.path.normcase(os.path.abspath(app_path))
    list_path = _vault_list()
    data = json.loads(list_path.read_text(encoding="utf-8")) if list_path.is_file() else {}
    vaults = data.setdefault("vaults", {})
    vault_id = next((k for k, v in vaults.items()
                     if os.path.normcase(os.path.abspath(v.get("path", ""))) == vault), None)
    if vault_id is None:
        vault_id = os.urandom(8).hex()
        vaults[vault_id] = {"path": os.path.abspath(app_path), "ts": int(time.time() * 1000)}
        list_path.parent.mkdir(parents=True, exist_ok=True)
        list_path.write_text(json.dumps(data), encoding="utf-8")
    return vault_id


def _vault_help():
    return ("Close Obsidian completely and retry the command. If the problem persists, "
            "ensure the vault is added in Obsidian before opening it with Token Buffet.")


def _run_cli(*args):
    executable = shutil.which("Obsidian.com" if sys.platform == "win32" else "obsidian")
    if not executable:
        raise FileNotFoundError("Enable Obsidian Settings > General > Command line interface, then retry the command")
    deadline = time.monotonic() + 15
    while True:
        try:
            result = subprocess.run([executable, *args], capture_output=True, text=True,
                                    encoding="utf-8", timeout=60)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"Obsidian command timed out. {_vault_help()}") from exc
        output = (result.stdout + result.stderr).strip()
        if (output.startswith('Error: Command "') and '" not found.' in output
                and time.monotonic() < deadline):
            time.sleep(0.5)
            continue
        break
    if result.returncode or "Error:" in output or "Vault not found." in output:
        raise RuntimeError(f"{output or 'Obsidian command failed.'}\n{_vault_help()}")
    return output


def launch(app_path):
    vault = os.path.normcase(os.path.abspath(app_path))
    if not Path(app_path).is_dir():
        raise FileNotFoundError(f"Vault folder does not exist: {app_path}")
    vaults = _run_cli("vaults", "verbose")
    if not any(os.path.normcase(os.path.abspath(line.split("\t", 1)[1])) == vault
               for line in vaults.splitlines() if "\t" in line):
        raise ValueError(f"Vault is not available in Obsidian: {app_path}\n{_vault_help()}")
    uri = "obsidian://open?vault=" + link(app_path)
    if sys.platform == "win32":
        os.startfile(uri)
    else:
        subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", uri])


def prepare_demo(app_path):
    """Trust and initialize this demo using Obsidian's CLI and the bundled plugin."""
    vault_id = link(app_path)

    def run(*args):
        return _run_cli(f"vault={vault_id}", *args)

    code = """(async () => {
        await new Promise(resolve => app.workspace.onLayoutReady(resolve));
        await app.plugins.setEnable(true);
        await app.plugins.enablePluginAndSave('karpathywiki');
        if (!app.plugins.isEnabled()) throw new Error('Vault trust was not saved');
        const plugin = app.plugins.plugins.karpathywiki;
        if (!plugin) throw new Error('LLM Wiki plugin did not load');
        await plugin.loadSettings();
        plugin.settings.apiKey = 'TokenBuffet';
        plugin.settings.llmReady = true;
        app.secretStorage.setSecret(plugin.settings.providerApiKeySecretId, 'TokenBuffet');
        await plugin.saveSettings();
        await plugin.wikiEngine.ensureWikiStructure();
        if (!plugin.llmClient) throw new Error('LLM Wiki connection settings are incomplete');
    })()"""
    run("eval", "code=" + code)
    run("reload")


def init(app_path=None):
    check()
    folder = Path(__file__).resolve().parent
    config = json.loads((folder / "app_config.json").read_text(encoding="utf-8"))
    target = Path(app_path) if app_path else folder / (config.get("path") or ".")
    (target / "_Inbox").mkdir(parents=True, exist_ok=True)
