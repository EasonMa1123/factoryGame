from __future__ import annotations

from dataclasses import dataclass
from typing import List

from common import GridCoord
from economy import Economy
from grid import Grid


@dataclass(frozen=True)
class TransferEvent:
    """One item movement that can be visualized by the renderer."""

    source_cell: GridCoord
    target_cell: GridCoord


class AutomationSystem:
    """Runs the factory simulation once per second."""

    EAST = (1, 0)

    def __init__(self, grid: Grid, economy: Economy) -> None:
        self.grid = grid
        self.economy = economy

    def tick(self) -> List[TransferEvent]:
        for _, building in self.grid.items():
            if building.building_type == "Generator":
                building.stored_items += 1

        transfers = []
        for cell, building in self.grid.items():
            if building.stored_items <= 0:
                continue
            target_cell = (cell[0] + self.EAST[0], cell[1] + self.EAST[1])
            target = self.grid.get(target_cell)
            if target and target.building_type in {"Conveyor", "Collector"}:
                transfers.append((cell, target_cell, building, target))

        events: List[TransferEvent] = []
        for source_cell, target_cell, source, target in transfers:
            if source.stored_items <= 0:
                continue
            source.stored_items -= 1
            events.append(TransferEvent(source_cell=source_cell, target_cell=target_cell))
            if target.building_type == "Collector":
                self.economy.sell_item()
            else:
                target.stored_items += 1

        return events

    def total_stored_items(self) -> int:
        return sum(building.stored_items for _, building in self.grid.items())
