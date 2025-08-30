"""Small anvil reader utilities (wrapper around anvil-parser)."""
from __future__ import annotations

from pathlib import Path
import anvil


def get_chunk_heightmap(region_path: Path, cx: int, cz: int):
    """Return simple column heightmap for chunk (topmost non-air Y per x,z)."""
    reg = anvil.Region.from_file(region_path)
    chunk = reg.get_chunk(cx, cz)
    # naive: return highest non-air for each (x,z)
    heightmap = [[0 for _ in range(16)] for __ in range(16)]
    for x in range(16):
        for z in range(16):
            for y in range(255, -1, -1):
                b = chunk.get_block(x, y, z)
                if b.id != "minecraft:air":
                    heightmap[z][x] = y
                    break
    return heightmap
