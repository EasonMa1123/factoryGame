from __future__ import annotations

from direct.interval.IntervalGlobal import Func, LerpPosInterval, Sequence
from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, LColor, TransparencyAttrib

from building_definition import BuildingDefinition
from common import GridCoord
from grid import Grid


class WorldRenderer:
    """Creates scene objects and keeps building models separate from game data."""

    def __init__(self, app: ShowBase, grid: Grid) -> None:
        self.app = app
        self.grid = grid
        self.placed_models = {}
        self.ghost_model = None

    def setup_environment(self) -> None:
        self.app.setBackgroundColor(0.07, 0.09, 0.12, 1)

        ground = self.app.loader.loadModel("models/misc/rgbCube")
        ground.reparentTo(self.app.render)
        ground.setScale(80, 80, 0.05)
        ground.setPos(0, 0, -0.05)
        ground.setColor(0.2, 0.25, 0.2, 1.0)

        dlight = DirectionalLight("sun")
        dlight.setColor(LColor(0.95, 0.95, 0.88, 1))
        dlnp = self.app.render.attachNewNode(dlight)
        dlnp.setHpr(-35, -50, 0)
        self.app.render.setLight(dlnp)

    def setup_ghost(self) -> None:
        self.ghost_model = self.app.loader.loadModel("models/misc/rgbCube")
        self.ghost_model.reparentTo(self.app.render)
        self.ghost_model.setScale(1, 1, 1)
        self.ghost_model.setTransparency(TransparencyAttrib.MAlpha)
        self.ghost_model.setColor(0.3, 0.9, 1.0, 0.4)

    def move_ghost(self, cell: GridCoord, valid: bool, definition: BuildingDefinition) -> None:
        if self.ghost_model is None:
            return
        pos = self.grid.cell_to_world(cell)
        self.ghost_model.setPos(pos.x, pos.y, 0.5)
        self.ghost_model.setColor((1.0, 0.2, 0.2, 0.5) if not valid else definition.color[:3] + (0.45,))

    def place_building_model(self, cell: GridCoord, definition: BuildingDefinition) -> None:
        pos = self.grid.cell_to_world(cell)
        model = self.app.loader.loadModel("models/misc/rgbCube")
        model.reparentTo(self.app.render)
        model.setPos(pos.x, pos.y, 0.5)
        model.setScale(1, 1, 1)
        model.setColor(definition.color)
        self.placed_models[cell] = model

    def animate_item_transfer(self, source_cell: GridCoord, target_cell: GridCoord) -> None:
        start = self.grid.cell_to_world(source_cell)
        end = self.grid.cell_to_world(target_cell)

        item = self.app.loader.loadModel("models/misc/rgbCube")
        item.reparentTo(self.app.render)
        item.setScale(0.25, 0.25, 0.25)
        item.setColor(1.0, 0.95, 0.35, 1.0)
        item.setPos(start.x, start.y, 1.35)

        move = LerpPosInterval(item, 0.45, (end.x, end.y, 1.35), startPos=(start.x, start.y, 1.35))
        Sequence(move, Func(item.removeNode)).start()
