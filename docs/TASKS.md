# Project Task Plan

Legend:
P1 = highest priority (foundational MVP)  |  P2 = next layer  |  P3 = later / nice-to-have
Status tags: TODO / WIP / DONE / BLOCKED / RESEARCH

## Phase 0 – Housekeeping / Foundation (P1)

| ID | Task | Details / Acceptance | Status |
|----|------|----------------------|--------|
| FND-001 | Refine config loader | Typed loader + validation for agent_config (host/port/log path). Error on missing file. | TODO |
| FND-002 | Structured logging | Introduce minimal logger wrapper (timestamp, level). | TODO |
| FND-003 | Graceful shutdown util | Context manager / signal handler reuse across runners. | TODO |
| FND-004 | CI matrix badge in README | Show build status for 3.10–3.12. | TODO |

## Phase 1 – Chat Bridge MVP (Vertical Slice) (P1)

Goal: Bot sees trigger in `latest.log`, replies via RCON, supports `!ping`, `!time`, `@bot help`.

| ID | Task | Details / Acceptance | Depends | Status |
|----|------|----------------------|---------|--------|
| CB-001 | Log tailer | Non-blocking generator; handles file rotation (simple reopen if inode changes / size shrink). | FND-* | TODO |
| CB-002 | Chat parsing integration | Use existing regex list; expose parse_chat(line) -> ChatEvent. | CB-001 | TODO |
| CB-003 | Trigger extraction | Detect prefixes; normalize command vs free-form mention. | CB-002 | TODO |
| CB-004 | Command handler wiring | Map commands to functions (ping/time/help). Unknown returns help sentence. | CB-003 | TODO |
| CB-005 | RCON connector | Reuse adapter; add retry/backoff (e.g., exponential up to N). | FND-001 | TODO |
| CB-006 | Outbound tellraw formatting | Escape quotes & backslashes; color config. | CB-005 | TODO |
| CB-007 | Rate limiting | Simple in-memory: max 1 reply / 2s & per-user cooldown optional. | CB-004 | TODO |
| CB-008 | Self-message suppression | Ignore messages from reply_prefix. | CB-002 | TODO |
| CB-009 | Integration test (simulated log + fake RCON) | Test full pipeline end-to-end without network. | CB-006 | TODO |
| CB-010 | README usage snippet | Document enabling RCON in server.properties. | CB-009 | TODO |

## Phase 2 – World Insight MVP (P1 → P2)

Goal: Offline scan of region file → heightmap + block histogram JSON.

| ID | Task | Details / Acceptance | Depends | Status |
|----|------|----------------------|---------|--------|
| WI-001 | Region file discovery | CLI argument or glob to locate region. | FND-* | TODO |
| WI-002 | Safe chunk load wrapper | Gracefully skip corrupted chunks; collect warnings. | WI-001 | TODO |
| WI-003 | Heightmap extraction (opt) | Provide `--mode heightmap` returning CSV/JSON grid. | WI-002 | TODO |
| WI-004 | Block histogram | Count top-layer OR full volume (flag). | WI-002 | TODO |
| WI-005 | Output writer | Writes JSON with metadata (region coords, counts, timestamp). | WI-004 | TODO |
| WI-006 | Tests (synthetic chunk) | Mock or construct chunk object to validate counts. | WI-004 | TODO |
| WI-007 | CLI: scan_region | `python -m mcai_world.cli.scan_region --region r.0.0.mca --out stats.json`. | WI-005 | TODO |

## Phase 3 – Transform + Undo MVP (P2)

| ID | Task | Details / Acceptance | Depends | Status |
|----|------|----------------------|---------|--------|
| TU-001 | Selection AABB model | Dataclass (x1,y1,z1,x2,y2,z2) + clamp & normalize. | WI-* | TODO |
| TU-002 | Replace operation | Iterate selected blocks; record diff (old/new) in undo log. | TU-001 | TODO |
| TU-003 | Undo log format | JSON lines with chunk coords + list of modified blocks compacted. | TU-002 | TODO |
| TU-004 | CLI replace command | `replace --from id --to id --selection ...`. | TU-002 | TODO |
| TU-005 | Tests (small synthetic volume) | Ensure replace + undo restore fidelity. | TU-004 | TODO |

## Phase 4 – Pathfinding Prototype (2D first) (P2)

| ID | Task | Details / Acceptance | Depends | Status |
|----|------|----------------------|---------|--------|
| PF-001 | Grid abstraction | Build grid from heightmap (walkable boolean). | WI-003 | TODO |
| PF-002 | A* implementation | Manhattan + tie-break; returns path list. | PF-001 | TODO |
| PF-003 | Obstacle tests | Unit tests: trivial, blocked, detour. | PF-002 | TODO |
| PF-004 | CLI pathfind tool | Input start/goal → JSON path or NOT_FOUND. | PF-003 | TODO |

## Phase 5 – Memory & Summarization Stub (P2)

| ID | Task | Details / Acceptance | Depends | Status |
|----|------|----------------------|---------|--------|
| MEM-001 | Event dataclasses | ChatEvent, CommandEvent, SystemEvent. | CB-* | TODO |
| MEM-002 | Ring buffer | Configurable max N events; eviction policy. | MEM-001 | TODO |
| MEM-003 | Summarizer stub | Simple rule-based summary every K events; placeholder for LLM. | MEM-002 | TODO |
| MEM-004 | Query API | Function to fetch last N or summary snapshot. | MEM-003 | TODO |
| MEM-005 | Tests | Ensure rotation and summary triggers at correct thresholds. | MEM-003 | TODO |

## Phase 6 – Movement & Control (Server Integration) (P3)

| ID | Task | Details / Acceptance | Depends | Status |
|----|------|----------------------|---------|--------|
| MOV-001 | Research plugin channel | Choose Spigot/Paper plugin or existing WS mod. | RESEARCH | TODO |
| MOV-002 | Minimal plugin scaffold | Position poll + command injection (move, chat). | MOV-001 | TODO |
| MOV-003 | Adapter for plugin comms | WebSocket / TCP client abstraction. | MOV-002 | TODO |
| MOV-004 | Action space definition | Move, look, chat, interact (abstract). | MOV-003 | TODO |
| MOV-005 | Tick loop integration | Merge with chat bridge loop. | MOV-004 | TODO |

## Phase 7 – Advanced World Editing (P3)

| ID | Task | Details / Acceptance | Depends | Status |
|----|------|----------------------|---------|--------|
| ADV-001 | Palette normalization | Map legacy IDs to modern names. | WI-* | TODO |
| ADV-002 | Pattern transforms | Rotate / mirror selection. | TU-* | TODO |
| ADV-003 | Procedural ops | Noise carve, gradient fill. | ADV-002 | TODO |
| ADV-004 | DSL prototype | YAML/JSON transform pipeline runner. | ADV-003 | TODO |
| ADV-005 | Diff patch export | Create minimal patch for remote apply. | TU-* | TODO |

## Cross-Cutting Enhancements

| ID | Task | Focus | Status |
|----|------|-------|--------|
| CC-LOGFMT | Structured logs JSON mode | Observability | TODO |
| CC-PERF | Hotspot profiling (chunk ops) | Performance | TODO |
| CC-DOCS | Expand architecture diagrams | Docs | TODO |
| CC-LINT | Add formatting pre-commit (black/isort) | DX | TODO |
| CC-TYPES | Gradual typing (mypy config) | Reliability | TODO |

## Backlog / Ideas Parking Lot

- Semantic selection growth (block similarity, biome boundaries)
- Player intention inference (goal classification from chat)
- Vector / embedding store for POIs & summaries
- Path cache & incremental re-planning
- WASM sandbox for user transform scripts

## Immediate Next (Execution Order suggestion)

1. FND-001, FND-002, FND-003
2. CB-001 → CB-006 (core loop functioning)
3. CB-007, CB-008 (stability/hardening)
4. CB-009, CB-010 (integration test + docs snippet)
5. Move to `WI-*` or `MEM-*` depending on whether world insight or memory is prioritized next.

---
Document updated: 2025-08-29
