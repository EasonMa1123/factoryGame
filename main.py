from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from direct.gui.DirectGui import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    CollisionHandlerQueue,
    CollisionNode,
    CollisionRay,
    DirectionalLight,
    LColor,
    MouseButton,
    Point3,
    Vec3,
)


GridCoord = Tuple[int, int]


@dataclass
class BuildingData:
    """Represents a placed building on the logical grid."""

    building_type: str


class AutomationTycoonGame(ShowBase):
    """Boilerplate foundation for a Panda3D 3D automation/tycoon game."""

    def __init__(self) -> None:
        super().__init__()

        # --- Core world state ---
        self.tile_size: float = 2.0
        self.resources: int = 0
        self.grid: Dict[GridCoord, BuildingData] = {}
        self.placed_models: Dict[GridCoord, object] = {}
        self.selected_building_type: str = "Generator"

        # Camera movement state (RTS style)
        self.camera_speed: float = 25.0
        self.move_keys = {"forward": False, "backward": False, "left": False, "right": False}

        # Mouse/grid preview state
        self.current_hover_cell: Optional[GridCoord] = None

        self.disableMouse()  # Disable default orbit camera controls.

        self._setup_environment()
        self._setup_ui()
        self._setup_camera()
        self._setup_input()
        self._setup_mouse_picker()
        self._setup_ghost_building()

        # Frame update for ghost/camera.
        self.taskMgr.add(self._update_frame, "update-frame")
        # 1-second automation loop.
        self.taskMgr.doMethodLater(1.0, self._automation_tick, "automation-tick")

    def _setup_environment(self) -> None:
        """Create simple lighting and a flat ground plane."""
        self.setBackgroundColor(0.07, 0.09, 0.12, 1)

        ground = self.loader.loadModel("models/misc/rgbCube")
        ground.reparentTo(self.render)
        ground.setScale(80, 80, 0.05)
        ground.setPos(0, 0, -0.05)
        ground.setColor(0.2, 0.25, 0.2, 1.0)

        dlight = DirectionalLight("sun")
        dlight.setColor(LColor(0.95, 0.95, 0.88, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(-35, -50, 0)
        self.render.setLight(dlnp)

    def _setup_ui(self) -> None:
        self.resources_text = OnscreenText(
            text="Resources: 0",
            parent=self.aspect2d,
            pos=(-1.3, 0.92),
            scale=0.06,
            fg=(1, 1, 1, 1),
            align=0,
            mayChange=True,
        )

    def _setup_camera(self) -> None:
        """Top-down RTS-like camera looking toward the ground center."""
        self.camera.setPos(20, -20, 28)
        self.camera.lookAt(0, 0, 0)

    def _setup_input(self) -> None:
        # WASD camera movement
        self.accept("w", self._set_move_key, ["forward", True])
        self.accept("w-up", self._set_move_key, ["forward", False])
        self.accept("s", self._set_move_key, ["backward", True])
        self.accept("s-up", self._set_move_key, ["backward", False])
        self.accept("a", self._set_move_key, ["left", True])
        self.accept("a-up", self._set_move_key, ["left", False])
        self.accept("d", self._set_move_key, ["right", True])
        self.accept("d-up", self._set_move_key, ["right", False])

        # Place building on left click.
        self.accept("mouse1", self._place_building)

    def _setup_mouse_picker(self) -> None:
        picker_node = CollisionNode("mouseRay")
        self.picker_ray = CollisionRay()
        picker_node.addSolid(self.picker_ray)
        picker_np = self.camera.attachNewNode(picker_node)

        self.picker_handler = CollisionHandlerQueue()
        self.picker_traverser = self.cTrav
        self.picker_traverser.addCollider(picker_np, self.picker_handler)

        # Ground collision target
        ground_col_node = CollisionNode("groundCollider")
        # Use a large thin cube model; collision is inherited from model geometry through collision masks.
        self.ground_for_collision = self.loader.loadModel("models/misc/rgbCube")
        self.ground_for_collision.reparentTo(self.render)
        self.ground_for_collision.setScale(80, 80, 0.05)
        self.ground_for_collision.setPos(0, 0, -0.05)
        self.ground_for_collision.hide()
        self.ground_for_collision.node().setIntoCollideMask(1)

    def _setup_ghost_building(self) -> None:
        self.ghost_model = self.loader.loadModel("models/misc/rgbCube")
        self.ghost_model.reparentTo(self.render)
        self.ghost_model.setScale(1, 1, 1)
        self.ghost_model.setColor(0.3, 0.9, 1.0, 0.4)
        self.ghost_model.setTransparency(True)

    def _set_move_key(self, key: str, is_down: bool) -> None:
        self.move_keys[key] = is_down

    def _update_frame(self, task):
        dt = globalClock.getDt()
        self._update_camera(dt)
        self._update_ghost_from_mouse()
        return task.cont

    def _update_camera(self, dt: float) -> None:
        direction = Vec3(0, 0, 0)
        if self.move_keys["forward"]:
            direction.y += 1
        if self.move_keys["backward"]:
            direction.y -= 1
        if self.move_keys["left"]:
            direction.x -= 1
        if self.move_keys["right"]:
            direction.x += 1

        if direction.lengthSquared() > 0:
            direction.normalize()
            self.camera.setPos(self.camera.getPos() + direction * self.camera_speed * dt)

    def _update_ghost_from_mouse(self) -> None:
        if not self.mouseWatcherNode.hasMouse():
            return

        mouse = self.mouseWatcherNode.getMouse()
        self.picker_ray.setFromLens(self.camNode, mouse.getX(), mouse.getY())
        self.picker_traverser.traverse(self.render)

        if self.picker_handler.getNumEntries() == 0:
            return

        self.picker_handler.sortEntries()
        hit = self.picker_handler.getEntry(0)
        hit_pos = hit.getSurfacePoint(self.render)

        cell = self._world_to_grid(hit_pos)
        world_pos = self._grid_to_world(cell)

        self.current_hover_cell = cell
        self.ghost_model.setPos(world_pos.x, world_pos.y, 0.5)

        # Visual feedback for occupancy.
        occupied = cell in self.grid
        self.ghost_model.setColor((1.0, 0.2, 0.2, 0.5) if occupied else (0.3, 0.9, 1.0, 0.4))

    def _world_to_grid(self, world: Point3) -> GridCoord:
        gx = round(world.x / self.tile_size)
        gy = round(world.y / self.tile_size)
        return gx, gy

    def _grid_to_world(self, cell: GridCoord) -> Point3:
        x = cell[0] * self.tile_size
        y = cell[1] * self.tile_size
        return Point3(x, y, 0)

    def _place_building(self) -> None:
        if not self.mouseWatcherNode.isButtonDown(MouseButton.one()):
            return

        cell = self.current_hover_cell
        if cell is None or cell in self.grid:
            return

        world_pos = self._grid_to_world(cell)
        model = self.loader.loadModel("models/misc/rgbCube")
        model.reparentTo(self.render)
        model.setPos(world_pos.x, world_pos.y, 0.5)
        model.setScale(1, 1, 1)

        # Expandable: use selected_building_type to swap models, colors, behaviors, or stats.
        if self.selected_building_type == "Generator":
            model.setColor(0.95, 0.75, 0.2, 1.0)
        else:
            model.setColor(0.7, 0.7, 0.8, 1.0)

        self.grid[cell] = BuildingData(building_type=self.selected_building_type)
        self.placed_models[cell] = model

    def _automation_tick(self, task):
        """Runs every second; generators produce resources."""
        produced = sum(1 for b in self.grid.values() if b.building_type == "Generator")
        self.resources += produced
        self.resources_text.setText(f"Resources: {self.resources}")

        return task.again


if __name__ == "__main__":
    game = AutomationTycoonGame()
    game.run()
