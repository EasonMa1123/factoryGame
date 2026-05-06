# Automation Tycoon Boilerplate (Panda3D)

A starter project for a 3D automation/tycoon-style game built with Panda3D.

## Features

- `ShowBase`-driven Panda3D app with scene setup, lighting, and a flat ground.
- Logical 2D grid for tile occupancy and placed building state.
- Mouse-following ghost building that snaps to grid.
- Money-based building purchases for generators and conveyors.
- Three starter building types:
  - `Generator`: produces raw items once per second.
  - `Conveyor`: moves stored items east toward the next building.
  - `Collector`: a fixed map building that sells delivered items for money.
- Animated item cubes that visibly travel from building to building.
- DirectGUI HUD showing money, selected building, and items still in machines.
- RTS-style top-down camera movement with WASD.
- Refactored systems: grid, catalog, economy, renderer, mouse picker, camera, build controller, HUD, and automation.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

- `W/A/S/D`: Move camera
- `Mouse`: Aim ghost building
- `Left Click`: Place selected building if the tile is free and you can afford it
- `1`: Select Generator
- `2`: Select Conveyor

## Starter Factory

The first playable chain is:

```text
Generator -> Conveyor -> Collector
```

The collector is already placed at grid cell `(4, 0)` and cannot be bought or placed again. Items currently move east, so place generators and conveyors to the left of the collector. For example, place a generator at `(0, 0)`, then conveyors at `(1, 0)`, `(2, 0)`, and `(3, 0)`.

Each item that reaches the collector is sold for money, which can be spent on more generators and conveyors.

## Extending Building Types

Most expansion points are now small classes:

- Add buildable types and costs in `building_catalog.py`.
- Add per-building state to `BuildingData`.
- Change grid rules in `grid.py`.
- Change models/colors and item animations in `world_renderer.py`.
- Add new production, recipes, directions, or storage limits in `automation_system.py`.
- Add buttons or richer UI in `hud.py` and `build_controller.py`.

## Project Structure

- `main.py` - Panda3D app orchestration.
- `automation_system.py` - production, transfer, and sale simulation.
- `build_controller.py` - selection, preview, and placement.
- `building_catalog.py` - building definitions and hotkeys.
- `building_data.py` - placed building state.
- `building_definition.py` - static building metadata.
- `camera_controller.py` - RTS camera movement.
- `common.py` - shared type aliases.
- `economy.py` - money and sale values.
- `grid.py` - tile occupancy and coordinate conversion.
- `hud.py` - DirectGUI status text.
- `mouse_picker.py` - mouse-to-ground collision picking.
- `world_renderer.py` - scene setup, building models, and item animations.
- `requirements.txt` - Python dependencies.
