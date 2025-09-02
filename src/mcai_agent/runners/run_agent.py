"""Agent runner entrypoint integrating config, logging, and shutdown."""
from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Any, Dict

from mcai_agent import config as config_mod
from mcai_agent import logging_setup, shutdown


def run(config_path: Path) -> int:
    cfg: Dict[str, Any] = {}
    try:
        if config_path.exists():
            cfg = config_mod.load_config(config_path)
    except Exception as e:  # pragma: no cover
        print(f"Failed to load config {config_path}: {e}")
    logger = logging_setup.configure_logger("mcai.agent")
    sh = shutdown.Shutdown()
    shutdown.register_signal_handlers(sh)
    logger.info(
        "agent_start",
        extra={
            "ctx": {
                "config_path": str(config_path),
                "have_cfg": bool(cfg),
            }
        },
    )
    tick = 0
    interval = config_mod.get_config_value(cfg, "loop_interval", 1.0)
    while True:
        try:
            shutdown.check_shutdown(sh)
        except shutdown.ShutdownRequested:
            logger.info("agent_stop", extra={"ctx": {"ticks": tick}})
            return 0
        logger.info("tick", extra={"ctx": {"tick": tick}})
        time.sleep(float(interval))
        tick += 1


def main() -> int:  # pragma: no cover - thin CLI wrapper
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", type=Path, default=Path("agent_config.json")
    )
    args = parser.parse_args()
    return run(args.config)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
