# mc_ai_tools

Minecraft AI tools: a repository for building an agent that can interact
with Minecraft servers (chat + movement + actions) and a next‑gen world
editor toolkit (chunk/NBT/anvil manipulation, diffs, transforms).

## Quickstart

1. Create a Python 3.10+ venv:

   python -m venv .venv
   source .venv/Scripts/activate  # on Windows use: .venv\Scripts\Activate.ps1

2. Install dev deps:

   python -m pip install -e .[dev]

3. Run tests:

   pytest -q

## Project layout

- `src/mcai_agent/` — agent runtime, adapters, perception, reasoning
- `src/mcai_world/` — NBT, anvil region/chunk ops, transforms and diffs
- `tests/` — unit tests
- `docs/` — architecture and roadmap

## Contributing

Feel free to open issues or PRs against ideas and experiments. For now,
this is an early prototype scaffold.

## Foundations Usage Example

Example of using the provided foundations in your own script (mirrors the
runner logic):

```python
from pathlib import Path
from mcai_agent import config, logging_setup, shutdown

cfg = config.load_config(Path("agent_config.json"))
logger = logging_setup.configure_logger("mcai.demo")
sh = shutdown.Shutdown()
shutdown.register_signal_handlers(sh)
logger.info("demo_start", extra={"ctx": {"have_cfg": bool(cfg)}})
try:
   tick = 0
   while True:
      shutdown.check_shutdown(sh)
      logger.info("tick", extra={"ctx": {"tick": tick}})
      tick += 1
except shutdown.ShutdownRequested:
   logger.info("demo_stop", extra={"ctx": {"ticks": tick}})
```

Environment overrides:

```bash
export MCAI_RCON__HOST=example.org
export MCAI_FEATURE_FLAGS__EXPERIMENTAL=true
```

These become nested keys like `cfg['rcon']['host']` and
`cfg['feature_flags']['experimental']`.
