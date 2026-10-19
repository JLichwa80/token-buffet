"""macOS service identity and shutdown using psutil.

API reference: https://psutil.readthedocs.io/stable/
"""

import psutil


def _has_pair(arguments, flag, value):
    return any(arguments[index:index + 2] == [flag, value]
               for index in range(len(arguments) - 1))


def stop_service(pid, module, provider=None):
    """Stop a verified service and its descendants; return False if already gone."""
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        raise ValueError("Service has no valid process ID")
    try:
        process = psutil.Process(pid)
        arguments = process.cmdline()
        direct = _has_pair(arguments, "-m", module)
        wrapped = (_has_pair(arguments, "-m", "tokenbuffet.logged_run")
                   and _has_pair(arguments, "--module", module))
        if not (direct or wrapped):
            raise ValueError("Process identity does not match the service")
        if provider is not None and not _has_pair(arguments, "--provider", provider):
            raise ValueError("Process identity does not match the provider")
        processes = [*reversed(process.children(recursive=True)), process]
        for child in processes:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        _, alive = psutil.wait_procs(processes, timeout=5)
        for child in alive:
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        _, alive = psutil.wait_procs(alive, timeout=5)
        if alive:
            raise RuntimeError("Service processes did not exit: "
                               + ", ".join(str(child.pid) for child in alive))
    except psutil.NoSuchProcess:
        return False
    except psutil.Error as exc:
        raise RuntimeError(f"Cannot stop service {pid}: {exc}") from exc
    return True


def stop_fleet(status_dir):
    """Stop this workspace's services without changing the Windows stop path."""
    import json

    failures = []
    for path in sorted(status_dir.glob("*_run_status.json")):
        status = json.loads(path.read_text(encoding="utf-8"))
        if status.get("status") != "running":
            continue
        name = path.stem.removesuffix("_run_status")
        module = {"router": "tokenbuffet.local_router",
                  "dashboard": "tokenbuffet.dashboard"}.get(name, "tokenbuffet.cli_proxy_server")
        provider = name if module == "tokenbuffet.cli_proxy_server" else None
        try:
            stopped = stop_service(status.get("pid"), module, provider)
            print(f"  {name}: {'stopped' if stopped else 'already exited'}")
        except (ValueError, RuntimeError) as exc:
            failures.append(f"{name}: {exc}")
    if failures:
        raise RuntimeError("Could not stop all services: " + "; ".join(failures))
