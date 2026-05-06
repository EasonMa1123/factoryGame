from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class BuildingDefinition:
    """Static data for a building type."""

    name: str
    cost: int
    color: Tuple[float, float, float, float]
    buildable: bool = True
