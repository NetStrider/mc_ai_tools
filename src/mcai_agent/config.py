"""Configuration loading utilities.

Features:
* Load JSON or TOML file (extension-based) into a dict.
* Environment variable overrides with prefix ``MCAI_``.
    * Double underscore ``__`` builds nested structures
        (e.g. ``MCAI_RCON__HOST``)
    * Values are JSON-parsed if they look like JSON (numbers, objects, lists)
* Simple get helper.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

try:  # Python 3.11+ has tomllib
    import tomllib as _toml  # type: ignore
except Exception:  # pragma: no cover
    _toml = None  # type: ignore


def load_file(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    suffix = p.suffix.lower()
    if suffix == ".json":
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    if suffix in {".toml", ".tml"}:
        if _toml is None:
            raise RuntimeError("TOML not supported on this Python version")
        with p.open("rb") as f:  # tomllib expects bytes
            return _toml.load(f)
    raise ValueError(f"Unsupported config extension: {suffix}")


def load_json(path: str | Path) -> Dict[str, Any]:
    """Backward-compatible JSON loader used by older tests."""
    return load_file(path)


def _parse_env_value(raw: str) -> Any:
    raw_strip = raw.strip()
    # Attempt JSON literal parse for structured/numeric types
    try:
        return json.loads(raw_strip)
    except Exception:
        return raw


def _merge_nested(base: Dict[str, Any], keys: list[str], value: Any) -> None:
    cur = base
    for k in keys[:-1]:
        cur = cur.setdefault(k.lower(), {})  # type: ignore[assignment]
    cur[keys[-1].lower()] = value


def apply_env_overrides(
    cfg: Dict[str, Any], prefix: str = "MCAI_"
) -> Dict[str, Any]:
    for k, v in os.environ.items():
        if not k.startswith(prefix):
            continue
        path_part = k[len(prefix):]
        if not path_part:
            continue
        pieces = path_part.split("__")
        parsed = _parse_env_value(v)
        _merge_nested(cfg, pieces, parsed)
    return cfg


def load_config(path: str | Path) -> Dict[str, Any]:
    cfg = load_file(path)
    return apply_env_overrides(cfg)


def get_config_value(
    cfg: Dict[str, Any], key: str, default: Any = None
) -> Any:
    return cfg.get(key, default)
