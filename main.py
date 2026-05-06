from __future__ import annotations

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock

from automation_system import AutomationSystem
from build_controller import BuildController
from building_catalog import BuildingCatalog
from camera_controller import CameraController
from common import GridCoord
from economy import Economy
from grid import Grid
from hud import Hud
from mouse_picker import MousePicker
from world_renderer import WorldRenderer


class AutomationTycoonGame(ShowBase):
    """Small orchestrator that wires the game systems together."""

    COLLECTOR_CELL: GridCoord = (4, 0)

    def __init__(self) -> None:
        super().__init__()

        self.catalog = BuildingCatalog()
        self.grid = Grid(tile_size=2.0)
        self.economy = Economy()
        self.renderer = WorldRenderer(self, self.grid)
        self.camera_controller = CameraController(self)

        self.renderer.setup_environment()
        self.camera_controller.setup()

        self.picker = MousePicker(self)
        self.renderer.setup_ghost()
        self.hud = Hud(self, self.economy)
        self.build_controller = BuildController(
            self,
            self.grid,
            self.catalog,
            self.economy,
            self.renderer,
            self.picker,
        )
        self.automation = AutomationSystem(self.grid, self.economy)

        self._place_fixed_collector()
        self.build_controller.setup_input()
        self.taskMgr.add(self.update_frame, "update-frame")
        self.taskMgr.doMethodLater(1.0, self.automation_tick, "automation-tick")
        self.refresh_hud()

    def _place_fixed_collector(self) -> None:
        collector = self.catalog.get("Collector")
        self.grid.place(self.COLLECTOR_CELL, collector.name)
        self.renderer.place_building_model(self.COLLECTOR_CELL, collector)

    def update_frame(self, task):
        dt = globalClock.getDt()
        self.camera_controller.update(dt)
        self.build_controller.update_preview()
        self.refresh_hud()
        return task.cont

    def automation_tick(self, task):
        events = self.automation.tick()
        for event in events:
            self.renderer.animate_item_transfer(event.source_cell, event.target_cell)
        self.refresh_hud()
        return task.again

    def refresh_hud(self) -> None:
        selected = self.build_controller.selected_type
        selected_cost = self.catalog.get(selected).cost
        stored_items = self.automation.total_stored_items()
        self.hud.update(selected, selected_cost, stored_items)


if __name__ == "__main__":
    game = AutomationTycoonGame()
    game.run()
