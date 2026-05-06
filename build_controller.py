from __future__ import annotations

from typing import Optional

from direct.showbase.ShowBase import ShowBase
from panda3d.core import MouseButton

from building_catalog import BuildingCatalog
from building_definition import BuildingDefinition
from common import GridCoord
from economy import Economy
from grid import Grid
from mouse_picker import MousePicker
from world_renderer import WorldRenderer


class BuildController:
    """Handles selection, ghost placement preview, and spending money to build."""

    def __init__(
        self,
        app: ShowBase,
        grid: Grid,
        catalog: BuildingCatalog,
        economy: Economy,
        renderer: WorldRenderer,
        picker: MousePicker,
    ) -> None:
        self.app = app
        self.grid = grid
        self.catalog = catalog
        self.economy = economy
        self.renderer = renderer
        self.picker = picker
        self.selected_type = "Generator"
        self.current_hover_cell: Optional[GridCoord] = None

    def setup_input(self) -> None:
        self.app.accept("mouse1", self.place_selected_building)
        for hotkey, building_type in self.catalog.hotkeys.items():
            self.app.accept(hotkey, self.select_building, [building_type])

    def select_building(self, building_type: str) -> None:
        definition = self.catalog.get(building_type)
        if definition.buildable:
            self.selected_type = building_type

    def update_preview(self) -> None:
        world_pos = self.picker.pick_world_position()
        if world_pos is None:
            return

        cell = self.grid.world_to_cell(world_pos)
        definition = self.catalog.get(self.selected_type)
        valid = self.can_place(cell, definition)

        self.current_hover_cell = cell
        self.renderer.move_ghost(cell, valid, definition)

    def can_place(self, cell: GridCoord, definition: BuildingDefinition) -> bool:
        return definition.buildable and not self.grid.is_occupied(cell) and self.economy.can_afford(definition.cost)

    def place_selected_building(self) -> None:
        if not self.app.mouseWatcherNode.isButtonDown(MouseButton.one()):
            return

        cell = self.current_hover_cell
        if cell is None:
            return

        definition = self.catalog.get(self.selected_type)
        if not self.can_place(cell, definition):
            return

        self.economy.spend(definition.cost)
        self.grid.place(cell, definition.name)
        self.renderer.place_building_model(cell, definition)
