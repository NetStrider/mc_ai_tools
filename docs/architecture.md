# Architecture

This project separates two major concerns:

1. Agent runtime (`src/mcai_agent`) — components that perceive the game,
   model a local world view, and decide on actions.  
2. World toolkit (`src/mcai_world`) — utilities for reading, modifying,
   and diffing world data (NBT, anvil regions, transforms).

Core contracts:

- Bridge Adapter: abstracts how chat/commands/position are observed and
  how actions (chat, movement, commands) are executed.
- World Reader: an API for efficient chunk/region reads and small writes.
- Memory Store: append-only events with periodic summarization for
  longer-term context.
