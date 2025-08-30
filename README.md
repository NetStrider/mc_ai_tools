# mc_ai_tools

Minecraft AI tools: a repository for building an agent that can interact
with Minecraft servers (chat + movement + actions) and a next‑gen world
editor toolkit (chunk/NBT/anvil manipulation, diffs, transforms).

Quickstart
---------

1. Create a Python 3.10+ venv:

   python -m venv .venv
   source .venv/Scripts/activate  # on Windows use: .venv\Scripts\Activate.ps1

2. Install dev deps:

   python -m pip install -e .[dev]

3. Run tests:

   pytest -q

Project layout
--------------

- `src/mcai_agent/` — agent runtime, adapters, perception, reasoning
- `src/mcai_world/` — NBT, anvil region/chunk ops, transforms and diffs
- `tests/` — unit tests
- `docs/` — architecture and roadmap

Contributing
------------
Feel free to open issues or PRs against ideas and experiments. For now,
this is an early prototype scaffold.
