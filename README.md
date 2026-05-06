# Automation Tycoon Boilerplate (Panda3D)

A starter project for a 3D automation/tycoon-style game built with Panda3D.

## Features

- `ShowBase`-driven game app with scene setup.
- Flat 3D ground and directional lighting.
- Logical 2D grid for tile occupancy and placed building metadata.
- Mouse-following **ghost building** that snaps to grid.
- Left-click placement that creates permanent buildings and marks grid occupied.
- 1-second automation loop that generates resources from `Generator` buildings.
- Simple DirectGUI HUD text showing current resources.
- RTS-style top-down camera movement with WASD.

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

- **W/A/S/D**: Move camera
- **Mouse**: Aim ghost building
- **Left Click**: Place building on highlighted tile

## Extending Building Types

The current code uses `selected_building_type` and `BuildingData` as extension points:

1. Add new building type names (`"Conveyor"`, `"Miner"`, etc.).
2. Swap model/color in `_place_building` based on type.
3. Extend `_automation_tick` with per-building production/consumption logic.
4. Add UI/buttons to change `selected_building_type`.

## Project Structure

- `main.py` – game boilerplate and core systems.
- `requirements.txt` – Python dependencies.
