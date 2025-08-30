# Roadmap

MVP:
- Region & chunk reader (anvil-format) with simple heightmap query.
- Java RCON chat bridge (tailing latest.log -> parse -> send reply).
- Agent basic loop + builtin commands (ping/time/help).
- Offline fill/replace operations on chunks with undo log.

Phase 2:
- Spigot plugin + Bedrock adapter for direct control & telemetry.
- Pathfinding + movement primitives.
- LLM summarization & plan generation (optional, gated).

Phase 3:
- Full editor UX, timeline, semantic operations and DSL for transforms.
