"""Minimal agent runner stub."""
from __future__ import annotations

import argparse
import json
import signal
import time
from pathlib import Path


def run(config_path: Path):
    print("Starting mcai agent (stub). Config:", config_path)
    stop = False

    def _sig(_signum, _frame):
        nonlocal stop
        stop = True

    signal.signal(signal.SIGINT, _sig)
    signal.signal(signal.SIGTERM, _sig)

    while not stop:
        print("Agent tick... (no-op)")
        time.sleep(1.0)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, default=Path("agent_config.json"))
    args = p.parse_args()
    run(args.config)
