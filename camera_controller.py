from __future__ import annotations

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3


class CameraController:
    """Simple top-down RTS camera movement."""

    def __init__(self, app: ShowBase) -> None:
        self.app = app
        self.speed = 25.0
        self.move_keys = {"forward": False, "backward": False, "left": False, "right": False}

    def setup(self) -> None:
        self.app.disableMouse()
        self.app.camera.setPos(20, -20, 28)
        self.app.camera.lookAt(0, 0, 0)

        self.app.accept("w", self.set_move_key, ["forward", True])
        self.app.accept("w-up", self.set_move_key, ["forward", False])
        self.app.accept("s", self.set_move_key, ["backward", True])
        self.app.accept("s-up", self.set_move_key, ["backward", False])
        self.app.accept("a", self.set_move_key, ["left", True])
        self.app.accept("a-up", self.set_move_key, ["left", False])
        self.app.accept("d", self.set_move_key, ["right", True])
        self.app.accept("d-up", self.set_move_key, ["right", False])

    def set_move_key(self, key: str, is_down: bool) -> None:
        self.move_keys[key] = is_down

    def update(self, dt: float) -> None:
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
            self.app.camera.setPos(self.app.camera.getPos() + direction * self.speed * dt)
