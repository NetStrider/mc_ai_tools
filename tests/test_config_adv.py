import json
from pathlib import Path

import pytest

from mcai_agent import config


@pytest.mark.parametrize(
    "ext,writer",
    [
        (
            ".json",
            lambda p, data: p.write_text(
                json.dumps(data), encoding="utf-8"
            ),
        ),
    ],
)
def test_load_file_basic(ext, writer, tmp_path: Path):
    data = {"a": 1, "b": {"c": True}}
    p = tmp_path / f"cfg{ext}"
    writer(p, data)
    loaded = config.load_file(p)
    assert loaded == data


def test_env_overrides_nested(tmp_path: Path, monkeypatch):
    base = {"rcon": {"host": "localhost", "port": 25575}}
    p = tmp_path / "cfg.json"
    p.write_text(json.dumps(base), encoding="utf-8")
    monkeypatch.setenv("MCAI_RCON__PORT", "25599")
    monkeypatch.setenv("MCAI_FEATURE_FLAGS__X", "true")
    loaded = config.load_config(p)
    assert loaded["rcon"]["port"] == 25599
    assert loaded["feature_flags"]["x"] is True


def test_env_override_json_object(tmp_path: Path, monkeypatch):
    p = tmp_path / "cfg.json"
    p.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("MCAI_AGENT__PARAMS", '{"speed":2}')
    loaded = config.load_config(p)
    assert loaded["agent"]["params"]["speed"] == 2
