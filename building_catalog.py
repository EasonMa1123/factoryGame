from __future__ import annotations

from typing import Dict, Iterable

from building_definition import BuildingDefinition


class BuildingCatalog:
    """Holds all building types and their costs/visuals."""

    def __init__(self) -> None:
        self.definitions: Dict[str, BuildingDefinition] = {
            "Generator": BuildingDefinition("Generator", 25, (0.95, 0.75, 0.2, 1.0)),
            "Conveyor": BuildingDefinition("Conveyor", 5, (0.2, 0.55, 0.95, 1.0)),
            "Collector": BuildingDefinition("Collector", 0, (0.25, 0.9, 0.45, 1.0), buildable=False),
        }
        self.hotkeys = {"1": "Generator", "2": "Conveyor"}

    def get(self, building_type: str) -> BuildingDefinition:
        return self.definitions[building_type]

    def buildable_types(self) -> Iterable[str]:
        return (name for name, definition in self.definitions.items() if definition.buildable)
