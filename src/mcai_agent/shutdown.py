"""Graceful shutdown helpers for the agent.

Provides a simple Event-like object to request shutdown and a decorator to
wrap long-running loops to check for shutdown requests.
"""
from __future__ import annotations

from threading import Event
import signal
from types import FrameType
from typing import Optional


class ShutdownRequested(Exception):
    pass


class Shutdown:
    def __init__(self) -> None:
        self._evt = Event()

    def request(self) -> None:
        self._evt.set()

    def is_set(self) -> bool:
        return self._evt.is_set()


def check_shutdown(shutdown: Shutdown) -> None:
    if shutdown.is_set():
        raise ShutdownRequested()


def register_signal_handlers(sh: Shutdown) -> None:
    """Register SIGINT/SIGTERM handlers that request shutdown.

    Safe to call multiple times; later calls overwrite previous handlers.
    """

    def _handler(signum: int, frame: Optional[FrameType]):  # pragma: no cover
        sh.request()

    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)
