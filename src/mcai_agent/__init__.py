"""mcai_agent package - runtime agent components."""

# Re-export key submodules for convenience and to help type checkers.
from . import (
    runners,
    adapters,
    perception,
    reasoning,
    plugins,
    config,
    logging_setup,
    shutdown,
)

__all__ = [
    "runners",
    "adapters",
    "perception",
    "reasoning",
    "plugins",
    "config",
    "logging_setup",
    "shutdown",
]
