from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BuildingData:
    """Mutable state for a building placed on the logical grid."""

    building_type: str
    stored_items: int = 0
