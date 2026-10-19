"""Run against an installed wheel on a real macOS runner, without vendor credentials."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

import tokenbuffet
from tokenbuffet import loopback


REPO = Path(__file__).resolve().parents[2]
REPORT = REPO / "macos-report"
FIXTURE = [sys.executable, str(Path(__file__).resolve()), "--fixture"]


def fixture(mode):
    if mode == "models":
        print("- smoke-model", flush=True)
    elif mode == "usage":
        print("Smoke CLI ready", flush=True)
        for line in sys.stdin:
            if line.strip() == "/usage":
                print("Smoke usage: 25% used", flush=True)
    elif mode == "completion":
        print(json.dumps({"text": "macOS smoke response"}), flush=True)
    else:
        raise ValueError(mode)


def request(port, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(loopback.url(port, path), data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.load(response)


def wait_for(description, action, timeout=45):
    deadline = time.monotonic() + timeout
    last_error = None
    while time.monotonic() < deadline:
        try:
            value = action()
            if value:
                print(f"PASS: {description}", flush=True)
                return value
        except (OSError, ValueError, KeyError) as exc:
            last_error = exc
        time.sleep(0.25)
    raise AssertionError(f"Timed out: {description}; last error: {last_error}")


def main():
    if sys.platform != "darwin":
        raise SystemExit("Run this validation on macOS")
    from tokenbuffet.platforms.macos.paths import expand_path
    from tokenbuffet.platforms.macos.processes import stop_service
    from tokenbuffet.platforms.macos.terminal import APPLESCRIPT, shell_command

    REPORT.mkdir(exist_ok=True)
    installed = Path(tokenbuffet.__file__).resolve()
    assert not installed.is_relative_to(REPO / "src"), installed
    templates = installed.parent / "default_templates"
    assert (templates / "integrations/chatbot/presets/codex/app_settings.json").is_file()
    assert (templates / "demo/Obsidian-LLM-Wiki/conference-notes/.obsidian").is_dir()
    assert expand_path(r"~\.grok\auth.json") == str(Path.home() / ".grok/auth.json")
    print(f"PASS: installed wheel and templates: {installed}", flush=True)

    # Compile against the installed Terminal scripting dictionary without opening a window.
    script = REPORT / "launch.applescript"
    script.write_text(APPLESCRIPT, encoding="utf-8")
    subprocess.run(["/usr/bin/osacompile", "-o", str(REPORT / "launch.scpt"), str(script)],
                   check=True, timeout=30)
    terminal = Path("/System/Applications/Utilities/Terminal.app")
    with (REPORT / "Terminal.sdef").open("w", encoding="utf-8") as output:
        subprocess.run(["/usr/bin/sdef", str(terminal)], stdout=output, check=True, timeout=30)
    print("PASS: Terminal AppleScript compiles against the installed dictionary", flush=True)

    with tempfile.TemporaryDirectory(prefix="tokenbuffet-macos-") as temporary:
        workspace = Path(temporary) / "Mac's workspace é"
        workspace.mkdir()
        statuses = workspace / "data/providers_status"
        env = {**os.environ, "TOKENBUFFET_NO_BROWSER": "1"}
        def cli(*args):
            with (REPORT / "cli.log").open("a", encoding="utf-8") as output:
                subprocess.run([sys.executable, "-m", "tokenbuffet.cli", *args],
                               cwd=workspace, env=env, stdout=output,
                               stderr=subprocess.STDOUT, check=True, timeout=70)

        cli("init")
        # Keep detected vendor registrations out of this credential-free validation.
        (workspace / "registered_providers").rename(workspace / "detected_providers")
        provider = workspace / "registered_providers/smoke"
        provider.mkdir(parents=True)
        config = {
            "usage": {"type": "tui", "cli_cmd": [*FIXTURE, "usage"],
                      "command": "/usage", "expect": "Smoke usage", "boot_wait": 1,
                      "view_wait": 1, "views": 1, "calculation": "100 - float(value)",
                      "periods": {"session": {"pct": r"Smoke usage: (\d+)% used"}}},
            "models": {"type": "subcmd", "list_cmd": [*FIXTURE, "models"],
                       "list_regex": r"^- (\S+)"},
            "execution": {"cmd_template": [*FIXTURE, "completion"]},
            "stream": {"text_extractors": [{"matches": {}, "path": "text"}]},
            "server": {"port": 18001}, "tiers": {"medium": "^smoke-model$"},
        }
        (provider / "config.json").write_text(json.dumps(config), encoding="utf-8")

        # Exercise shell quoting with cwd, argv and environment values containing metacharacters.
        probe = "import os,sys; print(os.getcwd()); print(os.environ['TB_PROBE']); print(sys.argv[1])"
        quoted = shell_command([sys.executable, "-c", probe, "literal $(false) ' é"],
                               workspace, {"TB_PROBE": "value ' $(false) é"})
        result = subprocess.run(["/bin/sh", "-c", quoted], capture_output=True, text=True,
                                check=True, timeout=10)
        assert result.stdout.splitlines() == [str(workspace.resolve()), "value ' $(false) é",
                                               "literal $(false) ' é"], result.stdout
        print("PASS: macOS launcher shell quoting and session environment", flush=True)

        try:
            cli("start", "--background")
            def status(name):
                value = json.loads((statuses / f"{name}_run_status.json").read_text())
                return value if value.get("status") == "running" and loopback.listening(value["port"]) else None
            proxy = wait_for("proxy binds", lambda: status("smoke"))
            router = wait_for("router binds", lambda: status("router"))
            dashboard = wait_for("dashboard binds", lambda: status("dashboard"))
            usage = wait_for("PTY capture and quota parsing", lambda: request(proxy["port"], "/usage"))
            assert usage["usage"]["limits"]["session"]["remaining_pct"] == 75, usage
            models = wait_for("model extraction", lambda: request(proxy["port"], "/models"))
            assert models["models"]["available"][0]["id"] == "smoke-model", models
            wait_for("router advertises model", lambda: any(
                model["id"] == "smoke-model" for model in request(router["port"], "/v1/models")["data"]))
            response = request(router["port"], "/v1/chat/completions",
                               {"model": "medium", "messages": [{"role": "user", "content": "hello"}],
                                "stream": False})
            assert response["choices"][0]["message"]["content"] == "macOS smoke response", response
            print("PASS: router -> proxy -> subprocess completion", flush=True)
            # An unrelated PID must be rejected without signaling this validator.
            try:
                stop_service(os.getpid(), "tokenbuffet.cli_proxy_server", "smoke")
            except ValueError:
                pass
            else:
                raise AssertionError("Unrelated process was accepted")
            request(dashboard["port"], "/api/providers/stop", {"provider": "smoke"})
            wait_for("dashboard stops provider", lambda: not loopback.listening(proxy["port"]))
            request(dashboard["port"], "/api/control/router-stop", {})
            wait_for("dashboard stops router", lambda: not loopback.listening(router["port"]))
        finally:
            try:
                cli("stop")
                if 'dashboard' in locals():
                    wait_for("CLI stops dashboard", lambda: not loopback.listening(dashboard["port"]))
            finally:
                if (workspace / "logs").exists():
                    shutil.copytree(workspace / "logs", REPORT / "logs", dirs_exist_ok=True)
                if statuses.exists():
                    shutil.copytree(statuses, REPORT / "status", dirs_exist_ok=True)
    print("PASS: macOS runtime smoke validation; desktop and vendor checks remain manual", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fixture":
        fixture(sys.argv[2])
    else:
        main()
