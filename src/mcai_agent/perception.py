"""Perception helpers: parse logs and produce chat events."""
from __future__ import annotations

import re
from typing import Optional, Tuple

CHAT_PATTERNS = [
    re.compile(r"^\[[0-9:]+\]\s+\[.+?\/INFO\]:\s+<(?P<name>[^>]+)>\s+(?P<msg>.+)$"),
    re.compile(r"^\[.+?\]:\s+<(?P<name>[^>]+)>\s+(?P<msg>.+)$"),
    re.compile(r"^(?P<name>[A-Za-z0-9_ ]{1,16}):\s+(?P<msg>.+)$"),
]


def parse_chat(line: str) -> Optional[Tuple[str, str]]:
    for p in CHAT_PATTERNS:
        m = p.match(line)
        if m:
            return m.group("name"), m.group("msg")
    return None
