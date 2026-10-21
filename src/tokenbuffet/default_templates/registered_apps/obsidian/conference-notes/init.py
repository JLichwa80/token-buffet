#!/usr/bin/env python3
import json
import os
import struct
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
        raise FileNotFoundError("Obsidian is not installed")


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


# Obsidian keeps "Trust author and enable plugins" as localStorage `enable-plugin-<vault id>` = "true" (app.plugins.setEnable,
# inspected in Obsidian 1.14.4). localStorage is a LevelDB database under the settings folder, so the entry is appended to its
# write-ahead log; LevelDB log format: https://github.com/google/leveldb/blob/main/doc/log_format.md
_BLOCK = 32768
_CRC_TABLE = []
for _i in range(256):
    _c = _i
    for _ in range(8):
        _c = (_c >> 1) ^ (0x82F63B78 if _c & 1 else 0)
    _CRC_TABLE.append(_c)


def _masked_crc32c(data):
    crc = 0xFFFFFFFF
    for byte in data:
        crc = _CRC_TABLE[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    crc ^= 0xFFFFFFFF
    return ((((crc >> 15) | (crc << 17)) & 0xFFFFFFFF) + 0xA282EAD8) & 0xFFFFFFFF


def _varint(number):
    out = b""
    while number >= 0x80:
        out += bytes([number & 0x7F | 0x80])
        number >>= 7
    return out + bytes([number])


def _last_sequence(log):
    data = log.read_bytes()
    pos, last, record = 0, 0, b""
    while pos + 7 <= len(data):
        if _BLOCK - pos % _BLOCK < 7:
            pos += _BLOCK - pos % _BLOCK
            continue
        crc, length, kind = struct.unpack_from("<IHB", data, pos)
        pos += 7
        chunk = data[pos:pos + length]
        pos += length
        if kind == 0 and length == 0:
            pos = (pos // _BLOCK + 1) * _BLOCK
            continue
        if _masked_crc32c(bytes([kind]) + chunk) != crc:
            raise ValueError(f"{log} has a bad checksum at byte {pos}")
        record = chunk if kind in (1, 2) else record + chunk
        if kind in (1, 4):
            sequence, count = struct.unpack_from("<QI", record, 0)
            last = sequence + count - 1
    return last, len(data)


def _append_put(log, key, value):
    last, pos = _last_sequence(log)
    rest = struct.pack("<QI", last + 1, 1) + b"\x01" + _varint(len(key)) + key + _varint(len(value)) + value
    out, first = bytearray(), True
    while True:
        room = _BLOCK - pos % _BLOCK
        if room < 7:
            out += b"\x00" * room
            pos += room
            room = _BLOCK
        size = min(len(rest), room - 7)
        final = size == len(rest)
        kind = (1 if final else 2) if first else (4 if final else 3)
        chunk, rest = rest[:size], rest[size:]
        out += struct.pack("<IHB", _masked_crc32c(bytes([kind]) + chunk), size, kind) + chunk
        pos += 7 + size
        first = False
        if final:
            break
    with open(log, "ab") as f:
        f.write(out)


def trust(vault_id):
    """Mark the vault trusted so Obsidian does not show its trust dialog; Obsidian must be closed."""
    storage = _settings_dir() / "Local Storage" / "leveldb"
    try:
        with open(storage / "LOCK", "a+b") as handle:
            if os.name != "nt":
                import fcntl
                fcntl.lockf(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        raise RuntimeError("Close Obsidian completely, then retry: its storage is locked") from exc
    logs = sorted(storage.glob("*.log"))
    if len(logs) != 1:
        raise RuntimeError(f"Expected one LevelDB log in {storage}, found {len(logs)}")
    _append_put(logs[0], b"_app://obsidian.md\x00\x01enable-plugin-" + vault_id.encode("ascii"), b"\x01true")


def launch(app_path):
    if not Path(app_path).is_dir():
        raise FileNotFoundError(f"Vault folder does not exist: {app_path}")
    uri = "obsidian://open?vault=" + link(app_path)
    if sys.platform == "win32":
        os.startfile(uri)
    else:
        subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", uri])


def prepare_demo(app_path):
    trust(link(app_path))


def init(app_path=None):
    check()
    folder = Path(__file__).resolve().parent
    config = json.loads((folder / "app_config.json").read_text(encoding="utf-8"))
    target = Path(app_path) if app_path else folder / (config.get("path") or ".")
    (target / "_Inbox").mkdir(parents=True, exist_ok=True)
