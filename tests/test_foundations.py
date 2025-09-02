import json
import logging
from pathlib import Path

from mcai_agent import config, logging_setup, shutdown


def test_load_json(tmp_path: Path) -> None:
    data = {"key": "value", "num": 5}
    p = tmp_path / "cfg.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    loaded = config.load_json(p)
    assert loaded == data
    assert config.get_config_value(loaded, "key") == "value"
    assert config.get_config_value(loaded, "missing", "d") == "d"


def test_configure_logger():
    # ensure logger config returns a Logger
    logger = logging_setup.configure_logger("mcai_test", level=logging.DEBUG)
    assert isinstance(logger, logging.Logger)


def test_shutdown_request_and_check() -> None:
    s = shutdown.Shutdown()
    assert not s.is_set()
    s.request()
    assert s.is_set()
    try:
        shutdown.check_shutdown(s)
    except shutdown.ShutdownRequested:
        return
    assert False, "ShutdownRequested should have been raised"
