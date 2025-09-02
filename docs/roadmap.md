# Roadmap

Status Legend: (✅ done) (🚧 in progress) (🗓 planned) (🧪 experimental) (❓ evaluate)

## Phase 0 – Foundations (✅ Complete)

Delivered:

- Packaging & project scaffold
- Config loader (JSON/TOML + env overrides `MCAI_*`)
- Structured JSON logging with context + optional file sink
- Graceful shutdown (signals) utilities
- Basic tests suite (10 passing)

Outcomes: Stable base to layer chat bridge and world tooling without rewriting core utilities.

## Phase 1 – Chat Bridge MVP (🚧 Next Up)

Goal: Bi-directional lightweight command interaction via Minecraft chat.

Scope:

1. Log tailer (follow `latest.log`) with backpressure & file rollover detection.
2. Chat line parsing -> event objects (reuse `perception.parse_chat`).
3. Command routing (`!ping`, `!time`, later `!help`).
4. RCON outbound messaging (tellraw) with minimal formatting.
5. Rate limiting (per user + global) to avoid spam.
6. Permissions map (config `commands.allowlist` & `users.admins`).
7. Error handling + user feedback (unknown command, permission denied).
8. Simple metrics counters (ticks processed, commands handled, errors) logged periodically.
9. Test harness simulating log lines -> verifying RCON adapter invocation (mock).
10. Documentation: Chat Bridge usage & configuration.

Stretch (optional if time permits):

- Multi-line / JSON chat support (future) – defer.
- Basic plugin system for injecting new commands dynamically.

Exit Criteria:

- Start runner, issue `!ping` in server chat, bot replies <2s.
- Unit/integration tests cover parsing, routing, permission, rate limit paths.

## Phase 2 – World Insight MVP (🗓 Planned)

Goal: Read server world (offline copy) and answer structural queries.

Milestones:

1. Region indexer (lazy scan + caching of coordinates -> file path).
2. Chunk metadata extraction (biome counts, height stats, palette sample).
3. Query API (CLI / internal) for: height at (x,z), biome distribution in area, block frequency histogram.
4. Caching layer w/ invalidation TTL.
5. Tests with fixture region files (small synthetic data set).
6. Logging enrichments: structured query logs for later analytics.

Stretch:

- Incremental watcher for new/changed region files.
- Precompute lightweight embeddings (❓ evaluate value later).

## Phase 3 – Transform + Undo MVP (🗓 Planned)

Goal: Safe offline block transforms with atomic diff & undo log.

Milestones:

1. Read chunk -> in-memory block array abstraction.
2. Apply fill/replace operations using selectors (block id, y-range, pattern).
3. Diff representation (changed coordinates + before/after palette indices).
4. Undo log (append-only JSONL) + apply_undo routine.
5. CLI commands (preview diff, apply diff, undo last N).
6. Tests: diff round-trip, undo integrity, performance micro-benchmark (time bound < X ms for small chunk).

Stretch:

- Composable transform pipeline (chain operations with dry-run preview).
- Scripting hooks (Python function transforms).

## Phase 4 – Pathfinding Prototype (🗓 Planned)

Goal: 2D/columnar A* for navigation scaffolding.

Milestones:

1. 2D grid extraction (walkable vs blocked).
2. A* baseline (heuristic = Manhattan) + cost metrics.
3. Serialization of path result + stats (expanded nodes, cost, length).
4. Caching of last N paths (LRU by start/goal hash).
5. Tests with synthetic maps & edge cases (no path, start==goal, narrow corridor).

Stretch:

- Elevation-aware 3D nodes (performance evaluation).
- Hierarchical abstraction (HPA*) after baseline validated.

## Phase 5 – Memory & Summarization (🗓 Planned / ❓ Evaluate)

Goal: Minimal episodic memory log + optional LLM summarization.

Milestones:

1. Event journal (JSONL) of chat & actions.
2. Rolling window query API.
3. Summarization stub (interface only) with pluggable backend.
4. Tests for persistence, rotation, retention policy.

Stretch:

- Embedding store for retrieval augmentation.

## Phase 6 – Movement & Control Integration (🗓 Planned)

Goal: Real-time server interaction beyond chat.

Milestones:

1. Spigot/Paper plugin or alternate bridge exposing a control channel (WS/RCON extended command).
2. Basic actions: move, look, say, interact (high-level commands queued).
3. Rate & safety guards (max velocity, action cooldown).
4. Telemetry ingestion: position, health, inventory snapshot.
5. Tests (mock plugin protocol or simulated responses).

Stretch:

- Action planner integrating pathfinding + world insight.

## Phase 7 – Advanced World Editing & DSL (🗓 Planned)

Goal: Expressive domain language for structural edits.

Milestones:

1. Selection language (shapes: box, sphere, cylinder; filters; unions).
2. Transform verbs (raise, smooth, replace-if, paint-biome).
3. Macro recording & replay.
4. Semantic tags (e.g., "road", "wall") stored in sidecar metadata.
5. Tests for DSL parsing & determinism.

Stretch:

- Collaborative diff merge strategies.

## Cross-Cutting Concerns

- Observability: log context expansion (request_id, session) & optional metrics sink.
- Performance: micro-bench harness for chunk parse & transform operations.
- Testing depth: property-based tests for transforms & parsing.
- Security: sandbox transforms to avoid arbitrary file writes.
- Configuration hygiene: schema docs + example configs updated each phase.

## Risk Register / Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Log tailer missing lines on rotation | Loss of chat events | Detect inode / size shrink -> reopen from start |
| RCON latency spikes | Slow responses | Introduce async queue + timeout/retry wrapper |
| Large region scans slow queries | UI lag | Lazy index & cache, background prefetch |
| Diff files grow unbounded | Disk bloat | Rotate & compress older logs, retention policy |
| Pathfinding perf in 3D | Slow actions | Prototype in 2D; measure before 3D expansion |

## Immediate Next Actions

1. Implement Chat Bridge Phase 1 tasks (log tail + routing + permissions + tests).
2. Add integration test harness simulating log file growth.
3. Document configuration options for chat bridge in README.
4. Prepare sample config with permissions & rate limits.

## Deferred / Idea Backlog

- Multi-agent coordination layer.
- In-game UI overlays (map previews) via plugin.
- Remote web dashboard for metrics & commands.
- AI planning with external LLM (only after deterministic core stable).

Last updated: 2025-09-02
