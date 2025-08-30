"""Simple RCON adapter wrapper for sending tellraw via mcrcon."""
from __future__ import annotations

from mcrcon import MCRcon


class RconAdapter:
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password
        self._conn: MCRcon | None = None

    def connect(self):
        self._conn = MCRcon(self.host, self.password, port=self.port)
        self._conn.connect()

    def tellraw_all(self, text: str, color: str = "aqua"):
        safe = text.replace("\\", "\\\\").replace('"', '\\"')
        cmd = f'tellraw @a {{"text":"{safe}","color":"{color}"}}'
        assert self._conn is not None
        return self._conn.command(cmd)
