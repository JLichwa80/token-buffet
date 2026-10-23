import os
import re
import signal
import sys
import shutil
import glob
import subprocess
import argparse
from pathlib import Path
import json
import time

TEMPLATES = Path(__file__).parent / "default_templates"


def _copy_missing(src, dst, label):
    """Copy src to dst unless dst already exists."""
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    print(f"  {label}")


def _is_demo(item):
    """Demo templates: demo/ itself and the bundled app instances under registered_apps/<type>/."""
    rel = item.relative_to(TEMPLATES)
    return rel.parts[0] == "demo" or (rel.parts[0] == "registered_apps" and item.is_dir())


def init_workspace():
    """Scaffold this directory, register the provider CLIs found on PATH, check app integrations."""
    from tokenbuffet.onboarding import add_known_provider, check_app_type, detect_providers, list_app_types, list_providers
    print(f"Directory: {Path.cwd()}")
    for d in ["registered_providers", "registered_apps", "config", "logs", "data",
              "data/providers_status", "data/provider_homes", "data/temp",
              "logs/router", "logs/proxy", "logs/dashboard", "logs/extractors", "logs/sessions"]:
        Path(d).mkdir(parents=True, exist_ok=True)

    print("\nCopying templates...")
    for folder in TEMPLATES.iterdir():
        for item in (folder.iterdir() if folder.is_dir() else [folder]):
            if not _is_demo(item):
                _copy_missing(item, Path(item.relative_to(TEMPLATES)), item.relative_to(TEMPLATES).as_posix())

    print("\nProviders:")
    registered = list_providers()
    for name, cli in detect_providers().items():
        if not cli:
            print(f"  {name}: CLI not found")
        elif name in registered:
            print(f"  {name}: registered")
        else:
            add_known_provider(name)
            print(f"  {name}: registered ({cli})")

    from tokenbuffet.extractors.process_env import prepare_isolated_home
    for name in list_providers():
        config = json.loads((Path("registered_providers") / name / "config.json").read_text(encoding="utf-8"))
        home = prepare_isolated_home(config)
        if home:
            print(f"  {name}: isolated home {home}")

    print("\nApps:")
    types = list_app_types()
    missing = [t for t in types if check_app_type(t)]
    ready = [t for t in types if t not in missing]
    if ready:
        print(f"  Installed: {', '.join(ready)}")
    if missing:
        print(f"  Not installed: {', '.join(missing)}")
    if not ready:
        print("  No apps installed")

    print("\nNext: tbuffet start   (demos: tbuffet demo init)")


def start_fleet(debug=False, foreground=True):
    """Start the fleet; a foreground session owns its entire process trees."""
    processes = []
    try:
        _start_fleet(debug, foreground, processes)
    except KeyboardInterrupt:
        if not foreground:
            raise
        print("\nStopping foreground services...")
    finally:
        if foreground:
            # A second Ctrl+C must not interrupt cleanup halfway through the fleet.
            previous = signal.signal(signal.SIGINT, signal.SIG_IGN)
            try:
                _stop_started_processes(processes)
            finally:
                signal.signal(signal.SIGINT, previous)


def _stop_started_processes(processes):
    """Stop only the service trees launched by this invocation, then reap them."""
    failures = []
    for process in reversed(processes):
        try:
            if os.name == "nt":
                if process.poll() is not None:
                    continue
                # /T includes the venv launcher, real Python process, and CLI children.
                result = subprocess.run(
                    ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                    capture_output=True, text=True, timeout=15,
                )
                if result.returncode and process.poll() is None:
                    raise RuntimeError((result.stderr or result.stdout).strip())
            else:
                # Each foreground service starts a separate session/process group.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass  # This service group has already exited.
            process.wait(timeout=10)
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
            failures.append(f"pid {process.pid}: {exc}")
    if failures:
        raise RuntimeError("Could not stop all foreground services: " + "; ".join(failures))


def _start_fleet(debug, foreground, processes):
    """Launch services and optionally wait for them in the foreground."""
    from tokenbuffet import loopback
    config_dir = Path("registered_providers")
    if not config_dir.exists():
        print(f"Error: Could not find registered_providers/ at {config_dir}")
        print(f"Run: tbuffet init")
        sys.exit(1)

    providers = [d.name for d in config_dir.iterdir() if d.is_dir() and (d / "config.json").exists()]

    if not providers:
        print("No providers registered. Run: tbuffet init")
        sys.exit(1)

    if os.name == "nt":
        from tokenbuffet import job
        job.join()

    process_options = {}
    if foreground:
        process_options = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
                           if os.name == "nt" else {"start_new_session": True})

    # A leftover status file from an earlier run must not look like a ready proxy.
    status_dir = Path("data/providers_status")
    for prov in providers:
        (status_dir / f"{prov}_run_status.json").unlink(missing_ok=True)

    # 1. Start a proxy for each provider
    for prov in providers:
        config_path = config_dir / prov / "config.json"
        port = 8000
        if config_path.exists():
            with open(config_path, "r") as f:
                c = json.load(f)
            if "server" in c and "port" in c["server"]:
                port = c["server"]["port"]

        print(f"Starting Proxy for {prov} on port {port}...")
        proxy_args = [sys.executable, "-m", "tokenbuffet.logged_run", "--log", "proxy/console.log", "--module", "tokenbuffet.cli_proxy_server", "--provider", prov, "--port", str(port)]
        if debug:
            proxy_args.append("--debug")
        p = subprocess.Popen(proxy_args, **process_options)
        processes.append(p)

    # Proxies bind first and read usage/models in the background. Poll every proxy's run-status file together and
    # report each as soon as it is ready or failed. The status pid is not the
    # Popen pid (a Windows venv python.exe is a launcher for the real process).
    started = time.monotonic()
    deadline = started + 30
    pending = dict(zip(providers, processes))
    print(f"Waiting for proxies to start (usage and models load in the background; up to 30s): {', '.join(providers)}")
    last_note = started
    while pending and time.monotonic() < deadline:
        for prov, process in list(pending.items()):
            try:
                with open(status_dir / f"{prov}_run_status.json", encoding="utf-8") as f:
                    status = json.load(f)
            except (OSError, ValueError):
                status = {}
            if status.get("status") == "running" and loopback.listening(status.get("port")):
                print(f"  {prov} ready on port {status['port']} (reading usage in the background)")
            elif status.get("status") == "failed":
                print(f"  {prov} failed: {status.get('reason', 'see logs')}")
            elif process.poll() is not None:
                print(f"  {prov} exited during startup (code {process.returncode}); see logs/{prov}/proxy/console.log")
            else:
                continue
            del pending[prov]
        if pending and time.monotonic() - last_note >= 10:
            last_note = time.monotonic()
            print(f"  still starting {', '.join(pending)}... ({int(last_note - started)}s)")
        time.sleep(0.5)
    for prov in pending:
        print(f"  {prov} did not start within 30s; starting the router without it.")

    # 2. Start router on 8090
    print("Starting Local Router on port 8090 (provider models and usage appear as each proxy finishes reading them)...")
    p = subprocess.Popen(
        [sys.executable, "-m", "tokenbuffet.logged_run", "--log", "router/console.log", "--module", "tokenbuffet.local_router", "--port", "8090"],
        **process_options,
    )
    processes.append(p)

    # 3. Start dashboard (a taken port is skipped; it publishes the one it got)
    print("Starting Dashboard (preferred port 8080)...")
    dashboard_status = Path("data/providers_status/dashboard_run_status.json")
    dashboard_status.unlink(missing_ok=True)
    p = subprocess.Popen(
        [sys.executable, "-m", "tokenbuffet.logged_run", "--log", "dashboard/console.log", "--module", "tokenbuffet.dashboard"],
        **process_options,
    )
    processes.append(p)

    dashboard_url = loopback.url(8080)
    wait_until = time.monotonic() + 15
    while time.monotonic() < wait_until and p.poll() is None:
        try:
            dashboard_url = loopback.url(json.loads(dashboard_status.read_text(encoding="utf-8"))["port"])
            break
        except (OSError, ValueError, KeyError):
            time.sleep(0.3)

    if foreground:
        print(f"\nRunning in foreground. Ctrl+C stops all services. Dashboard: {dashboard_url}")
        # An unbounded Windows Popen.wait() can defer Python's Ctrl+C handler.
        # Return to Python regularly so KeyboardInterrupt reaches fleet cleanup.
        while any(p.poll() is None for p in processes):
            time.sleep(0.2)
        return

    print(f"\nAll services launched in background. Dashboard: {dashboard_url}")
    print(f"Directory: {Path.cwd()}")
    print("Run: tbuffet status")
    print("Run: tbuffet stop")

def status_fleet():
    """Show status of all running services."""
    print(f"Directory: {Path.cwd()}")
    print("\nStatus:")

    status_dir = Path("data/providers_status")
    if not status_dir.exists():
        print("  (no status files found; run: tbuffet start)")
        return

    # Check provider proxies
    for status_file in sorted(status_dir.glob("*_run_status.json")):
        provider = status_file.stem.replace("_run_status", "")
        try:
            with open(status_file) as f:
                status = json.load(f)
                pid = status.get("pid")
                port = status.get("port")
                st = status.get("status", "unknown")
                if st == "running" and port:
                    from tokenbuffet import loopback
                    if not loopback.listening(port):
                        st = "stale"  # status file says running but nothing is listening
                print(f"  {provider:12} {st:10} pid={pid:6} port={port}")
        except (OSError, json.JSONDecodeError):
            print(f"  {provider:12} (no status)")

def stop_fleet():
    """Stop all running services."""
    if sys.platform == "darwin":
        from tokenbuffet.platforms.macos.processes import stop_fleet as stop_macos_fleet
        return stop_macos_fleet(Path("data/providers_status"))

    status_dir = Path("data/providers_status")
    if not status_dir.exists():
        print("No services running.")
        return

    killed = []
    for status_file in status_dir.glob("*_run_status.json"):
        try:
            with open(status_file) as f:
                status = json.load(f)
                pid = status.get("pid")
                if pid:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        killed.append((status_file.stem, pid))
                    except (ProcessLookupError, OSError):
                        pass
        except (OSError, json.JSONDecodeError):
            pass

    if killed:
        time.sleep(1)
    else:
        print("No running processes found.")

def force_stop():
    """Kill the Token Buffet job (Windows), then every Token Buffet service process (python -m tokenbuffet.<service>),
    except this command and its ancestors. Apps are never touched."""
    if os.name == "nt":
        from tokenbuffet import job
        if job.terminate():
            print("Killed every process in the TokenBuffet job.")
        listing = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process | ForEach-Object { \"$($_.ProcessId) $($_.ParentProcessId) $($_.CommandLine)\" }"],
            capture_output=True, text=True, check=True).stdout
    else:
        listing = subprocess.run(["ps", "-axo", "pid=,ppid=,command="], capture_output=True, text=True, check=True).stdout
    processes = {}
    for line in listing.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            processes[int(parts[0])] = (int(parts[1]), parts[2] if len(parts) > 2 else "")
    # The shell that ran this command also mentions tbuffet in its command line, so spare every ancestor.
    skip = set()
    pid = os.getpid()
    while pid in processes and pid not in skip:
        skip.add(pid)
        pid = processes[pid][0]
    # Only Token Buffet's own services; an app's command line may mention tokenbuffet through its workspace path.
    service = re.compile(r"(?:^|\s)-m\s+tokenbuffet\.(?:logged_run|cli_proxy_server|local_router|dashboard|extractors)(?:\s|$)"
                         r"|(?:-m\s+tokenbuffet\.cli|(?:tbuffet|tokenbuffet)(?:\.exe)?\"?)\s+start(?:\s|$)")
    targets = [(pid, command) for pid, (_, command) in processes.items()
               if pid not in skip and service.search(command)]
    for pid, command in targets:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
        else:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass  # already gone with its parent
        print(f"Killed {pid}: {command[:100]}")
    if not targets:
        print("No tbuffet processes found.")


def doctor():
    """Check directory health and dependencies."""
    registered_providers = Path("registered_providers")
    config = Path("config")
    logs = Path("logs")
    data_providers_status = Path("data/providers_status")

    print("Doctor")
    print(f"  Directory: {Path.cwd()}")

    checks = {
        "registered_providers/ exists": registered_providers.exists(),
        "config/ exists": config.exists(),
        "logs/ exists": logs.exists(),
    }

    # Check for providers
    provider_count = 0
    if registered_providers.exists():
        provider_count = len([d for d in registered_providers.iterdir() if d.is_dir()])
    checks[f"Providers configured ({provider_count})"] = provider_count > 0

    # Router config parses
    router_cfg = config / "router_config.json"
    if router_cfg.exists():
        try:
            json.loads(router_cfg.read_text(encoding="utf-8"))
            checks["config/router_config.json is valid JSON"] = True
        except (OSError, ValueError):
            checks["config/router_config.json is valid JSON"] = False

    # Per-provider: CLI on PATH; port free or held by our own running service
    from tokenbuffet import loopback
    ports = {}  # port -> service name
    for name in sorted(d.name for d in registered_providers.iterdir()
                       if d.is_dir() and (d / "config.json").exists()) if registered_providers.exists() else []:
        try:
            cfg = json.loads((registered_providers / name / "config.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            checks[f"{name}: config.json is valid JSON"] = False
            continue
        cmd = (cfg.get("usage") or {}).get("cli_cmd") or []
        if cmd:
            checks[f"{name}: CLI '{cmd[0]}' on PATH"] = shutil.which(cmd[0]) is not None
        port = (cfg.get("server") or {}).get("port")
        if isinstance(port, int):
            ports[port] = name
    ports.update({8090: "router", 8080: "dashboard"})

    for port, name in sorted(ports.items()):
        in_use = loopback.listening(port)
        ours = False
        try:
            st = json.loads((data_providers_status / f"{name}_run_status.json").read_text(encoding="utf-8"))
            ours = in_use and st.get("port") == port and st.get("status") == "running"
        except (OSError, ValueError):
            pass
        label = f"Port {port} ({name}) " + ("in use by this directory's running service" if ours
                                           else "in use by another process (the next free port will be used)" if in_use else "free")
        checks[label] = True

    # Registered app types may declare a check() (e.g. obsidian: the app is installed)
    from tokenbuffet.onboarding import check_app_type
    for app_type in sorted({p.parent.parent.name for p in Path("registered_apps").glob("*/*/app_config.json")}):
        error = check_app_type(app_type)
        if error is not None:
            checks[f"{app_type}: {error or 'app installed'}"] = not error

    # Print results
    print("\nChecks:")
    all_ok = True
    for check, result in checks.items():
        status = "OK" if result else "FAIL"
        print(f"  {status} {check}")
        if not result:
            all_ok = False

    if all_ok:
        print("\nAll checks passed! Run: tbuffet start")
    else:
        print("\nSome checks failed. See output above for details.")

def _cmd_add_provider(args):
    from tokenbuffet.onboarding import (
        known_providers, add_known_provider, import_provider_config, validate_provider
    )
    name = args.name

    if args.config_file:
        if not name:
            print("Error: provider name required when using --from. Example:")
            print(f"  tbuffet add-provider myname --from /path/to/config.json")
            sys.exit(1)
        try:
            result = import_provider_config(name, args.config_file, overwrite=args.overwrite)
            print(f"Provider '{name}' imported -> {result['path']}")
        except (FileNotFoundError, FileExistsError, ValueError) as exc:
            print(f"Error: {exc}")
            sys.exit(1)
    elif name:
        try:
            result = add_known_provider(name, overwrite=args.overwrite)
            print(f"Provider '{name}' configured -> {result['path']}")
        except FileExistsError:
            if not args.validate:
                print(f"Provider '{name}' is already configured (use --overwrite to reset, or --validate to check login).")
                return
            print(f"Provider '{name}' already configured; validating existing config.")
        except (FileNotFoundError, ValueError) as exc:
            print(f"Error: {exc}")
            sys.exit(1)
    else:
        print(f"Known providers: {', '.join(known_providers())}")
        print("Usage:")
        print("  tbuffet add-provider <name>               # add a known provider")
        print("  tbuffet add-provider <name> --from <cfg>  # import AI-authored config")
        return

    if args.validate:
        print(f"Validating '{name}' (capture+parse, may take ~30s)...")
        v = validate_provider(name)
        if v["success"]:
            quota = f"{v['remaining_pct']:.0f}% remaining" if v["remaining_pct"] is not None else "quota unknown"
            models = f"{v['models_count']} model(s)" if v["models_count"] else ""
            parts = [p for p in [quota, models] if p]
            print(f"  OK {name}: {', '.join(parts) or 'OK'}")
        else:
            print(f"  FAIL {name}: {v['error']}")
            print(f"    {v['hint']}")
            sys.exit(1)
    else:
        cli = shutil.which(name)
        if cli:
            print(f"  CLI found: {cli}")
            print(f"  Next: run `{name}` once and sign in, then: tbuffet add-provider {name} --validate")
        else:
            print(f"  CLI '{name}' not found on PATH. Install the vendor CLI, sign in, then re-run with --validate.")


def _cmd_list_providers():
    from tokenbuffet.onboarding import list_providers
    providers = list_providers()
    if not providers:
        print("No providers configured.")
        print("Run: tbuffet add-provider <name>")
        return
    print(f"Configured providers ({len(providers)}):")
    for name in providers:
        config_path = Path("registered_providers") / name / "config.json"
        print(f"  {name:12}  {config_path}")


def _cmd_remove_provider(args):
    from tokenbuffet.onboarding import remove_provider
    try:
        remove_provider(args.name)
        print(f"Provider '{args.name}' removed.")
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


def _path_required(app_type):
    """True when the app type needs a folder (its app_config.json path is the [app_path] placeholder)."""
    config = Path("integrations") / app_type / "app_config.json"
    return config.is_file() and json.loads(config.read_text(encoding="utf-8")).get("path") == "[app_path]"


def _cmd_add_app(args):
    from tokenbuffet.folder_picker import pick_folder
    from tokenbuffet.onboarding import add_app, list_app_types
    if args.type and not args.path and _path_required(args.type):
        args.path = pick_folder()
        if not args.path:
            print("Cancelled: no folder chosen.")
            return
    if not args.name and args.path:
        args.name = Path(args.path).resolve().name
    if not args.type or not args.name:
        print(f"App types: {', '.join(list_app_types()) or '(none; run tbuffet init)'}")
        print("Usage: tbuffet add-app <type> [name] [--path DIR] [--preset CLI] [--vault-type T] [--label L]")
        print("The name defaults to the --path folder's name.")
        return
    extras = {k: v for k, v in (("vault_type", args.vault_type), ("label", args.label), ("preset", args.preset)) if v}
    try:
        r = add_app(args.type, args.name, args.path or "", extras)
    except FileExistsError:
        print(f"Error: app instance {args.type}/{args.name} already exists (use reconfigure-app).")
        sys.exit(1)
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    print(f"Registered: {r['instance']}")
    print(f"Settings:   {r['target']}")


def _cmd_add_chatbot(args):
    """add-app for the chatbot type, with the CLI preset as the first argument."""
    args.type, args.preset, args.vault_type = "chatbot", args.cli, None
    _cmd_add_app(args)


def _cmd_list_apps():
    from tokenbuffet.onboarding import list_apps, list_app_types
    print(f"App types: {', '.join(list_app_types()) or '(none)'}")
    apps = list_apps()
    print("Registered apps:" if apps else "No apps registered.")
    for a in apps:
        print(f"  {a}")


def _cmd_reconfigure_app(args):
    from tokenbuffet.onboarding import reapply_app
    try:
        r = reapply_app(args.type, args.name)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    print(f"Re-applied settings: {r['target']}")


def _cmd_demo_init():
    """Copy the demo files and demo app instances, then check() + link() each demo app."""
    from tokenbuffet.onboarding import can_link, can_open, check_app_type, link_app, prepare_demo
    if not Path("integrations").is_dir():
        print("Error: not a Token Buffet directory. Run: tbuffet init")
        sys.exit(1)
    print("Copying demos...")
    demos = []
    for item in sorted(TEMPLATES.rglob("*")):
        rel = item.relative_to(TEMPLATES)
        if rel.parts[0] == "demo" and len(rel.parts) == 2 or rel.parts[0] == "registered_apps" and len(rel.parts) == 3 and item.is_dir():
            _copy_missing(item, Path(rel), rel.as_posix())
            if rel.parts[0] == "registered_apps":
                demos.append((rel.parts[1], rel.parts[2]))
    print("\nDemos:")
    setup_failed = False
    for app_type, name in demos:
        app = f"{app_type}/{name}"
        error = check_app_type(app_type)
        if error:
            print(f"  {app}: unavailable ({error})")
            continue
        if can_link(app_type):
            try:
                link_app(app_type, name)
            except (OSError, ValueError) as exc:
                print(f"  {app}: not linked ({exc})")
                continue
        try:
            prepare_demo(app_type, name)
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"  {app}: configuration failed: {exc}")
            setup_failed = True
            continue
        if can_open(app_type, name):
            print(f'  {app}: configured, open with: tbuffet open {app_type} "{name}"')
        else:
            print(f"  {app}: configured")
    print("\nNext: tbuffet start")
    if setup_failed:
        sys.exit(1)


def _pick_app(app_type, name):
    """Resolve open's optional type/name: list the matching openable instances and ask which one."""
    from tokenbuffet.onboarding import can_open, list_apps
    if app_type and name:
        return app_type, name
    choices = [a for a in list_apps() if (not app_type or a.split("/")[0] == app_type) and can_open(*a.split("/", 1))]
    if not choices:
        print("Error: no registered apps to open (see: tbuffet list-apps)")
        sys.exit(1)
    if len(choices) > 1:
        for number, choice in enumerate(choices, 1):
            print(f"  {number}. {choice}")
        if not sys.stdin.isatty():
            print("Error: several apps match; run: tbuffet open <type> <name>")
            sys.exit(1)
        answer = input("Open which? ").strip()
        if not answer.isdigit() or not 1 <= int(answer) <= len(choices):
            print("Error: enter a number from the list")
            sys.exit(1)
        choices = [choices[int(answer) - 1]]
    return tuple(choices[0].split("/", 1))


def _cmd_open(args):
    from tokenbuffet.onboarding import open_app
    args.type, args.name = _pick_app(args.type, args.name)
    try:
        path = open_app(args.type, args.name)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    print(f"Opened {args.type}/{args.name}: {path}")


def _cmd_install_abject():
    from tokenbuffet.onboarding import _app_type_module
    module = _app_type_module("abject")
    if module is None:
        sys.exit("Error: abject integration missing. Run: tbuffet init")
    try:
        module.install()
    except (OSError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Error: {exc}")


def _cmd_service(args):
    """Start or stop a single provider proxy, all provider proxies, or the router, via the dashboard's own controls."""
    from tokenbuffet.dashboard import server
    verb, target = args.command.split("-")
    try:
        if target == "router":
            result = (server.start_router if verb == "start" else server.stop_router)({})
        elif args.name:
            result = (server.launch_provider if verb == "start" else server.stop_provider)({"provider": args.name})
        else:
            result = (server.start_providers if verb == "start" else server.stop_providers)({})
    except (ValueError, RuntimeError, OSError) as exc:
        sys.exit(f"Error: {exc}")
    print(result.get("output") or f"{args.name}: {result}")


def main():
    parser = argparse.ArgumentParser(
        description="Token Buffet — expose your CLI subscriptions as a local LLM API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="tbuffet always operates on the current directory."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Scaffold this directory, register provider CLIs found on PATH, check app integrations.")

    start_parser = subparsers.add_parser("start", help="Start proxies, router, and dashboard; Ctrl+C stops them.")
    start_parser.add_argument("--debug", action="store_true", help="Capture full proxy request traces")
    start_parser.add_argument("--background", action="store_true", help="Launch services in the background instead of waiting for Ctrl+C")

    stop_parser = subparsers.add_parser("stop", help="Stop all running services.")
    stop_parser.add_argument("--force", action="store_true", help="Kill the Token Buffet job and every Token Buffet service process (never apps)")
    subparsers.add_parser("status", help="Show running services.")
    subparsers.add_parser("doctor", help="Check directory health and dependencies.")

    restart_parser = subparsers.add_parser("restart", help="Stop then start all services.")
    restart_parser.add_argument("--debug", action="store_true")
    restart_parser.add_argument("--background", action="store_true", help="Launch services in the background instead of waiting for Ctrl+C")

    demo_parser = subparsers.add_parser("demo", help="Demo apps.")
    demo_parser.add_argument("action", choices=["init"], help="init: copy the demos, add them to their apps, report which can run")

    open_parser = subparsers.add_parser("open", help="Open a registered app (e.g. tbuffet open obsidian conference-notes); omit type/name to pick from a list.")
    open_parser.add_argument("type", nargs="?")
    open_parser.add_argument("name", nargs="?")

    add_provider_parser = subparsers.add_parser("add-provider", help="Add or update a provider.")
    add_provider_parser.add_argument("name", nargs="?", help="Provider name (claude, codex, grok, agy, or custom)")
    add_provider_parser.add_argument("--from", dest="config_file", help="Import config from a file")
    add_provider_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing provider config")
    add_provider_parser.add_argument("--validate", action="store_true", help="Run capture+parse after import to verify login")

    subparsers.add_parser("list-providers", help="List configured providers.")

    remove_provider_parser = subparsers.add_parser("remove-provider", help="Remove a configured provider.")
    remove_provider_parser.add_argument("name", help="Provider name to remove")

    add_app_parser = subparsers.add_parser("add-app", help="Register a downstream app (Obsidian, chatbot, etc.).")
    add_app_parser.add_argument("type", nargs="?", help="App type (obsidian, chatbot, claudia, abject)")
    add_app_parser.add_argument("name", nargs="?", help="App instance name (defaults to the folder name)")
    add_app_parser.add_argument("--path", help="App folder (a folder chooser opens if omitted and the app type needs one)")
    add_app_parser.add_argument("--vault-type", dest="vault_type", help="Preset (e.g. obsidian vault type)")
    add_app_parser.add_argument("--preset", help="Client preset (claude, codex, grok, agy)")
    add_app_parser.add_argument("--label", help="Display label")

    add_chatbot_parser = subparsers.add_parser("add-chatbot", help="Register a chatbot CLI in a folder (opens a folder chooser when --path is omitted).")
    add_chatbot_parser.add_argument("cli", help="Chatbot CLI preset (claude, codex, grok, agy)")
    add_chatbot_parser.add_argument("--path", help="Workspace folder (a chooser opens if omitted)")
    add_chatbot_parser.add_argument("--name", help="Instance name (defaults to the folder name)")
    add_chatbot_parser.add_argument("--label", help="Display label")

    subparsers.add_parser("list-apps", help="List app types and registered apps.")

    reapply_parser = subparsers.add_parser("reconfigure-app", help="Re-apply an app's bridge settings.")
    reapply_parser.add_argument("type")
    reapply_parser.add_argument("name")

    subparsers.add_parser("install-abject", help="Install the headless edition of Abject with its own install script (https://abject.world/install).")

    subparsers.add_parser("dashboard", help="Start standalone web dashboard on port 8080.")

    for verb in ("start", "stop"):
        provider_parser = subparsers.add_parser(f"{verb}-provider", help=f"{verb.capitalize()} one provider proxy, or every provider proxy when no name is given.")
        provider_parser.add_argument("name", nargs="?", help="Provider name (omit for all providers)")
        subparsers.add_parser(f"{verb}-router", help=f"{verb.capitalize()} the router (port 8090).")

    args = parser.parse_args()

    if args.command == "init":
        init_workspace()
    elif args.command == "start":
        start_fleet(debug=args.debug, foreground=not args.background)
    elif args.command == "restart":
        stop_fleet()
        time.sleep(2)
        start_fleet(debug=args.debug, foreground=not args.background)
    elif args.command == "stop":
        force_stop() if args.force else stop_fleet()
    elif args.command == "status":
        status_fleet()
    elif args.command == "doctor":
        doctor()
    elif args.command == "demo":
        _cmd_demo_init()
    elif args.command == "open":
        _cmd_open(args)
    elif args.command == "add-provider":
        _cmd_add_provider(args)
    elif args.command == "list-providers":
        _cmd_list_providers()
    elif args.command == "remove-provider":
        _cmd_remove_provider(args)
    elif args.command == "add-app":
        _cmd_add_app(args)
    elif args.command == "add-chatbot":
        _cmd_add_chatbot(args)
    elif args.command == "list-apps":
        _cmd_list_apps()
    elif args.command == "reconfigure-app":
        _cmd_reconfigure_app(args)
    elif args.command in ("start-provider", "stop-provider", "start-router", "stop-router"):
        _cmd_service(args)
    elif args.command == "install-abject":
        _cmd_install_abject()
    elif args.command == "dashboard":
        from tokenbuffet.dashboard.server import main as run_dashboard
        run_dashboard()

if __name__ == "__main__":
    main()
