import io
import json
import logging

from mcai_agent import logging_setup


def test_logger_basic_context(monkeypatch):
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger("mcai_test_ctx")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    formatter = logging_setup.JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("hello", extra={"ctx": {"tick": 5}})
    line = stream.getvalue().strip()
    data = json.loads(line)
    assert data["msg"] == "hello"
    assert data["tick"] == 5
    assert data["level"] == "INFO"
    assert "ts" in data
