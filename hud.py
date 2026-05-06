from __future__ import annotations

from direct.gui.DirectGui import OnscreenText
from direct.showbase.ShowBase import ShowBase

from economy import Economy


class Hud:
    """DirectGUI text for money, selected building, and live factory state."""

    def __init__(self, app: ShowBase, economy: Economy) -> None:
        self.app = app
        self.economy = economy
        self.text = OnscreenText(
            text="",
            parent=self.app.aspect2d,
            pos=(-1.3, 0.92),
            scale=0.045,
            fg=(1, 1, 1, 1),
            align=0,
            mayChange=True,
        )

    def update(self, selected_type: str, selected_cost: int, stored_items: int) -> None:
        self.text.setText(
            f"Money: ${self.economy.money}\n"
            f"Selected: {selected_type} (${selected_cost})\n"
            f"Items in machines: {stored_items}\n"
            "1 Generator  2 Conveyor"
        )
