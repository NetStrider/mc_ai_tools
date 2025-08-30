"""Simple reasoning helpers and builtin commands."""
from __future__ import annotations

from datetime import datetime


def cmd_ping(_) -> str:
    return "pong"


def cmd_time(_) -> str:
    return datetime.utcnow().strftime("UTC %Y-%m-%d %H:%M:%S")

_BUILTINS = {"ping": cmd_ping, "time": cmd_time}


def handle_command(name: str, message: str) -> str:
    parts = message.strip().split()
    if not parts:
        return ""
    cmd = parts[0].lstrip("!")
    fn = _BUILTINS.get(cmd)
    if fn:
        return fn(None)
    return "Unknown command"
