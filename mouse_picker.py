from __future__ import annotations

from typing import Optional

from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    BitMask32,
    CollisionHandlerQueue,
    CollisionNode,
    CollisionPlane,
    CollisionRay,
    CollisionTraverser,
    Plane,
    Point3,
    Vec3,
)


class MousePicker:
    """Converts the current mouse position into a ground-grid cell."""

    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.traverser = CollisionTraverser("mouse-picker")
        self.handler = CollisionHandlerQueue()
        self.ray = CollisionRay()

        picker_node = CollisionNode("mouseRay")
        picker_node.addSolid(self.ray)
        picker_node.setFromCollideMask(BitMask32.bit(1))
        picker_node.setIntoCollideMask(BitMask32.allOff())
        picker_np = self.app.camera.attachNewNode(picker_node)
        self.traverser.addCollider(picker_np, self.handler)

        ground_col_node = CollisionNode("groundCollider")
        ground_col_node.addSolid(CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0))))
        ground_col_node.setFromCollideMask(BitMask32.allOff())
        ground_col_node.setIntoCollideMask(BitMask32.bit(1))
        self.ground_collision = self.app.render.attachNewNode(ground_col_node)
        self.ground_collision.hide()

    def pick_world_position(self) -> Optional[Point3]:
        if not self.app.mouseWatcherNode.hasMouse():
            return None

        mouse = self.app.mouseWatcherNode.getMouse()
        self.ray.setFromLens(self.app.camNode, mouse.getX(), mouse.getY())
        self.traverser.traverse(self.app.render)

        if self.handler.getNumEntries() == 0:
            return None

        self.handler.sortEntries()
        return self.handler.getEntry(0).getSurfacePoint(self.app.render)
