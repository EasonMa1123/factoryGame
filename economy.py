from __future__ import annotations


class Economy:
    """Tracks money and sale values."""

    def __init__(self) -> None:
        self.money = 60
        self.sale_value = 5

    def can_afford(self, cost: int) -> bool:
        return self.money >= cost

    def spend(self, cost: int) -> bool:
        if not self.can_afford(cost):
            return False
        self.money -= cost
        return True

    def sell_item(self) -> None:
        self.money += self.sale_value
