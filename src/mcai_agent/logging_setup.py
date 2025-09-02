"""Structured logging setup for mcai_agent.

Provides a small helper to configure a JSON-style logger for consistency in
tests and in the agent runtime.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from logging import Logger
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        payload: Dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "name": record.name,
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        # Merge context if provided via 'extra={"ctx": {...}}'
        ctx = getattr(record, "ctx", None)
        if isinstance(ctx, dict):  # shallow merge of context keys
            for k, v in ctx.items():
                if k not in payload:
                    payload[k] = v
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logger(name: str = "mcai", level: int = logging.INFO) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        formatter = JsonFormatter()
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        log_file = os.getenv("MCAI_LOG_FILE")
        if log_file:
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)
    return logger
