from __future__ import annotations

from typing import Dict, Optional

from panda3d.core import Point3

from building_data import BuildingData
from common import GridCoord


class Grid:
    """Owns tile occupancy and grid/world coordinate conversion."""

    def __init__(self, tile_size: float = 2.0) -> None:
        self.tile_size = tile_size
        self.buildings: Dict[GridCoord, BuildingData] = {}

    def is_occupied(self, cell: GridCoord) -> bool:
        return cell in self.buildings

    def place(self, cell: GridCoord, building_type: str) -> BuildingData:
        building = BuildingData(building_type=building_type)
        self.buildings[cell] = building
        return building

    def get(self, cell: GridCoord) -> Optional[BuildingData]:
        return self.buildings.get(cell)

    def items(self):
        return self.buildings.items()

    def world_to_cell(self, world: Point3) -> GridCoord:
        return round(world.x / self.tile_size), round(world.y / self.tile_size)

    def cell_to_world(self, cell: GridCoord) -> Point3:
        return Point3(cell[0] * self.tile_size, cell[1] * self.tile_size, 0)
