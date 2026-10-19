import errno
import json
import socket
from http.server import ThreadingHTTPServer

HOST = "127.0.0.1"


def serve(port, handler, server_cls=ThreadingHTTPServer):
    return server_cls((HOST, port), handler)


PORT_TRIES = 50


def serve_next(port, handler, server_cls=ThreadingHTTPServer, tries=PORT_TRIES):
    """Bind the first free port from `port` upward; the bound port is server.server_address[1].

    A taken port is skipped, never shared. The listening() probe comes first
    because http.server sets SO_REUSEADDR, which on Windows lets a bind succeed
    on a port another process is already listening on.
    """
    for candidate in range(port, port + tries):
        if listening(candidate):
            continue
        try:
            return server_cls((HOST, candidate), handler)
        except OSError as exc:
            if exc.errno not in (errno.EADDRINUSE, errno.EACCES):
                raise
    raise OSError(f"no free port in {port}-{port + tries - 1}")


def already_running(status_path):
    """The live port in a service's run-status file when that service is up, else None."""
    try:
        with open(status_path, encoding="utf-8") as f:
            status = json.load(f)
        port = int(status["port"])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return port if status.get("status") == "running" and listening(port) else None


def listening(port, timeout=0.2):
    try:
        with socket.create_connection((HOST, int(port)), timeout=timeout):
            return True
    except OSError:
        return False


def url(port, path=""):
    return f"http://{HOST}:{port}{path}"
